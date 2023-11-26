from dataclasses import dataclass
from typing import Any, Dict, List, Union


@dataclass
class SnapdResponse:
    """A response received from snapd's REST API.

    See https://snapcraft.io/docs/snapd-api
    """

    type: str
    status_code: int
    status: str
    result: Union[Dict[str, Any], List[Any]]
