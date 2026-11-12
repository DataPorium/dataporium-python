"""Today's US Treasury yield curve next to the curve one month and one year ago.

Run:
    export DATAPORIUM_API_KEY="YOUR_API_KEY"
    python examples/yield_curve.py
"""
from dataporium import DataPorium


def main() -> None:
    dp = DataPorium()
    answer = dp.treasury_yields_curve(compare=["1m", "1y"])
    print("As of:", answer.get("as_of"))
    for curve in answer.get("curves", []):
        print(
            f"{curve.get('label')} ({curve.get('date')}): "
            f"10y-2y spread {curve.get('spread_10y_2y')}, inverted: {curve.get('inverted_10y_2y')}"
        )


if __name__ == "__main__":
    main()
