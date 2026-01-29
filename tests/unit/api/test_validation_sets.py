from snap_http import api, http, types


def test_get_validation_sets(monkeypatch) -> None:
    """`api.get_validation_sets` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path):
        assert path == "/validation-sets"
        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_validation_sets()

    assert result == mock_response


def test_get_validation_set(monkeypatch) -> None:
    """`api.get_validation_set` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    account_id: str = "device-platform"
    validation_set_name: str = "dev-validation-set"

    def mock_get(path):
        assert path == f"/validation-sets/{account_id}/{validation_set_name}"
        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_validation_set(account_id, validation_set_name)

    assert result == mock_response


def test_refresh_validation_set(monkeypatch) -> None:
    """`api.refresh_validation_set` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    account_id: str = "device-platform"
    validation_set_name: str = "dev-validation-set"
    validation_set_sequence: int = 12

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {
                "action": "refresh",
                "validation-sets": [
                    f"{account_id}/{validation_set_name}={validation_set_sequence}"
                    ],
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.refresh_validation_set(account_id, validation_set_name, validation_set_sequence)

    assert result == mock_response


def test_enforce_validation_set(monkeypatch) -> None:
    """`api.enforce_validation_set` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    account_id: str = "device-platform"
    validation_set_name: str = "dev-validation-set"
    validation_set_sequence: int = 12

    def mock_post(path, body):
        assert path == f"/validation-sets/{account_id}/{validation_set_name}"
        assert body == {
                "action": "apply",
                "mode": "enforce",
                "sequence": validation_set_sequence
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.enforce_validation_set(account_id, validation_set_name, validation_set_sequence)

    assert result == mock_response


def test_forget_validation_set(monkeypatch) -> None:
    """`api.refresh_validation_set` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    account_id: str = "device-platform"
    validation_set_name: str = "dev-validation-set"
    validation_set_sequence: int = 12

    def mock_post(path, body):
        assert path == f"/validation-sets/{account_id}/{validation_set_name}"
        assert body == {
                "action": "forget",
                "sequence": validation_set_sequence
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.forget_validation_set(account_id, validation_set_name, validation_set_sequence)

    assert result == mock_response


def test_monitor_validation_set(monkeypatch) -> None:
    """`api.refresh_validation_set` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    account_id: str = "device-platform"
    validation_set_name: str = "dev-validation-set"
    validation_set_sequence: int = 12

    def mock_post(path, body):
        assert path == f"/validation-sets/{account_id}/{validation_set_name}"
        assert body == {
                "action": "apply",
                "mode": "monitor",
                "sequence": validation_set_sequence
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.monitor_validation_set(account_id, validation_set_name, validation_set_sequence)

    assert result == mock_response
