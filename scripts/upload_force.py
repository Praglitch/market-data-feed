import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CLIENT_SECRET_FILE = "credentials/oauth_client.json"
TOKEN_PICKLE = "credentials/token.pickle"
LOCAL_DATA_ROOT = "data"
DRIVE_ROOT_FOLDER_NAME = "indian-market-data"

FOLDER_MAP = {
    "nifty50_scrips": "nifty50_scrips",
    "nifty50_index": "nifty50_index",
    "nifty500_scrips": "nifty500_scrips",
    "nifty500_index": "nifty500_index",
}

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

def get_or_create_folder(service, folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])
    if folders:
        print(f"✅ Found folder: {folder_name}")
        return folders[0]["id"]
    file_metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        file_metadata["parents"] = [parent_id]
    folder = service.files().create(body=file_metadata, fields="id").execute()
    print(f"✅ Created folder: {folder_name}")
    return folder.get("id")

def upload_file_overwrite(service, local_path, drive_folder_id, file_name):
    # Delete if exists
    query = f"name='{file_name}' and '{drive_folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    for f in results.get("files", []):
        service.files().delete(fileId=f["id"]).execute()
        print(f"🗑️ Deleted existing {file_name}")
    # Upload
    media = MediaFileUpload(local_path, mimetype="text/csv", resumable=True)
    file_metadata = {"name": file_name, "parents": [drive_folder_id]}
    service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"✅ Uploaded: {file_name}")

def main():
    print("🔐 Authenticating...")
    service = authenticate()
    root_id = get_or_create_folder(service, DRIVE_ROOT_FOLDER_NAME)
    for local_folder, drive_folder_name in FOLDER_MAP.items():
        local_path = os.path.join(LOCAL_DATA_ROOT, local_folder)
        if not os.path.exists(local_path):
            print(f"⚠️ Local folder not found: {local_path}")
            continue
        subfolder_id = get_or_create_folder(service, drive_folder_name, parent_id=root_id)
        for file_name in os.listdir(local_path):
            if not file_name.endswith(".csv"):
                continue
            upload_file_overwrite(service, os.path.join(local_path, file_name), subfolder_id, file_name)
    print("\n🎉 All files uploaded (force overwrite)!")

if __name__ == "__main__":
    main()