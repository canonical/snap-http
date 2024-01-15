import pytest

import snap_http

from tests.utils import is_snap_installed, sideload_snap, wait_for

TEST_SNAPS = ["test-snap", "hello-world"]
LOCAL_TEST_SNAP_PATH = "tests/integration/test_snap/test-snap_perpetual_amd64.snap"


def pytest_configure():
    """Make sure the test environment is clean before running tests."""
    # remove test snaps if they exist
    installed = {snap["name"] for snap in snap_http.list().result}
    for snap in TEST_SNAPS:
        if snap in installed:
            wait_for(snap_http.remove)(snap)


@pytest.fixture(scope="function")
def test_snap():
    """Install the test snap."""
    yield sideload_snap(LOCAL_TEST_SNAP_PATH)

    # teardown
    if is_snap_installed("test-snap"):
        wait_for(snap_http.remove)("test-snap")
