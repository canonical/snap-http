import snap_http

from tests.utils import get_snap_details, is_snap_installed, remove_assertion, wait_for


def test_list_snaps():
    """Test listing snaps."""
    installed_snaps = {snap["name"] for snap in snap_http.list().result}
    assert "snapd" in installed_snaps


def test_list_all_snaps():
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
