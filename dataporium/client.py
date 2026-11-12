"""Python client for the DataPorium Data API (https://dataporium.tech/api-docs)."""
from __future__ import annotations

import datetime as _dt
import json
import os
import time
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import requests

from ._version import __version__
from .errors import (
    STATUS_ERRORS,
    APIConnectionError,
    APIError,
    MissingAPIKeyError,
    ServerError,
    UnknownEndpointError,
)

DEFAULT_BASE_URL = "https://api.dataporium.io"
ENV_API_KEY = "DATAPORIUM_API_KEY"
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})


@dataclass(frozen=True)
class Parameter:
    """One parameter of an endpoint."""

    name: str
    location: str  # "query" or "path"
    description: str
    example: Any = None


@dataclass(frozen=True)
class Endpoint:
    """One endpoint of the API, as listed in the public OpenAPI file."""

    name: str
    path: str
    summary: str
    description: str
    category: str
    params: Tuple[Parameter, ...]

    @property
    def path_params(self) -> Tuple[str, ...]:
        return tuple(p.name for p in self.params if p.location == "path")

    def __str__(self) -> str:
        lines = [f"{self.name}  ->  GET {self.path}", f"{self.category}: {self.summary}"]
        if self.description:
            lines += ["", self.description]
        if self.params:
            lines += ["", "Parameters:"]
            for p in self.params:
                where = " (in the path)" if p.location == "path" else ""
                example = f" Example: {p.example}" if p.example is not None else ""
                lines.append(f"  {p.name}{where}: {p.description}{example}")
        return "\n".join(lines)


@lru_cache(maxsize=1)
def _load_endpoints() -> Dict[str, Endpoint]:
    raw = json.loads(resources.files(__package__).joinpath("endpoints.json").read_text(encoding="utf-8"))
    endpoints = {}
    for name, ep in raw["endpoints"].items():
        params = tuple(
            Parameter(p["name"], p.get("in", "query"), p.get("description", ""), p.get("example"))
            for p in ep.get("params", [])
        )
        endpoints[name] = Endpoint(name, ep["path"], ep["summary"], ep.get("description", ""), ep["category"], params)
    return endpoints


