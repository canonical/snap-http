from typing import Any, Dict, List, Optional

from .. import http
from ..types import SnapdResponse


def get_confdb(
    account: str,
    confdb_schema: str,
    view: str,
    *,
    keys: Optional[List[str]] = None,
) -> SnapdResponse:
    """Get configuration values from confdb.

    :param account: The account ID.
    :param confdb_schema: The confdb schema name.
    :param view: The view name.
    :param keys: Retrieve the configuration for these specific `keys`. These paths
        refer to rules defined in the view. If not provided, the GET will match all
        readable view rules and return any stored values for those.
    """
    query_params = {}
    if keys:
        query_params["keys"] = ",".join(keys)

    return http.get(
        f"/confdb/{account}/{confdb_schema}/{view}", query_params=query_params
    )


def set_confdb(
    account: str, confdb_schema: str, view: str, config: Dict[str, Any]
) -> SnapdResponse:
    """Set configuration values in confdb.

    :param account: The account ID.
    :param confdb_schema: The confdb schema name.
    :param view: The view name.
    :param config: A key-value mapping of configuration paths to their values.
        Use `None` to unset a value.
    """
    body: Dict[str, Any] = {"values": config}

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
