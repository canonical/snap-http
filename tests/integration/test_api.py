import snap_http

from tests.utils import (
    assertion_exists,
    get_snap_details,
    is_snap_installed,
    is_snap_purged,
    remove_assertion,
    wait_for,
)


# configuration: get and set snap options


def test_get_config(test_snap):
    """Test getting snap configuration."""
    response = snap_http.get_conf("test-snap")
    assert response.status_code == 200
    assert response.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }


def test_get_specific_config_value(test_snap):
    """Test getting specific snap configuration."""
    response = snap_http.get_conf("test-snap", keys=["port"])
    assert response.status_code == 200
    assert response.result == {"port": 8080}


def test_get_nested_config_value(test_snap):
    """Test getting a specific nested snap configuration."""
    response = snap_http.get_conf("test-snap", keys=["foo.bar"])
    assert response.status_code == 200
    assert response.result == {"foo.bar": "default"}


def test_set_config(test_snap):
    """Test setting snap configuration."""
    before = snap_http.get_conf("test-snap")
    assert before.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }

    response = wait_for(snap_http.set_conf)(
        "test-snap",
        {
            "foo": {"bar": "qux", "baz": "quux"},
            "port": 8080,
        },
    )
    assert response.status_code == 202

    after = snap_http.get_conf("test-snap")
    assert after.result == {
        "foo": {"bar": "qux", "baz": "quux"},
        "port": 8080,
    }


def test_set_specific_config_value(test_snap):
    """Test setting specific snap configuration."""
    before = snap_http.get_conf("test-snap")
    assert before.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }

    response = wait_for(snap_http.set_conf)(
        "test-snap",
        {"port": 443, "foo.baz": "lambda"},
    )
    assert response.status_code == 202

    after = snap_http.get_conf("test-snap")
    assert after.result == {
        "foo": {"bar": "default", "baz": "lambda"},
        "port": 443,
    }


def test_set_config_with_invalid_key(test_snap):
    """Test setting config with an invalid key."""
    before = snap_http.get_conf("test-snap")
    assert before.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }

    response = wait_for(snap_http.set_conf)("test-snap", {"foo /bar": 80})
    assert response.status_code == 202

    change = snap_http.check_change(response.change).result
    assert change["status"] == "Error"
    assert 'invalid option name: "foo /bar"' in change["err"]

    # confirm settings haven't changed
    after = snap_http.get_conf("test-snap")
    assert after.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }


def test_unset_config_value(test_snap):
    """Test unsetting snap configuration."""
    before = snap_http.get_conf("test-snap")
    assert before.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }

    response = wait_for(snap_http.set_conf)(
        "test-snap",
        {"foo.bar": "meta"},
    )
    assert response.status_code == 202

    after = snap_http.get_conf("test-snap", keys=["foo.bar"])
    assert after.result == {"foo.bar": "meta"}

    response = wait_for(snap_http.set_conf)(
        "test-snap",
        {"foo.bar": None},
    )
    assert response.status_code == 202

    after_unset = snap_http.get_conf("test-snap", keys=["foo.bar"])
    assert after_unset.result == {"foo.bar": "default"}


# snaps: list and manage installed snaps


def test_list_snaps():
    """Test listing snaps."""
    installed_snaps = {snap["name"] for snap in snap_http.list().result}
    assert "snapd" in installed_snaps


def test_list__all_snaps():
    """Test listing snaps."""
    installed_snaps = {snap["name"] for snap in snap_http.list_all().result}
    assert "snapd" in installed_snaps


def test_install_snap_from_the_store(hello_world_snap_declaration_assertion):
    """Test installing a snap from the store."""
    assert is_snap_installed("hello-world") is False

    response = wait_for(snap_http.install)("hello-world")
    assert response.status_code == 202
    assert is_snap_installed("hello-world") is True

    wait_for(snap_http.remove)("hello-world")
    remove_assertion(**hello_world_snap_declaration_assertion[1])


def test_remove_snap(test_snap):
    """Test removing a snap."""
    assert is_snap_installed("test-snap") is True

    response = wait_for(snap_http.remove)("test-snap")
    assert response.status_code == 202
    assert is_snap_installed("test-snap") is False


def test_purge_snap(test_snap):
    """Test removing a snap."""
    assert is_snap_installed("test-snap") is True

    response = wait_for(snap_http.purge)("test-snap")
    assert response.status_code == 202
    assert is_snap_purged("test-snap") is True


