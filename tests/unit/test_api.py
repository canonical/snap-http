import tempfile

import pytest

from snap_http import api, http, types


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Removes _make_request from snap_http.http to prevent inadvertent requests going out."""
    monkeypatch.delattr("snap_http.http._make_request")


def test_check_change(monkeypatch):
    """`api.check_change` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={
            "id": "1",
            "kind": "install-snap",
            "summary": 'Install "placeholder" snap',
            "status": "Done",
        },
    )

    def mock_get(path):
        assert path == "/changes/1"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.check_change("1")

    assert result == mock_response


def test_check_change_exception(monkeypatch):
    """`api.check_change` raises a `http.SnapdHttpException`."""

    def mock_get(path):
        assert path == "/changes/1"

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "get", mock_get)

    with pytest.raises(http.SnapdHttpException):
        _ = api.check_change("1")


def test_check_changes(monkeypatch):
    """`api.check_changes` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={
            "id": "1",
            "kind": "install-snap",
            "summary": 'Install "placeholder" snap',
            "status": "Done",
        },
    )

    def mock_get(path):
        assert path == "/changes?select=all"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.check_changes()

    assert result == mock_response


def test_check_changes_exception(monkeypatch):
    """`api.check_changes` raises a `http.SnapdHttpException`."""

    def mock_get(path):
        assert path == "/changes?select=all"

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "get", mock_get)

    with pytest.raises(http.SnapdHttpException):
        _ = api.check_changes()


def test_enable(monkeypatch):
    """`api.enable` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "enable"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.enable("placeholder")

    assert result == mock_response


def test_enable_exception(monkeypatch):
    """`api.enable` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "enable"}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.enable("placeholder")


def test_enable_all_exception(monkeypatch):
    """`api.enable_all` raises a `http.SnapdHttpException`.

    NOTE: as of 2024-01-08, enable/disable is not yet supported for multiple snaps.
    """

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "enable", "snaps": ["placeholder1", "placeholder2"]}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.enable_all(["placeholder1", "placeholder2"])


def test_disable(monkeypatch):
    """`api.disable` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "disable"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.disable("placeholder")

    assert result == mock_response


def test_disable_exception(monkeypatch):
    """`api.disable` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "disable"}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.disable("placeholder")


def test_disable_all_exception(monkeypatch):
    """`api.enable_all` raises a `http.SnapdHttpException`.

    NOTE: as of 2024-01-08, enable/disable is not yet supported for multiple snaps.
    """

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "disable", "snaps": ["placeholder1", "placeholder2"]}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.disable_all(["placeholder1", "placeholder2"])


def test_hold(monkeypatch):
    """`api.hold` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "hold", "hold-level": "general", "time": "forever"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.hold("placeholder")

    assert result == mock_response


def test_hold_exception(monkeypatch):
    """`api.hold` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "hold", "hold-level": "general", "time": "forever"}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.hold("placeholder")


def test_hold_all(monkeypatch):
    """`api.hold_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {
            "action": "hold",
            "snaps": ["placeholder1", "placeholder2"],
            "hold-level": "general",
            "time": "forever",
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.hold_all(["placeholder1", "placeholder2"])

    assert result == mock_response


def test_hold_all_exception(monkeypatch):
    """`api.hold_all` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {
            "action": "hold",
            "snaps": ["placeholder1", "placeholder2"],
            "hold-level": "general",
            "time": "forever",
        }

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.hold_all(["placeholder1", "placeholder2"])


def test_install(monkeypatch):
    """`api.install` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "install"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.install("placeholder")

    assert result == mock_response


def test_install_revision(monkeypatch):
    """`api.install` returns a `types.SnapdResponse` when provided a specific revision to install."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "install", "revision": "1"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.install("placeholder", revision="1")

    assert result == mock_response


def test_install_channel(monkeypatch):
    """`api.install` returns a `types.SnapdResponse` when provided a specific channel to install from."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "install", "channel": "latest/beta"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.install("placeholder", channel="latest/beta")

    assert result == mock_response


def test_install_classic(monkeypatch):
    """`api.install` returns a `types.SnapdResponse` when installing with classic confinement."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "install", "classic": True}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.install("placeholder", classic=True)

    assert result == mock_response


def test_install_exception(monkeypatch):
    """`api.install` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "install"}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.install("placeholder")


def test_install_all(monkeypatch):
    """`api.install_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "install", "snaps": ["placeholder1", "placeholder2"]}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.install_all(["placeholder1", "placeholder2"])

    assert result == mock_response


