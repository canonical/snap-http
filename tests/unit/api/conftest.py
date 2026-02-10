import pytest


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Removes _make_request from snap_http.http to prevent inadvertent requests going out."""
    monkeypatch.delattr("snap_http.http._make_request")
