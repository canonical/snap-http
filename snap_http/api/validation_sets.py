from typing import Dict, Optional, Union

from .. import http
from ..types import SnapdResponse


def get_validation_sets() -> SnapdResponse:
    """
    GET all enabled validation sets
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get("/validation-sets")


def get_validation_set(account_id: str, validation_set_name: str) -> SnapdResponse:
    """
    GET specific validation set
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    return http.get(f"/validation-sets/{account_id}/{validation_set_name}")


def refresh_validation_set(account_id: str, validation_set_name: str, validation_set_sequence: Optional[int] = None) -> SnapdResponse:
    """
    Refresh validation set of system
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :param validation_set_sequence: Sequence value of the validation set
    :return: A SnapdResponse containing the response from the snapd API.
    """
    validation_set_str = f"{account_id}/{validation_set_name}"
    if validation_set_sequence is not None:
        validation_set_str += f"={validation_set_sequence}"

    body = {
        "action": "refresh",
        "validation-sets": [
            validation_set_str
        ],
    }
    return http.post("/snaps", body=body)


def forget_validation_set(account_id: str, validation_set_name: str, validation_set_sequence: Optional[int] = None) -> SnapdResponse:
    """
    Forget a validation set of system
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :return: A SnapdResponse containing the response from the snapd API.
    """

    body: Dict[str, Union[str, int]] = {
        "action": "forget"
    }

    if validation_set_sequence is not None:
        body["sequence"] = validation_set_sequence

    return http.post(f"/validation-sets/{account_id}/{validation_set_name}", body=body)


def enforce_validation_set(account_id: str, validation_set_name: str, validation_set_sequence: Optional[int] = None) -> SnapdResponse:
    """
    Enforce a validation set of system
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body: Dict[str, Union[str, int]] = {
        "action": "apply",
        "mode": "enforce"
        }

    if validation_set_sequence is not None:
        body["sequence"] = validation_set_sequence

    return http.post(f"/validation-sets/{account_id}/{validation_set_name}", body=body)


def monitor_validation_set(account_id: str, validation_set_name: str, validation_set_sequence: Optional[int] = None) -> SnapdResponse:
    """
    Apply a validation set of system
    :param account_id:  Identifier for the developer account (creator of the validation-set).
    :param validation_set_name: Name of the validation set.
    :return: A SnapdResponse containing the response from the snapd API.
    """
    body: Dict[str, Union[str, int]] = {
        "action": "apply",
        "mode": "monitor"
    }

    if validation_set_sequence is not None:
        body["sequence"] = validation_set_sequence

    return http.post(f"/validation-sets/{account_id}/{validation_set_name}", body=body)
