# Quick start

This page follows the three steps of the [DataPorium API documentation](https://dataporium.tech/api-docs): get your API key, authenticate, and make your first request.

## 1. Get your API key

Sign up at [dataporium.tech](https://dataporium.tech/pricing) and subscribe to the Premium plan, which includes API access. Your API key is in your account settings once you subscribe.

The same key works for the REST API and for the [MCP server](use-with-ai-assistants-mcp.md).

## 2. Authentication

Every request needs your API key. The API accepts it in two ways:

| Way | Example |
|---|---|
| `apikey` request header (recommended) | `apikey: YOUR_API_KEY` |
| Query parameter | `?apikey=YOUR_API_KEY` |

The header is recommended, because a key in a URL can end up in server and proxy logs. This library always uses the header.

Install the library and store the key in an environment variable, so it never ends up in your code:

```bash
pip install git+https://github.com/dataporium/dataporium-python.git

export DATAPORIUM_API_KEY="YOUR_API_KEY"     # macOS and Linux
setx DATAPORIUM_API_KEY "YOUR_API_KEY"       # Windows (open a new terminal afterwards)
```

## 3. Make your first request

```python
import json
from dataporium import DataPorium

dp = DataPorium()   # reads DATAPORIUM_API_KEY

profile = dp.company_info(symbol="AAPL")
print(json.dumps(profile, indent=2)[:1500])
```

The same request without the library, to the base URL `https://api.dataporium.io`:

```bash
curl -H "apikey: YOUR_API_KEY" "https://api.dataporium.io/company-info?symbol=AAPL"
```

If you see company data, everything works. If you see an error:

| Code | Meaning |
|---|---|
| 401 | API key required. Include your API key in the request |
| 403 | Invalid or expired API key, or subscription inactive |
| 429 | Rate limit exceeded. The maximum is 600 requests per minute |
| 500 | Internal server error. Try again or contact support |

## Find what you need

The API has 203 endpoints in 42 categories. Search them from Python:

```python
for endpoint in dp.endpoints("price"):
    print(endpoint.name, "-", endpoint.summary)

print(dp.describe("stock_price_1d"))   # path, parameters and examples
```

## Next steps

- [Get stock, ETF and crypto prices in Python](stock-prices-python.md)
- [Get company financial statements in Python](financial-statements-python.md)
- [Get US economic data in Python](us-economic-data-python.md)
- [Get US housing market data in Python](us-housing-data-python.md)
- [Use DataPorium with AI assistants through MCP](use-with-ai-assistants-mcp.md)
- [All endpoints](endpoints.md)
