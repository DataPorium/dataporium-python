# Get company financial statements in Python

This guide shows how to read income statements, balance sheets and cash flow statements for listed companies with the DataPorium Python client. The figures come from the companies' SEC filings.

You need the library and an API key. See the [quick start](quickstart.md) if you have not set them up.

## The three statements

```python
from dataporium import DataPorium

dp = DataPorium()

income = dp.income_statements(symbol="AAPL")
balance = dp.balance_sheet_statements(symbol="AAPL")
cash_flow = dp.cash_flow_statements(symbol="AAPL")
```

Each statement also has a shorter summary version with the main lines only:

```python
dp.income_statements_summary(symbol="AAPL")
dp.balance_sheet_statements_summary(symbol="AAPL")
dp.cash_flow_statements_summary(symbol="AAPL")
```

You can use `company_name="Apple Inc."` in place of `symbol`.

## Pick a period

To ask for one quarter, give the fiscal year and quarter together, or the combined form:

```python
# Fiscal year and quarter
q2 = dp.income_statements(symbol="AAPL", fiscal_year=2024, fiscal_qtr="Q2")

# The same period in one parameter
q2 = dp.income_statements(symbol="AAPL", fiscal_year_qtr="2024Q2")
```

The income statement can also be limited to annual or quarterly periods:

```python
annual = dp.income_statements(symbol="AAPL", period_type="Annual")
quarterly = dp.income_statements(symbol="AAPL", period_type="Quarterly")
```

Fiscal years are the company's own. Apple's fiscal year, for example, ends in September, so its fiscal Q2 covers January to March.

## Read the lines of a statement

The answer is a list with one record per period. Each record names the period and holds the lines of the statement:

```python
periods = dp.income_statements_summary(symbol="AAPL", fiscal_year_qtr="2024Q2")
period = periods[0]

print(period["company_name"], period["fiscal_year_qtr"], period["period_end"], period["currency"])

lines = {line["metric"]: line["value"] for line in period["income_statement"]}
print("Revenue:   ", lines["Total Revenue"])
print("Net income:", lines["Net Income"])
print("Diluted EPS:", lines["Diluted EPS"])
```

Each period also carries `data_status`. It is `final`, or `temporary` for a quarter the company has just reported, which is shown early with only the lines already confirmed.

The balance sheet and cash flow answers follow the same pattern. Print the keys of one record to see the name of the field that holds their lines:

```python
record = dp.balance_sheet_statements_summary(symbol="AAPL", fiscal_year_qtr="2024Q2")[0]
print(list(record.keys()))
```

## Compare companies

```python
from dataporium import DataPorium

dp = DataPorium()

for symbol in ["AAPL", "MSFT", "GOOGL"]:
    period = dp.income_statements_summary(symbol=symbol, fiscal_year_qtr="2024Q2")[0]
    lines = {line["metric"]: line["value"] for line in period["income_statement"]}
    print(symbol, period["period_end"], lines.get("Total Revenue"), lines.get("Net Income"))
```

Fiscal quarters end on different dates for different companies, so check `period_end` when you compare. Line items also differ between companies, because each company reports its own; `lines.get(...)` returns `None` when a company does not report a line.

## As a DataFrame

```python
from dataporium import to_frame

frame = to_frame(dp.income_statements_summary(symbol="AAPL", fiscal_year_qtr="2024Q2"), key="income_statement")
print(frame[["metric", "value"]])
```

## Revenue by segment, product and region

Many companies report revenue by business segment. These endpoints return that breakdown:

```python
dp.business_segments(symbol="AAPL")
dp.business_segments_quarterly(symbol="AAPL", fiscal_year=2024)
```

There is a dedicated page for this API: [Company business segments API](https://dataporium.tech/api-docs/business-segments-api).

## Related data

```python
dp.company_info(symbol="AAPL")                  # profile and fundamentals
dp.sec_filings(symbol="AAPL", form_type="10-K") # filings
dp.earnings_transcripts(symbol="AAPL", year=2024, quarter="Q2")
dp.earnings_split_calendar(symbol="AAPL")       # earnings dates and splits
```

Use `print(dp.describe("sec_filings"))` to see the parameters of any of them.

*Financial data is for information only and is not investment advice.*
