"""Python client for the DataPorium Data API.

    from dataporium import DataPorium

    dp = DataPorium(api_key="YOUR_API_KEY")   # or set DATAPORIUM_API_KEY
    print(dp.company_info(symbol="AAPL"))

Documentation: https://github.com/dataporium/dataporium-python
API reference:  https://dataporium.tech/api-docs
"""
from ._version import __version__
from .client import DEFAULT_BASE_URL, DataPorium, Endpoint, Parameter, to_frame
from .errors import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    DataPoriumError,
    MissingAPIKeyError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    UnknownEndpointError,
)

__all__ = [
    "DataPorium",
    "Endpoint",
    "Parameter",
    "to_frame",
    "DEFAULT_BASE_URL",
    "DataPoriumError",
    "MissingAPIKeyError",
    "UnknownEndpointError",
    "APIConnectionError",
    "APIError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "__version__",
]
