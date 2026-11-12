"""Tests for the client. They never call the real API: a fake session stands in for requests."""
import datetime as dt

import pytest
import requests

import dataporium
from dataporium import (
    APIConnectionError,
    AuthenticationError,
    DataPorium,
    MissingAPIKeyError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    UnknownEndpointError,
)


class FakeResponse:
    def __init__(self, status_code=200, body=None, headers=None, text=None):
        self.status_code = status_code
        self._body = body
        self.headers = headers or {}
        self.text = text if text is not None else ""
        self.reason = "reason"

    def json(self):
        if self._body is None:
            raise ValueError("no json")
        return self._body


class FakeSession:
    def __init__(self, *answers):
        self.answers = list(answers)
        self.calls = []

    def get(self, url, params=None, headers=None, timeout=None):
        self.calls.append({"url": url, "params": params, "headers": headers, "timeout": timeout})
        answer = self.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer


def make(*answers, **kwargs):
    session = FakeSession(*answers)
    client = DataPorium("test-key", session=session, **kwargs)
    client._sleep = lambda seconds: session.calls.append({"slept": seconds})
    return client, session


def requests_made(session):
    return [c for c in session.calls if "url" in c]


def test_needs_a_key(monkeypatch):
    monkeypatch.delenv("DATAPORIUM_API_KEY", raising=False)
    with pytest.raises(MissingAPIKeyError):
        DataPorium()


def test_key_from_environment(monkeypatch):
    monkeypatch.setenv("DATAPORIUM_API_KEY", "env-key")
    session = FakeSession(FakeResponse(body={"ok": True}))
    DataPorium(session=session).company_info(symbol="AAPL")
    assert session.calls[0]["headers"]["apikey"] == "env-key"


def test_key_goes_in_header_not_in_url_or_repr():
    client, session = make(FakeResponse(body={"symbol": "AAPL"}))
    assert client.company_info(symbol="AAPL") == {"symbol": "AAPL"}
    call = session.calls[0]
    assert call["url"] == "https://api.dataporium.io/company-info"
    assert call["params"] == {"symbol": "AAPL"}
    assert call["headers"]["apikey"] == "test-key"
    assert "apikey" not in call["params"]
    assert "test-key" not in repr(client)


def test_values_are_cleaned():
    client, session = make(FakeResponse(body={}))
    client.properties(zip=[92602, 92603], price_cut=True, new_construction=False, beds_min=3, city=None)
    assert session.calls[0]["params"] == {
        "zip": "92602,92603", "price_cut": "true", "new_construction": "false", "beds_min": "3",
    }


def test_dates_and_reserved_words():
    client, session = make(FakeResponse(body={}), FakeResponse(body={}))
    client.treasury_yields(date_from=dt.date(2024, 1, 1), maturity=("2y", "10y"))
    assert session.calls[0]["params"] == {"date_from": "2024-01-01", "maturity": "2y,10y"}
    client.futures_positioning(market="gold", from_="2024-01-01")
    assert session.calls[1]["params"] == {"market": "gold", "from": "2024-01-01"}


def test_path_parameters():
    client, session = make(FakeResponse(body={}))
    client.layoffs_company_ticker(ticker="MSFT")
    assert session.calls[0]["url"] == "https://api.dataporium.io/layoffs/company/MSFT"
    assert session.calls[0]["params"] == {}
    with pytest.raises(TypeError):
        client.layoffs_company_ticker()


def test_get_any_path():
    client, session = make(FakeResponse(body=[1, 2]))
    assert client.get("company-info", symbol="AAPL") == [1, 2]
    assert session.calls[0]["url"] == "https://api.dataporium.io/company-info"


@pytest.mark.parametrize(
    "status, error",
    [(401, AuthenticationError), (403, PermissionDeniedError), (404, NotFoundError)],
)
def test_errors_are_not_retried(status, error):
    client, session = make(FakeResponse(status, {"detail": "nope"}))
    with pytest.raises(error) as info:
        client.company_info(symbol="AAPL")
    assert info.value.status_code == status
    assert info.value.message == "nope"
    assert len(requests_made(session)) == 1


def test_rate_limit_is_retried_then_succeeds():
    client, session = make(
        FakeResponse(429, {"detail": "slow down"}, headers={"Retry-After": "3"}),
        FakeResponse(body={"ok": True}),
    )
    assert client.company_info(symbol="AAPL") == {"ok": True}
    assert {"slept": 3.0} in session.calls


def test_server_error_after_retries():
    client, session = make(FakeResponse(503, None, text="down"), FakeResponse(503, None, text="down"),
                           FakeResponse(503, None, text="down"))
    with pytest.raises(ServerError) as info:
        client.company_info(symbol="AAPL")
    assert info.value.status_code == 503
    assert len(requests_made(session)) == 3  # first try + 2 retries


def test_rate_limit_error_when_retries_run_out():
    client, _ = make(FakeResponse(429, {"detail": "slow down"}), max_retries=0)
    with pytest.raises(RateLimitError):
        client.company_info(symbol="AAPL")


def test_network_error_does_not_leak_key():
    boom = requests.ConnectionError("failed for apikey=test-key")
    client, _ = make(boom, boom, boom)
    with pytest.raises(APIConnectionError) as info:
        client.company_info(symbol="AAPL")
    assert "test-key" not in str(info.value)


def test_unknown_endpoint():
    client, _ = make()
    with pytest.raises(UnknownEndpointError):
        client.not_a_real_endpoint(symbol="AAPL")
    assert not hasattr(client, "not_a_real_endpoint")


def test_discovery():
    client, _ = make()
    assert len(client.endpoints()) > 150
    names = [e.name for e in client.endpoints("treasury")]
    assert "treasury_yields" in names
    described = str(client.describe("fx"))
    assert "/fx" in described and "currency_conversion" in described
    assert "company_info" in dir(client)
    assert "GET /company-info" in client.company_info.__doc__


def test_to_frame():
    pd = pytest.importorskip("pandas")
    assert list(dataporium.to_frame([{"a": 1}, {"a": 2}])["a"]) == [1, 2]
    frame = dataporium.to_frame({"total": 2, "rows": [{"a": 1}, {"a": 2}]})
    assert isinstance(frame, pd.DataFrame) and len(frame) == 2


def test_to_frame_nested_rows():
    pytest.importorskip("pandas")
    prices = [{"ticker": "AAPL", "price_history": [{"date": "2026-01-02", "close": 1.0}, {"date": "2026-01-01", "close": 2.0}]}]
    assert list(dataporium.to_frame(prices)["close"]) == [1.0, 2.0]
    assert list(dataporium.to_frame(prices, key="price_history")["date"]) == ["2026-01-02", "2026-01-01"]
    periods = [
        {"fiscal_year_qtr": "2024Q2", "income_statement": [{"metric": "Total Revenue", "value": 10}]},
        {"fiscal_year_qtr": "2024Q1", "income_statement": [{"metric": "Total Revenue", "value": 9}]},
    ]
    assert len(dataporium.to_frame(periods)) == 2  # one row per period
    assert list(dataporium.to_frame(periods, key="income_statement")["value"]) == [10, 9]
    with pytest.raises(KeyError):
        dataporium.to_frame(prices, key="missing")
