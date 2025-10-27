"""
Functions for interacting with the snapd REST API.
See https://snapcraft.io/docs/snapd-api for documentation of the API.

Permissions are based on the user calling the API, most mutative interactions
(install, refresh, etc) require root.
"""

from typing import Any, Dict, List, Literal, Optional, Union

from . import http
from .types import AssertionData, FileUpload, FormData, SnapdResponse


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


def sideload(
    file_paths: List[str],
    *,
    classic: bool = False,
    dangerous: bool = False,
    devmode: bool = False,
    jailmode: bool = False,
    system_restart_immediate: bool = False,
) -> SnapdResponse:
    """Sideload a snap from the local filesystem.

    :param file_paths: Paths to the snap files to install.
    :param classic: if true, put snaps in classic mode and disable
        security confinement
    :param dangerous: if true, install the given snap files even if there are
        no pre-acknowledged signatures for them
    :param devmode: if true, put snaps in development mode and disable
        security confinement
    :param jailmode: if true, put snaps in enforced confinement mode
    :param system_restart_immediate: if true, makes any system restart,
        immediately and without delay (requires snapd 2.52)
    """
    data: Dict[str, Union[str, bool]] = {"action": "install"}

    if classic:
        data["classic"] = classic

    if dangerous:
        data["dangerous"] = dangerous

    if devmode:
        data["devmode"] = devmode

    if jailmode:
        data["jailmode"] = jailmode

    if system_restart_immediate:
        data["system-restart-immediate"] = system_restart_immediate

    files = [FileUpload(name="snap", path=file_path) for file_path in file_paths]

    return http.post("/snaps", FormData(data=data, files=files))


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


def remove(name: str,
           purge: Optional[bool] = False,
           terminate: Optional[bool] = False) -> SnapdResponse:
    """Uninstalls a snap identified by `name`."""
    body = {
        "action": "remove",
        "purge": purge,
        "terminate": terminate,
    }

    return http.post("/snaps/" + name, body)


def remove_all(names: List[str]) -> SnapdResponse:
    """Uninstalls all snaps identified in `names`."""
    return http.post("/snaps", {"action": "remove", "snaps": names})


def snapshots() -> SnapdResponse:
    """Gets a list of all snapshots."""
    return http.get("/snapshots")


def forget_snapshot(id: str, snaps: Optional[List[str]] = None, users: Optional[List[str]] = None) -> SnapdResponse:
    """Deletes a snapshot identified by `id`.

    :param snap_id: The ID of the snapshot to delete.
    """

    body: Dict[str, Union[str, List[str]]] = {
        "action": "forget",
        "set": id
    }

    if snaps is not None:
        body["snaps"] = snaps
    if users is not None:
        body["users"] = users

    return http.post("/snapshots", body)


def save_snapshot(
    snaps: Optional[List[str]] = None,
    users: Optional[List[str]] = None,
) -> SnapdResponse:
    """Saves a snapshot of the current state of the system.

    :param name: The name of the snapshot.
    :param users:  array of user names to whom snapshots are to be restricted .
    :param snaps: Optional list of snaps to include in the snapshot.
    """
    body: Dict[str, Union[str, List[str]]] = {"action": "snapshot"}

    if users is not None:
        body["users"] = users
    if snaps is not None:
        body["snaps"] = snaps

    return http.post("/snaps", body)


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


def list_all() -> SnapdResponse:
    """GETs a list of all installed snaps including disabled ones.
    """
    return http.get("/snaps?select=all")

# Configuration: get and set snap options


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


# Connections: get connections


def get_connections(
    snap: Optional[str] = None, select: Optional[str] = None, interface: Optional[str] = None
) -> SnapdResponse:
    """Retrieve connections from snapd.

    :param snap: Optional; The name of the snap to filter connections.
    :param select: Optional; When set to all, unconnected slots and plugs are included in the results.
    :param interface: Optional; Limit results to the selected interface.
    :return: A SnapdResponse containing the snapd response for the connections query.
    """
    query_params = {
        k: v
        for k, v in {
            "snap": snap,
            "select": select,
            "interface": interface,
        }.items()
        if v
    }

    return http.get("/connections", query_params=query_params)


# Interfaces: get/connect/disconnect interfaces


def get_interfaces(
    select: Optional[str] = None,
    slots: bool = False,
    plugs: bool = False,
    doc: bool = False,
    names: Optional[str] = None,
) -> SnapdResponse:
    """Retrieve interfaces from snapd.

    :param select: Optional; When set to "all", unconnected slots and plugs are included in the results.
    :param slots: Optional; If True, includes only slot connections in the results.
    :param plugs: Optional; If True, includes only plug connections in the results.
    :param doc: Optional; If True, includes additional documentation details in the response.
    :param names: Optional; If given, includes names of interfaces in the results
    :return: A SnapdResponse containing the snapd response for the interfaces query.
    """
    query_params = {
        k: v
        for k, v in {
            "select": select,
            "slots": slots,
            "plugs": plugs,
            "doc": doc,
            "names": names,
        }.items()
        if v
    }

    return http.get("/interfaces", query_params=query_params)


