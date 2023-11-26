"""Lower-level functions for making actual HTTP requests to snapd's REST API."""
import json
import socket
from http.client import HTTPResponse
from typing import Any, Dict, Optional

from .types import SnapdResponse

BASE_URL = "http://localhost/v2"
SNAPD_SOCKET = "/run/snapd.socket"

_MAXLINE = 65536


class SnapdHttpException(Exception):
    """An exception raised during HTTP communication with snapd."""


def get(path: str) -> SnapdResponse:
    """Peform a GET request of `path`.

    Currently a stub.
    """
    return _make_request(path, "GET")


def post(path: str, body: Dict[str, Any]) -> SnapdResponse:
    """Perform a POST request of `path`, JSON-ifying `body`.

    Currently a stub.
    """
    return SnapdResponse(
        type="stub",
        status_code=500,
        status="stub",
        result={"nothing": "this is a stub"},
    )


def _make_request(path: str, method: str, body: Optional[Dict[str, Any]] = None) -> Any:
    """Performs a request to `path` using `method`, including `body`, if provided.

    urllib doesn't support HTTP requests to UNIX sockets, so we create out own socket, start the
    connection, then hand it off to `HTTPResponse` to read from and parse.
    """
    sock = socket.socket(family=socket.AF_UNIX)

    sock.connect(SNAPD_SOCKET)
    url = BASE_URL + path
    response = HTTPResponse(sock, method=method, url=url)

    request = f"{method} {url} HTTP/1.1\r\nHost: localhost\r\n"

    if body:
        json_body = json.dumps(body)
        request += f"Content-Length: {len(json_body)}\r\n\r\n{json_body}"
    else:
        request += "\r\n"

    sock.sendall(request.encode())

    response.begin()
    response_body = response.read()

    response.close()
    sock.close()

    if response.status >= 400:
        raise SnapdHttpException(body)

    return json.loads(response_body)
