from typing import Optional

from .. import http
from ..types import SnapdResponse


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
