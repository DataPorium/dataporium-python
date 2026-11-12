"""First request: a company profile.

Run:
    export DATAPORIUM_API_KEY="YOUR_API_KEY"
    python examples/quickstart.py AAPL
"""
import json
import sys

from dataporium import DataPorium, DataPoriumError


def main() -> None:
    symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    dp = DataPorium()  # reads DATAPORIUM_API_KEY
    try:
        profile = dp.company_info(symbol=symbol)
    except DataPoriumError as error:
        sys.exit(f"Request failed: {error}")
    print(json.dumps(profile, indent=2)[:3000])


if __name__ == "__main__":
    main()
