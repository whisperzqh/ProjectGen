import pytest
from click.testing import CliRunner

import os
from pathlib import Path

from cookiecutter.cli import main
from cookiecutter import utils


@pytest.fixture(scope='session')
def cli_runner():
    """Fixture that returns a helper function to run the cookiecutter cli."""
    runner = CliRunner()

    def cli_main(*cli_args, **cli_kwargs):
        """Run cookiecutter cli main with the given args."""
        return runner.invoke(main, cli_args, **cli_kwargs)

    return cli_main

@pytest.fixture
def remove_fake_project_dir(request) -> None:
    """Remove the fake project directory created during the tests."""

    def fin_remove_fake_project_dir() -> None:
        for prefix in ('', 'input'):
            dir_name = f'{prefix}fake-project'
            if os.path.isdir(dir_name):
                utils.rmtree(dir_name)

    request.addfinalizer(fin_remove_fake_project_dir)

@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli(cli_runner) -> None:
    """Original test"""
    result = cli_runner('tests/fake-repo-pre/', '--no-input')
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')
    content = Path("fake-project", "README.rst").read_text()
    assert 'Project name: **Fake Project**' in content