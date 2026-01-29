import snap_http

from tests.utils import wait_for


def test_get_all_apps(test_snap):
    """Test getting all apps."""
    response = snap_http.get_apps()
    assert response.status_code == 200

    result = sorted(response.result, key=lambda app: app["name"], reverse=True)
    assert len(result) > 3  # 3 apps come from `test_snap`
    apps = list(filter(lambda app: app["snap"] == "test-snap", result))
    assert apps == [
        {"snap": "test-snap", "name": "test-snap"},
        {
            "snap": "test-snap",
            "name": "hello-svc",
            "daemon": "simple",
            "daemon-scope": "system",
        },
        {
            "snap": "test-snap",
            "name": "bye-svc",
            "daemon": "simple",
            "daemon-scope": "system",
        },
    ]


def test_get_all_apps_in_snap(test_snap):
    """Test getting apps in a single snap."""
    response = snap_http.get_apps(names=["test-snap"])
    assert response.status_code == 200

    apps = sorted(response.result, key=lambda app: app["name"], reverse=True)
    assert apps == [
        {"snap": "test-snap", "name": "test-snap"},
        {
            "snap": "test-snap",
            "name": "hello-svc",
            "daemon": "simple",
            "daemon-scope": "system",
        },
        {
            "snap": "test-snap",
            "name": "bye-svc",
            "daemon": "simple",
            "daemon-scope": "system",
        },
    ]


def test_get_services_only(test_snap):
    """Test getting services only."""
    response = snap_http.get_apps(names=["test-snap"], services_only=True)
    assert response.status_code == 200

    apps = sorted(response.result, key=lambda app: app["name"], reverse=True)
    assert apps == [
        {
            "snap": "test-snap",
            "name": "hello-svc",
            "daemon": "simple",
            "daemon-scope": "system",
        },
        {
            "snap": "test-snap",
            "name": "bye-svc",
            "daemon": "simple",
            "daemon-scope": "system",
        },
    ]


def test_start_single_service(test_snap):
    """Test starting a single service."""
    response = wait_for(snap_http.start)("test-snap.hello-svc")
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    apps = sorted(after.result, key=lambda app: app["name"], reverse=True)
    assert apps[0]["name"] == "hello-svc"
    assert apps[0]["active"] is True
    assert "enabled" not in apps[0]
    assert apps[1]["name"] == "bye-svc"
    assert "active" not in apps[1]
    assert "enabled" not in apps[1]


def test_start_all_services_in_single_snap(test_snap):
    """Test starting all services in a single snap."""
    response = wait_for(snap_http.start)("test-snap")
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    apps = sorted(after.result, key=lambda app: app["name"], reverse=True)
    assert apps[0]["name"] == "hello-svc"
    assert apps[0]["active"] is True
    assert "enabled" not in apps[0]
    assert apps[1]["name"] == "bye-svc"
    assert apps[1]["active"] is True
    assert "enabled" not in apps[1]


def test_start_multiple_services(test_snap):
    """Test starting multiple services individually."""
    response = wait_for(snap_http.start_all)(
        ["test-snap.hello-svc", "test-snap.bye-svc"]
    )
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    apps = sorted(after.result, key=lambda app: app["name"], reverse=True)
    assert apps[0]["name"] == "hello-svc"
    assert apps[0]["active"] is True
    assert "enabled" not in apps[0]
    assert apps[1]["name"] == "bye-svc"
    assert apps[1]["active"] is True
    assert "enabled" not in apps[1]


def test_start_and_enable_service(test_snap):
    """Test starting and enabling a single service."""
    response = wait_for(snap_http.start)("test-snap.hello-svc", enable=True)
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    app = sorted(after.result, key=lambda app: app["name"], reverse=True)[0]
    assert app["name"] == "hello-svc"
    assert app["active"] is True
    assert app["enabled"] is True


def test_stop_single_service(test_snap):
    """Test stopping a single service."""
    wait_for(snap_http.start)("test-snap.hello-svc")

    response = wait_for(snap_http.stop)("test-snap.hello-svc")
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    app = sorted(after.result, key=lambda app: app["name"], reverse=True)[0]
    assert app["name"] == "hello-svc"
    assert "active" not in app
    assert "enabled" not in app


