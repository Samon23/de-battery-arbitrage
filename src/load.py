import pandas as pd
from pathlib import Path

RAW = Path("data/raw/day_ahead_2025.csv")


def load_raw(path=RAW):
    """Read the SMARD export: semicolon separated, dot decimals."""
    df = pd.read_csv(
        path,
        sep=";",
        decimal=".",
        thousands=",",
        na_values=["-", ""],
    )
    df.columns = [c.strip() for c in df.columns]
    return df

def audit(df, name="dataframe"):
    """Print a data-quality summary. Returns df so it can be chained."""
    print(f"--- audit: {name} ---")
    print(f"rows: {len(df):,}   columns: {df.shape[1]}")
    print("\ndtypes:", df.dtypes, sep="\n")
    print("\nmissing per column:", df.isna().sum(), sep="\n")
    print(f"\nduplicate rows: {df.duplicated().sum()}")
    return df

def to_timeseries(df):
    """Return a tidy frame: ts (datetime) and price (float)."""
    df = df.copy()

    start_col = df.columns[0]
    price_col = [c for c in df.columns
                 if c.startswith("Germany/Luxembourg")][0]

    df["ts"] = pd.to_datetime(
        df[start_col],
        format="%b %d, %Y %I:%M %p",
        errors="coerce",
    )

    unparsed = df["ts"].isna().sum()
    if unparsed:
        raise ValueError(f"{unparsed} timestamps failed to parse — check the date format")

    out = df[["ts", price_col]].rename(columns={price_col: "price"})
    out = out.dropna(subset=["price"]).sort_values("ts").reset_index(drop=True)
    return out

def check_calendar(df):
    """Flag any day that does not have exactly 24 hourly prices."""
    per_day = df.groupby(df["ts"].dt.date).size()
    odd = per_day[per_day != 24]
    print(f"days without 24 hours: {len(odd)}")
    print(odd)
    return odd

if __name__ == "__main__":
    df = load_raw()
    audit(df, "raw SMARD export")

    ts = to_timeseries(df)
    audit(ts, "clean timeseries")

    check_calendar(ts)

    negative = (ts["price"] < 0).sum()
    print(f"negative price hours: {negative} of {len(ts)}")