def _clean_value(value: Any) -> str:
    """Turn a Python value into the text the API expects in a query string."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (_dt.datetime, _dt.date)):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, (list, tuple, set, frozenset)):
        return ",".join(_clean_value(v) for v in value)
    return str(value)


def _clean_params(params: Dict[str, Any]) -> Dict[str, str]:
    cleaned = {}
    for key, value in params.items():
        if value is None:
            continue
        # from_ and class_ are sent as "from" and "class" (Python reserves those words).
        if key.endswith("_") and not key.endswith("__"):
            key = key[:-1]
        cleaned[key] = _clean_value(value)
    return cleaned


class DataPorium:
    """Client for the DataPorium Data API.

    Every endpoint of the API is a method on this object::

        from dataporium import DataPorium

        dp = DataPorium()                      # reads DATAPORIUM_API_KEY
        profile = dp.company_info(symbol="AAPL")
        prices = dp.stock_price_1d(ticker="AAPL")

    Args:
        api_key: Your own API key. If left out, the DATAPORIUM_API_KEY
            environment variable is used.
        base_url: Address of the API. Change it only for testing.
        timeout: Seconds to wait for each answer.
        max_retries: How many times a failed request is tried again. Only
            rate-limit answers (429), server errors (5xx) and network
            problems are retried.
        session: A ``requests.Session`` to reuse, for proxies or custom adapters.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 2,
        session: Optional[requests.Session] = None,
    ) -> None:
        key = api_key or os.environ.get(ENV_API_KEY)
        if not key:
            raise MissingAPIKeyError(
                "No API key. Pass DataPorium(api_key=...) or set the "
                f"{ENV_API_KEY} environment variable. Get a key at https://dataporium.tech/pricing"
            )
        self._api_key = key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max(0, int(max_retries))
        self._session = session or requests.Session()
        self._sleep: Callable[[float], None] = time.sleep

    def __repr__(self) -> str:  # never show the key
        return f"DataPorium(base_url={self.base_url!r})"

    # ------------------------------------------------------------------ requests

    def get(self, path: str, **params: Any) -> Any:
        """Call any path of the API and return the decoded JSON answer.

        ``dp.get("/company-info", symbol="AAPL")`` is the same as
        ``dp.company_info(symbol="AAPL")``. Use it for a path that is newer
        than the endpoint list shipped with this library.
        """
        url = self.base_url + "/" + path.lstrip("/")
        return self._request(url, _clean_params(params))

    def call(self, name: str, **params: Any) -> Any:
        """Call an endpoint by its method name, for example ``dp.call("company_info", symbol="AAPL")``."""
        endpoint = self.describe(name)
        cleaned = _clean_params(params)
        path = endpoint.path
        for part in endpoint.path_params:
            if part not in cleaned:
                raise TypeError(f"{name}() needs {part!r}, because it is part of the path {endpoint.path}")
            path = path.replace("{" + part + "}", requests.utils.quote(cleaned.pop(part), safe=""))
        return self._request(self.base_url + path, cleaned)

    def __getattr__(self, name: str) -> Callable[..., Any]:
        if name.startswith("_") or name not in _load_endpoints():
            raise UnknownEndpointError(
                f"{name!r} is not a DataPorium endpoint. Use dp.endpoints() to list them, "
                "or dp.get('/path', ...) for a path that is not in the list."
            )

        def method(**params: Any) -> Any:
            return self.call(name, **params)

        endpoint = _load_endpoints()[name]
        method.__name__ = name
        method.__doc__ = str(endpoint)
        return method

    def __dir__(self) -> Iterable[str]:
        return sorted(set(super().__dir__()) | set(_load_endpoints()))

    # ------------------------------------------------------------------ discovery

    def endpoints(self, search: Optional[str] = None) -> List[Endpoint]:
        """List the endpoints. ``search`` keeps those whose name, category or summary contains the text."""
        found = list(_load_endpoints().values())
        if search:
            text = search.lower()
            found = [
                e for e in found
                if text in e.name.lower() or text in e.category.lower() or text in e.summary.lower()
            ]
        return found

    def describe(self, name: str) -> Endpoint:
        """Return one endpoint with its path and parameters. ``print(dp.describe("fx"))`` shows them."""
        try:
            return _load_endpoints()[name]
        except KeyError:
            raise UnknownEndpointError(
                f"{name!r} is not a DataPorium endpoint. Use dp.endpoints() to list them."
            ) from None

    # ------------------------------------------------------------------ internals

    def _request(self, url: str, params: Dict[str, str]) -> Any:
        headers = {
            "apikey": self._api_key,  # sent as a header, so the key stays out of URLs and logs
            "Accept": "application/json",
            "User-Agent": f"dataporium-python/{__version__}",
        }
        attempt = 0
        while True:
            try:
                response = self._session.get(url, params=params, headers=headers, timeout=self.timeout)
            except requests.RequestException as exc:
                if attempt < self.max_retries:
                    self._sleep(self._delay(attempt, None))
                    attempt += 1
                    continue
                raise APIConnectionError(f"Could not reach {self.base_url}: {type(exc).__name__}") from exc

            if response.status_code in RETRY_STATUSES and attempt < self.max_retries:
                self._sleep(self._delay(attempt, response.headers.get("Retry-After")))
                attempt += 1
                continue
            return self._decode(response)

    @staticmethod
    def _delay(attempt: int, retry_after: Optional[str]) -> float:
        if retry_after:
            try:
                return min(float(retry_after), 60.0)
            except ValueError:
                pass
        return float(min(2 ** attempt, 30))  # 1s, 2s, 4s ...

    @staticmethod
    def _decode(response: requests.Response) -> Any:
        try:
            body: Any = response.json()
        except ValueError:
            body = response.text
        if response.status_code < 400:
            if isinstance(body, str):
                raise APIError(response.status_code, "The answer was not JSON", body[:500])
            return body
        message = body.get("detail") if isinstance(body, dict) else None
        if not isinstance(message, str):
            message = response.reason or "Request failed"
        error_class = STATUS_ERRORS.get(response.status_code, ServerError if response.status_code >= 500 else APIError)
        raise error_class(response.status_code, message, body)


def _nested_rows(record: Dict[str, Any], key: Optional[str]) -> Optional[List[Any]]:
    """Find the list of rows inside one record: under ``key``, a usual name, or the only list of rows."""
    if key is not None:
        value = record.get(key)
        return value if isinstance(value, list) else None
    for name in ("rows", "data", "results", "items", "price_history"):
        if isinstance(record.get(name), list):
            return record[name]
    lists = [v for v in record.values() if isinstance(v, list) and v and isinstance(v[0], dict)]
    return lists[0] if len(lists) == 1 else None


def to_frame(data: Any, key: Optional[str] = None):
    """Turn an answer into a pandas DataFrame (needs ``pip install pandas``).

    Many answers are a plain list of rows, and some hold their rows inside a
    record, for example the daily prices under "price_history" or paged
    answers under "rows". ``to_frame`` looks for the rows in the usual
    places. Name the field yourself with ``key`` when you want a specific one::

        to_frame(dp.economic_metrics(economic_metrics="GDP"))
        to_frame(dp.stock_price_1d(ticker="AAPL"), key="price_history")

    Answers differ between endpoints, so check the result.
    """
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover - depends on the environment
        raise ImportError("to_frame() needs pandas. Install it with: pip install pandas") from exc

    if isinstance(data, dict):
        rows = _nested_rows(data, key)
        if rows is None and key is not None:
            raise KeyError(f"The answer has no list under {key!r}")
        return pd.DataFrame(rows if rows is not None else [data])
    if isinstance(data, list):
        records = [r for r in data if isinstance(r, dict)]
        if key is not None:
            rows = []
            for record in records:
                nested = _nested_rows(record, key)
                if nested is None:
                    raise KeyError(f"The answer has no list under {key!r}")
                rows.extend(nested)
            return pd.DataFrame(rows)
        if len(data) == 1 and records:
            nested = _nested_rows(records[0], None)
            if nested is not None:
                return pd.DataFrame(nested)
        return pd.DataFrame(data)
    raise TypeError(f"Cannot turn {type(data).__name__} into a DataFrame")
