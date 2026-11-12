# Get stock, ETF and crypto prices in Python

This guide shows how to pull daily and intraday prices for stocks, ETFs, indexes and cryptocurrencies with the DataPorium Python client, and how to put them in a pandas DataFrame.

You need the library and an API key. See the [quick start](quickstart.md) if you have not set them up.

## Daily prices

`stock_price_1d` returns the daily open, high, low, close and volume of one ticker:

```python
from dataporium import DataPorium

dp = DataPorium()

answer = dp.stock_price_1d(ticker="AAPL")
record = answer[0]

print(record["name"], record["currency"], record["regular_market_price"])
for bar in record["price_history"][:5]:
    print(bar["date"], bar["open"], bar["high"], bar["low"], bar["close"], bar["volume"])
```

The answer is a list with one record for the ticker. The record holds facts about the ticker (name, exchange, currency, latest price, 52-week high and low) and the daily bars under `price_history`, newest first.

You can also search by company name. Use one of the two filters, not both:

```python
answer = dp.stock_price_1d(name="Apple Inc.")
```

## ETFs and indexes

The same method covers ETFs and market indexes. Index tickers start with `^`:

| What | Ticker |
|---|---|
| S&P 500 index | `^GSPC` |
| Dow Jones Industrial Average | `^DJI` |
| Nasdaq Composite | `^IXIC` |
| Russell 2000 | `^RUT` |
| VIX volatility index | `^VIX` |
| S&P 500 ETF | `SPY` |
| Nasdaq 100 ETF | `QQQ` |

```python
sp500 = dp.stock_price_1d(ticker="^GSPC")
spy = dp.stock_price_1d(ticker="SPY")
```

The library encodes the `^` for you.

## Crypto

Cryptocurrencies use the same method. Add `-USD` to the symbol:

```python
bitcoin = dp.stock_price_1d(ticker="BTC-USD")
ether = dp.stock_price_1d(ticker="ETH-USD")
```

## Intraday prices

`stock_price_5m` returns prices in 5-minute steps:

```python
intraday = dp.stock_price_5m(ticker="AAPL")
```

## Put the prices in a DataFrame

```python
from dataporium import DataPorium, to_frame

dp = DataPorium()

frame = to_frame(dp.stock_price_1d(ticker="AAPL"), key="price_history")
frame = frame.sort_values("date")
frame["daily_return"] = frame["close"].pct_change()
print(frame[["date", "close", "volume", "daily_return"]].tail())
```

`key="price_history"` tells `to_frame` which part of the answer holds the rows.

## Several tickers

One request returns one ticker. Loop for more, and stay under the limit of 600 requests per minute:

```python
tickers = ["AAPL", "MSFT", "NVDA", "SPY", "BTC-USD"]
closes = {}
for ticker in tickers:
    record = dp.stock_price_1d(ticker=ticker)[0]
    closes[ticker] = record["price_history"][0]["close"]   # newest bar
print(closes)
```

## Related data

```python
dp.company_info(symbol="AAPL")          # company profile
dp.gain_loss(symbol="AAPL")             # performance over several periods
dp.sector_performance(sector="Energy")  # performance of one sector
dp.stock_news(ticker="AAPL")            # recent news
dp.symbols_list(company_name="Apple Inc.")   # find a ticker by company name
dp.exchange_hours(exchange="NYSE")      # trading hours
dp.fx(currency_conversion="USD-EUR")    # exchange rates
dp.commodity_price_1d(symbol="GC=F")    # gold futures
```

Use `print(dp.describe("gain_loss"))` to see the parameters of any of them.

*Price data is for information only and is not investment advice.*
