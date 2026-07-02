---
layout: default
title: Indices
parent: NSE India
nav_order: 3
---

# Capital Market — Indices

**Category:** `capital_market` | **Sub-section:** `indices`

Covers NSE broad-market and sectoral index data, plus the derived movers helper.

---

## Summary Table

| Function / Dataset | Description | Return type |
| :--- | :--- | :--- |
| `ind_close_all` | Daily closing values for all NSE indices | DataFrame |
| `top_movers` | Derived helper — largest gainers/losers from a bhavcopy DataFrame | DataFrame |

---

## Quick Start

```python
from nsedata import nse

df = nse.get("capital_market", "indices", "ind_close_all", "2026-06-30")
print(df.head())
```

---

## `ind_close_all` — Daily Index Closing Values

**Signature:**
```python
nse.get("capital_market", "indices", "ind_close_all", date)
```

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `date` | str | Yes | — | `YYYY-MM-DD` trading day |

**Example:**
```python
df = nse.get("capital_market", "indices", "ind_close_all", "2026-06-30")
nifty = df[df["Index Name"].str.contains("Nifty 50", case=False, na=False)]
print(nifty[["Index Name", "Closing Index Value"]])
```

**Sample output (illustrative — column names per `nse.py` docstrings, e.g. via `derive_tri`):**

Index Name           Closing Index Value
0  Nifty 50             25419.22
1  Nifty Bank           56230.10
2  Nifty IT             38210.55

> Note: exact column names for `ind_close_all` weren't in the pasted registry snippet — `nse.py`'s `derive_tri()` expects either `Close` or `Closing Index Value`, confirming this is the column NSE returns. Verify against a live pull before publishing if precision matters.

---

## `top_movers` — Gainers/Losers Helper

This isn't a raw NSE dataset call — it's a **pattern**, not a confirmed function in the pasted source. If `top_movers` exists as a real function in your registry/API, paste its signature and I'll update this section with the verified details. For now, here's the equivalent using `pandas` directly on `ind_close_all` output:

```python
df = nse.get("capital_market", "indices", "ind_close_all", "2026-06-30")
top_gainers = df.nlargest(5, "Closing Index Value")
top_losers  = df.nsmallest(5, "Closing Index Value")
```

---

## Common Patterns

**1. Track Nifty 50 across a date**
```python
df = nse.get("capital_market", "indices", "ind_close_all", "2026-06-30")
nifty50 = df[df["Index Name"] == "Nifty 50"]
```

**2. Combine with historical TRI**
```python
from nsedata import nse

price_df = nse.get("capital_market", "indices", "ind_close_all", "2026-06-30")
nifty = price_df[price_df["Index Name"] == "Nifty 50"].rename(
    columns={"Closing Index Value": "Close"})
tri_df = nse.derive_tri(nifty)
```

**3. Save to CSV**
```python
df = nse.get("capital_market", "indices", "ind_close_all", "2026-06-30")
df.to_csv("nse_indices_2026-06-30.csv", index=False)
```

## Notes & Limitations

- **Date format:** `YYYY-MM-DD`, trading days only.
- For **niftyindices.com**-based historical/TRI data (different from `ind_close_all`), see `nse.get_historical_index()` and `nse.get_tri()` — these hit a Cloudflare-protected endpoint that may be blocked from cloud/Lambda IPs; works reliably from residential IPs.
- `nse.derive_tri()` is an approximation when the TRI endpoint is unreachable — provide real dividend records for accuracy.

## Related Pages

- [Capital Market — Equities & SME](capital-market)
- [NSE F&O](derivatives-equity)
- [API Reference](api-reference)