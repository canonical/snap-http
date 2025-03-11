"""Lower-level functions for making actual HTTP requests to snapd's REST API."""

import json
import socket
from functools import cached_property
from http.client import HTTPResponse, responses
from io import BytesIO
from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode

from .types import JsonData, SnapdRequestBody, SnapdResponse

BASE_URL = "http://localhost/v2"
SNAPD_SOCKET = "/run/snapd.socket"


class SnapdHttpException(Exception):
    """An exception raised during HTTP communication with snapd."""

    @cached_property
    def json(self) -> Union[Dict[str, Any], None]:
        """Attempts to parse the body of this exception as json."""
        result = None
        if self.args:
            body = self.args[0]
            result = json.loads(body)

        return result


def get(path: str, **kwargs: Any) -> SnapdResponse:
    """Peform a GET request of `path`."""
    response = _make_request(path, "GET", **kwargs)

    return SnapdResponse.from_http_response(response)


def post(path: str, body: SnapdRequestBody) -> SnapdResponse:
    """Perform a POST request of `path`, JSON-ifying `body`."""
    response = _make_request(path, "POST", body=body)

    return SnapdResponse.from_http_response(response)


def put(path: str, body: SnapdRequestBody) -> SnapdResponse:
    """Perform a PUT request of `path`, JSON-ifying `body`."""
    response = _make_request(path, "PUT", body=body)

    return SnapdResponse.from_http_response(response)


def _make_request(
    path: str,
    method: str,
    *,
    body: Optional[SnapdRequestBody] = None,
    query_params: Optional[Dict[str, Any]] = None,
) -> Any:
    """Performs a request to `path` using `method`, including `body`, if provided.

    urllib doesn't support HTTP requests to UNIX sockets, so we create out own socket, start the
    connection, then hand it off to `HTTPResponse` to read from and parse.
    """
    sock = socket.socket(family=socket.AF_UNIX)
    sock.connect(SNAPD_SOCKET)

    url = BASE_URL + path
    if query_params:
        url += "?" + urlencode(query_params)

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

    response_type = response.getheader("Content-Type")
    if response_type == "application/json":
        return json.loads(response_body)
    else:  # other types like application/x.ubuntu.assertion
        response_code = response.getcode()
        is_async = response_code == 202
        return {
            "type": "async" if is_async else "sync",
            "status_code": response_code,
            "status": responses[response_code],
            "result": response_body,
        }