def test_install_all_exception(monkeypatch):
    """`api.install_all` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "install", "snaps": ["placeholder1", "placeholder2"]}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.install_all(["placeholder1", "placeholder2"])


def test_sideload_snap(monkeypatch):
    """`api.sideload` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body: types.FormData):
        assert path == "/snaps"
        assert body.data == {"action": "install"}
        assert len(body.files) == 1

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    with tempfile.NamedTemporaryFile() as tmp:
        result = api.sideload([tmp.name])

    assert result == mock_response


def test_sideload_with_classic_confinement(monkeypatch):
    """`api.sideload` returns a `types.SnapdResponse` when sideloading with classic confinement."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body: types.FormData):
        assert path == "/snaps"
        assert body.data == {"action": "install", "classic": True}
        assert len(body.files) == 1

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    with tempfile.NamedTemporaryFile() as tmp:
        result = api.sideload([tmp.name], classic=True)

    assert result == mock_response


def test_sideload_dangerous_snap(monkeypatch):
    """`api.sideload` returns a `types.SnapdResponse` when sideloading in dangerous mode."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body: types.FormData):
        assert path == "/snaps"
        assert body.data == {"action": "install", "dangerous": True}
        assert len(body.files) == 1

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    with tempfile.NamedTemporaryFile() as tmp:
        result = api.sideload([tmp.name], dangerous=True)

    assert result == mock_response


def test_sideload_snap_with_devmode_confinement(monkeypatch):
    """`api.sideload` returns a `types.SnapdResponse` when sideloading in devmode confinement."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body: types.FormData):
        assert path == "/snaps"
        assert body.data == {"action": "install", "devmode": True}
        assert len(body.files) == 1

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    with tempfile.NamedTemporaryFile() as tmp:
        result = api.sideload([tmp.name], devmode=True)

    assert result == mock_response


def test_sideload_snap_with_enforced_confinement(monkeypatch):
    """`api.sideload` returns a `types.SnapdResponse` when sideloading with enforced confinement."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body: types.FormData):
        assert path == "/snaps"
        assert body.data == {"action": "install", "jailmode": True}
        assert len(body.files) == 1

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    with tempfile.NamedTemporaryFile() as tmp:
        result = api.sideload([tmp.name], jailmode=True)

    assert result == mock_response


def test_sideload_snap_restart_system(monkeypatch):
    """`api.sideload` returns a `types.SnapdResponse` when a system restart is required."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body: types.FormData):
        assert path == "/snaps"
        assert body.data == {"action": "install", "system-restart-immediate": True}
        assert len(body.files) == 1

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    with tempfile.NamedTemporaryFile() as tmp:
        result = api.sideload([tmp.name], system_restart_immediate=True)

    assert result == mock_response


def test_sideload_multiple_snaps(monkeypatch):
    """`api.sideload` returns a `types.SnapdResponse` when sideloading multiple snaps."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body: types.FormData):
        assert path == "/snaps"
        assert body.data == {"action": "install"}
        assert len(body.files) == 2

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    with tempfile.NamedTemporaryFile() as tmp1, tempfile.NamedTemporaryFile() as tmp2:
        result = api.sideload([tmp1.name, tmp2.name])

    assert result == mock_response


def test_sideload_snap_exception(monkeypatch):
    """`api.sideload` raises a `http.SnapHttpException`."""

    def mock_post(path, body: types.FormData):
        assert path == "/snaps"
        assert body.data == {"action": "install"}
        assert len(body.files) == 1

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with tempfile.NamedTemporaryFile() as tmp, pytest.raises(http.SnapdHttpException):
        api.sideload([tmp.name])


def test_revert(monkeypatch):
    """`api.revert` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "revert"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.revert("placeholder")

    assert result == mock_response


def test_revert_revision(monkeypatch):
    """`api.revert` returns a `types.SnapdResponse` when given a specific revision."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "revert", "revision": "1"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.revert("placeholder", revision="1")

    assert result == mock_response


def test_revert_classic(monkeypatch):
    """`api.revert` returns a `types.SnapdResponse` when reverting to classic confinement."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "revert", "classic": True}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.revert("placeholder", classic=True)

    assert result == mock_response


def test_revert_exception(monkeypatch):
    """`api.revert` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "revert"}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.revert("placeholder")


