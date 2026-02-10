import pytest

from snap_http import api, http, types


def test_get_assertion_types(monkeypatch):
    """`api.get_assertion_types` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={
            "types": ["account", "base-declaration", "serial", "system-user"],
        },
    )

    def mock_get(path):
        assert path == "/assertions"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_assertion_types()
    assert result == mock_response


def test_get_assertions(monkeypatch):
    """`api.get_assertions` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=(
            "assertion-header0: value0\n\nsignature0\n\n"
            "assertion-header: value\nassertion-header1: value1\n\nsignature"
        ).encode(),
    )

    def mock_get(path, query_params):
        assert path == "/assertions/serial-request"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_assertions("serial-request")
    assert result == mock_response


def test_get_assertions_with_filters(monkeypatch):
    """`api.get_assertions` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=b"assertion-header0: value0\n\nsignature0",
    )

    def mock_get(path, query_params):
        assert path == "/assertions/serial-request"
        assert query_params == {"assertion-header0": "value0"}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_assertions(
        "serial-request", filters={"assertion-header0": "value0"}
    )
    assert result == mock_response


def test_add_assertion(monkeypatch):
    """`api.add_assertion` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=None,
    )

    def mock_post(path, assertion):
        assert path == "/assertions"

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.add_assertion("assertion-header0: value0\n\nsignature0")
    assert result == mock_response


def test_add_assertion_exception(monkeypatch):
    """`api.add_assertion` raises a `http.SnapdHttpException`."""

    def mock_post(path, assertion):
        assert path == "/assertions"

        raise http.SnapdHttpException(
            {"message": "cannot decode request body into assertions: unexpected EOF"}
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.add_assertion("not an assertion")
