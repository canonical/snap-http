from __future__ import annotations

import json
from abc import ABC, abstractproperty
from dataclasses import dataclass
from functools import cached_property
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union
from uuid import uuid4

# For the below, refer to https://snapcraft.io/docs/snapd-api#heading--changes
COMPLETE_STATUSES = {"Done", "Error", "Hold", "Abort"}
INCOMPLETE_STATUSES = {"Do", "Doing", "Undo", "Undoing"}
SUCCESS_STATUSES = {"Done"}
ERROR_STATUSES = {"Error", "Hold", "Unknown"}

SnapdRequestBody = Union[
    Dict[str, Any],
    "JsonData",
    "FormData",
    "AssertionData",
]


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
    warning_timestamp: Union[str, None] = None
    warning_count: Union[int, None] = None

    @classmethod
    def from_http_response(
        cls: Type["SnapdResponse"], response: Dict[str, Any]
    ) -> SnapdResponse:
        return cls(**{k.replace("-", "_"): v for k, v in response.items()})


class AbstractRequestBody(ABC):
    """An abstract base class for the request body of a HTTP request."""

    content_type: str

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize the class with `data`."""
        self.data = data

    @abstractproperty
    def serialized(self) -> bytes:
        """Serialize the request body based on the `content_type`."""

    @cached_property
    def content_length(self) -> int:
        """Get the length of the serialized request body."""
        return len(self.serialized)

    @cached_property
    def content_type_header(self) -> str:
        """Get the content type header value."""
        return self.content_type


class JsonData(AbstractRequestBody):
    """A `SnapdRequestBody` that is serialized to the application/json content type."""

    content_type = "application/json"

    @cached_property
    def serialized(self) -> bytes:
        """Serialize the request body to byte-encoded JSON."""
        return json.dumps(self.data).encode()


class FormData(AbstractRequestBody):
    """A `SnapdRequestBody` that is serialized to the multipart/form-data content type."""

    content_type = "multipart/form-data"
    files: List[FileUpload]
    boundary: str

    def __init__(
        self,
        data: Dict[str, Any],
        files: Optional[List["FileUpload"]] = None,
    ) -> None:
        """Initialize the class."""
        super().__init__(data)
        self.files = files or []
        self.boundary = str(uuid4())

    @cached_property
    def serialized(self) -> bytes:
        """Serialize the request data & files to the multipart/form-data format."""
        content = BytesIO()
        for key, value in self.data.items():
            content.write(
                (
                    f"--{self.boundary}\r\n"
                    f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
                    f"{value}\r\n"
                ).encode()
            )

        for file in self.files:
            content.write(
                (
                    f"--{self.boundary}\r\n"
                    f'Content-Disposition: form-data; name="{file.name}"; '
                    f'filename="{file.filename}"\r\n\r\n'
                ).encode()
            )
            content.write(file.content)
            content.write(b"\r\n")

        content.write(f"--{self.boundary}--\r\n".encode())
        return content.getvalue()

    @cached_property
    def content_type_header(self) -> str:
        """Get the content type header value."""
        return f"{self.content_type}; boundary={self.boundary}"


class AssertionData(AbstractRequestBody):
    """A `SnapdRequestBody` for an assertion payload."""

    content_type = "application/x.ubuntu.assertion"

    def __init__(self, assertion: str):
        """Initialize the class with `data`."""
        self.assertion = assertion

    @cached_property
    def serialized(self) -> bytes:
        """Serialize the assertion to bytes."""
        return self.assertion.encode()


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
