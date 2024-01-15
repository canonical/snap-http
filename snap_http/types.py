from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List, Type, Union


# For the below, refer to https://snapcraft.io/docs/snapd-api#heading--changes
COMPLETE_STATUSES = {"Done", "Error", "Hold", "Abort"}
INCOMPLETE_STATUSES = {"Do", "Doing", "Undo", "Undoing"}
SUCCESS_STATUSES = {"Done"}
ERROR_STATUSES = {"Error", "Hold", "Unknown"}


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


@dataclass
class FileUpload:
    """A file to upload to snapd's REST API."""

    name: str
    path: str

    @cached_property
    def filename(self) -> str:
        """Return the filename."""
        return Path(self.path).name

    @cached_property
    def content(self) -> bytes:
        """Read and return the file's binary content."""
        with open(self.path, "rb") as f:
            return f.read()