def connect_interface(
    in_snap: str, in_slot: str, out_snap: str, out_plug: str
) -> SnapdResponse:
    """
    Establish a connection between a snap plug and a snap slot.

    :param in_snap: The name of the snap providing the slot.
    :param in_slot: The slot name within the providing snap.
    :param out_snap: The name of the snap requiring the plug connection.
    :param out_plug: The plug name within the requesting snap.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    connect_action_body = {
        "action": "connect",
        "slots": [{"snap": in_snap, "slot": in_slot}],
        "plugs": [{"snap": out_snap, "plug": out_plug}],
    }
    return http.post("/interfaces", body=connect_action_body)


def disconnect_interface(
    in_snap: str, in_slot: str, out_snap: str, out_plug: str
) -> SnapdResponse:
    """
    Remove an existing connection between a snap plug and a snap slot.

    :param in_snap: The name of the snap providing the slot.
    :param in_slot: The slot name within the providing snap.
    :param out_snap: The name of the snap requiring the plug connection.
    :param out_plug: The plug name within the requesting snap.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    disconnect_action_body = {
        "action": "disconnect",
        "slots": [{"snap": in_snap, "slot": in_slot}],
        "plugs": [{"snap": out_snap, "plug": out_plug}],
    }
    return http.post("/interfaces", body=disconnect_action_body)


# Model: get model and remodel

def get_model() -> SnapdResponse:
    """
    GETs the active model assertion of system.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get("/model")


def remodel(new_model_assertion: str, offline: bool = False) -> SnapdResponse:
    """
    Replace the current model assertion of system
    :param new_model_assertion: New model assertion content
    :param offline: enables offline remodelling
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body = {"new-model" : new_model_assertion, "offline": offline}
    return http.post("/model", body=body)


# Validation sets: list/refresh validation sets

def get_validation_sets() -> SnapdResponse:
    """
    GET all enabled validation sets
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get("/validation-sets")


def get_validation_set(account_id: str, validation_set_name: str) -> SnapdResponse:
    """
    GET specific validation set
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get(f"/validation-sets/{account_id}/{validation_set_name}")


def refresh_validation_set(account_id: str, validation_set_name: str, validation_set_sequence: Optional[int] = None) -> SnapdResponse:
    """
    Refresh validation set of system
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :param validation_set_sequence: Sequence value of the validation set
    :return: A SnapdResponse containing the response from the snapd API.
    """
    validation_set_str = f"{account_id}/{validation_set_name}"
    if validation_set_sequence is not None:
        validation_set_str += f"={validation_set_sequence}"

    body = {
        "action": "refresh",
        "validation-sets": [
            validation_set_str
        ],
    }
    return http.post("/snaps", body=body)


def forget_validation_set(account_id: str, validation_set_name: str, validation_set_sequence: Optional[int] = None) -> SnapdResponse:
    """
    Forget a validation set of system
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :return: A SnapdResponse containing the response from the snapd API.
    """

    body: Dict[str, Union[str, int]] = {
        "action": "forget"
    }

    if validation_set_sequence is not None:
        body["sequence"] = validation_set_sequence

    return http.post(f"/validation-sets/{account_id}/{validation_set_name}", body=body)


def enforce_validation_set(account_id: str, validation_set_name: str, validation_set_sequence: Optional[int] = None) -> SnapdResponse:
    """
    Enforce a validation set of system
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body: Dict[str, Union[str, int]] = {
        "action": "apply",
        "mode": "enforce"
        }

    if validation_set_sequence is not None:
        body["sequence"] = validation_set_sequence

    return http.post(f"/validation-sets/{account_id}/{validation_set_name}", body=body)


def monitor_validation_set(account_id: str, validation_set_name: str, validation_set_sequence: Optional[int] = None) -> SnapdResponse:
    """
    Apply a validation set of system
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body: Dict[str, Union[str, int]] = {
        "action": "apply",
        "mode": "monitor"
    }

    if validation_set_sequence is not None:
        body["sequence"] = validation_set_sequence

    return http.post(f"/validation-sets/{account_id}/{validation_set_name}", body=body)


# System: Get and perform action with recovery system
def get_recovery_systems() -> SnapdResponse:
    """
    GET all recovery systems
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get("/systems")

def get_recovery_system(label: str) -> SnapdResponse:
    """
    GET specific recovery system
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get(f"/systems/{label}")


def perform_system_action(action: str, mode: str)-> SnapdResponse:
    """
    Attempt to perform an action with the current active recovery system.
    :param action: Action to perform, which is either “reboot”, “create” or “do”.
    :param mode:  The mode to transition to either "run", "recover", "install" or "factory-reset".
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body = {
        "action": action,
        "mode": mode
    }
    return http.post("/systems", body=body)


def perform_recovery_action(label: str, action: str, mode: str)-> SnapdResponse:
    """
    Attempt to perform an action with the current active recovery system.
    :param label: Label to specify recovery system.
    :param action: Action to perform, which is either “reboot”, “create” or “do”.
    :param mode:  The mode to transition to either "run", "recover", "install" or "factory-reset".
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body = {
        "action": action,
        "mode": mode
    }
    return http.post(f"/systems/{label}", body=body)



# Assertions: list and add assertions


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


# Users


def list_users() -> SnapdResponse:
    """Get information on user accounts."""
    return http.get("/users")


def add_user(
    username: str,
    email: str,
    sudoer: bool = False,
    known: bool = False,
    force_managed: bool = False,
    automatic: bool = False,
) -> SnapdResponse:
    """Create a local user."""
    body = {
        "action": "create",
        "username": username,
        "email": email,
        "sudoer": sudoer,
        "known": known,
        "force-managed": force_managed,
        "automatic": automatic,
    }
    return http.post("/users", body)


def remove_user(username: str) -> SnapdResponse:
    """Remove a local user."""
    body = {"action": "remove", "username": username}
    return http.post("/users", body)


# Apps and Services


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
