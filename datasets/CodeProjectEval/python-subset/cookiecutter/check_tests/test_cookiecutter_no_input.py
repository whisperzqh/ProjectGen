import pytest
import os

from cookiecutter import main, utils


@pytest.fixture(scope='function')
def remove_additional_dirs(request) -> None:
    """Fixture. Remove special directories which are created during the tests."""

    def fin_remove_additional_dirs() -> None:
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-extra'):
            utils.rmtree('fake-project-extra')
        if os.path.isdir('fake-project-templated'):
            utils.rmtree('fake-project-templated')
        if os.path.isdir('fake-project-dict'):
            utils.rmtree('fake-project-dict')
        if os.path.isdir('fake-tmp'):
            utils.rmtree('fake-tmp')

    request.addfinalizer(fin_remove_additional_dirs)


@pytest.mark.parametrize('path', ['tests/fake-repo-pre/', 'tests/fake-repo-pre'])
@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_no_input_return_project_dir(path) -> None:
    """Original test"""
    project_dir = main.cookiecutter(path, no_input=True)
    assert os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}')
    assert not os.path.isdir('tests/fake-repo-pre/fake-project')
    assert os.path.isdir(project_dir)
    assert os.path.isfile('fake-project/README.rst')
    assert not os.path.exists('fake-project/json/')