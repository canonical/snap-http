import pytest

from snap_http import api, http, types


def test_list_users(monkeypatch):
    """`api.list_users` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[{"id": 1, "username": "john", "email": "john.doe@example.com"}],
    )

    def mock_get(path):
        assert path == "/users"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.list_users()
    assert result == mock_response


def test_add_user(monkeypatch):
    """`api.add_user` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[
            {
                "username": "john-doe",
                "ssh-keys": [
                    "ssh-ed25519 some-ssh-key john@localhost # "
                    'snapd {"origin":"store","email":"john.doe@example.com"}'
                ],
            }
        ],
    )

    def mock_post(path, body):
        assert path == "/users"

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.add_user(
        username="john-doe", email="john.doe@example.com", force_managed=True
    )
    assert result == mock_response


def test_add_user_exception(monkeypatch):
    """`api.add_user` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/users"

        raise http.SnapdHttpException(
            {"message": "cannot create user: device already managed"}
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.add_user(username="john-doe", email="john.doe@example.com")


def test_remove_user(monkeypatch):
    """`api.remove_user` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={
            "removed": [
                {"id": 4, "username": "john-doe", "email": "john.doe@example.com"}
            ]
        },
    )

    def mock_post(path, body):
        assert path == "/users"

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.remove_user(username="john-doe")
    assert result == mock_response


def test_remove_user_exception(monkeypatch):
    """`api.remove_user` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/users"

        raise http.SnapdHttpException({"message": 'user "jane-doe" is not known'})

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.remove_user(username="jane-doe")
