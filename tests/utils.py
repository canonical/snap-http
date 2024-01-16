import time
from typing import Any, Callable

import snap_http


def wait_for(
    func: Callable[..., snap_http.SnapdResponse]
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


def is_snap_installed(snap_name: str) -> bool:
    """Check if the snap with name `snap_name` is installed."""
    return snap_name in {snap["name"] for snap in snap_http.list().result}


@wait_for
def sideload_snap(file_path: str) -> bool:
    """Sideload a snap from the local filesystem."""
    data = {"action": "install", "devmode": "true"}
    file = snap_http.FileUpload(name="snap", path=file_path)
    response = snap_http.http._make_request(
        "/snaps", "POST", body=snap_http.FormData(data=data, files=[file])
    )
    return snap_http.SnapdResponse.from_http_response(response)
