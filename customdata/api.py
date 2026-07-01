import pandas as pd
from .drive_client import (
    authenticate,
    get_root_folder_id,
    get_subfolder_id,
    list_files_in_folder,
    download_file_as_df,
)

_FOLDER_CACHE = {}
_DRIVE_SERVICE = None


def _get_service():
    global _DRIVE_SERVICE
    if _DRIVE_SERVICE is None:
        _DRIVE_SERVICE = authenticate()
    return _DRIVE_SERVICE


def _get_folder_id(folder_name):
    if folder_name not in _FOLDER_CACHE:
        service = _get_service()
        root_id = get_root_folder_id(service)
        if not root_id:
            raise Exception("Root folder 'indian-market-data' not found on Drive.")
        sub_id = get_subfolder_id(service, folder_name, root_id)
        if not sub_id:
            raise Exception(f"Subfolder '{folder_name}' not found on Drive.")
        _FOLDER_CACHE[folder_name] = sub_id
    return _FOLDER_CACHE[folder_name]


def _fetch_csv(folder_name, file_name, start=None, end=None):
    service = _get_service()
    folder_id = _get_folder_id(folder_name)

    files = list_files_in_folder(service, folder_id)
    file_id = None
    for f in files:
        if f["name"] == file_name:
            file_id = f["id"]
            break

    if not file_id:
        raise FileNotFoundError(f"{file_name} not found in {folder_name}")

    df = download_file_as_df(service, file_id)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if start:
        df = df[df["timestamp"] >= pd.to_datetime(start)]
    if end:
        df = df[df["timestamp"] <= pd.to_datetime(end)]

    return df


def get_scrip(symbol, index="nifty50", start=None, end=None):
    folder_map = {
        "nifty50": "nifty50_scrips",
        "nifty500": "nifty500_scrips",
    }
    if index not in folder_map:
        raise ValueError("index must be 'nifty50' or 'nifty500'")

    folder_name = folder_map[index]
    file_name = f"{symbol.upper()}.csv"
    return _fetch_csv(folder_name, file_name, start, end)


def get_index(index_type="nifty50", start=None, end=None):
    folder_map = {
        "nifty50": "nifty50_index",
        "nifty500": "nifty500_index",
    }
    if index_type not in folder_map:
        raise ValueError("index_type must be 'nifty50' or 'nifty500'")

    folder_name = folder_map[index_type]
    file_name = "NIFTY50_INDEX.csv" if index_type == "nifty50" else "NIFTY500_INDEX.csv"
    return _fetch_csv(folder_name, file_name, start, end)


def get_all_scrips(index="nifty50", start=None, end=None):
    folder_map = {
        "nifty50": "nifty50_scrips",
        "nifty500": "nifty500_scrips",
    }
    if index not in folder_map:
        raise ValueError("index must be 'nifty50' or 'nifty500'")

    service = _get_service()
    folder_id = _get_folder_id(folder_map[index])
    files = list_files_in_folder(service, folder_id)

    result = {}
    for f in files:
        symbol = f["name"].replace(".csv", "")
        try:
            df = _fetch_csv(folder_map[index], f["name"], start, end)
            result[symbol] = df
            print(f"✅ {symbol}: {len(df)} rows")
        except Exception as e:
            print(f"❌ {symbol}: {e}")

    return result