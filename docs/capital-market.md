---
layout: default
title: Capital Market
parent: NSE India
nav_order: 1
---

# Capital Market

This page documents the NSE Capital Market Equities and SME segment in `nsedata` (`capital_market` / `equities_sme`). It covers 32 of the 91 total datasets, including daily bhavcopy files, delivery and surveillance reports, risk and settlement outputs, static reference files, and monthly categorization files.

## Installation / Import

Install and environment setup are covered in [Installation]({{ site.baseurl }}/installation).

```python
from nsedata import nse
```

## Function Reference Summary (32 Datasets)

| Function name | Description | Segment | Return type |
|---|---|---|---|
| `nse.get("capital_market", "equities_sme", "bhavcopy_pr", date)` | Bhavcopy (PR) daily ZIP bundle (price records) | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "sec_bhavdata_full", date)` | Full securities bhavcopy with delivery | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "bhav_udiff", date)` | CM bhavcopy in UDiFF/ISIN format | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "security_master", date)` | CM security master (ISIN, lot size, face value) | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "market_activity", date)` | Daily market activity summary | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "cmvolt", date)` | Security volatility for VaR | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "short_selling", date)` | Short selling report | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "mto", date)` | Multiple Trade Orders delivery file | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "52wk_high_low", date)` | 52-week high/low list (portal only) | Equity | Portal file (manual) |
| `nse.get("capital_market", "equities_sme", "block_deals", date)` | Block deals | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "bulk_deals", date)` | Bulk deals | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "pe", date)` | Index P/E, P/B, dividend yield file | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "reg_ind", date)` | Regional indices (primary cut) | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "reg1_ind", date)` | Regional indices (secondary cut) | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "sme", date)` | SME platform EOD market data | SME | DataFrame |
| `nse.get("capital_market", "equities_sme", "sme_bands", date)` | SME complete price bands | SME | DataFrame |
| `nse.get("capital_market", "equities_sme", "eq_band_changes", date)` | Equity price band changes | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "sec_list", date)` | Current security list | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "series_change", date)` | Series change notifications | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "auction_buy", date, settno=...)` | Auction buy file (settlement-based) | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "cm_latency", date)` | CM latency statistics | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "mf_var", date)` | Mutual fund VaR file | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "appsec_collval", date)` | Approved security collateral valuation | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "csqr", date, settno=...)` | Client segregation report | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "c_stt", date)` | Securities transaction tax data | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "c_stt_ind", date)` | STT indicator file | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "fcm_bc", date)` | FCM interim bhavcopy | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "mrg_trading", date)` | Margin trading facility report | Equity | DataFrame |
| `nse.download("capital_market", "equities_sme", "cvar1", date, snapshot=1..6)` | VaR margin snapshots (DAT) | Equity | File path / S3 URI |
| `nse.get("capital_market", "equities_sme", "corpbond", date)` | Corporate bond file extracted from PR ZIP | Equity | DataFrame |
| `nse.get("capital_market", "equities_sme", "c_catg", "YYYY-MM")` | Monthly security categorization (T01) | Equity | DataFrame |
| `nse.download("capital_market", "equities_sme", "daily_settlement_doc", date)` | Daily settlement statistics document | Equity | File path / S3 URI |

## Quick Start

```python
from nsedata import nse

# Recommended daily EOD dataset (price + delivery)
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
print(df.shape)

# See available capital market datasets
capital_df = nse.list_datasets(category="capital_market", subcategory="equities_sme")
print(len(capital_df))
```

## Function Reference

Core API signatures used on this page:

```python
nse.get(category, subcategory, dataset, date, **kwargs)          # -> DataFrame
nse.download(category, subcategory, dataset, date, **kwargs)     # -> local path or s3:// URI
nse.list_datasets(category=None, subcategory=None)               # -> DataFrame
nse.get_config_info(category, subcategory, dataset)              # -> dict
```

### 1) Bhavcopy and Price Data

Function signature:

```python
nse.get("capital_market", "equities_sme", dataset, date, **kwargs)
```

Parameters:

| Name | Type | Required | Description | Default |
|---|---|---|---|---|
| `category` | `str` | Yes | Use `capital_market` | None |
| `subcategory` | `str` | Yes | Use `equities_sme` | None |
| `dataset` | `str` | Yes | Example: `bhavcopy_pr`, `sec_bhavdata_full`, `bhav_udiff` | None |
| `date` | `str` | Yes | `YYYY-MM-DD` for daily datasets | None |
| `kwargs` | `dict` | Optional | Extra dataset-specific args | `{}` |

Example:

```python
from nsedata import nse

bhav_df = nse.get("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22")
full_df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")

reliance = full_df[full_df["SYMBOL"] == "RELIANCE"]
print(bhav_df.shape)
print(reliance[["SYMBOL", "OPEN_PRICE", "HIGH_PRICE", "LOW_PRICE", "CLOSE_PRICE"]].head())
```

Sample output:

```text
(3500+, 14)
    SYMBOL  OPEN_PRICE  HIGH_PRICE  LOW_PRICE  CLOSE_PRICE
0  RELIANCE     ...        ...         ...        ...
```

### 2) Delivery, Trade Activity, and Surveillance Files

Function signature:

```python
nse.get("capital_market", "equities_sme", dataset, date)
```

Parameters:

| Name | Type | Required | Description | Default |
|---|---|---|---|---|
| `dataset` | `str` | Yes | Example: `mto`, `short_selling`, `market_activity`, `eq_band_changes` | None |
| `date` | `str` | Yes | Trading date in `YYYY-MM-DD` format | None |

