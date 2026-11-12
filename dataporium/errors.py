"""Errors raised by the DataPorium client."""
from __future__ import annotations

from typing import Any, Optional


class DataPoriumError(Exception):
    """Base class for every error raised by this library."""


class MissingAPIKeyError(DataPoriumError):
    """No API key was given and DATAPORIUM_API_KEY is not set."""


class UnknownEndpointError(DataPoriumError, AttributeError):
    """The endpoint name is not in the endpoint list shipped with this library."""


class APIConnectionError(DataPoriumError):
    """The request never got an answer (network problem or timeout)."""


class APIError(DataPoriumError):
    """The API answered with an error status.

    Attributes:
        status_code: HTTP status of the answer.
        message: The ``detail`` text sent by the API, when there is one.
        body: The decoded answer body (dict, list or text), for debugging.
    """

    def __init__(self, status_code: int, message: str, body: Optional[Any] = None) -> None:
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.body = body


class AuthenticationError(APIError):
    """401: the request had no API key."""


class PermissionDeniedError(APIError):
    """403: the API key is not valid, has expired, or the subscription is not active."""


class NotFoundError(APIError):
    """404: the path does not exist."""


class RateLimitError(APIError):
    """429: more requests than the plan allows per minute."""


class ServerError(APIError):
    """5xx: the API had a problem. These are retried automatically before this is raised."""


STATUS_ERRORS = {
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    429: RateLimitError,
}
