import pathlib
import shutil
import time
from typing import Any, Callable, Dict

import snap_http


def wait_for(
    func: Callable[..., snap_http.SnapdResponse],
) -> Callable[..., snap_http.SnapdResponse]:
    """Call `func` and wait for changes to be applied in snapd."""

    def wrapper(*args: Any, **kwargs: Any) -> snap_http.SnapdResponse:
        response = func(*args, **kwargs)

        if response.type == "sync":
            return response

        change = response.change
        while True:
            time.sleep(0.1)

            status = snap_http.check_change(change).result
            if status["status"] in snap_http.COMPLETE_STATUSES:
                return response

    return wrapper


# Snaps


def is_snap_installed(snap_name: str) -> bool:
    """Check if the snap with name `snap_name` is installed."""
    return snap_name in {snap["name"] for snap in snap_http.list().result}


def is_snap_purged(snap_name: str) -> bool:
    """Check if the snap with name `snap_name` is purged."""
    # Iterate over all results and collect all snapshots
    snapshots = []
    for result in snap_http.snapshots().result:
        if result:
            snapshots.extend(result.get("snapshots", []))
    installed = is_snap_installed(snap_name)
    snapshot = snap_name in {
        snapshot["snap"]
        for snapshot in snapshots
        
    return snapshot


def get_snap_details(snap_name: str) -> Dict[str, Any]:
    """Get the details of an installed snap."""
    return next(
        filter(
            lambda snap: snap["name"] == snap_name,
            snap_http.list().result,
        )
    )


# Assertions


def assertion_exists(assertion_type, snap_id, series) -> bool:
    """Check if an assertion that matches the `*args` exists."""
    response = snap_http.get_assertions(
        assertion_type,
        filters={"snap-id": snap_id, "series": series},
    )
    return snap_id in response.result.decode()


def remove_assertion(assertion_type, snap_id, series) -> None:
    """Remove an assertion.

    Use ONLY for testing assertions. Removing any type of assertion doesn't
    seem to be officially supported by the snap CLI or the snap REST API.
    """
    path = f"/var/lib/snapd/assertions/asserts-v0/{assertion_type}/{series}/{snap_id}"
    if pathlib.Path(path).is_dir():
        shutil.rmtree(path)
