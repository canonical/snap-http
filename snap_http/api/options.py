from typing import Any, Dict, List, Optional

from .. import http
from ..types import SnapdResponse


def get_conf(name: str, *, keys: Optional[List[str]] = None) -> SnapdResponse:
    """Get the configuration details for the snap `name`.

    :param name: the name of the snap.
    :param keys: retrieve the configuration for these specific `keys`. Dotted
        keys can be used to retrieve nested values.
    """
    query_params = {}
    if keys:
        query_params["keys"] = ",".join(keys)

    return http.get(f"/snaps/{name}/conf", query_params=query_params)


def set_conf(name: str, config: Dict[str, Any]) -> SnapdResponse:
    """Set the configuration details for the snap `name`.

    :param name: the name of the snap.
    :param config: A key-value mapping of snap configuration.
        Keys can be dotted, `None` can be used to unset config options.
    """
    return http.put(f"/snaps/{name}/conf", config)
