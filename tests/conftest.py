import pytest

from tests.utils import call_and_await_api, is_snap_installed


def pytest_configure():
    """Make sure the test snap is not installed before running any tests."""
    if is_snap_installed("hello-world"):
        call_and_await_api("remove", "hello-world")


@pytest.fixture(scope="function")
def test_snap():
    yield call_and_await_api("install", "hello-world")

    # teardown
    if is_snap_installed("hello-world"):
        call_and_await_api("remove", "hello-world")
