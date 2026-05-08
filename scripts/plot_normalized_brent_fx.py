# plot_normalized_brent_fx.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(r"C:\Users\hocke\Desktop\quant_portfolio_scaffold\data\FX-Hedging-main")

FILES = {
    "Brent Crude": BASE_DIR / "Commodities" / "Global Stats" / "Brent Crude" / "brent_crude_5y_daily.csv",
    "USD/NGN": BASE_DIR / "FX Rates (USD - NGN)" / "usdngn_5y_daily.csv",
    "USD/ZMW": BASE_DIR / "FX Rates (USD - ZMW)" / "usdzmw_5y_daily.csv",
    "USD/GHS": BASE_DIR / "FX Rates (USD - GHS)" / "usdghs_5y_daily.csv",
}

OUTPUT_DIR = BASE_DIR / "outputs" / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = OUTPUT_DIR / "normalized_brent_usdngn_usdzmw_usdghs_5y.png"


def load_series(label, path):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df = df[["Date", "Close"]].dropna()
    df = df[df["Close"] > 0]
    df = df.rename(columns={"Close": label})
    return df


# Load and merge on Date
merged = None

for label, path in FILES.items():
    if not path.exists():
        raise FileNotFoundError(f"Missing file for {label}: {path}")

    temp = load_series(label, path)

    if merged is None:
        merged = temp
    else:
        merged = pd.merge(merged, temp, on="Date", how="outer")


# Sort, forward-fill gaps from different market calendars
merged = merged.sort_values("Date").set_index("Date")
merged = merged.ffill().dropna()

# Normalize each series to 100 at first common available date
normalized = merged / merged.iloc[0] * 100

# Save normalized data too
normalized_out = OUTPUT_DIR / "normalized_brent_fx_5y.csv"
normalized.to_csv(normalized_out)

# Plot
plt.figure(figsize=(14, 8))

for col in normalized.columns:
    plt.plot(normalized.index, normalized[col], label=col, linewidth=2)

plt.axhline(100, linewidth=1, linestyle="--")

plt.title("Normalized Brent Crude vs African FX Rates (5Y)", fontsize=16, pad=15)
plt.ylabel("Normalized Index Level (Start = 100)")
plt.xlabel("Date")

plt.legend()
plt.tight_layout()

plt.savefig(OUT_FILE, dpi=300)

print(f"Saved chart: {OUT_FILE}")
print(f"Saved normalized data: {normalized_out}")

plt.show()