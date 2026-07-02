import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from customdata.drive_client import (
    authenticate,
    get_root_folder_id,
    get_subfolder_id,
    list_files_in_folder,
    download_file_as_df,
    upload_df_as_csv,
)

INDEX_TICKERS = {
    "nifty50": "^NSEI",
    "nifty500": "^NSE500",
}
FOLDER_MAP = {
    "nifty50_scrips": {"type": "scrip", "index": "nifty50"},
    "nifty50_index": {"type": "index", "index": "nifty50"},
    "nifty500_scrips": {"type": "scrip", "index": "nifty500"},
    "nifty500_index": {"type": "index", "index": "nifty500"},
}
TICKER_SUFFIX = ".NS"

def get_last_timestamp(df):
    if df.empty:
        return None
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df["timestamp"].max()

def fetch_new_data(symbol, start_date, end_date, is_index=False):
    ticker = symbol if is_index else f"{symbol}{TICKER_SUFFIX}"
    print(f"  Fetching {ticker} from {start_date} to {end_date}...")
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval="1m")
    except Exception as e:
        print(f"  ❌ yfinance error: {e}")
        return None
    if data.empty:
        return None
    data = data.reset_index()
    data.rename(columns={
        "Datetime": "timestamp",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    }, inplace=True)
    data["open_interest"] = 0
    if data["timestamp"].dt.tz is None:
        data["timestamp"] = data["timestamp"].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
    else:
        data["timestamp"] = data["timestamp"].dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
    return data[["timestamp", "open", "high", "low", "close", "volume", "open_interest"]]

def update_file(service, folder_name, file_name, symbol, is_index=False):
    root_id = get_root_folder_id(service)
    if not root_id:
        print("❌ Root folder not found")
        return
    folder_id = get_subfolder_id(service, folder_name, root_id)
    if not folder_id:
        print(f"❌ Folder {folder_name} not found")
        return

    files = list_files_in_folder(service, folder_id)
    file_id = None
    for f in files:
        if f["name"] == file_name:
            file_id = f["id"]
            break
    if not file_id:
        print(f"❌ File {file_name} not found in {folder_name}")
        return

    df = download_file_as_df(service, file_id)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df[df['timestamp'].notna()]
    last_ts = get_last_timestamp(df)

    if last_ts is None:
        start_date = datetime(2026, 3, 2)
    else:
        start_date = last_ts + timedelta(minutes=1)

    end_date = datetime.now()
    if start_date >= end_date:
        print(f"⏭️ {file_name}: No new data needed")
        return

    new_data = fetch_new_data(symbol, start_date, end_date, is_index)
    if new_data is None or new_data.empty:
        print(f"⏭️ {file_name}: No new data from yfinance")
        return

    updated_df = pd.concat([df, new_data], ignore_index=True)
    updated_df.drop_duplicates(subset=['timestamp'], inplace=True)
    updated_df.sort_values('timestamp', inplace=True)

    upload_df_as_csv(service, updated_df, folder_id, file_name)
    print(f"✅ {file_name}: Added {len(new_data)} rows")

def main():
    print("🔄 Starting Drive update...")
    service = authenticate()

    for folder_name, config in FOLDER_MAP.items():
        if config["type"] == "index":
            idx = config["index"]
            file_name = "NIFTY50_INDEX.csv" if idx == "nifty50" else "NIFTY500_INDEX.csv"
            symbol = INDEX_TICKERS[idx]   # <-- FIX
            update_file(service, folder_name, file_name, symbol, is_index=True)

    for folder_name, config in FOLDER_MAP.items():
        if config["type"] == "scrip":
            root_id = get_root_folder_id(service)
            if not root_id:
                continue
            folder_id = get_subfolder_id(service, folder_name, root_id)
            if not folder_id:
                continue
            files = list_files_in_folder(service, folder_id)
            for f in files:
                raw_symbol = f["name"].replace(".csv", "")
                if raw_symbol.endswith("_1min"):
                    symbol = raw_symbol.replace("_1min", "")
                elif raw_symbol.endswith("_1MIN"):
                    symbol = raw_symbol.replace("_1MIN", "")
                else:
                    symbol = raw_symbol
                update_file(service, folder_name, f["name"], symbol, is_index=False)

    print("🎉 Update complete!")

if __name__ == "__main__":
    main()