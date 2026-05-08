# plot_fx_devaluation_rankings.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================

CSV_PATH = Path(
    r"C:\Users\hocke\Desktop\quant_portfolio_scaffold\data\FX-Hedging-main\outputs\fx_devaluation_rankings.csv"
)

OUTPUT_DIR = CSV_PATH.parent / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)

PERIODS = ["1y", "3y", "5y"]

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(CSV_PATH)

# =========================================================
# PLOT FUNCTION
# =========================================================

for period in PERIODS:

    period_df = df[df["period"] == period].copy()

    if period_df.empty:
        print(f"No data for {period}")
        continue

    # Sort descending
    period_df = period_df.sort_values(
        "pct_change_usd_local",
        ascending=False
    )

    # =====================================================
    # PLOT
    # =====================================================

    plt.figure(figsize=(12, 7))

    bars = plt.bar(
        period_df["currency"],
        period_df["pct_change_usd_local"]
    )

    # Add value labels
    for bar, value in zip(bars, period_df["pct_change_usd_local"]):

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.axhline(0, linewidth=1)

    plt.title(
        f"African Currency Devaluation vs USD ({period.upper()})",
        fontsize=16,
        pad=15
    )

    plt.ylabel("% Change in USD/Local FX Rate")
    plt.xlabel("Currency")

    plt.xticks(rotation=0)

    plt.tight_layout()

    out_file = OUTPUT_DIR / f"fx_devaluation_{period}.png"

    plt.savefig(out_file, dpi=300)

    print(f"Saved: {out_file}")

    plt.show()