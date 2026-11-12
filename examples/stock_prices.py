"""Daily prices of one ticker as a pandas DataFrame.

Run:
    pip install pandas
    export DATAPORIUM_API_KEY="YOUR_API_KEY"
    python examples/stock_prices.py SPY        # or BTC-USD for bitcoin
"""
import sys

from dataporium import DataPorium, to_frame


def main() -> None:
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    dp = DataPorium()
    frame = to_frame(dp.stock_price_1d(ticker=ticker), key="price_history")
    print(f"{ticker}: {len(frame)} daily bars")
    print(frame[["date", "open", "high", "low", "close", "volume"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
