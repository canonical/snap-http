from snap_http import api, http, types


def test_get_recovery_systems(monkeypatch) -> None:
    """`api.get_recovery_systems` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path):
        assert path == "/systems"
        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_recovery_systems()

    assert result == mock_response

def test_get_recovery_system(monkeypatch) -> None:
    """`api.get_recovery_system` returns a `types.SnapdResponse`."""
    label="20251022"
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path):
        assert path == f"/systems/{label}"
        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_recovery_system(label)

    assert result == mock_response

def test_perform_system_action(monkeypatch) -> None:
    """`api.perform_system_action` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    action: str = "do"
    mode: str = "recover"
    def mock_post(path, body):
        assert path == "/systems"
        assert body == {
                "action": action,
                "mode": mode
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.perform_system_action(action, mode)

    assert result == mock_response


def test_perform_recovery_action(monkeypatch) -> None:
    """`api.perform_recovery_action` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    action: str = "do"
    mode: str = "recover"
    label: str = "20250410"
    def mock_post(path, body):
        assert path == f"/systems/{label}"
        assert body == {
                "action": action,
                "mode": mode
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.perform_recovery_action(label, action, mode)

    assert result == mock_response
