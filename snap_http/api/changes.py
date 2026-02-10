from .. import http
from ..types import  SnapdResponse


def check_change(cid: str) -> SnapdResponse:
    """Checks the status of snapd change with id `cid`."""
    return http.get("/changes/" + cid)


def check_changes() -> SnapdResponse:
    """Checks the status of all snapd changes."""
    return http.get("/changes?select=all")
