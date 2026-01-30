from snap_http import api, http, types


def test_snapshots(monkeypatch):
    """`api.snapshots` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[{"title": "placeholder1"}, {"title": "placeholder2"}],
    )

    def mock_get(path):
        assert path == "/snapshots"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.snapshots()

    assert result == mock_response


def test_save_snapshot(monkeypatch):
    """`api.snapshots` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result=[{"title": "placeholder1"}, {"title": "placeholder2"}],
    )

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {
            "action": "snapshot",
            "snaps": ["snapd"],
            "users": ["user1"],}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.save_snapshot(snaps=["snapd"], users=["user1"])

    assert result == mock_response


def test_forget_snapshot(monkeypatch):
    """`api.forget_snapshot` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result=[{"title": "placeholder1"}, {"title": "placeholder2"}],
    )

    def mock_post(path, body):
        assert path == "/snapshots"
        assert body == {
            "action": "forget",
            "set": 1,
            "snaps": ["snapd"],
            "users": ["user1"],
            }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.forget_snapshot(1, snaps=["snapd"], users=["user1"])

    assert result == mock_response
