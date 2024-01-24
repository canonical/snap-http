import tempfile
import uuid

import pytest

from snap_http import types


@pytest.fixture(autouse=True)
def constant_uuid(monkeypatch):
    """Patch `uuid.uuid4` to always return a constant value."""
    monkeypatch.setattr(
        types,
        "uuid4",
        lambda: uuid.UUID("c747ef5f-cef1-40a7-86e5-12ca0aff6cd5"),
    )


def test_json_serialization():
    """Test JSON serialization with the `JsonData` type."""
    body = types.JsonData(
        {
            "foo": {"bar": 80, "baz": 443},
            "port": 8080,
            "enabled": True,
        }
    )

    expected = b'{"foo": {"bar": 80, "baz": 443}, "port": 8080, "enabled": true}'
    assert body.content_type == "application/json"
    assert body.content_type_header == "application/json"
    assert body.serialized == expected
    assert body.content_length == len(expected)


def test_form_data_serialization_no_files(monkeypatch):
    """Test serialization of `FormData` with no files."""
    body = types.FormData(
        {
            "action": "install",
            "devmode": True,
            "port": 8080,
        }
    )

    expected = (
        "--c747ef5f-cef1-40a7-86e5-12ca0aff6cd5\r\n"
        'Content-Disposition: form-data; name="action"\r\n\r\ninstall\r\n'
        "--c747ef5f-cef1-40a7-86e5-12ca0aff6cd5\r\n"
        'Content-Disposition: form-data; name="devmode"\r\n\r\nTrue\r\n'
        "--c747ef5f-cef1-40a7-86e5-12ca0aff6cd5\r\n"
        'Content-Disposition: form-data; name="port"\r\n\r\n8080\r\n'
        "--c747ef5f-cef1-40a7-86e5-12ca0aff6cd5--\r\n"
    ).encode()
    assert body.content_type == "multipart/form-data"
    assert body.content_type_header == (
        "multipart/form-data; boundary=c747ef5f-cef1-40a7-86e5-12ca0aff6cd5"
    )
    assert body.serialized == expected
    assert body.content_length == len(expected)


def test_form_data_serialization_with_files(monkeypatch):
    """Test serialization of `FormData` with files."""
    with tempfile.NamedTemporaryFile() as tmp1, tempfile.NamedTemporaryFile() as tmp2:
        tmp1.write(b"the answer is 42")
        tmp1.flush()

        tmp2.write(b"the answer to life, the universe, and everything")
        tmp2.flush()

        files = [
            types.FileUpload("snap", tmp1.name),
            types.FileUpload("snap", tmp2.name),
        ]
        body = types.FormData({"action": "install"}, files)

        expected = (
            "--c747ef5f-cef1-40a7-86e5-12ca0aff6cd5\r\n"
            'Content-Disposition: form-data; name="action"\r\n\r\ninstall\r\n'
            "--c747ef5f-cef1-40a7-86e5-12ca0aff6cd5\r\n"
            'Content-Disposition: form-data; name="snap"; '
            f'filename="{files[0].filename}"\r\n\r\n'
            "the answer is 42\r\n"
            "--c747ef5f-cef1-40a7-86e5-12ca0aff6cd5\r\n"
            'Content-Disposition: form-data; name="snap"; '
            f'filename="{files[1].filename}"\r\n\r\n'
            "the answer to life, the universe, and everything\r\n"
            "--c747ef5f-cef1-40a7-86e5-12ca0aff6cd5--\r\n"
        ).encode()
        assert body.serialized == expected
        assert body.content_length == len(expected)


def test_reading_file_uploads():
    """Test reading of file uploads."""
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(b"the answer is 42")
        tmp.flush()

        file = types.FileUpload("snap", tmp.name)
        assert file.content == b"the answer is 42"
        assert file.filename == tmp.name.split("/")[-1]
