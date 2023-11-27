from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Type, Union


@dataclass
class SnapdResponse:
    """A response received from snapd's REST API.

    See https://snapcraft.io/docs/snapd-api
    """

    type: str
    status_code: int
    status: str
    result: Union[Dict[str, Any], List[Any]]
    sources: Union[List[str], None] = None
    change: Union[str, None] = None

    @classmethod
    def from_http_response(cls: Type, response: Dict[str, Any]) -> SnapdResponse:
        return cls(**{k.replace("-", "_"): v for k, v in response.items()})
