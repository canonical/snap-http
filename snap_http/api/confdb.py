import json
from typing import Any, Dict, List, Optional

from .. import http
from ..types import SnapdResponse


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
    :param access_timeout: How long to wait for the confdb access to complete, as a
        Go-style duration string (e.g. "5s", "500ms"). If not provided, snapd's
        default timeout applies.
    """
    query_params = {}
    if keys:
        query_params["keys"] = ",".join(keys)

    if constraints:
        query_params["constraints"] = json.dumps(constraints)

    if access_timeout:
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
    :param access_timeout: How long to wait for the confdb access to complete, as a
        Go-style duration string (e.g. "5s", "500ms"). If not provided, snapd's
        default timeout applies.
    """
    body: Dict[str, Any] = {"values": config}

    if access_timeout:
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
