import time
from typing import Any, Callable

import snap_http


def call_and_await_api(name: str, *args: Any, **kwargs: Any) -> snap_http.SnapdResponse:
    """Call the `name` endpoint and wait until changes are applied."""
    f: Callable[..., snap_http.SnapdResponse] = getattr(snap_http, name)
    response = f(*args, **kwargs)

    if response.type == "sync":
        return response

    change = response.change
    while True:
        time.sleep(0.1)

        status = snap_http.check_change(change).result
        if status["status"] in snap_http.COMPLETE_STATUSES:
            break

    return response


def is_snap_installed(snap_name: str) -> bool:
    """Check if the snap with name `snap_name` is installed."""
    return snap_name in {snap["name"] for snap in snap_http.list().result}
