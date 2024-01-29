import snap_http

from tests.utils import get_snap_details, is_snap_installed, wait_for


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


def test_install_snap_from_the_store():
    """Test installing a snap from the store."""
    assert is_snap_installed("hello-world") is False

    response = wait_for(snap_http.install)("hello-world")
    assert response.status_code == 202
    assert is_snap_installed("hello-world") is True

    wait_for(snap_http.remove)("hello-world")


def test_remove_snap(test_snap):
    """Test removing a snap."""
    assert is_snap_installed("test-snap") is True

    response = wait_for(snap_http.remove)("test-snap")
    assert response.status_code == 202
    assert is_snap_installed("test-snap") is False


def test_sideload_snap_no_flags(local_hello_world_snap_path):
    """Test sideloading a snap with no flags specified."""
    assert is_snap_installed("hello-world") is False

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


def test_sideload_snap_with_enforced_confinement(local_hello_world_snap_path):
    """Test sideloading a snap with enforced confinement."""
    assert is_snap_installed("hello-world") is False

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
):
    """Test sideloading multiple snaps."""
    assert is_snap_installed("test-snap") is False
    assert is_snap_installed("hello-world") is False

    response = wait_for(snap_http.sideload)(
        file_paths=[local_test_snap_path, local_hello_world_snap_path],
        devmode=True,
    )
    assert response.status_code == 202

    assert is_snap_installed("test-snap") is True
    assert is_snap_installed("hello-world") is True

    wait_for(snap_http.remove_all)(["test-snap", "hello-world"])
