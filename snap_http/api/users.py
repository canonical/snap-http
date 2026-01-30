from .. import http
from ..types import SnapdResponse


def list_users() -> SnapdResponse:
    """Get information on user accounts."""
    return http.get("/users")


def add_user(
    username: str,
    email: str,
    sudoer: bool = False,
    known: bool = False,
    force_managed: bool = False,
    automatic: bool = False,
) -> SnapdResponse:
    """Create a local user."""
    body = {
        "action": "create",
        "username": username,
        "email": email,
        "sudoer": sudoer,
        "known": known,
        "force-managed": force_managed,
        "automatic": automatic,
    }
    return http.post("/users", body)


def remove_user(username: str) -> SnapdResponse:
    """Remove a local user."""
    body = {"action": "remove", "username": username}
    return http.post("/users", body)
