from .. import http
from ..types import SnapdResponse


def get_keyslots() -> SnapdResponse:
    """Enumerate keyslots"""
    return http.get("/system-volumes")


def generate_recovery_key() -> SnapdResponse:
    """Generate a recovery key."""
    return http.post(
        "/system-volumes",
        {"action": "generate-recovery-key"},
    )


def update_recovery_key(
    key_id: str, keyslot_name: str, replace: bool = False
) -> SnapdResponse:
    """Add or replace the recovery key for a keyslot.

    :param key_id: unique id from generating the recovery key.
    :param keyslot_name: name of the keyslot to generate.
    :param replace: if `True`, updates the recovery key for the keyslot.
    """
    if replace:
        action = "replace-recovery-key"
    else:
        action = "add-recovery-key"

    return http.post(
        "/system-volumes",
        {
            "action": action,
            "key-id": key_id,
            "keyslots": [{"name": keyslot_name}],
        },
    )
