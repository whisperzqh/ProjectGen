"""
tests_output_folder.

Test formerly known from a unittest residing in test_generate.py named
TestOutputFolder.test_output_folder
"""

import os
from pathlib import Path

import pytest

from cookiecutter import exceptions, generate, utils


@pytest.fixture(scope='function')
def remove_output_folder():
    """Remove the output folder after test."""
    yield
    if os.path.exists('output_folder'):
        utils.rmtree('output_folder')


@pytest.mark.usefixtures('clean_system', 'remove_output_folder')
def test_exception_when_output_folder_exists() -> None:
    """Tests should raise error as output folder created before `generate_files`."""
    context = generate.generate_context(
        context_file='tests/test-output-folder/cookiecutter.json'
    )
    output_folder = context['cookiecutter']['test_name']

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with pytest.raises(exceptions.OutputDirExistsException):
        generate.generate_files(context=context, repo_dir='tests/test-output-folder')
