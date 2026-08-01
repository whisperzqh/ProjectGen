"""
test_custom_extension_in_hooks.

Tests to ensure custom cookiecutter extensions are properly made available to
pre- and post-gen hooks.
"""

from pathlib import Path

import pytest

from cookiecutter import main


@pytest.fixture(autouse=True)
def modify_syspath(monkeypatch) -> None:
    """Fixture. Make sure that the custom extension can be loaded."""
    monkeypatch.syspath_prepend('tests/test-extensions/hello_extension')

