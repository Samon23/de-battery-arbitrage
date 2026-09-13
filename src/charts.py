from pathlib import Path

import matplotlib.pyplot as plt

from load import load_raw, to_timeseries
from backtest import simulate

OUT = Path("outputs")


def chart_hourly_profile(ts):
    """Average price by hour of day — this is why the strategy works."""
    profile = ts.groupby(ts["ts"].dt.hour)["price"].mean()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(profile.index, profile.values, linewidth=2, color="#0e7c86")
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Average price (EUR/MWh)")
    ax.set_title("Midday solar collapses prices; demand peaks in the evening")
    ax.set_xticks(range(0, 24, 2))
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "hourly_profile.png", dpi=150)
    plt.close(fig)


def chart_monthly_revenue(result):
    """Arbitrage revenue by month — the seasonality."""
    monthly = result.groupby(result["ts"].dt.to_period("M"))["cashflow"].sum()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar([str(p) for p in monthly.index], monthly.values, color="#b4590c")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (EUR)")
    ax.set_title("Arbitrage revenue is not earned evenly across the year")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(OUT / "monthly_revenue.png", dpi=150)
    plt.close(fig)


def chart_spread_distribution(ts):
    """How many days were actually worth trading."""
    grouped = ts.groupby(ts["ts"].dt.date)["price"]
    spread = grouped.max() - grouped.min()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(spread, bins=40, color="#0e7c86", edgecolor="white")
    ax.set_xlabel("Daily price spread (EUR/MWh)")
    ax.set_ylabel("Number of days")
    ax.set_title("Most days offer a modest spread; a few are worth far more")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(OUT / "spread_distribution.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    ts = to_timeseries(load_raw())
    result = simulate(ts)

    chart_hourly_profile(ts)
    chart_monthly_revenue(result)
    chart_spread_distribution(ts)
    print("saved 3 charts to outputs/")