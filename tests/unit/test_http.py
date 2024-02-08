"""Tests for `snap_http.http`, lower-level functions for interacting with Snapd via HTTP."""

import io
import json
import os
import socket
import tempfile
import threading

import pytest

from snap_http import http, types

FAKE_SNAPD_SOCKET = "/tmp/testsnapd.socket"


@pytest.fixture
def use_snapd_response():
    """A mock Snapd, listening on a socket like the real one does, in another thread."""

    if os.path.exists(FAKE_SNAPD_SOCKET):
        os.remove(FAKE_SNAPD_SOCKET)

    sock = socket.socket(family=socket.AF_UNIX)
    sock.bind(FAKE_SNAPD_SOCKET)
    sock.listen()

    thread = None

    def run_snapd_thread(code, response_body, result_type="application/json"):
        if result_type == "application/json":
            body = json.dumps(response_body)
            encoded_length = len(body.encode())
        else:
            encoded_length = len(response_body)
            body = response_body.decode()

        http_response = (
            f"HTTP/1.1 {code}\r\n"
            f"Content-Type: {result_type}\r\n"
            f"Content-Length: {encoded_length}\r\n\r\n{body}"
        )

        receiver = io.BytesIO()

        def run():
            conn, _ = sock.accept()
            receiver.write(conn.recv(1024))
            conn.sendall(http_response.encode())

        nonlocal thread
        thread = threading.Thread(target=run)
        thread.start()

        return receiver, thread

    yield run_snapd_thread

    if thread is not None:
        thread.join()

    sock.close()


def assert_request_contains(receiver, thread, expected):
    """Checks that the receiver, as written to by the mock snapd running in thread,
    contains the expected content.

    NOTE: intended to be called only at the end of test methods that use
    `use_snapd_response`.
    """
    thread.join()

    assert expected.encode() in receiver.getvalue()


def test_get(use_snapd_response, monkeypatch):
    """`http.get` returns a `types.SnapdResponse`."""
    monkeypatch.setattr(http, "SNAPD_SOCKET", FAKE_SNAPD_SOCKET)
    mock_response = {
        "type": "sync",
        "status_code": 200,
        "status": "OK",
        "result": [{"title": "placeholder1"}, {"title": "placeholder2"}],
    }
    use_snapd_response(200, mock_response)

    result = http.get("/snaps")

    assert result == types.SnapdResponse.from_http_response(mock_response)


def test_get_exception(use_snapd_response, monkeypatch):
    """`http.get` raises a `http.SnapdHttpException` for error response codes."""
    monkeypatch.setattr(http, "SNAPD_SOCKET", FAKE_SNAPD_SOCKET)
    mock_response = {
        "type": "sync",
        "status_code": 404,
        "status": "Not Found",
        "result": None,
    }
    use_snapd_response(404, mock_response)

    with pytest.raises(http.SnapdHttpException):
        _ = http.get("/snaps/placeholder")


def test_get_non_json_data(use_snapd_response, monkeypatch):
    """`http.get` returns a `types.SnapdResponse.`"""
    monkeypatch.setattr(http, "SNAPD_SOCKET", FAKE_SNAPD_SOCKET)
    mock_response = b"assertion-header: value\n\nsignature"
    use_snapd_response(
        200,
        mock_response,
        "application/x.ubuntu.assertion",
    )

    result = http.get("/assertions/serial")

    assert result == types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=b"assertion-header: value\n\nsignature",
    )


def test_get_returns_a_warning(use_snapd_response, monkeypatch):
    """`http.get` returns a `types.SnapdResponse.`"""
    monkeypatch.setattr(http, "SNAPD_SOCKET", FAKE_SNAPD_SOCKET)
    mock_response = {
        "type": "sync",
        "status-code": 200,
        "status": "OK",
        "result": [],
        "warning-timestamp": "2024-02-08T10:05:14.471969021Z",
        "warning-count": 1,
    }
    use_snapd_response(200, mock_response)

    result = http.get("/users")

    assert result == types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[],
        warning_timestamp="2024-02-08T10:05:14.471969021Z",
        warning_count=1,
    )


