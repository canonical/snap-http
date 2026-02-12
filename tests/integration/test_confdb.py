import snap_http

from tests.integration.conftest import NETWORK_CONFDB_ACCOUNT_ID
from tests.utils import parse_assertion, wait_for


def test_set_confdb(network_confdb_setup):
    """Test setting confdb values."""
    response = wait_for(snap_http.set_confdb)(
        NETWORK_CONFDB_ACCOUNT_ID,
        "network",
        "proxy-admin",
        {
            "ftp.url": "ftp://proxy.example.com",
            "ftp.bypass": ["*.company.internal"],
        },
    )
    assert response.status_code == 202

    change = snap_http.check_change(response.change)
    assert change.result["status"] == "Done"


def test_get_confdb(network_confdb_setup):
    """Test getting confdb values."""
    wait_for(snap_http.set_confdb)(
        NETWORK_CONFDB_ACCOUNT_ID,
        "network",
        "proxy-admin",
        {"https.url": "https://proxy.example.com", "https.bypass": ["localhost"]},
    )

    response = wait_for(snap_http.get_confdb)(
        NETWORK_CONFDB_ACCOUNT_ID, "network", "proxy-state"
    )
    assert response.status_code == 202

    change = snap_http.check_change(response.change)
    assert change.result["status"] == "Done"

    values = change.result["data"]["values"]
    assert values["https"]["url"] == "https://proxy.example.com"
    assert values["https"]["bypass"] == ["localhost"]


def test_get_confdb_with_keys(network_confdb_setup):
    """Test getting specific confdb values with keys parameter."""
    wait_for(snap_http.set_confdb)(
        NETWORK_CONFDB_ACCOUNT_ID,
        "network",
        "proxy-admin",
        {
            "https.url": "https://proxy.example.com",
            "ftp.url": "ftp://proxy.example.com",
        },
    )

    response = wait_for(snap_http.get_confdb)(
        NETWORK_CONFDB_ACCOUNT_ID,
        "network",
        "proxy-state",
        keys=["https"],
    )
    assert response.status_code == 202

    change = snap_http.check_change(response.change)
    values = change.result["data"]["values"]
    assert "https" in values
    assert "ftp" not in values


def test_unset_confdb(network_confdb_setup):
    """Test unsetting a confdb value by setting it to None."""
    wait_for(snap_http.set_confdb)(
        NETWORK_CONFDB_ACCOUNT_ID,
        "network",
        "proxy-admin",
        {
            "https.url": "https://proxy.example.com",
            "ftp.url": "ftp://proxy.example.com",
        },
    )

    wait_for(snap_http.set_confdb)(
        NETWORK_CONFDB_ACCOUNT_ID,
        "network",
        "proxy-admin",
        {"https": None},
    )

    response = wait_for(snap_http.get_confdb)(NETWORK_CONFDB_ACCOUNT_ID, "network", "proxy-state")
    values = snap_http.check_change(response.change).result["data"]["values"]
    assert "https" not in values
    assert "ftp" in values


def test_delegate_confdb(network_confdb_setup):
    """Test delegating confdb access to an operator."""
    response = snap_http.delegate_confdb(
        "alice",
        authentications=["operator-key", "store"],
        views=[
            f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-admin",
            f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-state",
        ],
    )
    assert response.status_code == 200

    assertion = parse_assertion(snap_http.get_assertions("confdb-control").result)
    groups = assertion["groups"]
    assert len(groups) == 1
    assert groups[0]["operators"] == ["alice"]
    assert groups[0]["authentications"] == ["operator-key", "store"]
    assert groups[0]["views"] == [
        f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-admin",
        f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-state",
    ]


def test_undelegate_confdb(network_confdb_setup):
    """Test withdrawing confdb access from an operator."""
    snap_http.delegate_confdb(
        "alice",
        authentications=["operator-key"],
        views=[f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-admin"],
    )

    response = snap_http.undelegate_confdb("alice")
    assert response.status_code == 200

    raw = snap_http.get_assertions("confdb-control").result
    assert b"alice" not in raw

    assertion = parse_assertion(raw)
    assert "groups" not in assertion


def test_undelegate_confdb_partial(network_confdb_setup):
    """Test withdrawing specific confdb access from an operator."""
    snap_http.delegate_confdb(
        "alice",
        authentications=["operator-key", "store"],
        views=[
            f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-admin",
            f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-state",
        ],
    )

    response = snap_http.undelegate_confdb(
        "alice",
        authentications=["store"],
        views=[f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-admin"],
    )
    assert response.status_code == 200

    assertion = parse_assertion(snap_http.get_assertions("confdb-control").result)
    groups = assertion["groups"]
    assert len(groups) == 2

    assert groups[0]["operators"] == ["alice"]
    assert groups[0]["authentications"] == ["operator-key"]
    assert groups[0]["views"] == [
        f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-admin",
    ]

    assert groups[1]["operators"] == ["alice"]
    assert groups[1]["authentications"] == ["operator-key", "store"]
    assert groups[1]["views"] == [
        f"{NETWORK_CONFDB_ACCOUNT_ID}/network/proxy-state",
    ]
