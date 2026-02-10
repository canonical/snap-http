from snap_http import api, http, types


def test_get_conf(monkeypatch):
    """`api.get_conf` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path, query_params):
        assert path == "/snaps/placeholder/conf"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_conf("placeholder")

    assert result == mock_response


def test_get_specific_config_values(monkeypatch):
    """`api.get_conf` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={"foo.bar": "default", "port": 8080},
    )

    def mock_get(path, query_params):
        assert path == "/snaps/placeholder/conf"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_conf("placeholder", keys=["foo.bar", "port"])

    assert result == mock_response


def test_set_conf(monkeypatch):
    """`api.set_conf` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_put(path, _):
        assert path == "/snaps/placeholder/conf"

        return mock_response

    monkeypatch.setattr(http, "put", mock_put)

    result = api.set_conf("placeholder", {"foo": "bar"})

    assert result == mock_response
