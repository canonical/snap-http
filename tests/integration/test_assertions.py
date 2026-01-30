import snap_http

from tests.utils import assertion_exists


def test_get_assertion_types():
    """Test getting assertion types."""
    response = snap_http.get_assertion_types()
    assert response.status_code == 200
    types = response.result["types"]
    assert len(types) > 0
    assert "account" in types
    assert "model" in types
    assert "snap-declaration" in types
    assert "store" in types


def test_get_assertions():
    """Test getting assertions."""
    response = snap_http.get_assertions("snap-declaration")
    assert response.status_code == 200
    assert len(response.result) > 0
    assert b"type: snap-declaration" in response.result


def test_get_assertions_with_filters(hello_world_snap_declaration_assertion):
    """Test getting assertions with filters."""
    assertion, metadata = hello_world_snap_declaration_assertion

    before = snap_http.get_assertions(
        "snap-declaration", filters={"snap-id": metadata["snap_id"]}
    )
    assert before.result == b""

    response = snap_http.add_assertion(assertion)
    assert response.status_code == 200

    after = snap_http.get_assertions(
        "snap-declaration",
        filters={"snap-id": metadata["snap_id"], "series": metadata["series"]},
    )
    assert after.result.decode() == assertion


def test_add_an_assertion(hello_world_snap_declaration_assertion):
    """Test adding an assertion."""
    assertion, metadata = hello_world_snap_declaration_assertion
    assert assertion_exists(**metadata) is False

    response = snap_http.add_assertion(assertion)
    assert response.status_code == 200
    assert assertion_exists(**metadata) is True
