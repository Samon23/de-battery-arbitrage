from load import load_raw, to_timeseries
from backtest import simulate, summarise


def add_forecast(ts, lag_hours=168):
    """Naive forecast: each hour's price = the same hour one week earlier."""
    ts = ts.copy()
    ts["forecast"] = ts["price"].shift(lag_hours)
    return ts.dropna(subset=["forecast"]).reset_index(drop=True)


def evaluate(ts):
    """Mean absolute error of the naive forecast."""
    mae = (ts["forecast"] - ts["price"]).abs().mean()
    print(f"MAE:        EUR {mae:.2f}/MWh")
    print(f"mean price: EUR {ts['price'].mean():.2f}/MWh")
    return mae


def simulate_on_forecast(ts, charge_hours=2, discharge_hours=2,
                         power_mw=1.0, efficiency=0.85):
    """Choose hours using the forecast, but settle at actual prices."""
    ts = ts.copy()
    ts["date"] = ts["ts"].dt.date

    ts["rank_cheap"] = ts.groupby("date")["forecast"].rank(method="first")
    ts["rank_dear"] = ts.groupby("date")["forecast"].rank(method="first",
                                                          ascending=False)

    ts["action"] = "idle"
    ts.loc[ts["rank_cheap"] <= charge_hours, "action"] = "charge"
    ts.loc[(ts["rank_dear"] <= discharge_hours) &
           (ts["action"] == "idle"), "action"] = "discharge"

    ts["cashflow"] = 0.0
    ts.loc[ts["action"] == "charge", "cashflow"] = -ts["price"] * power_mw
    ts.loc[ts["action"] == "discharge", "cashflow"] = (
        ts["price"] * power_mw * efficiency
    )
    return ts


if __name__ == "__main__":
    ts = add_forecast(to_timeseries(load_raw()))
    evaluate(ts)

    print("\n--- perfect foresight ---")
    perfect = summarise(simulate(ts))

    print("\n--- naive forecast ---")
    naive = summarise(simulate_on_forecast(ts))

    captured = naive.sum() / perfect.sum() * 100
    print(f"\nforecast captures {captured:.1f}% of perfect-foresight revenue")