def test_sideload_snap_no_flags(
    local_hello_world_snap_path,
    hello_world_snap_declaration_assertion,
):
    """Test sideloading a snap with no flags specified."""
    assert is_snap_installed("hello-world") is False

    # ack the assertion
    snap_http.add_assertion(hello_world_snap_declaration_assertion[0])
    # sideload
    response = wait_for(snap_http.sideload)(
        file_paths=[local_hello_world_snap_path],
    )
    assert response.status_code == 202

    snap = get_snap_details("hello-world")
    assert snap["status"] == "active"
    assert snap["confinement"] == "strict"
    assert snap["devmode"] is False
    assert snap["jailmode"] is False

    wait_for(snap_http.remove)("hello-world")


def test_sideload_snap_in_devmode_confinement(local_test_snap_path):
    """Test sideloading a snap in devmode confinement."""
    assert is_snap_installed("test-snap") is False

    response = wait_for(snap_http.sideload)(
        file_paths=[local_test_snap_path],
        devmode=True,
    )
    assert response.status_code == 202

    snap = get_snap_details("test-snap")
    assert snap["status"] == "active"
    assert snap["confinement"] == "devmode"
    assert snap["devmode"] is True
    assert snap["jailmode"] is False

    wait_for(snap_http.remove)("test-snap")


def test_sideload_dangerous_snap(local_hello_world_snap_path):
    """Test sideloading a snap in dangerous mode."""
    assert is_snap_installed("hello-world") is False

    response = wait_for(snap_http.sideload)(
        file_paths=[local_hello_world_snap_path],
        dangerous=True,
    )
    assert response.status_code == 202

    snap = get_snap_details("hello-world")
    assert snap["status"] == "active"
    assert snap["confinement"] == "strict"
    assert snap["devmode"] is False
    assert snap["jailmode"] is False

    wait_for(snap_http.remove)("hello-world")


def test_sideload_snap_with_enforced_confinement(
    local_hello_world_snap_path,
    hello_world_snap_declaration_assertion,
):
    """Test sideloading a snap with enforced confinement."""
    assert is_snap_installed("hello-world") is False

    # ack the assertion
    snap_http.add_assertion(hello_world_snap_declaration_assertion[0])
    # sideload
    response = wait_for(snap_http.sideload)(
        file_paths=[local_hello_world_snap_path],
        jailmode=True,
    )
    assert response.status_code == 202

    snap = get_snap_details("hello-world")
    assert snap["status"] == "active"
    assert snap["confinement"] == "strict"
    assert snap["devmode"] is False
    assert snap["jailmode"] is True

    wait_for(snap_http.remove)("hello-world")


def test_sideload_multiple_snaps(
    local_test_snap_path,
    local_hello_world_snap_path,
    hello_world_snap_declaration_assertion,
):
    """Test sideloading multiple snaps."""
    assert is_snap_installed("test-snap") is False
    assert is_snap_installed("hello-world") is False

    # ack the assertion
    snap_http.add_assertion(hello_world_snap_declaration_assertion[0])
    # sideload
    response = wait_for(snap_http.sideload)(
        file_paths=[local_test_snap_path, local_hello_world_snap_path],
        devmode=True,
    )
    assert response.status_code == 202

    assert is_snap_installed("test-snap") is True
    assert is_snap_installed("hello-world") is True

    wait_for(snap_http.remove_all)(["test-snap", "hello-world"])


# Assertions: list and add assertions


def test_get_assertion_types():
    """Test getting assertion types."""
    response = snap_http.get_assertion_types()
    assert response.status_code == 200
    types = response.result["types"]
    assert len(types) > 0
    assert "account" in types
    assert "model" in types
    assert "snap-declaration" in types
    assert "store" in types


def test_get_assertions():
    """Test getting assertions."""
    response = snap_http.get_assertions("snap-declaration")
    assert response.status_code == 200
    assert len(response.result) > 0
    assert b"type: snap-declaration" in response.result


def test_get_assertions_with_filters(hello_world_snap_declaration_assertion):
    """Test getting assertions with filters."""
    assertion, metadata = hello_world_snap_declaration_assertion

    before = snap_http.get_assertions(
        "snap-declaration", filters={"snap-id": metadata["snap_id"]}
    )
    assert before.result == b""

    response = snap_http.add_assertion(assertion)
    assert response.status_code == 200

    after = snap_http.get_assertions(
        "snap-declaration",
        filters={"snap-id": metadata["snap_id"], "series": metadata["series"]},
    )
    assert after.result.decode() == assertion


def test_add_an_assertion(hello_world_snap_declaration_assertion):
    """Test adding an assertion."""
    assertion, metadata = hello_world_snap_declaration_assertion
    assert assertion_exists(**metadata) is False

    response = snap_http.add_assertion(assertion)
    assert response.status_code == 200
    assert assertion_exists(**metadata) is True


# Apps and Services


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