def test_stop_all_services_in_single_snap(test_snap):
    """Test stopping all services in a single snap."""
    wait_for(snap_http.start)("test-snap")

    response = wait_for(snap_http.stop)("test-snap")
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    apps = sorted(after.result, key=lambda app: app["name"], reverse=True)
    assert apps[0]["name"] == "hello-svc"
    assert "active" not in apps[0]
    assert "enabled" not in apps[0]
    assert apps[1]["name"] == "bye-svc"
    assert "active" not in apps[1]
    assert "enabled" not in apps[1]


def test_stop_multiple_services(test_snap):
    """Test stopping multiple services individually."""
    wait_for(snap_http.start)("test-snap")

    response = wait_for(snap_http.stop_all)(
        ["test-snap.hello-svc", "test-snap.bye-svc"]
    )
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    apps = sorted(after.result, key=lambda app: app["name"], reverse=True)
    assert apps[0]["name"] == "hello-svc"
    assert "active" not in apps[0]
    assert "enabled" not in apps[0]
    assert apps[1]["name"] == "bye-svc"
    assert "active" not in apps[1]
    assert "enabled" not in apps[1]


def test_stop_and_disable_service(test_snap):
    """Test stopping and disabling a single service."""
    wait_for(snap_http.start)("test-snap", enable=True)

    response = wait_for(snap_http.stop)("test-snap.hello-svc", disable=True)
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    apps = sorted(after.result, key=lambda app: app["name"], reverse=True)
    assert apps[0]["name"] == "hello-svc"
    assert "active" not in apps[0]
    assert "enabled" not in apps[0]
    assert apps[1]["name"] == "bye-svc"
    assert apps[1]["active"] is True
    assert apps[1]["enabled"] is True


def test_restart_single_service(test_snap):
    """Test restarting a single service."""
    wait_for(snap_http.start)("test-snap.hello-svc")

    response = wait_for(snap_http.restart)("test-snap.hello-svc")
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    app = sorted(after.result, key=lambda app: app["name"], reverse=True)[0]
    assert app["name"] == "hello-svc"
    assert app["active"] is True
    assert "enabled" not in app


def test_restart_all_services_in_single_snap(test_snap):
    """Test restarting all services in a single snap."""
    wait_for(snap_http.start)("test-snap")

    response = wait_for(snap_http.restart)("test-snap")
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    apps = sorted(after.result, key=lambda app: app["name"], reverse=True)
    assert apps[0]["name"] == "hello-svc"
    assert apps[0]["active"] is True
    assert "enabled" not in apps[0]
    assert apps[1]["name"] == "bye-svc"
    assert apps[1]["active"] is True
    assert "enabled" not in apps[1]


def test_restart_multiple_services(test_snap):
    """Test restarting multiple services individually."""
    wait_for(snap_http.start)("test-snap")

    response = wait_for(snap_http.restart_all)(
        ["test-snap.hello-svc", "test-snap.bye-svc"]
    )
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    apps = sorted(after.result, key=lambda app: app["name"], reverse=True)
    assert apps[0]["name"] == "hello-svc"
    assert apps[0]["active"] is True
    assert "enabled" not in apps[0]
    assert apps[1]["name"] == "bye-svc"
    assert apps[1]["active"] is True
    assert "enabled" not in apps[1]


def test_reload_service(test_snap):
    """Test reloading a single service."""
    wait_for(snap_http.start)("test-snap")

    response = wait_for(snap_http.restart)("test-snap.hello-svc", reload=True)
    assert response.status_code == 202

    after = snap_http.get_apps(names=["test-snap"], services_only=True)
    apps = sorted(after.result, key=lambda app: app["name"], reverse=True)
    assert apps[0]["name"] == "hello-svc"
    assert apps[0]["active"] is True
    assert "enabled" not in apps[0]
    assert apps[1]["name"] == "bye-svc"
    assert apps[1]["active"] is True
    assert "enabled" not in apps[1]
