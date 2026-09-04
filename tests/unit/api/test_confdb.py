import json

import pytest

from snap_http import api, http, types
from snap_http.api.confdb import _validate_access_timeout


def test_get_confdb(monkeypatch):
    """`api.get_confdb` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_get(path, query_params):
        assert path == "/confdb/system/network/wifi-state"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_confdb("system", "network", "wifi-state")

    assert result == mock_response


def test_get_confdb_with_keys(monkeypatch):
    """`api.get_confdb` with keys parameter returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_get(path, query_params):
        assert path == "/confdb/system/network/wifi-state"
        assert query_params == {"keys": "ssid,status"}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_confdb(
        "system", "network", "wifi-state", keys=["ssid", "status"]
    )

    assert result == mock_response


def test_get_confdb_with_constraints(monkeypatch):
    """`api.get_confdb` with constraints parameter returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_get(path, query_params):
        assert path == "/confdb/system/network/wifi-state"
        assert query_params == {"constraints": json.dumps({"protocol": "https"})}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_confdb(
        "system", "network", "wifi-state", constraints={"protocol": "https"}
    )

    assert result == mock_response


def test_get_confdb_with_access_timeout(monkeypatch):
    """`api.get_confdb` with access_timeout parameter returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_get(path, query_params):
        assert path == "/confdb/system/network/wifi-state"
        assert query_params == {"access-timeout": "5s"}

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_confdb(
        "system", "network", "wifi-state", access_timeout="5s"
    )

    assert result == mock_response


def test_get_confdb_with_access_timeout_exceeding_max(monkeypatch):
    """`api.get_confdb` rejects an access_timeout over the 2h cap."""

    def mock_get(path, query_params):
        pytest.fail("should not have made an HTTP request")

    monkeypatch.setattr(http, "get", mock_get)

    with pytest.raises(ValueError):
        api.get_confdb("system", "network", "wifi-state", access_timeout="3h")


def test_set_confdb(monkeypatch):
    """`api.set_confdb` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_put(path, body):
        assert path == "/confdb/system/network/wifi-admin"
        assert body == {"values": {"ssid": "my-network", "password": None}}

        return mock_response

    monkeypatch.setattr(http, "put", mock_put)

    result = api.set_confdb(
        "system",
        "network",
        "wifi-admin",
        {"ssid": "my-network", "password": None},
    )

    assert result == mock_response


def test_set_confdb_with_access_timeout(monkeypatch):
    """`api.set_confdb` with access_timeout parameter returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="Accepted",
        result=None,
        change="1",
    )

    def mock_put(path, body):
        assert path == "/confdb/system/network/wifi-admin"
        assert body == {
            "values": {"ssid": "my-network"},
            "options": {"access-timeout": "15m6.7s"},
        }

        return mock_response

    monkeypatch.setattr(http, "put", mock_put)

    result = api.set_confdb(
        "system",
        "network",
        "wifi-admin",
        {"ssid": "my-network"},
        access_timeout="15m6.7s",
    )

    assert result == mock_response


def test_set_confdb_with_malformed_access_timeout(monkeypatch):
    """`api.set_confdb` rejects a malformed access_timeout."""

    def mock_put(path, body):
        pytest.fail("should not have made an HTTP request")

    monkeypatch.setattr(http, "put", mock_put)

    with pytest.raises(ValueError):
        api.set_confdb(
            "system",
            "network",
            "wifi-admin",
            {"ssid": "my-network"},
            access_timeout="abc",
        )


def test_delegate_confdb(monkeypatch):
    """`api.delegate_confdb` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=None,
    )

    def mock_post(path, body):
        assert path == "/confdb"
        assert body == {
            "action": "delegate",
            "operator-id": "alice",
            "authentications": ["operator-key", "store"],
            "views": ["bob/network/wifi-admin", "bob/network/wifi-state"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.delegate_confdb(
        "alice",
        authentications=["operator-key", "store"],
        views=["bob/network/wifi-admin", "bob/network/wifi-state"],
    )

    assert result == mock_response


def test_undelegate_confdb_all(monkeypatch):
    """`api.undelegate_confdb` withdraws all access."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=None,
    )

    def mock_post(path, body):
        assert path == "/confdb"
        assert body == {
            "action": "undelegate",
            "operator-id": "alice",
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.undelegate_confdb("alice")

    assert result == mock_response


def test_undelegate_confdb_partial(monkeypatch):
    """`api.undelegate_confdb` withdraws specific access."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result=None,
    )

    def mock_post(path, body):
        assert path == "/confdb"
        assert body == {
            "action": "undelegate",
            "operator-id": "alice",
            "authentications": ["store"],
            "views": ["bob/network/wifi-admin"],
        }

        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.undelegate_confdb(
        "alice",
        authentications=["store"],
        views=["bob/network/wifi-admin"],
    )

    assert result == mock_response


@pytest.mark.parametrize(
    "access_timeout",
    [
        "0",
        "+0",
        "-0",
        "0s",
        "0h0m0s",
        "5s",
        "500ms",
        "1ns",
        "1us",
        "1µs",  # U+00B5 MICRO SIGN
        "1μs",  # U+03BC GREEK SMALL LETTER MU
        "+5s",
        "5.s",
        ".5s",
        "1h.5s",
        "1h3m0.5s",
        "1h2m3s4ms5us6ns",
        "2h",  # exactly at the cap
        "120m",  # exactly at the cap, different unit
        "7200s",  # exactly at the cap, different unit
        "1h59m59.999s",
        "0.5h",
        "59m59s999ms",
    ],
)
def test_validate_access_timeout_accepts_valid_durations(access_timeout):
    """`_validate_access_timeout` accepts well-formed durations at or under the cap."""
    _validate_access_timeout(access_timeout)  # should not raise


@pytest.mark.parametrize(
    "access_timeout",
    [
        "",
        "abc",
        "5",
        "5x",
        "5S",  # wrong case
        "5s\n",  # trailing newline
        "5s ",  # trailing space
        " 5s",  # leading space
        "5 s",  # internal space
        "00",  # bare zero requires exactly "0"
        "0.0",  # same
        ".s",  # no digits on either side of the decimal point
        "s",  # unit with no number
        "5ss",  # doubled unit suffix
        "5.5.5s",  # multiple decimal points
        "++5s",  # doubled sign
        "+-5s",  # conflicting sign
        "5d",  # unsupported unit (days)
        "5w",  # unsupported unit (weeks)
        "5y",  # unsupported unit (years)
        "٥s",  # Unicode (Arabic-Indic) digit, not ASCII
        "-5s",  # negative duration
        "-1h",  # negative duration
        "3h",  # over the cap
        "2h0m0.001s",  # just over the cap
        "7201s",  # over the cap, different unit
        "121m",  # over the cap, different unit
        "2540400h10m10.000000000s",  # wildly over the cap
    ],
)
def test_validate_access_timeout_rejects_invalid_durations(access_timeout):
    """`_validate_access_timeout` rejects malformed, negative, or over-cap durations."""
    with pytest.raises(ValueError):
        _validate_access_timeout(access_timeout)
