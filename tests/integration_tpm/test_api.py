import snap_http

from tests.utils import (
    wait_for,
)


def test_get_keyslots():
    """Test getting keyslots."""
    response = snap_http.get_keyslots()
    assert response.status_code == 200
    assert "by-container-role" in response.result
    assert "system-data" in response.result["by-container-role"]
    assert "keyslots" in response.result["by-container-role"]["system-data"]


def test_generate_recovery_key():
    """Test generating a recovery key."""
    response = snap_http.generate_recovery_key()
    assert response.status_code == 200
    assert "key-id" in response.result
    assert "recovery-key" in response.result


def test_add_recovery_key():
    """Test adding a recovery key."""
    generate_result = snap_http.generate_recovery_key().result
    key_id = generate_result["key-id"]

    response = wait_for(snap_http.update_recovery_key)(key_id, "test-add-key", False)
    assert response.status_code == 202

    keyslots = snap_http.get_keyslots().result
    assert "test-add-key" in keyslots["by-container-role"]["system-data"]["keyslots"]


def test_replace_recovery_key():
    """Test replacing a recovery key."""
    key_id = snap_http.generate_recovery_key().result["key-id"]
    response = wait_for(snap_http.update_recovery_key)(
        key_id, "test-replace-key", False
    )
    assert response.status_code == 202

    keyslots = snap_http.get_keyslots().result
    assert "test-add-key" in keyslots["by-container-role"]["system-data"]["keyslots"]

    key_id = snap_http.generate_recovery_key().result["key-id"]
    response = wait_for(snap_http.update_recovery_key)(key_id, "test-replace-key", True)
    assert response.status_code == 202

    keyslots = snap_http.get_keyslots().result
    assert (
        "test-replace-key" in keyslots["by-container-role"]["system-data"]["keyslots"]
    )
