# Changelog

## 0.1.0

First release.

- `DataPorium` client: every endpoint of the DataPorium Data API is a method.
- API key from the `api_key` argument or the `DATAPORIUM_API_KEY` environment variable, sent as a header.
- Typed errors, with automatic retries for rate limits, server errors and network problems.
- `endpoints()` and `describe()` to explore the API from Python.
- `to_frame()` helper for pandas.
