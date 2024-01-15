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


def test_get_conf(monkeypatch):
    """`api.get_conf` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path):
        assert path == "/snaps/placeholder/conf"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_conf("placeholder")

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
