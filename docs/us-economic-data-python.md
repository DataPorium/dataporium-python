# Get US economic data in Python

This guide shows how to read the main US economic series with the DataPorium Python client: GDP, inflation, jobs, Treasury yields, Federal Reserve decisions and exchange rates.

You need the library and an API key. See the [quick start](quickstart.md) if you have not set them up.

## Headline indicators

`economic_metrics` takes the name of one series:

```python
from dataporium import DataPorium

dp = DataPorium()

gdp = dp.economic_metrics(economic_metrics="GDP")
cpi = dp.economic_metrics(economic_metrics="CPI")
unemployment = dp.economic_metrics(economic_metrics="unemployment_Rate")

latest = unemployment[0]
print(latest["date"], latest["value"])
```

The answer is a list of rows with a `date` and a `value`, newest first.

Names you can use include:

| Topic | Names |
|---|---|
| Output | `GDP`, `real_GDP`, `real_GDP_Per_Capita`, `industrial_Production_Total_Index` |
| Prices | `CPI`, `inflation`, `inflation_Rate` |
| Jobs | `unemployment_Rate`, `total_Non_farm_Payroll`, `initial_Claims` |
| Consumers | `consumer_Sentiment`, `retail_Sales`, `total_Vehicle_Sales` |
| Rates | `federal_Funds`, `30Year_Fixed_Rate_Mortgage_Average`, `15Year_Fixed_Rate_Mortgage_Average` |
| Housing | `new_Privately_Owned_HousingUnits_Started_Total_Units` |

The names are case-sensitive. `print(dp.describe("economic_metrics"))` shows the full list.

## Treasury yields

Daily US Treasury yields go back to 1990, for 12 maturities from 1 month to 30 years:

```python
yields = dp.treasury_yields(
    maturity=["2y", "10y"],
    date_from="2024-01-01",
    frequency="monthly",   # daily (default), weekly or monthly
    order="asc",
)

print(yields["as_of"])
for row in yields["rows"][:5]:
    print(row)
```

The answer holds the rows under `rows`, next to `total`, `limit` and `offset`. For a long history, raise `limit` (up to 5000) or page with `offset`.

## The yield curve

`treasury_yields_curve` returns the curve of one day, compared with earlier curves, with the 10-year minus 2-year spread already calculated:

```python
curve = dp.treasury_yields_curve(compare=["1m", "1y"])

for item in curve["curves"]:
    print(item["label"], item["date"], "10y-2y spread:", item["spread_10y_2y"],
          "inverted:", item["inverted_10y_2y"])
```

Add `date="2020-03-16"` for the curve of a past day.

## Federal Reserve decisions

Rate decisions since 1994, with the meetings that are scheduled ahead:

```python
fed = dp.fed_decisions(limit=10)

print("Current target range:", fed["current_target"])
print("Next meeting:", fed["next_meeting"])
for row in fed["rows"]:
    print(row)
```

## Inflation by category

```python
inflation = dp.inflation_categories(latest=True)
for row in inflation["rows"][:10]:
    print(row)
```

## Exchange rates

`fx` takes a currency pair. Add one interval if you want a history:

```python
usd_eur = dp.fx(currency_conversion="USD-EUR")
daily = dp.fx(currency_conversion="USD-EUR", one_day_interval="1d", year=2024)
```

## Jobs in a state, metro or county

```python
jobs = dp.local_jobs(area_type="county", state="TX", latest=True,
                     sort="unemployment_rate", order="desc", limit=10)
for row in jobs["rows"]:
    print(row)
```

## As a DataFrame

```python
from dataporium import to_frame

rates = to_frame(dp.economic_metrics(economic_metrics="federal_Funds"))
print(rates[["date", "value"]].head())

yields = to_frame(dp.treasury_yields(maturity="10y", limit=250))
print(yields.head())
```

## Related data

```python
dp.corporate_bond_yields()     # high-grade corporate bond yields
dp.us_trade_summary()          # imports, exports and trade balance
dp.building_permits(state="CA")
dp.local_wages(state="CA")
dp.commodity_price_1d(symbol="GC=F")   # gold futures
```

*Economic data is for information only and is not investment advice.*
