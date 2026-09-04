import json
import re
from typing import Any, Dict, List, Optional

from .. import http
from ..types import SnapdResponse

_DURATION_UNIT_SECONDS = {
    "ns": 1e-9,
    "us": 1e-6,
    "µs": 1e-6,  # U+00B5 MICRO SIGN
    "μs": 1e-6,  # U+03BC GREEK SMALL LETTER MU
    "ms": 1e-3,
    "m": 60,
    "h": 3600,
    "s": 1,
}
_UNIT_ALTERNATION = "ns|us|µs|μs|ms|m|h|s"
_NUMBER = r"(?:[0-9]+\.[0-9]*|\.[0-9]+|[0-9]+)"
_DURATION_COMPONENT_RE = re.compile(rf"({_NUMBER})({_UNIT_ALTERNATION})")
_DURATION_RE = re.compile(rf"\A[+-]?(?:0|(?:{_DURATION_COMPONENT_RE.pattern})+)\Z")
_MAX_ACCESS_TIMEOUT_SECONDS = 2 * 60 * 60  # 2 hours


def _validate_access_timeout(access_timeout: str) -> None:
    """Ensure `access_timeout` is a well-formed Go-style duration that doesn't
    exceed `_MAX_ACCESS_TIMEOUT_SECONDS`.

    :raises ValueError: If `access_timeout` is malformed, negative, or exceeds
        the maximum allowed duration.
    """
    if not _DURATION_RE.match(access_timeout):
        raise ValueError(f"invalid access_timeout duration: {access_timeout!r}")

    magnitude = sum(
        float(value) * _DURATION_UNIT_SECONDS[unit]
        for value, unit in _DURATION_COMPONENT_RE.findall(access_timeout)
    )
    total_seconds = -magnitude if access_timeout.startswith("-") else magnitude
    if total_seconds < 0:
        raise ValueError(f"access_timeout {access_timeout!r} must not be negative")
    if total_seconds > _MAX_ACCESS_TIMEOUT_SECONDS:
        raise ValueError(
            f"access_timeout {access_timeout!r} exceeds the maximum allowed "
            "duration of 2h"
        )


def get_confdb(
    account: str,
    confdb_schema: str,
    view: str,
    *,
    keys: Optional[List[str]] = None,
    constraints: Optional[Dict[str, Any]] = None,
    access_timeout: Optional[str] = None,
) -> SnapdResponse:
    """Get configuration values from confdb.

    :param account: The account ID.
    :param confdb_schema: The confdb schema name.
    :param view: The view name.
    :param keys: Retrieve the configuration for these specific `keys`. These paths
        refer to rules defined in the view. If not provided, the GET will match all
        readable view rules and return any stored values for those.
    :param constraints: A mapping of parameter names to values, used to constrain and
        filter the data returned according to the placeholders and field filters in
        the matched view rules.
    :param access_timeout: How long to wait for other confdb accesses to complete, as a
        Go-style duration string (e.g. "5s", "500ms", "1h3m0.5s"), capped at 2 hours.
        If not provided, snapd's default timeout of 10 minutes applies.
    :raises ValueError: If `access_timeout` is malformed, negative, or exceeds
        the maximum allowed duration.
    """
    query_params = {}
    if keys:
        query_params["keys"] = ",".join(keys)

    if constraints:
        query_params["constraints"] = json.dumps(constraints)

    if access_timeout:
        _validate_access_timeout(access_timeout)
        query_params["access-timeout"] = access_timeout

    return http.get(
        f"/confdb/{account}/{confdb_schema}/{view}", query_params=query_params
    )


def set_confdb(
    account: str,
    confdb_schema: str,
    view: str,
    config: Dict[str, Any],
    *,
    access_timeout: Optional[str] = None,
) -> SnapdResponse:
    """Set configuration values in confdb.

    :param account: The account ID.
    :param confdb_schema: The confdb schema name.
    :param view: The view name.
    :param config: A key-value mapping of configuration paths to their values.
        Use `None` to unset a value.
    :param access_timeout: How long to wait for other confdb accesses to complete, as a
        Go-style duration string (e.g. "5s", "500ms", "1h3m0.5s"), capped at 2 hours.
        If not provided, snapd's default timeout of 10 minutes applies.
    :raises ValueError: If `access_timeout` is malformed, negative, or exceeds
        the maximum allowed duration.
    """
    body: Dict[str, Any] = {"values": config}

    if access_timeout:
        _validate_access_timeout(access_timeout)
        body["options"] = {"access-timeout": access_timeout}

    return http.put(f"/confdb/{account}/{confdb_schema}/{view}", body)


def delegate_confdb(
    operator_id: str,
    authentications: List[str],
    views: List[str],
) -> SnapdResponse:
    """Grant an operator the ability to remotely manage confdb views.

    :param operator_id: The account ID of the operator.
    :param authentications: Authentication methods ("operator-key" or "store").
    :param views: The confdb views in the format "<account-id>/<schema>/<view-name>".
    """
    body = {
        "action": "delegate",
        "operator-id": operator_id,
        "authentications": authentications,
        "views": views,
    }

    return http.post("/confdb", body)


def undelegate_confdb(
    operator_id: str,
    *,
    authentications: Optional[List[str]] = None,
    views: Optional[List[str]] = None,
) -> SnapdResponse:
    """Withdraw an operator's ability to remotely manage confdb views.

    :param operator_id: The account ID of the operator.
    :param authentications: Authentication methods to withdraw. Omit to withdraw
        all authentication methods.
    :param views: The confdb views to withdraw access from. Omit to withdraw
        access from all views.
    """
    body: Dict[str, Any] = {
        "action": "undelegate",
        "operator-id": operator_id,
    }

    if authentications is not None:
        body["authentications"] = authentications

    if views is not None:
        body["views"] = views

    return http.post("/confdb", body)
