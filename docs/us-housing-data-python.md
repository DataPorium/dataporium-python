# Get US housing market data in Python

This guide shows how to search US homes and read local housing figures with the DataPorium Python client: listings by ZIP code, city, county or state, price cuts, property tax and mortgage lending.

You need the library and an API key. See the [quick start](quickstart.md) if you have not set them up.

## Search homes

`properties` is one method for homes of every status. Give a place and any filters you want:

```python
from dataporium import DataPorium

dp = DataPorium()

homes = dp.properties(
    zip="92602",
    status="for_sale",        # for_sale (default), pending, rent, sold or off_market
    beds_min=3,
    price_max=1_500_000,
    sort="newest",
    limit=25,
)
print(homes)
```

The place can be a ZIP code (or a list of up to 25), a city, a county or a whole state:

```python
dp.properties(city="Irvine", state="CA", style="single_family")
dp.properties(county="Orange", state="CA", status="rent", price_max=4000)
dp.properties(zip=["92602", "92603", "92604"], status="sold", sold_within_days=30)
```

Add the state when a city name exists in more than one state.

## Find price cuts and long listings

```python
cuts = dp.properties(
    city="Irvine", state="CA",
    price_cut=True,
    price_cut_within_days=7,
    cut_pct_min=5,            # total cut of at least 5 percent
    sort="biggest_cut",
)

stale = dp.properties(
    county="Orange", state="CA",
    true_dom_min=90,          # at least 90 days on the market, earlier listings included
    relisted=True,
)
```

`true_dom_min` counts the whole selling effort of a home, not only its latest listing.

## Page through a large search

A search returns up to `limit` homes (100 by default, 5000 at most). When there are more, the answer gives `next_offset`:

```python
offset = 0
pages = []
while offset is not None and len(pages) < 5:
    page = dp.properties(state="CA", status="for_sale", limit=1000, offset=offset)
    pages.append(page)
    offset = page.get("next_offset")
```

A search with no place, or over a very large area, is answered from a sample and marked `approximate: true`.

## One home in detail

Look up a home by address, or by the property ID from a search answer:

```python
home = dp.properties(address="41 Carpenteria Irvine CA")
home = dp.properties(property_id="2559714761", radius_miles=1, nearby_same_beds=True)
```

The detail answer compares the home with nearby homes. `radius_miles` and the `nearby_...` filters control that comparison.

## Estimated monthly payment

```python
homes = dp.properties(
    zip="92602",
    with_payment=True,
    down_payment_pct=20,
    interest_rate=6.5,
    loan_term_years=30,
)
```

Without `interest_rate`, the latest average 30-year fixed rate is used.

## Listings by date

These endpoints return the listings of one ZIP code for a short date range (3 days at most):

```python
dp.realestate_for_sale(zip_code="77493", list_date="2025-01-03")
dp.realestate_sold(zip_code="77493", last_sold_date_between="2025-01-01,2025-01-03")
dp.realestate_rent(zip_code="77493", list_date_gte="2025-01-01")
```

For anything larger, use `properties`.

## Property tax and mortgage lending

```python
tax = dp.property_tax(zip="92602")

lending = dp.mortgage_lending_summary(state="CA", county="Orange")
print(lending["totals"])
print(lending["top_lenders"][:5])
```

## The local economy around a home

```python
dp.local_jobs(county="Orange", state="CA", latest=True)        # unemployment
dp.local_wages(county="Orange", state="CA")                    # jobs and pay
dp.building_permits(county="Orange", state="CA")               # new home permits
dp.migration(county="Orange", state="CA")                      # moves in and out
dp.flood_insurance(county="Orange", state="CA")                # flood insurance claims
```

Use `print(dp.describe("properties"))` to see every filter.

*Housing data is for information only. It is not an appraisal and is not investment advice.*
