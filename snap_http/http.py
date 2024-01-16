"""Lower-level functions for making actual HTTP requests to snapd's REST API."""
import json
import socket
from http.client import HTTPResponse
from io import BytesIO
from typing import Any, Optional

from .types import JsonData, SnapdRequestBody, SnapdResponse

BASE_URL = "http://localhost/v2"
SNAPD_SOCKET = "/run/snapd.socket"


class SnapdHttpException(Exception):
    """An exception raised during HTTP communication with snapd."""


def get(path: str) -> SnapdResponse:
    """Peform a GET request of `path`."""
    response = _make_request(path, "GET")

    return SnapdResponse.from_http_response(response)


def post(path: str, body: SnapdRequestBody) -> SnapdResponse:
    """Perform a POST request of `path`, JSON-ifying `body`."""
    response = _make_request(path, "POST", body)

    return SnapdResponse.from_http_response(response)


def put(path: str, body: SnapdRequestBody) -> SnapdResponse:
    """Perform a PUT request of `path`, JSON-ifying `body`."""
    response = _make_request(path, "PUT", body)

    return SnapdResponse.from_http_response(response)


def _make_request(
    path: str, method: str, body: Optional[SnapdRequestBody] = None
) -> Any:
    """Performs a request to `path` using `method`, including `body`, if provided.

    urllib doesn't support HTTP requests to UNIX sockets, so we create out own socket, start the
    connection, then hand it off to `HTTPResponse` to read from and parse.
    """
    sock = socket.socket(family=socket.AF_UNIX)

    sock.connect(SNAPD_SOCKET)
    url = BASE_URL + path
    response = HTTPResponse(sock, method=method, url=url)

    request = BytesIO()
    request.write(f"{method} {url} HTTP/1.1\r\nHost: localhost\r\n".encode())

    if body:
        if isinstance(body, dict):
            body = JsonData(body)

        request.write(
            (
                f"Content-Type: {body.content_type_header}\r\n"
                f"Content-Length: {body.content_length}\r\n\r\n"
            ).encode()
        )
        request.write(body.serialized)
    else:
        request.write(b"\r\n")

    sock.sendall(request.getvalue())

    response.begin()
    response_body = response.read()

    response.close()
    sock.close()

    if response.status >= 400:
        raise SnapdHttpException(response_body)

    return json.loads(response_body)
