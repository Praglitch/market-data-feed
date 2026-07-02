#!/usr/bin/env python3
"""
market-data-feed Demo Script
Fetches data from NSE, BSE, MCX, and shows the most recent custom 1‑minute data.
"""

import sys
from datetime import datetime, timedelta

# --- Helper: latest trading day (Mon-Fri) ---
def get_latest_trading_day():
    today = datetime.now()
    for i in range(5):
        dt = today - timedelta(days=i)
        if dt.weekday() < 5:
            return dt
    return today - timedelta(days=1)

primary_date = get_latest_trading_day()
date_str = primary_date.strftime("%Y-%m-%d")
fallback_date_str = "2026-06-30"

print(f"📅 Primary date: {date_str} (latest trading day)")
print(f"📅 Fallback date: {fallback_date_str} (if NSE fails)\n")

# --- 1. NSE ---
def fetch_nse(date_str):
    import nsedata
    nse = nsedata.nse
    try:
        df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", date_str)
        return df, None
    except Exception as e:
        return None, e

try:
    import nsedata
    df_nse, err = fetch_nse(date_str)
    if df_nse is not None:
        print(f"✅ NSE ({date_str}): {len(df_nse)} securities")
        print(df_nse[["SYMBOL", "CLOSE_PRICE"]].head(3).to_string(index=False))
    else:
        print(f"⚠️ NSE on {date_str} failed (file not yet published).")
        print(f"   Retrying with fallback {fallback_date_str}...")
        df_nse, err2 = fetch_nse(fallback_date_str)
        if df_nse is not None:
            print(f"✅ NSE ({fallback_date_str}): {len(df_nse)} securities")
            print(df_nse[["SYMBOL", "CLOSE_PRICE"]].head(3).to_string(index=False))
        else:
            print(f"❌ NSE failed even on fallback: {err2}")
except Exception as e:
    print(f"❌ NSE: {e}")

print("\n" + "-"*50 + "\n")

# --- 2. BSE ---
try:
    import bsedata
    bse = bsedata.bse
    start = (primary_date - timedelta(days=7)).strftime("%Y-%m-%d")
    df_bse = bse.get_index("SENSEX", start, date_str)
    if df_bse.empty:
        start_fallback = (datetime.strptime(fallback_date_str, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
        df_bse = bse.get_index("SENSEX", start_fallback, fallback_date_str)
    print(f"✅ BSE SENSEX: {len(df_bse)} rows")
    print(df_bse[["Date", "Close"]].tail(3).to_string(index=False))
except Exception as e:
    print(f"❌ BSE: {e}")

print("\n" + "-"*50 + "\n")

# --- 3. MCX ---
try:
    import mcxdata
    mcx = mcxdata.mcx
    df_mcx = mcx.get_spot_recent(commodity="GOLD")
    if df_mcx.empty:
        print("⏭️ MCX Gold: No data (market may be closed or API empty)")
    else:
        print(f"✅ MCX Gold: {len(df_mcx)} rows")
        print(df_mcx[["Commodity", "Spot Price (Rs.)", "Location"]].head(3).to_string(index=False))
except Exception as e:
    print(f"❌ MCX: {e}")

print("\n" + "-"*50 + "\n")

# --- 4. Custom Data (1-minute) – ALWAYS SHOWS LATEST ---
try:
    from customdata import get_scrip

    # Fetch the entire RELIANCE file (no date filter) to get the very latest row
    df_full = get_scrip("RELIANCE")
    if df_full.empty:
        print("⏭️ Custom RELIANCE: No data (check OAuth and folder access)")
    else:
        latest_ts = df_full['timestamp'].iloc[-1]
        print(f"✅ Custom RELIANCE: {len(df_full)} rows total")
        print(f"   📌 Latest available timestamp: {latest_ts}")
        print("\n   Last 5 rows (showing the most recent data):")
        print(df_full[["timestamp", "close", "volume"]].tail(5).to_string(index=False))

except ImportError as e:
    print(f"❌ Customdata import error: {e}")
except Exception as e:
    print(f"❌ Customdata: {e}")
