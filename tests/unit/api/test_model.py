from snap_http import api, http, types


def test_get_model(monkeypatch) -> None:
    """`api.get_model` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="sync",
        status_code=200,
        status="OK",
        result={},
    )

    def mock_get(path):
        assert path == "/model"

        return mock_response

    monkeypatch.setattr(http, "get", mock_get)

    result = api.get_model()

    assert result == mock_response


def test_remodel(monkeypatch):
    """`api.remodel` returns a `types.SnapdResponse`."""
    mock_response = types.SnapdResponse(
        type="async",
        status_code=202,
        status="OK",
        result={},
    )

    def mock_post(path, body):
        assert path == "/model"
        assert body == {"new-model": "dummy_model_assertion", "offline" : True}
        return mock_response

    monkeypatch.setattr(http, "post", mock_post)

    result = api.remodel("dummy_model_assertion", True)

    assert result == mock_response
