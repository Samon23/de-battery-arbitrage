## Data quality

- All 365 days contain exactly 24 hourly prices — checked explicitly rather
  than assumed.
- 573 of 8,760 hours had negative prices. These were kept, not cleaned: they
  are the most valuable hours for a battery, since it is paid to charge.

  # Battery Storage Energy Arbitrage — German Day-Ahead Market

How much revenue a 1 MW / 2 MWh grid-scale battery would have earned in 2025
by buying electricity in the cheapest hours of each day and selling it in the
most expensive, on real German day-ahead market prices.

## Findings

- A 1 MW / 2 MWh battery would have earned **EUR 68,050** across 2025.
- The best single day earned **EUR 687** on 2025-05-11; **0** days would have lost money.
- **573** of 8,760 hours had negative prices — hours where a battery is *paid* to charge.
- Revenue is strongly seasonal, concentrated in [FILL: which months look highest on your monthly chart].
- A naive forecast (same hour, one week earlier) captures **79.3%** of the
  perfect-foresight revenue, quantifying how much of this result depends on
  knowing prices in advance.

## Charts

![Average price by hour of day](outputs/hourly_profile.png)

Solar output drives prices to their daily low around midday, while demand peaks
in the evening. That gap is what the strategy captures.

![Monthly arbitrage revenue](outputs/monthly_revenue.png)

![Distribution of daily price spreads](outputs/spread_distribution.png)

Most days offer a modest spread. A small number of high-spread days account for
a disproportionate share of the annual total.

## Data

Day-ahead wholesale electricity prices for the Germany/Luxembourg bidding zone,
1 January – 31 December 2025, hourly resolution. 8,760 rows.

Source: [SMARD.de](https://www.smard.de), Bundesnetzagentur. Licensed CC BY 4.0.
The raw file is not committed; it is re-downloadable from the source.

## Method

Each day is treated independently. The hourly prices are ranked; the battery
charges during the 2 cheapest hours and discharges during the 2 most expensive.
Revenue is discharge income minus charging cost, with round-trip losses applied
on discharge.

| Parameter | Value | Meaning |
|---|---|---|
| Power | 1 MW | Charge/discharge rate |
| Capacity | 2 MWh | Two hours at full power |
| Round-trip efficiency | 85% | 2 MWh in, 1.7 MWh out |
| Cycles per day | 1 | Limits battery degradation |

The 85% efficiency sets a floor on a profitable trade: the selling price must
exceed roughly 1 ÷ 0.85 ≈ 1.18 times the buying price, or the trade loses money
despite the apparent spread.

## Data quality

- All 363 days contain exactly 24 hourly
  prices" or "30 March has 23 hours and 26 October has 25, following the
  daylight-saving clock changes"]. Checked explicitly rather than assumed.
- 573 hours had negative prices. These were kept, not cleaned — they are
  the most valuable hours for a battery, since it is paid to take the power.
- The SMARD export uses English number conventions (dot decimals). The loader
  states this explicitly, because reading it with German conventions silently
  multiplies every price by 100 rather than raising an error.

## Limitations

**This backtest assumes perfect foresight.** It selects the cheapest and dearest
hours knowing the whole day's prices in advance. A trader at 11:00 does not know
what 20:00 will cost. The result is therefore an upper bound on achievable
revenue, not a profit forecast — the real problem is price forecasting.

Also excluded:

- Grid fees, taxes and levies.
- Battery degradation cost per cycle.
- Intraday and balancing market revenue, which in practice form a large share of
  a real battery's income.
- Any optimisation of cycles per day, which is fixed at one here.
- Re-running the strategy on a naive one-week-lag forecast rather than actual
prices captures 79.3% of the theoretical maximum, with a mean absolute forecast
error of EUR 32.68/MWh.

## Repository structure

    src/load.py       load, audit and clean the SMARD export
    src/run_sql.py    execute the .sql files against the database
    src/backtest.py   the arbitrage simulation
    src/charts.py     generate the three figures
    sql/              four analysis queries
    outputs/          charts and daily revenue results

## How to run

    git clone https://github.com/Samon23/de-battery-arbitrage.git
    cd de-battery-arbitrage
    pip install -r requirements.txt
    python src/load.py
    python src/backtest.py
    python src/charts.py

Download the price data from the SMARD English download centre (Wholesale prices
→ Day-ahead prices → Germany/Luxembourg → hourly → CSV) and save it as
`data/raw/day_ahead_2025.csv`.