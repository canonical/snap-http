from .. import http
from ..types import SnapdResponse


def get_recovery_systems() -> SnapdResponse:
    """
    GET all recovery systems
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get("/systems")

def get_recovery_system(label: str) -> SnapdResponse:
    """
    GET specific recovery system
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get(f"/systems/{label}")


def perform_system_action(action: str, mode: str)-> SnapdResponse:
    """
    Attempt to perform an action with the current active recovery system.
    :param action: Action to perform, which is either “reboot”, “create” or “do”.
    :param mode:  The mode to transition to either "run", "recover", "install" or "factory-reset".
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body = {
        "action": action,
        "mode": mode
    }
    return http.post("/systems", body=body)


def perform_recovery_action(label: str, action: str, mode: str)-> SnapdResponse:
    """
    Attempt to perform an action with the current active recovery system.
    :param label: Label to specify recovery system.
    :param action: Action to perform, which is either “reboot”, “create” or “do”.
    :param mode:  The mode to transition to either "run", "recover", "install" or "factory-reset".
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body = {
        "action": action,
        "mode": mode
    }
    return http.post(f"/systems/{label}", body=body)
