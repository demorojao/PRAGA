"""Tests for utility functions.

To run the tests, install pytest (e.g. `pip install pytest`) and execute:

    pytest
"""

import pytest

from app import allowed_file


@pytest.mark.parametrize("filename", [
    "image.png",
    "photo.jpg",
    "pic.jpeg",
    "anim.gif",
])
def test_allowed_file_valid_extensions(filename):
    assert allowed_file(filename) is True


@pytest.mark.parametrize("filename", [
    "document.txt",
    "archive.zip",
    "script.py",
    "noextension",
])
def test_allowed_file_invalid_extensions(filename):
    assert allowed_file(filename) is False

