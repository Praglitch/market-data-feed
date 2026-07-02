import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# ---------- CONFIG ----------
DATA_ROOT = "data"
FOLDER_MAP = {
    "nifty50_scrips": {"type": "scrip", "index": "nifty50"},
    "nifty50_index": {"type": "index", "index": "nifty50"},
    "nifty500_scrips": {"type": "scrip", "index": "nifty500"},
    "nifty500_index": {"type": "index", "index": "nifty500"},
}
INDEX_TICKERS = {"nifty50": "^NSEI", "nifty500": "^NSE500"}
TICKER_SUFFIX = ".NS"
STANDARD_COLUMNS = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
# ------------------------------------

def get_last_timestamp(df):
    """Return the maximum timestamp from a DataFrame."""
    if df.empty:
        return None
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df['timestamp'].max()

def fetch_new_data(symbol, start_date, end_date, is_index=False):
    """
    Fetch 1-minute OHLCV data from yfinance.
    Converts UTC timestamps to IST and makes them naive.
    """
    ticker = symbol if is_index else f"{symbol}{TICKER_SUFFIX}"
    print(f"  Fetching {ticker} from {start_date} to {end_date}...")
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval="1m")
    except Exception as e:
        print(f"  ❌ yfinance error: {e}")
        return None
    if data.empty:
        return None

    # Flatten MultiIndex columns (if any)
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
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

    # Convert UTC → IST
    if data["timestamp"].dt.tz is None:
        data["timestamp"] = data["timestamp"].dt.tz_localize('UTC')
    data["timestamp"] = data["timestamp"].dt.tz_convert('Asia/Kolkata')
    data["timestamp"] = data["timestamp"].dt.tz_localize(None)

    return data[STANDARD_COLUMNS]

def update_local_file(folder_name, file_name, symbol, is_index=False):
    """Update a single local CSV file by appending missing data."""
    local_path = os.path.join(DATA_ROOT, folder_name, file_name)
    if not os.path.exists(local_path):
        print(f"❌ Local file not found: {local_path}")
        return

    # Read the file (all columns)
    try:
        df = pd.read_csv(local_path)
    except Exception as e:
        print(f"⚠️ Skipping {file_name}: Could not read file: {e}")
        return

    # Handle column count
    if df.shape[1] == 6:
        # Only 6 columns -> add open_interest with 0
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df['open_interest'] = 0
    elif df.shape[1] == 7:
        # 7 columns -> ensure correct naming
        df.columns = STANDARD_COLUMNS
    else:
        print(f"⚠️ Skipping {file_name}: Unexpected number of columns ({df.shape[1]})")
        return

    # Clean and convert timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df[df['timestamp'].notna()]   # drop NaT

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

    updated = pd.concat([df, new_data], ignore_index=True)
    updated.drop_duplicates(subset=['timestamp'], inplace=True)
    updated.sort_values('timestamp', inplace=True)

    # Save only the 7 standard columns
    updated[STANDARD_COLUMNS].to_csv(local_path, index=False)
    print(f"✅ {file_name}: Added {len(new_data)} rows")

def main():
    print("🔄 Starting local update...")

    # Update indexes first
    for folder_name, config in FOLDER_MAP.items():
        if config["type"] == "index":
            idx = config["index"]
            file_name = "NIFTY50_INDEX.csv" if idx == "nifty50" else "NIFTY500_INDEX.csv"
            symbol = INDEX_TICKERS[idx]   # e.g., "^NSEI"
            update_local_file(folder_name, file_name, symbol, is_index=True)

    # Update all scrips
    for folder_name, config in FOLDER_MAP.items():
        if config["type"] == "scrip":
            folder_path = os.path.join(DATA_ROOT, folder_name)
            if not os.path.exists(folder_path):
                print(f"⚠️ Folder not found: {folder_path}")
                continue
            for file_name in os.listdir(folder_path):
                if not file_name.endswith(".csv"):
                    continue
                raw_symbol = file_name.replace(".csv", "")
                # Remove _1min or _1MIN suffix
                if raw_symbol.endswith("_1min"):
                    symbol = raw_symbol.replace("_1min", "")
                elif raw_symbol.endswith("_1MIN"):
                    symbol = raw_symbol.replace("_1MIN", "")
                else:
                    symbol = raw_symbol
                update_local_file(folder_name, file_name, symbol, is_index=False)

    print("🎉 Local update complete!")

if __name__ == "__main__":
    main()