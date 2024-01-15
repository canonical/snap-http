import snap_http

from tests.utils import wait_for, is_snap_installed


# configuration: get and set snap options


def test_get_config(test_snap):
    """Test getting snap configuration."""
    response = snap_http.get_conf("test-snap")
    assert response.status_code == 200
    assert response.result == {"foo": {"bar": "default", "baz": "default"}}


def test_set_config(test_snap):
    """Test setting snap configuration."""
    before = snap_http.get_conf("test-snap")
    assert before.result == {"foo": {"bar": "default", "baz": "default"}}

    response = wait_for(snap_http.set_conf)(
        "test-snap", {"foo": {"bar": "qux", "baz": "quux"}}
    )
    assert response.status_code == 202

    after = snap_http.get_conf("test-snap")
    assert after.result == {"foo": {"bar": "qux", "baz": "quux"}}


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
