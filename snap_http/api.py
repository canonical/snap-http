"""
Functions for interacting with the snapd REST API.
See https://snapcraft.io/docs/snapd-api for documentation of the API.

Permissions are based on the user calling the API, most mutative interactions
(install, refresh, etc) require root.
"""
from typing import Any, Dict, List, Literal, Optional, Union

from . import http
from .types import SnapdResponse


def check_change(cid: str) -> SnapdResponse:
    """Checks the status of snapd change with id `cid`."""
    return http.get("/changes/" + cid)


def check_changes() -> SnapdResponse:
    """Checks the status of all snapd changes."""
    return http.get("/changes?select=all")


def enable(name: str) -> SnapdResponse:
    """Enables a previously disabled snap by `name`."""
    return http.post("/snaps/" + name, {"action": "enable"})


def enable_all(names: List[str]) -> SnapdResponse:
    """Like `enable_snap`, but for the list of snaps in `names`.

    NOTE: as of 2024-01-08, enable/disable is not yet supported for multiple snaps.
    """
    return http.post("/snaps", {"action": "enable", "snaps": names})


def disable(name: str) -> SnapdResponse:
    """Disables a snap by `name`, making its binaries and services unavailable."""
    return http.post("/snaps/" + name, {"action": "disable"})


def disable_all(names: List[str]) -> SnapdResponse:
    """Like `disable_snap`, but for the list of snaps in `names`.

    NOTE: as of 2024-01-08, enable/disable is not yet supported for multiple snaps.
    """
    return http.post("/snaps", {"action": "disable", "snaps": names})


def hold(
    name: str,
    *,
    hold_level: Literal["general", "auto-refresh"] = "general",
    time: str = "forever",
) -> SnapdResponse:
    """Holds a snap by `name` at `hold_level` until `time`.

    :param time: RFC3339 timestamp to hold the snap until, or "forever".
    """
    return http.post(
        "/snaps/" + name, {"action": "hold", "hold-level": hold_level, "time": time}
    )


def hold_all(
    names: List[str],
    *,
    hold_level: Literal["general", "auto-refresh"] = "general",
    time: str = "forever",
) -> SnapdResponse:
    """Like `hold_snap`, but for the list of snaps in `names`."""
    return http.post(
        "/snaps",
        {"action": "hold", "snaps": names, "hold-level": hold_level, "time": time},
    )


def install(
    name: str,
    *,
    revision: Optional[str] = None,
    channel: Optional[str] = None,
    classic: bool = False,
) -> SnapdResponse:
    """Installs a snap by `name` at `revision`, tracking `channel`.

    :param revision: revision to install. Defaults to latest.
    :param channel: channel to track. Defaults to stable.
    :param classic: if `True`, snap is installed in classic containment mode.
    """
    body: Dict[str, Union[str, bool]] = {"action": "install"}

    if revision is not None:
        body["revision"] = revision

    if channel is not None:
        body["channel"] = channel

    if classic:
        body["classic"] = classic

    return http.post("/snaps/" + name, body)


def install_all(names: List[str]) -> SnapdResponse:
    """Installs all snaps in `names` using the latest rev of the stable channel, with strict
    confinement.
    """
    return http.post("/snaps", {"action": "install", "snaps": names})


def refresh(
    name: str,
    *,
    revision: Optional[str] = None,
    channel: Optional[str] = None,
    classic: bool = False,
) -> SnapdResponse:
    """Refreshes a snap by `name`, to `revision`, tracking `channel`.

    :param revision: revision to refresh to. Defaults to latest.
    :param channel: channel to switch tracking to. Default to stable.
    :param classic: If `True`, snap is changed to classic containment mode.
    """
    body: Dict[str, Union[str, bool]] = {"action": "refresh"}

    if revision is not None:
        body["revision"] = revision

    if channel is not None:
        body["channel"] = channel

    if classic:
        body["classic"] = classic

    return http.post("/snaps/" + name, body)


def refresh_all(names: Optional[List[str]] = None) -> SnapdResponse:
    """Refreshes all snaps in `names` to the latest revision. If `names` is not provided or empty,
    all snaps are refreshed.
    """
    body: Dict[str, Union[str, List[str]]] = {"action": "refresh"}

    if names:
        body["snaps"] = names

    return http.post("/snaps", body)


def revert(
    name: str, *, revision: Optional[str] = None, classic: Optional[bool] = None
) -> SnapdResponse:
    """Reverts a snap, switching what revision is currently installed.

    :param revision: If provided, the revision to switch to. Otherwise, the revision used prior to
        the last refresh is used.
    :param classic: If `True`, confinement is changed to classic. If `False`, confinement is
        changed to strict. If not provided, confinement is left as-is.
    """
    body: Dict[str, Union[str, bool]] = {"action": "revert"}

    if revision is not None:
        body["revision"] = revision

    if classic is not None:
        body["classic"] = classic

    return http.post("/snaps/" + name, body)


def revert_all(names: List[str]) -> SnapdResponse:
    """Reverts all snaps in `names` to the revision used prior to the last refresh."""
    return http.post("/snaps", {"action": "revert", "snaps": names})


def remove(name: str) -> SnapdResponse:
    """Uninstalls a snap identified by `name`."""
    return http.post("/snaps/" + name, {"action": "remove"})


def remove_all(names: List[str]) -> SnapdResponse:
    """Uninstalls all snaps identified in `names`."""
    return http.post("/snaps", {"action": "remove", "snaps": names})


def switch(name: str, *, channel: str = "stable") -> SnapdResponse:
    """Switches the tracking channel of snap `name`."""
    return http.post("/snaps/" + name, {"action": "switch", "channel": channel})


def switch_all(names: List[str], channel: str = "stable") -> SnapdResponse:
    """Switches the tracking channels of all snaps in `names`.

    NOTE: as of 2024-01-08, switch is not yet supported for multiple snaps.
    """
    return http.post("/snaps", {"action": "switch", "channel": channel, "snaps": names})


def unhold(name: str) -> SnapdResponse:
    """Removes the hold on a snap, allowing it to refresh on its usual schedule."""
    return http.post("/snaps/" + name, {"action": "unhold"})


def unhold_all(names: List[str]) -> SnapdResponse:
    """Removes the holds on all snaps in `names`, allowing them to refresh on their usual
    schedule.
    """
    return http.post("/snaps", {"action": "unhold", "snaps": names})


def list() -> SnapdResponse:
    """GETs a list of installed snaps.

    This stomps on builtins.list, so please import it namespaced.
    """
    return http.get("/snaps")


# Configuration: get and set snap options


def get_conf(name: str) -> SnapdResponse:
    """Get the configuration details for the snap `name`."""
    return http.get(f"/snaps/{name}/conf")


def set_conf(name: str, config: Dict[str, Any]) -> SnapdResponse:
    """Set the configuration details for the snap `name`."""
    return http.put(f"/snaps/{name}/conf", config)
