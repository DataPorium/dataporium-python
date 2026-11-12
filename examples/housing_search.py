"""Homes for sale in one ZIP code with a recent price cut.

Run:
    export DATAPORIUM_API_KEY="YOUR_API_KEY"
    python examples/housing_search.py 92602
"""
import json
import sys

from dataporium import DataPorium


def main() -> None:
    zip_code = sys.argv[1] if len(sys.argv) > 1 else "92602"
    dp = DataPorium()
    answer = dp.properties(
        zip=zip_code,
        status="for_sale",
        price_cut=True,
        price_cut_within_days=30,
        sort="biggest_cut",
        limit=10,
    )
    print(json.dumps(answer, indent=2)[:4000])


if __name__ == "__main__":
    main()
