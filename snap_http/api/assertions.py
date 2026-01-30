from typing import Any, Dict, Optional

from .. import http
from ..types import AssertionData, SnapdResponse


def get_assertion_types() -> SnapdResponse:
    """GETs the list of assertion types."""
    return http.get("/assertions")


def get_assertions(
    assertion_type: str, filters: Optional[Dict[str, Any]] = None
) -> SnapdResponse:
    """GETs all the assertions of the given type.

    The response is a stream of assertions separated by double newlines.

    :param assertion_type: The type of the assertion.
    :param filters: A (assertion-header, filter-value) mapping to filter
        assertions with. Examples of headers are: username, authority-id,
        account-id, series, publisher, snap-name, and publisher-id.
    """
    return http.get(f"/assertions/{assertion_type}", query_params=filters)


def add_assertion(assertion: str) -> SnapdResponse:
    """Add an assertion to the system assertion database.

    :param assertion: The assertion to add. It may also be a newer revision
        of a pre-existing assertion that it will replace.
    """
    body = AssertionData(assertion)
    return http.post("/assertions", body)
