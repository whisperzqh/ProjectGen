from pathlib import Path

import pytest

from cookiecutter import main


@pytest.fixture(
    params=['custom-extension-pre', 'custom-extension-post'],
    ids=['pre_gen_hook', 'post_gen_hook'],
)
def template(request) -> str:
    """Original test"""
    return f"tests/test-extensions/{request.param}"


@pytest.fixture(autouse=True)
def modify_syspath(monkeypatch) -> None:
    """Fixture. Make sure that the custom extension can be loaded."""
    monkeypatch.syspath_prepend('tests/test-extensions/hello_extension')



def test_hook_with_extension(template, output_dir) -> None:
    """Original test"""
    project_dir = main.cookiecutter(
        template,
        no_input=True,
        output_dir=output_dir,
        extra_context={'project_slug': 'foobar', 'name': 'Cookiemonster'},
    )

    readme = Path(project_dir, 'README.rst').read_text(encoding="utf-8")
    assert readme.strip() == 'Hello Cookiemonster!'