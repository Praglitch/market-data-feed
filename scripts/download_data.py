import os
import pandas as pd
from customdata.drive_client import authenticate, get_root_folder_id, get_subfolder_id, list_files_in_folder, download_file_as_df

def main():
    service = authenticate()
    root_id = get_root_folder_id(service)
    if not root_id:
        print("Root folder not found")
        return

    folders = ['nifty50_scrips', 'nifty50_index', 'nifty500_scrips', 'nifty500_index']
    for folder in folders:
        folder_id = get_subfolder_id(service, folder, root_id)
        if not folder_id:
            print(f'Folder {folder} not found, skipping')
            continue
        os.makedirs(f'data/{folder}', exist_ok=True)
        files = list_files_in_folder(service, folder_id)
        for f in files:
            if not f['name'].endswith('.csv'):
                continue
            print(f'Downloading {folder}/{f["name"]}...')
            df = download_file_as_df(service, f['id'])
            df.to_csv(f'data/{folder}/{f["name"]}', index=False)

if __name__ == '__main__':
    main()
