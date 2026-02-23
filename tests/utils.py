import pathlib
import shutil
import time
from typing import Any, Callable, Dict, Optional, Tuple

import yaml

import snap_http


def wait_for(
    func: Callable[..., snap_http.SnapdResponse],
) -> Callable[..., Tuple[snap_http.SnapdResponse, Optional[snap_http.SnapdResponse]]]:
    """Call `func` and wait for changes to be applied in snapd."""

    def wrapper(
        *args: Any, **kwargs: Any
    ) -> Tuple[snap_http.SnapdResponse, Optional[snap_http.SnapdResponse]]:
        response = func(*args, **kwargs)

        if response.type == "sync":
            return response, None

        change_id = response.change
        while True:
            time.sleep(0.1)

            change_response = snap_http.check_change(change_id)
            if change_response.result["status"] in snap_http.COMPLETE_STATUSES:
                return response, change_response

    return wrapper


# Snaps


def is_snap_installed(snap_name: str) -> bool:
    """Check if the snap with name `snap_name` is installed."""
    return snap_name in {snap["name"] for snap in snap_http.list().result}


def get_snap_details(snap_name: str) -> Dict[str, Any]:
    """Get the details of an installed snap."""
    return snap_http.list(snaps=[snap_name]).result[0]


# Assertions


def parse_assertion(raw: bytes) -> dict:
    """Parse a snapd assertion, stripping the trailing signature block."""
    headers, _ = raw.decode().rsplit("\n\n", 1)
    return yaml.safe_load(headers)


ASSERTION_BASE_PATH = "/var/lib/snapd/assertions/asserts-v0"

ASSERTION_HANDLERS = {
    "snap-declaration": {
        "path": lambda snap_id, series: f"snap-declaration/{series}/{snap_id}",
        "filters": lambda snap_id, series: {"snap-id": snap_id, "series": series},
        "identifier": lambda snap_id, series: f"snap-id: {snap_id}",
    },
    "confdb-schema": {
        "path": lambda account_id, name: f"confdb-schema/{account_id}/{name}",
        "filters": lambda account_id, name: {"account-id": account_id, "name": name},
        "identifier": lambda account_id, name: f"name: {name}",
    },
}


def assertion_exists(assertion_type: str, **kwargs) -> bool:
    """Check if an assertion that matches the kwargs exists."""
    handler = ASSERTION_HANDLERS[assertion_type]
    filters = handler["filters"](**kwargs)
    identifier = handler["identifier"](**kwargs)

    response = snap_http.get_assertions(assertion_type, filters=filters)
    return identifier in response.result.decode()


def remove_assertion(assertion_type: str, **kwargs) -> None:
    """Remove an assertion.

    Use ONLY for testing assertions. Removing any type of assertion doesn't
    seem to be officially supported by the snap CLI or the snap REST API.
    """
    handler = ASSERTION_HANDLERS[assertion_type]
    relative_path = handler["path"](**kwargs)
    full_path = pathlib.Path(ASSERTION_BASE_PATH) / relative_path

    if full_path.is_dir():
        shutil.rmtree(full_path)
