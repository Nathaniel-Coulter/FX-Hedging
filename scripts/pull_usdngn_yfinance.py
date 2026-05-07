# pull_usdngn_yfinance.py

import yfinance as yf
from pathlib import Path

TICKER = "USDNGN=X"
PERIOD = "5y"
INTERVAL = "1d"

out_dir = Path("data")
out_dir.mkdir(exist_ok=True)

out_file = out_dir / "usdngn_5y_daily.csv"

df = yf.download(
    TICKER,
    period=PERIOD,
    interval=INTERVAL,
    auto_adjust=False,
    progress=True,
)

if df.empty:
    raise ValueError("No data returned from yfinance.")

# Flatten columns if yfinance returns multi-index columns
if isinstance(df.columns, tuple) or hasattr(df.columns, "levels"):
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

df = df.reset_index()

# Keep volume if present, but FX usually has no real volume on Yahoo
cols_to_keep = ["Date", "Open", "High", "Low", "Close", "Adj Close"]
if "Volume" in df.columns:
    cols_to_keep.append("Volume")

df = df[cols_to_keep]

df.to_csv(out_file, index=False)

print(f"Saved {len(df):,} rows to: {out_file}")
print(df.head())
print(df.tail())