# pull_fx_yfinance.py
# This script just pulls the USD to (NGN) FX rates from yfinance Api. All you have to do is change the second currency and it works with all currencies not just african.

import yfinance as yf
from pathlib import Path

TICKER = "USDMAD=X" #change "MAD" to the currency of your choice
PERIOD = "5y" #change "5y" to the time period you want
INTERVAL = "1d"

out_dir = Path("data")
out_dir.mkdir(exist_ok=True)

out_file = out_dir / "usdmad_5y_daily.csv" # change the "5y" to whatever time period you're pulling just so the CSV file is named correctly :)

df = yf.download(
    TICKER,
    period=PERIOD,
    interval=INTERVAL,
    auto_adjust=False,
    progress=True,
)

if df.empty:
    raise ValueError("No data returned from yfinance.")

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