import pytest

from snap_http import api, http, types


def test_get_apps_all_apps_on_system(monkeypatch):
    """`api.get_apps` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[
            {
                "snap": "lxd",
                "name": "activate",
                "daemon": "oneshot",
                "daemon-scope": "system",
                "enabled": True,
            },
            {
                "snap": "test-snap",
                "name": "bye-svc",
                "daemon": "simple",
                "daemon-scope": "system",
            },
            {
                "snap": "test-snap",
                "name": "hello-svc",
                "daemon": "simple",
                "daemon-scope": "system",
            },
            {"snap": "test-snap", "name": "test-snap"},
        ],
    )

    def mock_get(path, query_params):
        assert path == "/apps"
        assert query_params == {}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_apps()
    assert result == mock_response


def test_get_apps_from_specific_snaps(monkeypatch):
    """`api.get_apps` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[
            {
                "snap": "lxd",
                "name": "activate",
                "daemon": "oneshot",
                "daemon-scope": "system",
                "enabled": True,
            },
            {
                "snap": "lxd",
                "name": "user-daemon",
                "daemon": "simple",
                "daemon-scope": "system",
                "enabled": True,
                "activators": [
                    {
                        "Name": "unix",
                        "Type": "socket",
                        "Active": True,
                        "Enabled": True,
                    }
                ],
            },
            {
                "snap": "test-snap",
                "name": "bye-svc",
                "daemon": "simple",
                "daemon-scope": "system",
            },
            {
                "snap": "test-snap",
                "name": "hello-svc",
                "daemon": "simple",
                "daemon-scope": "system",
            },
            {"snap": "test-snap", "name": "test-snap"},
        ],
    )

    def mock_get(path, query_params):
        assert path == "/apps"
        assert query_params == {"names": "lxd,test-snap"}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_apps(names=["lxd", "test-snap"])
    assert result == mock_response


def test_get_apps_filter_services_only(monkeypatch):
    """`api.get_apps` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[
            {
                "snap": "test-snap",
                "name": "bye-svc",
                "daemon": "simple",
                "daemon-scope": "system",
            },
            {
                "snap": "test-snap",
                "name": "hello-svc",
                "daemon": "simple",
                "daemon-scope": "system",
            },
            {"snap": "test-snap", "name": "test-snap"},
        ],
    )

    def mock_get(path, query_params):
        assert path == "/apps"
        assert query_params == {"names": "test-snap", "select": "service"}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_apps(names=["test-snap"], services_only=True)
    assert result == mock_response


def test_get_apps_exception(monkeypatch):
    """`api.get_apps` raises a `http.SnapdHttpException`."""

    def mock_get(path, query_params):
        assert path == "/apps"

        raise http.SnapdHttpException(
            {
                "message": 'snap "idonotexist" not found',
                "kind": "snap-not-found",
                "value": "idonotexist",
            }
        )

    monkeypatch.setattr(http, "get", mock_get)

    with pytest.raises(http.SnapdHttpException):
        api.get_apps(names=["idonotexist"])


def test_start(monkeypatch):
    """`api.start` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "start",
            "enable": False,
            "names": ["test-snap"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.start("test-snap")
    assert result == mock_response


def test_start_and_enable(monkeypatch):
    """`api.start` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "start",
            "enable": True,
            "names": ["test-snap"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.start("test-snap", True)
    assert result == mock_response


def test_start_exception(monkeypatch):
    """`api.start` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/apps"

        raise http.SnapdHttpException(
            {
                "message": 'snap "idonotexist" not found',
                "kind": "snap-not-found",
                "value": "idonotexist",
            }
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.start("idonotexist")


def test_start_all(monkeypatch):
    """`api.start_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "start",
            "enable": False,
            "names": ["test-snap", "lxd", "multipass"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.start_all(["test-snap", "lxd", "multipass"])
    assert result == mock_response


def test_start_all_and_enable(monkeypatch):
    """`api.start_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "start",
            "enable": True,
            "names": ["test-snap", "lxd", "multipass"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.start_all(["test-snap", "lxd", "multipass"], True)
    assert result == mock_response


def test_start_all_exception(monkeypatch):
    """`api.start_all` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/apps"

        raise http.SnapdHttpException(
            {
                "message": 'snap "idonotexist" not found',
                "kind": "snap-not-found",
                "value": "idonotexist",
            }
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.start_all(["idonotexist", "lxd"])


def test_stop(monkeypatch):
    """`api.stop` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "stop",
            "disable": False,
            "names": ["test-snap"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.stop("test-snap")
    assert result == mock_response


def test_stop_and_disable(monkeypatch):
    """`api.stop` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "stop",
            "disable": True,
            "names": ["test-snap"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.stop("test-snap", True)
    assert result == mock_response


def test_stop_exception(monkeypatch):
    """`api.stop` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/apps"

        raise http.SnapdHttpException(
            {
                "message": 'snap "idonotexist" not found',
                "kind": "snap-not-found",
                "value": "idonotexist",
            }
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.stop("idonotexist")


def test_stop_all(monkeypatch):
    """`api.stop_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "stop",
            "disable": False,
            "names": ["test-snap", "lxd", "multipass"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.stop_all(["test-snap", "lxd", "multipass"])
    assert result == mock_response


def test_stop_all_and_disable(monkeypatch):
    """`api.stop_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "stop",
            "disable": True,
            "names": ["test-snap", "lxd", "multipass"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.stop_all(["test-snap", "lxd", "multipass"], True)
    assert result == mock_response


def test_stop_all_exception(monkeypatch):
    """`api.stop_all` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/apps"

        raise http.SnapdHttpException(
            {
                "message": 'snap "idonotexist" not found',
                "kind": "snap-not-found",
                "value": "idonotexist",
            }
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.stop_all(["idonotexist", "lxd"])


def test_restart(monkeypatch):
    """`api.restart` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "restart",
            "reload": False,
            "names": ["test-snap"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.restart("test-snap")
    assert result == mock_response


def test_restart_and_reload(monkeypatch):
    """`api.restart` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "restart",
            "reload": True,
            "names": ["test-snap"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.restart("test-snap", True)
    assert result == mock_response


def test_restart_exception(monkeypatch):
    """`api.restart` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/apps"

        raise http.SnapdHttpException(
            {
                "message": 'snap "idonotexist" not found',
                "kind": "snap-not-found",
                "value": "idonotexist",
            }
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.restart("idonotexist")


def test_restart_all(monkeypatch):
    """`api.restart_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "restart",
            "reload": False,
            "names": ["test-snap", "lxd", "multipass"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.restart_all(["test-snap", "lxd", "multipass"])
    assert result == mock_response


def test_restart_all_and_reload(monkeypatch):
    """`api.restart_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/apps"
        assert body == {
            "action": "restart",
            "reload": True,
            "names": ["test-snap", "lxd", "multipass"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.restart_all(["test-snap", "lxd", "multipass"], True)
    assert result == mock_response


def test_restart_all_exception(monkeypatch):
    """`api.restart_all` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/apps"

        raise http.SnapdHttpException(
            {
                "message": 'snap "idonotexist" not found',
                "kind": "snap-not-found",
                "value": "idonotexist",
            }
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.restart_all(["idonotexist", "lxd"])
