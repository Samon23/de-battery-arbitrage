import pandas as pd


def simulate(df, charge_hours=2, discharge_hours=2,
             power_mw=1.0, efficiency=0.85):
    """
    Simple daily arbitrage: charge in the cheapest hours,
    discharge in the dearest. One cycle per day.
    """
    df = df.copy()
    df["date"] = df["ts"].dt.date

    # rank every hour within its own day
    df["rank_cheap"] = df.groupby("date")["price"].rank(method="first")
    df["rank_dear"]  = df.groupby("date")["price"].rank(method="first",
                                                       ascending=False)

    # assign actions — charge first, so an hour is never both
    df["action"] = "idle"
    df.loc[df["rank_cheap"] <= charge_hours, "action"] = "charge"
    df.loc[(df["rank_dear"] <= discharge_hours) &
           (df["action"] == "idle"), "action"] = "discharge"

    # cash: pay full price to charge, earn on what survives the losses
    df["cashflow"] = 0.0
    df.loc[df["action"] == "charge", "cashflow"] = (
        -df["price"] * power_mw
    )
    df.loc[df["action"] == "discharge", "cashflow"] = (
        df["price"] * power_mw * efficiency
    )

    return df


def summarise(df):
    """Daily and annual revenue."""
    daily = df.groupby("date")["cashflow"].sum().rename("revenue_eur")
    total = daily.sum()
    print(f"annual revenue:     EUR {total:,.0f}")
    print(f"best day:           EUR {daily.max():,.0f} on {daily.idxmax()}")
    print(f"worst day:          EUR {daily.min():,.0f} on {daily.idxmin()}")
    print(f"days with a loss:   {(daily < 0).sum()}")
    return daily

if __name__ == "__main__":
    from load import load_raw, to_timeseries

    ts = to_timeseries(load_raw())
    result = simulate(ts)
    daily = summarise(result)

    daily.to_csv("outputs/daily_revenue.csv")
    print("saved outputs/daily_revenue.csv")