def test_revert_all(monkeypatch):
    """`api.revert_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "revert", "snaps": ["placeholder1", "placeholder2"]}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.revert_all(["placeholder1", "placeholder2"])

    assert result == mock_response


def test_revert_all_exception(monkeypatch):
    """`api.revert_all` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "revert", "snaps": ["placeholder1", "placeholder2"]}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.revert_all(["placeholder1", "placeholder2"])


def test_remove(monkeypatch):
    """`api.remove` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "remove"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.remove("placeholder")

    assert result == mock_response


def test_remove_exception(monkeypatch):
    """`api.remove` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "remove"}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.remove("placeholder")


def test_remove_all(monkeypatch):
    """`api.remove_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "remove", "snaps": ["placeholder1", "placeholder2"]}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.remove_all(["placeholder1", "placeholder2"])

    assert result == mock_response


def test_remove_all_exception(monkeypatch):
    """`api.remove_all` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "remove", "snaps": ["placeholder1", "placeholder2"]}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.remove_all(["placeholder1", "placeholder2"])


def test_snapshots(monkeypatch):
    """`api.snapshots` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=None,
    )

    def mock_post(path):
        assert path == "/snapshots"

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.snapshots()

    assert result == mock_response


def test_switch(monkeypatch):
    """`api.switch` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "switch", "channel": "stable"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.switch("placeholder")

    assert result == mock_response


def test_switch_exception(monkeypatch):
    """`api.switch` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "switch", "channel": "stable"}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.switch("placeholder")


def test_switch_all_exception(monkeypatch):
    """`api.revert_all` raises a `http.SnapdHttpException`.

    NOTE: as of 2024-01-08, switch is not yet supported for multiple snaps.
    """

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {
            "action": "switch",
            "channel": "stable",
            "snaps": ["placeholder1", "placeholder2"],
        }

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.switch_all(["placeholder1", "placeholder2"])


def test_unhold(monkeypatch):
    """`api.unhold` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "unhold"}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.unhold("placeholder")

    assert result == mock_response


def test_unhold_exception(monkeypatch):
    """`api.unhold` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps/placeholder"
        assert body == {"action": "unhold"}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.unhold("placeholder")


def test_unhold_all(monkeypatch):
    """`api.unhold_all` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "unhold", "snaps": ["placeholder1", "placeholder2"]}

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.unhold_all(["placeholder1", "placeholder2"])

    assert result == mock_response


def test_unhold_all_exception(monkeypatch):
    """`api.revert_all` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {"action": "unhold", "snaps": ["placeholder1", "placeholder2"]}

        raise http.SnapdHttpException()

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        _ = api.unhold_all(["placeholder1", "placeholder2"])


def test_list(monkeypatch):
    """`api.list` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[{"title": "placeholder1"}, {"title": "placeholder2"}],
    )

    def mock_get(path):
        assert path == "/snaps"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.list()

    assert result == mock_response


def test_list_all(monkeypatch):
    """`api.list` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[{"title": "placeholder1"}, {"title": "placeholder2"}],
    )

    def mock_get(path):
        assert path == "/snaps?select=all"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.list_all()

    assert result == mock_response


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

def test_get_model(monkeypatch) -> None:
    """`api.get_model` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path):
        assert path == "/model"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_model()

    assert result == mock_response

def test_remodel(monkeypatch):
    """`api.remodel` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    def mock_post(path, body):
        assert path == "/model"
        assert body == {"new-model": "dummy_model_assertion", "offline" : True}
        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.remodel("dummy_model_assertion", True)

    assert result == mock_response


def test_get_validation_sets(monkeypatch) -> None:
    """`api.get_validation_sets` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path):
        assert path == "/validation-sets"
        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_validation_sets()

    assert result == mock_response


