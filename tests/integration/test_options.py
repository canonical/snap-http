import snap_http

from tests.utils import wait_for


def test_get_config(test_snap):
    """Test getting snap configuration."""
    response = snap_http.get_conf("test-snap")
    assert response.status_code == 200
    assert response.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }


def test_get_specific_config_value(test_snap):
    """Test getting specific snap configuration."""
    response = snap_http.get_conf("test-snap", keys=["port"])
    assert response.status_code == 200
    assert response.result == {"port": 8080}


def test_get_nested_config_value(test_snap):
    """Test getting a specific nested snap configuration."""
    response = snap_http.get_conf("test-snap", keys=["foo.bar"])
    assert response.status_code == 200
    assert response.result == {"foo.bar": "default"}


def test_set_config(test_snap):
    """Test setting snap configuration."""
    before = snap_http.get_conf("test-snap")
    assert before.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }

    response = wait_for(snap_http.set_conf)(
        "test-snap",
        {
            "foo": {"bar": "qux", "baz": "quux"},
            "port": 8080,
        },
    )
    assert response.status_code == 202

    after = snap_http.get_conf("test-snap")
    assert after.result == {
        "foo": {"bar": "qux", "baz": "quux"},
        "port": 8080,
    }


def test_set_specific_config_value(test_snap):
    """Test setting specific snap configuration."""
    before = snap_http.get_conf("test-snap")
    assert before.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }

    response = wait_for(snap_http.set_conf)(
        "test-snap",
        {"port": 443, "foo.baz": "lambda"},
    )
    assert response.status_code == 202

    after = snap_http.get_conf("test-snap")
    assert after.result == {
        "foo": {"bar": "default", "baz": "lambda"},
        "port": 443,
    }


def test_set_config_with_invalid_key(test_snap):
    """Test setting config with an invalid key."""
    before = snap_http.get_conf("test-snap")
    assert before.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }

    response = wait_for(snap_http.set_conf)("test-snap", {"foo /bar": 80})
    assert response.status_code == 202

    change = snap_http.check_change(response.change).result
    assert change["status"] == "Error"
    assert 'invalid option name: "foo /bar"' in change["err"]

    # confirm settings haven't changed
    after = snap_http.get_conf("test-snap")
    assert after.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }


def test_unset_config_value(test_snap):
    """Test unsetting snap configuration."""
    before = snap_http.get_conf("test-snap")
    assert before.result == {
        "foo": {"bar": "default", "baz": "default"},
        "port": 8080,
    }

    response = wait_for(snap_http.set_conf)(
        "test-snap",
        {"foo.bar": "meta"},
    )
    assert response.status_code == 202

    after = snap_http.get_conf("test-snap", keys=["foo.bar"])
    assert after.result == {"foo.bar": "meta"}

    response = wait_for(snap_http.set_conf)(
        "test-snap",
        {"foo.bar": None},
    )
    assert response.status_code == 202

    after_unset = snap_http.get_conf("test-snap", keys=["foo.bar"])
    assert after_unset.result == {"foo.bar": "default"}

