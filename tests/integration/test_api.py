import snap_http

from tests.utils import call_and_await_api, is_snap_installed


# configuration: get and set snap options


def test_get_config(test_snap):
    response = snap_http.get_conf("hello-world")
    assert response.status_code == 200
    # the `hello-world` snap doesn't have any configuration options
    assert response.result == {}


# snaps: list and manage installed snaps


def test_list_snaps():
    installed_snaps = {snap["name"] for snap in snap_http.list().result}
    assert "snapd" in installed_snaps


def test_install_snap():
    assert is_snap_installed("hello-world") is False

    response = call_and_await_api("install", "hello-world")
    assert response.status_code == 202
    assert is_snap_installed("hello-world") is True

    call_and_await_api("remove", "hello-world")


def test_remove_snap(test_snap):
    assert is_snap_installed("hello-world") is True

    response = call_and_await_api("remove", "hello-world")
    assert response.status_code == 202
    assert is_snap_installed("hello-world") is False
