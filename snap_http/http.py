"""Lower-level functions for making actual HTTP requests to snapd's REST API."""
import json
import socket
from http.client import HTTPResponse
from io import BytesIO
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .types import FileUpload, SnapdResponse

BASE_URL = "http://localhost/v2"
SNAPD_SOCKET = "/run/snapd.socket"


class SnapdHttpException(Exception):
    """An exception raised during HTTP communication with snapd."""


def get(path: str) -> SnapdResponse:
    """Peform a GET request of `path`."""
    response = _make_request(path, "GET")

    return SnapdResponse.from_http_response(response)


def post(path: str, body: Dict[str, Any]) -> SnapdResponse:
    """Perform a POST request of `path`, JSON-ifying `body`."""
    response = _make_request(path, "POST", body)

    return SnapdResponse.from_http_response(response)


def put(path: str, body: Dict[str, Any]) -> SnapdResponse:
    """Perform a PUT request of `path`, JSON-ifying `body`."""
    response = _make_request(path, "PUT", body)

    return SnapdResponse.from_http_response(response)


def _make_request(
    path: str,
    method: str,
    body: Optional[Dict[str, Any]] = None,
    form_data: Optional[Dict[str, Any]] = None,
    files: Optional[List[FileUpload]] = None,
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
    request_str = f"{method} {url} HTTP/1.1\r\nHost: localhost\r\n"

    if body:
        json_body = json.dumps(body)
        encoded_length = len(json_body.encode())
        request_str += "Content-Type: application/json\r\n"
        request_str += f"Content-Length: {encoded_length}\r\n\r\n{json_body}"
        request.write(request_str.encode())
    elif form_data or files:
        form_data = form_data or {}
        payload, boundary = BytesIO(), str(uuid4())
        for key, value in form_data.items():
            payload.write(
                (
                    f"--{boundary}\r\n"
                    f"Content-Disposition: form-data; name=\"{key}\"\r\n\r\n"
                    f"{value}\r\n"
                ).encode()
            )

        files = files or []
        for file in files:
            payload.write(
                (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; name="{file.name}"; filename="{file.filename}"'
                    "\r\n\r\n"
                ).encode()
            )
            payload.write(file.content)
            payload.write(b"\r\n")
        payload.write(f"--{boundary}--\r\n".encode())

        request_str += f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
        request_str += f"Content-Length: {payload.getbuffer().nbytes}\r\n\r\n"
        request.write(request_str.encode())
        request.write(payload.getvalue())
    else:
        request_str += "\r\n"
        request.write(request_str.encode())

    sock.sendall(request.getvalue())

    response.begin()
    response_body = response.read()

    response.close()
    sock.close()

    if response.status >= 400:
        raise SnapdHttpException(response_body)

    return json.loads(response_body)