Example:

```python
from nsedata import nse

mto_df = nse.get("capital_market", "equities_sme", "mto", "2026-05-22")
ss_df = nse.get("capital_market", "equities_sme", "short_selling", "2026-05-22")

print(mto_df.shape)
print(ss_df.head(3))
```

Sample output:

```text
mto_df: (rows, cols)
short_selling head:
  Security Name  Symbol Name  Trade Date   Quantity
0 ...            ...          ...          ...
```

### 3) Clearing, Margin, and Settlement Workflows

Function signatures:

```python
nse.get("capital_market", "equities_sme", "auction_buy", date, settno=None)
nse.get("capital_market", "equities_sme", "csqr", date, settno=None)
nse.download("capital_market", "equities_sme", "cvar1", date, snapshot=1..6, output_dir=...)
nse.download("capital_market", "equities_sme", "daily_settlement_doc", date, output_dir=...)
```

Parameters:

| Name | Type | Required | Description | Default |
|---|---|---|---|---|
| `dataset` | `str` | Yes | `auction_buy`, `csqr`, `cvar1`, `daily_settlement_doc` | None |
| `date` | `str` | Yes | `YYYY-MM-DD` trading date | None |
| `settno` | `str` | Optional | Override settlement number for `auction_buy`/`csqr` | Auto-calculated |
| `snapshot` | `int` | Optional | `1..6` for `cvar1` | None |
| `output_dir` | `str` | Optional | Local target directory for `download` | Current directory |
| `s3_bucket` | `str` | Optional | Upload target S3 bucket (for `download`) | None |
| `s3_prefix` | `str` | Optional | Upload key prefix in S3 | None |

Example:

```python
from nsedata import nse

aub_df = nse.get("capital_market", "equities_sme", "auction_buy", "2026-05-22")
csqr_df = nse.get("capital_market", "equities_sme", "csqr", "2026-05-22")

for snap in range(1, 7):
    nse.download(
        "capital_market",
        "equities_sme",
        "cvar1",
        "2026-05-22",
        snapshot=snap,
        output_dir="./data",
    )
```

Sample output:

```text
auction_buy: DataFrame returned
csqr: DataFrame returned
Downloaded: ./data/C_VAR1_22052026_1.DAT ... ./data/C_VAR1_22052026_6.DAT
```

### 4) Monthly and Static Datasets

Function signatures:

```python
nse.get("capital_market", "equities_sme", "c_catg", "YYYY-MM")
nse.get("capital_market", "equities_sme", dataset, "YYYY-MM-DD")   # for static daily files
```

Parameters:

| Name | Type | Required | Description | Default |
|---|---|---|---|---|
| `dataset` | `str` | Yes | `c_catg` (monthly) or static keys like `block_deals`, `bulk_deals`, `series_change` | None |
| `date` | `str` | Yes | `YYYY-MM` for monthly, `YYYY-MM-DD` for daily/static calls | None |

Example:

```python
from nsedata import nse

monthly_df = nse.get("capital_market", "equities_sme", "c_catg", "2026-05")
bulk_df = nse.get("capital_market", "equities_sme", "bulk_deals", "2026-05-22")

print(monthly_df.shape)
print(bulk_df.head(3))
```

Sample output:

```text
c_catg: (13000+, cols)
bulk_deals: DataFrame with deal-level rows
```

## Common Patterns

### Pattern 1: Fetch a date range and combine

```python
from datetime import date, timedelta
import pandas as pd
from nsedata import nse

start = date(2026, 5, 18)
end = date(2026, 5, 22)

frames = []
d = start
while d <= end:
    ds = d.strftime("%Y-%m-%d")
    try:
        df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", ds)
        df["trade_date"] = ds
        frames.append(df)
    except Exception:
        pass
    d += timedelta(days=1)

combined = pd.concat(frames, ignore_index=True)
print(combined.shape)
```

### Pattern 2: Filter one symbol and save CSV

```python
from nsedata import nse

df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
rel = df[df["SYMBOL"] == "RELIANCE"].copy()
rel.to_csv("reliance_sec_bhavdata_full_2026-05-22.csv", index=False)
```

### Pattern 3: Keep both parsed DataFrame and raw archive file

```python
from nsedata import nse

df = nse.get("capital_market", "equities_sme", "fcm_bc", "2026-05-22")
raw_path = nse.download("capital_market", "equities_sme", "fcm_bc", "2026-05-22", output_dir="./raw")

print(df.shape)
print(raw_path)
```

## Notes / Limitations

- Source in package docs: `nsearchives.nseindia.com` direct archives.
- `nse.get(...)` returns a DataFrame only for datasets that support DataFrame output; use `nse.download(...)` for download-only datasets like `cvar1` and `daily_settlement_doc`.
- Date formats are strict: `YYYY-MM-DD` for daily datasets, `YYYY-MM` for monthly datasets.
- Non-trading days (weekends/holidays) can return missing-file errors.
- `auction_buy` and `csqr` support optional `settno`; if omitted, settlement number is auto-calculated.
- `52wk_high_low` is marked portal-only in registry and is not available via direct archive URL.

## Related Pages

- [Capital Market - Indices]({{ site.baseurl }}/nse/capital-market-indices)
- [Derivatives - Equity F&O]({{ site.baseurl }}/nse/derivatives-equity)
- [API Reference]({{ site.baseurl }}/nse/api-reference)
