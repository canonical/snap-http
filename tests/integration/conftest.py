from typing import Dict

import pytest

import snap_http
from tests.utils import is_snap_installed, remove_assertion, wait_for

TEST_SNAPS = ["test-snap", "hello-world"]

HELLO_WORLD_SNAP_DECLARATION = {
    "assertion_type": "snap-declaration",
    "snap_id": "buPKUD3TKqCOgLEjjHx5kSiCpIs5cMuQ",
    "series": "16",
}
NETWORK_CONFDB_ACCOUNT_ID = "f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN"
NETWORK_CONFDB_SCHEMA = {
    "assertion_type": "confdb-schema",
    "account_id": NETWORK_CONFDB_ACCOUNT_ID,
    "name": "network",
}
TEST_ASSERTIONS = [
    HELLO_WORLD_SNAP_DECLARATION,
    NETWORK_CONFDB_SCHEMA,
]


def pytest_configure():
    """Make sure the test environment is clean before running tests."""
    # remove test snaps if they exist
    installed = {snap["name"] for snap in snap_http.list().result}
    for snap in TEST_SNAPS:
        if snap in installed:
            wait_for(snap_http.remove)(snap)

    # remove test assertions if they exist
    for assertion in TEST_ASSERTIONS:
        remove_assertion(**assertion)


@pytest.fixture
def local_test_snap_path():
    return "tests/integration/test_snap/test-snap_perpetual_amd64.snap"


@pytest.fixture
def local_hello_world_snap_path():
    return "tests/integration/test_snap/hello-world.snap"


@pytest.fixture
def test_snap(local_test_snap_path):
    """Install the test snap."""
    wait_for(snap_http.sideload)(file_paths=[local_test_snap_path], devmode=True)

    yield

    # teardown
    if is_snap_installed("test-snap"):
        wait_for(snap_http.remove)("test-snap")


@pytest.fixture
def hello_world_snap_declaration_assertion() -> (str, Dict[str, str]):
    path = "tests/integration/assets/hello_world_snap_declaration.assert"
    with open(path, "r") as f:
        yield (f.read(), HELLO_WORLD_SNAP_DECLARATION)

    # teardown
    remove_assertion(**HELLO_WORLD_SNAP_DECLARATION)


@pytest.fixture
def network_confdb_schema_assertion() -> (str, Dict[str, str]):
    path = "tests/integration/assets/network_confdb_schema.assert"
    with open(path, "r") as f:
        yield (f.read(), NETWORK_CONFDB_SCHEMA)

    # teardown
    remove_assertion(**NETWORK_CONFDB_SCHEMA)


@pytest.fixture
def network_confdb_setup(test_snap, network_confdb_schema_assertion):
    # Add confdb schema assertion & its prerequisite assertions
    for path in [
        "tests/integration/assets/st3v3nmw_account.assert",
        "tests/integration/assets/st3v3nmw_account_key_1.assert",
    ]:
        with open(path) as f:
            snap_http.add_assertion(f.read())

    assertion, _ = network_confdb_schema_assertion
    snap_http.add_assertion(assertion)

    # Enable confdb & confdb-control features
    wait_for(snap_http.set_conf)("system", {"experimental.confdb": True})
    wait_for(snap_http.set_conf)("system", {"experimental.confdb-control": True})

    # Connect custodian snap to confdb plugs
    wait_for(snap_http.connect_interface)(
        "core", "confdb", "test-snap", "network-proxy-admin"
    )
    wait_for(snap_http.connect_interface)(
        "core", "confdb", "test-snap", "network-proxy-state"
    )

    yield

    # teardown
    wait_for(snap_http.set_confdb)(
        NETWORK_CONFDB_ACCOUNT_ID,
        "network",
        "proxy-admin",
        {"http": None, "https": None, "ftp": None},
    )
