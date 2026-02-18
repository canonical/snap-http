from snap_http import api, http, types


def test_get_confdb(monkeypatch):
    """`api.get_confdb` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_get(path, query_params):
        assert path == "/confdb/system/network/wifi-state"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_confdb("system", "network", "wifi-state")

    assert result == mock_response


def test_get_confdb_with_keys(monkeypatch):
    """`api.get_confdb` with keys parameter returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_get(path, query_params):
        assert path == "/confdb/system/network/wifi-state"
        assert query_params == {"keys": "ssid,status"}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_confdb(
        "system", "network", "wifi-state", keys=["ssid", "status"]
    )

    assert result == mock_response


def test_set_confdb(monkeypatch):
    """`api.set_confdb` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_put(path, body):
        assert path == "/confdb/system/network/wifi-admin"
        assert body == {"values": {"ssid": "my-network", "password": None}}

        return mock_response

    monkeypatch.setattr(http, "put", mock_put)

    result = api.set_confdb(
        "system",
        "network",
        "wifi-admin",
        {"ssid": "my-network", "password": None},
    )

    assert result == mock_response


def test_delegate_confdb(monkeypatch):
    """`api.delegate_confdb` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=None,
    )

    def mock_post(path, body):
        assert path == "/confdb"
        assert body == {
            "action": "delegate",
            "operator-id": "alice",
            "authentications": ["operator-key", "store"],
            "views": ["bob/network/wifi-admin", "bob/network/wifi-state"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.delegate_confdb(
        "alice",
        authentications=["operator-key", "store"],
        views=["bob/network/wifi-admin", "bob/network/wifi-state"],
    )

    assert result == mock_response


def test_undelegate_confdb_all(monkeypatch):
    """`api.undelegate_confdb` withdraws all access."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=None,
    )

    def mock_post(path, body):
        assert path == "/confdb"
        assert body == {
            "action": "undelegate",
            "operator-id": "alice",
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.undelegate_confdb("alice")

    assert result == mock_response


def test_undelegate_confdb_partial(monkeypatch):
    """`api.undelegate_confdb` withdraws specific access."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=None,
    )

    def mock_post(path, body):
        assert path == "/confdb"
        assert body == {
            "action": "undelegate",
            "operator-id": "alice",
            "authentications": ["store"],
            "views": ["bob/network/wifi-admin"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.undelegate_confdb(
        "alice",
        authentications=["store"],
        views=["bob/network/wifi-admin"],
    )

    assert result == mock_response