def test_post(use_snapd_response, monkeypatch):
    """`http.post` returns a `types.SnapdResponse`."""
    monkeypatch.setattr(http, "SNAPD_SOCKET", FAKE_SNAPD_SOCKET)
    mock_response = {
        "type": "async",
        "status_code": 202,
        "status": "Accepted",
        "result": None,
        "change": "1",
    }
    receiver, thread = use_snapd_response(202, mock_response)

    result = http.post("/snaps/placeholder", {"action": "install"})

    assert result == types.SnapdResponse.from_http_response(mock_response)
    assert_request_contains(receiver, thread, '{"action": "install"}')


def test_post_exception(use_snapd_response, monkeypatch):
    """`http.post` raises a `http.SnapdHttpException` for error response codes."""
    monkeypatch.setattr(http, "SNAPD_SOCKET", FAKE_SNAPD_SOCKET)
    mock_response = {
        "type": "sync",
        "status_code": 404,
        "status": "Not Found",
        "result": None,
    }
    receiver, thread = use_snapd_response(404, mock_response)

    with pytest.raises(http.SnapdHttpException):
        _ = http.post("/snaps/placeholder", {"action": "install"})

    assert_request_contains(receiver, thread, '{"action": "install"}')


def test_put(use_snapd_response, monkeypatch):
    """`http.put` returns a `types.SnapdResponse`."""
    monkeypatch.setattr(http, "SNAPD_SOCKET", FAKE_SNAPD_SOCKET)
    mock_response = {
        "type": "async",
        "status_code": 202,
        "status": "Accepted",
        "result": None,
        "change": "1",
    }
    receiver, thread = use_snapd_response(202, mock_response)

    result = http.put("/snaps/placeholder/set_conf", {"foo": "bar"})

    assert result == types.SnapdResponse.from_http_response(mock_response)
    assert_request_contains(receiver, thread, '{"foo": "bar"}')


def test_put_exception(use_snapd_response, monkeypatch):
    """`http.put` raises a `http.SnapdHttpException` for error response codes."""
    monkeypatch.setattr(http, "SNAPD_SOCKET", FAKE_SNAPD_SOCKET)
    mock_response = {
        "type": "error",
        "status_code": 404,
        "status": "Not Found",
        "result": {
            "message": 'snap "placeholder" is not installed',
            "kind": "snap-not-found",
            "value": "placeholder",
        },
    }
    receiver, thread = use_snapd_response(404, mock_response)

    with pytest.raises(http.SnapdHttpException) as e:
        http.put("/snaps/placeholder/conf", {"foo": "bar"})

    assert_request_contains(receiver, thread, '{"foo": "bar"}')
    assert e.value.json == {
        "type": "error",
        "status_code": 404,
        "status": "Not Found",
        "result": {
            "message": 'snap "placeholder" is not installed',
            "kind": "snap-not-found",
            "value": "placeholder",
        }
    }


def test_parse_snap_exception_body_no_args():
    """`SnapdHttpException.json` returns `None`."""
    exception = http.SnapdHttpException()

    assert exception.json is None


def test_making_multipart_request(use_snapd_response, monkeypatch):
    """`http._make_request` successfully makes a multi-part form request."""
    monkeypatch.setattr(http, "SNAPD_SOCKET", FAKE_SNAPD_SOCKET)
    mock_response = {
        "type": "async",
        "status_code": 202,
        "status": "Accepted",
        "result": None,
        "change": "1",
    }
    receiver, thread = use_snapd_response(202, mock_response)

    with tempfile.NamedTemporaryFile() as tmp:
        data = {"action": "install", "devmode": "true"}
        file = types.FileUpload(name="snap", path=tmp.name)
        result = http._make_request(
            "/snaps", "POST", body=types.FormData(data=data, files=[file])
        )

    assert result == mock_response
    assert_request_contains(
        receiver,
        thread,
        f'Content-Disposition: form-data; name="snap"; filename="{file.filename}"',
    )
