import pytest

from snap_http import api, http, types


def test_check_change(monkeypatch):
    """`api.check_change` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={
            "id": "1",
            "kind": "install-snap",
            "summary": 'Install "placeholder" snap',
            "status": "Done",
        },
    )

    def mock_get(path):
        assert path == "/changes/1"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.check_change("1")

    assert result == mock_response


def test_check_change_exception(monkeypatch):
    """`api.check_change` raises a `http.SnapdHttpException`."""

    def mock_get(path):
        assert path == "/changes/1"

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "get", mock_get)

    with pytest.raises(http.SnapdHttpException):
        _ = api.check_change("1")


def test_check_changes(monkeypatch):
    """`api.check_changes` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={
            "id": "1",
            "kind": "install-snap",
            "summary": 'Install "placeholder" snap',
            "status": "Done",
        },
    )

    def mock_get(path):
        assert path == "/changes?select=all"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.check_changes()

    assert result == mock_response


def test_check_changes_exception(monkeypatch):
    """`api.check_changes` raises a `http.SnapdHttpException`."""

    def mock_get(path):
        assert path == "/changes?select=all"

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "get", mock_get)

    with pytest.raises(http.SnapdHttpException):
        _ = api.check_changes()
