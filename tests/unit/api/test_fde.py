import pytest

from snap_http import api, http, types


def test_get_keyslots(monkeypatch):
    """`api.get_keyslots` returns a `types.SnapdResponse`."""

    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="Accepted",
        result={
            "by-container-role": {
                "system-data": {
                    "volume-name": "pc",
                    "name": "ubuntu-data",
                    "encrypted": True,
                    "keyslots": {"default-recovery": {"type": "recovery"}},
                }
            }
        },
    )

    def mock_get(path):
        assert path == "/system-volumes"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_keyslots()
    assert result == mock_response


def test_get_keyslots_exception(monkeypatch):
    """`api.get_keyslots` raises a `http.SnapdHttpException`."""

    def mock_get(path):
        assert path == "/system-volumes"

        raise http.SnapdHttpException(
            {
                "message": "Bad Request",
                "kind": "bad-request",
                "value": {"reason": "bad-request"},
            }
        )

    monkeypatch.setattr(http, "get", mock_get)

    with pytest.raises(http.SnapdHttpException):
        api.get_keyslots()


def test_generate_recovery_key(monkeypatch):
    """`api.generate_recovery_key` returns a `types.SnapdResponse`."""

    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="Accepted",
        result={
            "key-id": "myrec_key1",
            "recovery-key": "21720-04915-27494-19258-36455-33442-54786-27068",
        },
    )

    def mock_post(path, body):
        assert path == "/system-volumes"
        assert body == {
            "action": "generate-recovery-key",
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.generate_recovery_key()
    assert result == mock_response


def test_generate_recovery_key_exception(monkeypatch):
    """`api.generate_recovery_key` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/system-volumes"
        assert body == {"action": "generate-recovery-key"}

        raise http.SnapdHttpException(
            {
                "message": "Bad Request",
                "kind": "not-supported",
                "value": {"reason": "not-supported"},
            }
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.generate_recovery_key()


def test_add_recovery_key(monkeypatch):
    """`api.update_recovery_key` returns a `types.SnapdResponse` for `replace`=`False`."""

    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/system-volumes"
        assert body == {
            "action": "add-recovery-key",
            "key-id": "real-key-id",
            "keyslots": [{"name": "mykeyslot"}],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.update_recovery_key("real-key-id", "mykeyslot", False)
    assert result == mock_response


def test_add_recovery_key_exception(monkeypatch):
    """`api.update_recovery_key` raises a `http.SnapdHttpException` for `replace`=`False`."""

    def mock_post(path, body):
        assert path == "/system-volumes"
        assert body == {
            "action": "add-recovery-key",
            "key-id": "fake-key-id",
            "keyslots": [{"name": "mykeyslot"}],
        }

        raise http.SnapdHttpException(
            {
                "message": "invalid recovery key: not found",
                "kind": "invalid-recovery-key",
                "value": {"reason": "not-found"},
            }
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.update_recovery_key("fake-key-id", "mykeyslot", False)


def test_replace_recovery_key(monkeypatch):
    """`api.update_recovery_key` returns a `types.SnapdResponse` for `replace`=`True`."""

    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/system-volumes"
        assert body == {
            "action": "replace-recovery-key",
            "key-id": "real-key-id",
            "keyslots": [{"name": "mykeyslot"}],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.update_recovery_key("real-key-id", "mykeyslot", True)
    assert result == mock_response


def test_replace_recovery_key_exception(monkeypatch):
    """`api.update_recovery_key` raises a `http.SnapdHttpException` for `replace`=`True`."""

    def mock_post(path, body):
        assert path == "/system-volumes"
        assert body == {
            "action": "replace-recovery-key",
            "key-id": "fake-key-id",
            "keyslots": [{"name": "mykeyslot"}],
        }

        raise http.SnapdHttpException(
            {
                "message": "invalid recovery key: not found",
                "kind": "invalid-recovery-key",
                "value": {"reason": "not-found"},
            }
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.update_recovery_key("fake-key-id", "mykeyslot", True)
