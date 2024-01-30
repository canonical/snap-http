from typing import Dict

import pytest

import snap_http
from tests.utils import is_snap_installed, remove_assertion, wait_for

TEST_SNAPS = ["test-snap", "hello-world"]

HELLO_WORLD_SNAP_DECLARATION_ASSERTION = {
    "assertion_type": "snap-declaration",
    "snap_id": "buPKUD3TKqCOgLEjjHx5kSiCpIs5cMuQ",
    "series": "16",
}
TEST_ASSERTIONS = [HELLO_WORLD_SNAP_DECLARATION_ASSERTION]


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
    yield wait_for(snap_http.sideload)(
        file_paths=[local_test_snap_path],
        devmode=True,
    )

    # teardown
    if is_snap_installed("test-snap"):
        wait_for(snap_http.remove)("test-snap")


@pytest.fixture
def hello_world_snap_declaration_assertion() -> (str, Dict[str, str]):
    path = "tests/integration/assets/hello_world_snap_declaration.assert"
    with open(path, "r") as f:
        yield (f.read(), HELLO_WORLD_SNAP_DECLARATION_ASSERTION)

    # teardown
    remove_assertion(**HELLO_WORLD_SNAP_DECLARATION_ASSERTION)
