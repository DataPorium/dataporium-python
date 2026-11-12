# DataPorium Python client

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

The official Python client for the [DataPorium](https://dataporium.tech) Data API, a REST financial data API with real-time and historical market data across stocks, ETFs, crypto, forex and commodities, plus company fundamentals, news, the US economy and US housing.

The API has 203 endpoints in 42 categories, and every one of them is a method on the client. You use your own API key:

```python
from dataporium import DataPorium

dp = DataPorium(api_key="YOUR_API_KEY")

profile = dp.company_info(symbol="AAPL")          # company profile
prices = dp.stock_price_1d(ticker="AAPL")         # daily prices (stocks, ETFs, indexes, crypto)
curve = dp.treasury_yields_curve()                # US Treasury yield curve
homes = dp.properties(zip="92602", beds_min=3)    # homes for sale in a ZIP code
```

The same data is available to AI assistants through the [DataPorium MCP server](docs/use-with-ai-assistants-mcp.md), with the same key.

## Install

```bash
pip install git+https://github.com/DataPorium/dataporium-python.git
```

Python 3.10 or newer. The only dependency is `requests`. For DataFrames, also install pandas:

```bash
pip install pandas
```

## Get an API key

1. Sign up at [dataporium.tech](https://dataporium.tech/pricing).
2. Subscribe to the Premium plan. It includes the REST API (600 calls per minute) and the MCP server with the same key. The [pricing page](https://dataporium.tech/pricing) has the current price.
3. Your API key is in your account settings once you subscribe.

The safest way to give the key to the library is an environment variable, so it never ends up in your code:

```bash
export DATAPORIUM_API_KEY="YOUR_API_KEY"     # macOS and Linux
setx DATAPORIUM_API_KEY "YOUR_API_KEY"       # Windows
```

```python
from dataporium import DataPorium

dp = DataPorium()   # reads DATAPORIUM_API_KEY
```

The API accepts the key in an `apikey` request header or as a `?apikey=` query parameter. The header is recommended, because a key in a URL can end up in server and proxy logs. This library always uses the header.

## What you can get

| Area | Examples | Methods to start with |
|---|---|---|
| Stocks, ETFs, indexes and crypto | Daily and 5-minute prices, performance, news | `stock_price_1d`, `stock_price_5m`, `gain_loss`, `stock_news` |
| Companies | Profile, business segments, SEC filings, earnings transcripts, insiders, shareholders, short interest, options | `company_info`, `business_segments`, `sec_filings`, `short_interest` |
| Financial statements | Income statement, balance sheet, cash flow | `income_statements`, `balance_sheet_statements`, `cash_flow_statements` |
| Forex and commodities | Currency pairs, gold, oil and other futures, futures positioning | `fx`, `commodity_price_1d`, `futures_positioning` |
| US economy | GDP, inflation, jobs, Treasury yields, Fed decisions, trade | `economic_metrics`, `treasury_yields`, `fed_decisions` |
| US housing | Homes for sale, pending, for rent and sold, price cuts, property tax, mortgage lending | `properties`, `realestate_price_changes`, `property_tax` |
| Local economy and layoffs | Jobs, pay, building permits and migration by area; layoff notices by company, state and industry | `local_jobs`, `local_wages`, `layoffs_events` |
| Government and politics | Stock trades reported by members of Congress, federal contracts, lobbying, US election results | `politician_trades`, `government_contracts`, `lobbying`, `elections_results` |
| Industries | Healthcare providers, banks, energy, transportation, agriculture, colleges, recalls and more | `healthcare_hospitals`, `banks`, `electricity_rates` |

The full list is in [docs/endpoints.md](docs/endpoints.md). Three of the most used APIs have their own pages on the website:

- [Congress stock trading API](https://dataporium.tech/api-docs/congress-trading-api)
- [Layoffs / WARN notices API](https://dataporium.tech/api-docs/layoffs-api)
- [Company business segments API](https://dataporium.tech/api-docs/business-segments-api)

## Find an endpoint

You do not need to leave Python to see what is available:

```python
for endpoint in dp.endpoints("treasury"):
    print(endpoint.name, "-", endpoint.summary)

print(dp.describe("treasury_yields"))   # path, parameters and examples
help(dp.treasury_yields)                # the same text
```

Method names follow the API paths: `/company-info` is `dp.company_info(...)`, and `/treasury-yields/curve` is `dp.treasury_yields_curve(...)`.

If the API gains a path that this version of the library does not list yet, call it directly:

```python
dp.get("/some-new-path", symbol="AAPL")
```

## Parameters

Pass parameters as keyword arguments with the names from the [API documentation](https://dataporium.tech/api-docs). The library converts Python values for you:

| You pass | The API receives |
|---|---|
| `True` / `False` | `true` / `false` |
| `["2y", "10y"]` | `2y,10y` |
| `datetime.date(2024, 1, 1)` | `2024-01-01` |
| `None` | nothing (the parameter is left out) |
| `from_="2024-01-01"`, `class_=9` | `from`, `class` (Python reserves these two words) |

```python
import datetime as dt

rows = dp.treasury_yields(
    maturity=["2y", "10y"],
    date_from=dt.date(2024, 1, 1),
    frequency="monthly",
    order="asc",
)
```

Many endpoints page their answers with `limit` and `offset`. See the parameter list of each endpoint with `dp.describe(...)`.

## Answers

Every endpoint returns structured JSON, which the library hands you as Python dictionaries and lists. The fields differ between endpoints, so print an answer once to see what it holds. The [API documentation](https://dataporium.tech/api-docs) describes every endpoint.

```python
record = dp.stock_price_1d(ticker="AAPL")[0]
print(record["name"], record["regular_market_price"])
print(record["price_history"][0])          # newest daily bar: date, open, high, low, close, volume

rates = dp.economic_metrics(economic_metrics="federal_Funds")
print(rates[0]["date"], rates[0]["value"])  # newest value
```

For tables, `to_frame` turns an answer into a pandas DataFrame:

```python
from dataporium import DataPorium, to_frame

dp = DataPorium()
prices = to_frame(dp.stock_price_1d(ticker="AAPL"), key="price_history")
rates = to_frame(dp.economic_metrics(economic_metrics="federal_Funds"))
```

## Errors and retries

```python
from dataporium import DataPorium, DataPoriumError, PermissionDeniedError, RateLimitError

dp = DataPorium()

try:
    data = dp.company_info(symbol="AAPL")
except PermissionDeniedError:
    print("The API key is not valid, has expired, or the subscription is not active.")
except RateLimitError:
    print("Too many requests. The limit is 600 requests per minute.")
except DataPoriumError as error:
    print("Request failed:", error)
```

| Error | HTTP status | Meaning |
|---|---|---|
| `MissingAPIKeyError` | none | No key was given and `DATAPORIUM_API_KEY` is not set |
| `AuthenticationError` | 401 | API key required. The request had no API key |
| `PermissionDeniedError` | 403 | Invalid or expired API key, or subscription inactive |
| `NotFoundError` | 404 | The path does not exist |
| `RateLimitError` | 429 | Rate limit exceeded. The maximum is 600 requests per minute |
| `ServerError` | 500 and above | Internal server error. Try again or contact support |
| `APIConnectionError` | none | No answer (network problem or timeout) |

All of them are subclasses of `DataPoriumError`.

Rate-limit answers, server errors and network problems are retried automatically, twice by default, waiting 1 and then 2 seconds. Change this with `DataPorium(max_retries=5)` or switch it off with `max_retries=0`. The wait for each answer is 30 seconds by default: `DataPorium(timeout=60)`.

## Use DataPorium with AI assistants (MCP)

DataPorium runs a Model Context Protocol (MCP) server with 46 tools. Connect it once and Claude, ChatGPT, Claude Code, Cursor, Gemini CLI and other MCP clients can query the same data in plain language, with the same API key and no code:

```
https://mcp.dataporium.io/mcp
```

See [docs/use-with-ai-assistants-mcp.md](docs/use-with-ai-assistants-mcp.md) for the setup in each app.

## Other languages

- JavaScript and TypeScript: [dataporium-js](https://github.com/DataPorium/dataporium-js)
- curl, R, Google Sheets, Excel and plain Python or JavaScript: [dataporium-examples](https://github.com/DataPorium/dataporium-examples)

## Guides

- [Quick start](docs/quickstart.md)
- [Get stock, ETF and crypto prices in Python](docs/stock-prices-python.md)
- [Get company financial statements in Python](docs/financial-statements-python.md)
- [Get US economic data in Python](docs/us-economic-data-python.md)
- [Get US housing market data in Python](docs/us-housing-data-python.md)
- [Use DataPorium with AI assistants through MCP](docs/use-with-ai-assistants-mcp.md)
- [Endpoint reference](docs/endpoints.md)

Runnable scripts are in [examples/](examples).

## Keep your key safe

- Do not put the key in code that you commit or share. Use the environment variable.
- Do not put the key in a browser app or a mobile app. Call the API from your own server.
- If a key leaks, create a new key in your account settings. The old one stops working.

## Development

```bash
git clone https://github.com/DataPorium/dataporium-python.git
cd dataporium-python
pip install -e ".[dev,pandas]"
pytest
```

The tests never call the real API. To refresh the endpoint list after the API changes, run `python scripts/generate_endpoints.py`.

## Links

- Website: <https://dataporium.tech>
- API documentation: <https://dataporium.tech/api-docs>
- MCP server: <https://dataporium.tech/mcp>
- Pricing: <https://dataporium.tech/pricing>
- JavaScript library: <https://github.com/DataPorium/dataporium-js>
- Examples in other languages: <https://github.com/DataPorium/dataporium-examples>
- Questions: [open an issue](https://github.com/DataPorium/dataporium-python/issues) or write to info@dataporium.tech

## License and disclaimer

The code in this repository is released under the [MIT License](LICENSE). Use of the API and its data is governed by the DataPorium [Terms of Use](https://dataporium.tech/terms-of-use).

Data is for information only and is not investment advice.
