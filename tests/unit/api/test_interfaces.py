from snap_http import api, http, types


def test_get_connections(monkeypatch):
    """`api.get_connections` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path, query_params):
        assert path == "/connections"
        assert query_params == {"snap": "placeholder", "select": "all", "interface": "snapd"}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_connections(snap="placeholder", select="all", interface="snapd")

    assert result == mock_response


def test_get_interfaces(monkeypatch):
    """`api.get_interfaces` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path, query_params):
        assert path == "/interfaces"
        assert query_params == {"select": "all", "slots": True, "plugs": True, "doc": True, "names": "snapd"}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_interfaces(select="all", slots=True, plugs=True, doc=True, names="snapd")

    assert result == mock_response


def test_connect_interface(monkeypatch):
    """`api.connect_interface` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    def mock_post(path, body):
        assert path == "/interfaces"
        assert body == {
                "action": "connect",
                "slots": [{"snap": "placeholder1", "slot": "config"}],
                "plugs": [{"snap": "placeholder2", "plug": "config"}],
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.connect_interface(in_snap="placeholder1", in_slot="config", out_snap="placeholder2", out_plug="config")

    assert result == mock_response


def test_disconnect_interface(monkeypatch):
    """`api.disconnect_interface` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    def mock_post(path, body):
        assert path == "/interfaces"
        assert body == {
                "action": "disconnect",
                "slots": [{"snap": "placeholder1", "slot": "config"}],
                "plugs": [{"snap": "placeholder2", "plug": "config"}],
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.disconnect_interface(in_snap="placeholder1", in_slot="config", out_snap="placeholder2", out_plug="config")

    assert result == mock_response
