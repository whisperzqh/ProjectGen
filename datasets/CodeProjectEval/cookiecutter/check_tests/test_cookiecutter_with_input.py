import os

import pytest

from cookiecutter import main, utils


@pytest.fixture(scope='function')
def remove_additional_dirs():
    """Remove special directories which are created during the tests."""
    yield
    if os.path.isdir('fake-project'):
        utils.rmtree('fake-project')
    if os.path.isdir('fake-project-input-extra'):
        utils.rmtree('fake-project-input-extra')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_local_with_input(monkeypatch) -> None:
    """Original test"""
    monkeypatch.setattr(
        'cookiecutter.prompt.read_user_variable',
        lambda _var, default, _prompts, _prefix: default,
    )
    main.cookiecutter('tests/fake-repo-pre/', no_input=False)
    assert os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}')
    assert not os.path.isdir('tests/fake-repo-pre/fake-project')
    assert os.path.isdir('fake-project')
    assert os.path.isfile('fake-project/README.rst')
    assert not os.path.exists('fake-project/json/')