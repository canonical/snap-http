from typing import List

from .. import http
from ..types import SnapdResponse


def get_apps(names: List[str] = [], services_only: bool = False) -> SnapdResponse:
    """List available apps.

    :param services_only: Return only services.
    :param names: List apps for the snaps in `names` only.
    """
    query_params = {}

    if services_only:
        query_params["select"] = "service"

    if names:
        query_params["names"] = ",".join(names)

    return http.get("/apps", query_params=query_params)


def start(name: str, enable: bool = False) -> SnapdResponse:
    """Start the service `name`.

    :param enable: arranges to have the service start at system start.
    """
    return http.post(
        "/apps",
        {"action": "start", "names": [name], "enable": enable},
    )


def start_all(names: List[str], enable: bool = False) -> SnapdResponse:
    """Start the services in `names`.

    :param enable: arranges to have the service start at system start.
    """
    return http.post(
        "/apps",
        {"action": "start", "names": names, "enable": enable},
    )


def stop(name: str, disable: bool = False) -> SnapdResponse:
    """Stop the service `name`.

    :param disable: arranges to no longer start the service at system start.
    """
    return http.post(
        "/apps",
        {"action": "stop", "names": [name], "disable": disable},
    )


def stop_all(names: List[str], disable: bool = False) -> SnapdResponse:
    """Stop the services in `names`.

    :param disable: arranges to no longer start the service at system start.
    """
    return http.post(
        "/apps",
        {"action": "stop", "names": names, "disable": disable},
    )


def restart(name: str, reload: bool = False) -> SnapdResponse:
    """Restart the service `name`.

    :param reload: try to reload the service instead of restarting.
    """
    return http.post(
        "/apps",
        {"action": "restart", "names": [name], "reload": reload},
    )


def restart_all(names: List[str], reload: bool = False) -> SnapdResponse:
    """Restart the services in `names`.

    :param reload: try to reload the service instead of restarting.
    """
    return http.post(
        "/apps",
        {"action": "restart", "names": names, "reload": reload},
    )
