# market-data-feed

**Unified Indian Market Data + Custom 1‑Minute OHLCV**

[![PyPI version](https://badge.fury.io/py/market-data-feed.svg)](https://pypi.org/project/market-data-feed/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 📦 Installation

```bash
pip install market-data-feed

🚀 Quick Start
python
import nsedata
import bsedata
import mcxdata
from customdata import get_scrip

# NSE: Daily Bhavcopy
nse = nsedata.nse
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-06-30")
print(f"NSE: {len(df)} securities")

# BSE: SENSEX Historical
bse = bsedata.bse
df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")
print(f"BSE SENSEX: {len(df)} rows")

# MCX: Gold Spot Price
mcx = mcxdata.mcx
df = mcx.get_spot_recent(commodity="GOLD")
print(f"MCX Gold: {len(df)} rows")
📊 What This Package Gives You
Module	Source	What You Get
nsedata	NSE India	91 datasets — equities, F&O, debt, indices, SLB, EGR
bsedata	BSE India	55+ indices — SENSEX, BSE500, BANKEX, sectoral/thematic
mcxdata	MCX India	28 commodities — spot prices (recent + archive)
customdata	Google Drive	1‑minute OHLCV for Nifty 50 & 500 scrips and indices
🔐 Custom Data Setup (One‑Time)
customdata uses Google Drive. One‑time OAuth setup required.

Create a Google Cloud Project and enable the Drive API.

Create an OAuth 2.0 Desktop Client ID and download the JSON.

Place it as credentials/oauth_client.json in your working directory.

Run get_scrip() once — your browser will open for authentication.

📄 License
MIT — Data sourced from NSE India, BSE India, and MCX India.


Happy Trading! 🚀