def test_get_validation_set(monkeypatch) -> None:
    """`api.get_validation_set` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    account_id: str = "device-platform"
    validation_set_name: str = "dev-validation-set"
    def mock_get(path):
        assert path == f"/validation-sets/{account_id}/{validation_set_name}"
        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_validation_set(account_id, validation_set_name)

    assert result == mock_response

def test_refresh_validation_set(monkeypatch) -> None:
    """`api.refresh_validation_set` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    account_id: str = "device-platform"
    validation_set_name: str = "dev-validation-set"
    validation_set_sequence: int = 12
    def mock_post(path, body):
        assert path == "/snaps"
        assert body == {
                "action": "refresh",
                "validation-sets": [
                    f"{account_id}/{validation_set_name}={validation_set_sequence}"
                    ],
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.refresh_validation_set(account_id, validation_set_name, validation_set_sequence)

    assert result == mock_response


def test_get_recovery_systems(monkeypatch) -> None:
    """`api.get_recovery_systems` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path):
        assert path == "/systems"
        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_recovery_systems()

    assert result == mock_response


def test_perform_system_action(monkeypatch) -> None:
    """`api.perform_system_action` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    action: str = "do"
    mode: str = "recover"
    def mock_post(path, body):
        assert path == "/systems"
        assert body == {
                "action": action,
                "mode": mode
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.perform_system_action(action, mode)

    assert result == mock_response

def test_perform_recovery_action(monkeypatch) -> None:
    """`api.perform_recovery_action` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    action: str = "do"
    mode: str = "recover"
    label: str = "20250410"
    def mock_post(path, body):
        assert path == f"/systems/{label}"
        assert body == {
                "action": action,
                "mode": mode
                }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.perform_recovery_action(label, action, mode)

    assert result == mock_response



def test_get_assertion_types(monkeypatch):
    """`api.get_assertion_types` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={
            "types": ["account", "base-declaration", "serial", "system-user"],
        },
    )

    def mock_get(path):
        assert path == "/assertions"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_assertion_types()
    assert result == mock_response


def test_get_assertions(monkeypatch):
    """`api.get_assertions` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=(
            "assertion-header0: value0\n\nsignature0\n\n"
            "assertion-header: value\nassertion-header1: value1\n\nsignature"
        ).encode(),
    )

    def mock_get(path, query_params):
        assert path == "/assertions/serial-request"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_assertions("serial-request")
    assert result == mock_response


def test_get_assertions_with_filters(monkeypatch):
    """`api.get_assertions` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=b"assertion-header0: value0\n\nsignature0",
    )

    def mock_get(path, query_params):
        assert path == "/assertions/serial-request"
        assert query_params == {"assertion-header0": "value0"}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_assertions(
        "serial-request", filters={"assertion-header0": "value0"}
    )
    assert result == mock_response


def test_add_assertion(monkeypatch):
    """`api.add_assertion` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=None,
    )

    def mock_post(path, assertion):
        assert path == "/assertions"

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.add_assertion("assertion-header0: value0\n\nsignature0")
    assert result == mock_response


def test_add_assertion_exception(monkeypatch):
    """`api.add_assertion` raises a `http.SnapdHttpException`."""

    def mock_post(path, assertion):
        assert path == "/assertions"

        raise http.SnapdHttpException(
            {"message": "cannot decode request body into assertions: unexpected EOF"}
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.add_assertion("not an assertion")


def test_list_users(monkeypatch):
    """`api.list_users` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[{"id": 1, "username": "john", "email": "john.doe@example.com"}],
    )

    def mock_get(path):
        assert path == "/users"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.list_users()
    assert result == mock_response


def test_add_user(monkeypatch):
    """`api.add_user` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=[
            {
                "username": "john-doe",
                "ssh-keys": [
                    "ssh-ed25519 some-ssh-key john@localhost # "
                    'snapd {"origin":"store","email":"john.doe@example.com"}'
                ],
            }
        ],
    )

    def mock_post(path, body):
        assert path == "/users"

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.add_user(
        username="john-doe", email="john.doe@example.com", force_managed=True
    )
    assert result == mock_response


def test_add_user_exception(monkeypatch):
    """`api.add_user` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/users"

        raise http.SnapdHttpException(
            {"message": "cannot create user: device already managed"}
        )

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.add_user(username="john-doe", email="john.doe@example.com")


def test_remove_user(monkeypatch):
    """`api.remove_user` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={
            "removed": [
                {"id": 4, "username": "john-doe", "email": "john.doe@example.com"}
            ]
        },
    )

    def mock_post(path, body):
        assert path == "/users"

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.remove_user(username="john-doe")
    assert result == mock_response


def test_remove_user_exception(monkeypatch):
    """`api.remove_user` raises a `http.SnapdHttpException`."""

    def mock_post(path, body):
        assert path == "/users"

        raise http.SnapdHttpException({"message": 'user "jane-doe" is not known'})

    monkeypatch.setattr(http, "post", mock_post)

    with pytest.raises(http.SnapdHttpException):
        api.remove_user(username="jane-doe")


# Apps and Services


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
