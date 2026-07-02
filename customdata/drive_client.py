import os
import pickle
import io
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CLIENT_SECRET_FILE = "credentials/oauth_client.json"
TOKEN_PICKLE = "credentials/token.pickle"
ROOT_FOLDER_NAME = "indian-market-data"


def authenticate():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, "wb") as token:
            pickle.dump(creds, token)
    return build("drive", "v3", credentials=creds)


def get_folder_id(service, folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])
    return folders[0]["id"] if folders else None


def get_root_folder_id(service):
    return get_folder_id(service, ROOT_FOLDER_NAME)


def get_subfolder_id(service, folder_name, parent_id):
    return get_folder_id(service, folder_name, parent_id)


def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed=false and mimeType='text/csv'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get("files", [])


def download_file_as_df(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file_bytes = io.BytesIO()
    downloader = MediaIoBaseDownload(file_bytes, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_bytes.seek(0)
    return pd.read_csv(file_bytes)


def upload_df_as_csv(service, df, folder_id, file_name):
    """
    Upload DataFrame as CSV, deleting any existing file first.
    Verifies upload by checking row count.
    """
    temp_path = f"/tmp/{file_name}"
    df.to_csv(temp_path, index=False)

    # Check if file exists and delete it
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    if files:
        file_id = files[0]["id"]
        service.files().delete(fileId=file_id).execute()
        print(f"🗑️ Deleted old {file_name}")

    # Upload new file
    media = MediaFileUpload(temp_path, mimetype="text/csv", resumable=True)
    file_metadata = {"name": file_name, "parents": [folder_id]}
    new_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"✅ Uploaded new {file_name} (ID: {new_file['id']})")

    os.remove(temp_path)

    # Verification: download and compare row count
    verify_df = download_file_as_df(service, new_file['id'])
    if len(verify_df) != len(df):
        print(f"⚠️ Verification failed: expected {len(df)} rows, got {len(verify_df)} rows")
    else:
        print(f"✅ Verification passed: {len(verify_df)} rows")
    return new_file['id']