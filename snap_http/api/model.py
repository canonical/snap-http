from .. import http
from ..types import SnapdResponse


def get_model() -> SnapdResponse:
    """
    GETs the active model assertion of system.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get("/model")


def remodel(new_model_assertion: str, offline: bool = False) -> SnapdResponse:
    """
    Replace the current model assertion of system
    :param new_model_assertion: New model assertion content
    :param offline: enables offline remodelling
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body = {"new-model" : new_model_assertion, "offline": offline}
    return http.post("/model", body=body)
