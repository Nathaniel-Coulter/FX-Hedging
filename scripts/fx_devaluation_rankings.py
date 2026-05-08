# fx_devaluation_rankings.py

import pandas as pd
from pathlib import Path

BASE_DIR = Path(r"C:\Users\hocke\Desktop\quant_portfolio_scaffold\data\FX-Hedging-main")
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

PERIODS = ["1y", "3y", "5y"]

results = []

for fx_folder in BASE_DIR.glob("FX Rates (USD - *)"):
    if not fx_folder.is_dir():
        continue

    currency = fx_folder.name.replace("FX Rates (USD - ", "").replace(")", "")

    for period in PERIODS:
        files = list(fx_folder.glob(f"*_{period}_daily.csv"))

        if not files:
            print(f"Missing {period} file for {currency}")
            continue

        file_path = files[0]

        df = pd.read_csv(file_path)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        df = df.dropna(subset=["Close"])
        df = df[df["Close"] > 0]

        if len(df) < 2:
            print(f"Not enough data for {currency} {period}")
            continue

        start_date = df["Date"].iloc[0]
        end_date = df["Date"].iloc[-1]

        start_fx = df["Close"].iloc[0]
        end_fx = df["Close"].iloc[-1]

        # Since these are USD/LOCAL pairs:
        # positive = local currency devalued vs USD
        # negative = local currency appreciated vs USD
        pct_change = (end_fx / start_fx - 1) * 100

        results.append({
            "currency": currency,
            "period": period,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
            "start_usd_local": start_fx,
            "end_usd_local": end_fx,
            "pct_change_usd_local": pct_change,
            "interpretation": "devalued vs USD" if pct_change > 0 else "appreciated vs USD",
            "file": str(file_path),
        })

rankings = pd.DataFrame(results)

if rankings.empty:
    raise ValueError("No FX ranking data found.")

rankings = rankings.sort_values(
    ["period", "pct_change_usd_local"],
    ascending=[True, False]
)

out_file = OUTPUT_DIR / "fx_devaluation_rankings.csv"
rankings.to_csv(out_file, index=False)

print("\nSaved:")
print(out_file)

for period in PERIODS:
    print("\n" + "=" * 70)
    print(f"{period.upper()} FX DEVALUATION RANKING")
    print("=" * 70)

    period_df = rankings[rankings["period"] == period].copy()
    period_df = period_df.sort_values("pct_change_usd_local", ascending=False)

    print(
        period_df[
            [
                "currency",
                "start_date",
                "end_date",
                "start_usd_local",
                "end_usd_local",
                "pct_change_usd_local",
                "interpretation",
            ]
        ].to_string(index=False)
    )