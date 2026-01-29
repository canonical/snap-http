from typing import Dict, List, Optional, Union

from .. import http
from ..types import SnapdResponse


def snapshots() -> SnapdResponse:
    """Gets a list of all snapshots."""
    return http.get("/snapshots")


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
