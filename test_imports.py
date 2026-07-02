import nsedata
import bsedata
import mcxdata
from customdata import get_scrip

print("✅ All imports work!")

# Test NSE
nse = nsedata.nse
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
print(f"NSE: {len(df)} rows")

# Test BSE
bse = bsedata.bse
df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")
print(f"BSE SENSEX: {len(df)} rows")

# Test MCX
mcx = mcxdata.mcx
df = mcx.get_spot_recent(commodity="GOLD")
print(f"MCX Gold: {len(df)} rows")

# Test custom data
df = get_scrip("RELIANCE", start="2026-06-01", end="2026-06-30")
print(f"Custom RELIANCE: {len(df)} rows")
