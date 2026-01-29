import snap_http

from tests.utils import wait_for


def test_save_snapshot(test_snap):
    """Test saving a snapshot."""
    response = wait_for(snap_http.save_snapshot)(snaps=["snapd"])
    assert response.status_code == 202

    set_id = response.result["set-id"]
    snapshots = snap_http.snapshots().result
    assert any(shot['id'] == set_id for shot in snapshots)


def test_forget_snapshot(test_snap):
    """Test forgetting a snapshot."""
    response = wait_for(snap_http.save_snapshot)(snaps=["snapd"])
    assert response.status_code == 202

    set_id = response.result["set-id"]
    snapshots = snap_http.snapshots().result
    assert any(shot['id'] == set_id for shot in snapshots)

    response = wait_for(snap_http.forget_snapshot)(set_id)
    assert response.status_code == 202

    snapshots = snap_http.snapshots().result
    assert not any(shot['id'] == set_id for shot in snapshots)
