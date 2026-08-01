from __future__ import print_function

import inspect
import re
import sys
import textwrap
import warnings

import pytest

# Attempt to import the deprecated library.
# If it's not installed, these tests will fail with an ImportError,
# which is the expected behavior.

import deprecated.classic
import deprecated.sphinx


class MyDeprecationWarning(DeprecationWarning):
    """Custom warning category for testing the 'category' parameter."""
    pass


class WrongStackLevelWarning(DeprecationWarning):
    """Custom warning category used to identify specific parameterized tests."""
    pass


# Parameters used by the classic_* fixtures to test various decorator arguments.
_PARAMS = [
    None,
    (('Good reason',), {}),
    ((), {'reason': 'Good reason'}),
    ((), {'version': '1.2.3'}),
    ((), {'action': 'once'}),
    ((), {'category': MyDeprecationWarning}),
    ((), {'extra_stacklevel': 1, 'category': WrongStackLevelWarning}),
]


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecated_function(request):
    """Provides a deprecated function, parameterized with various options."""
    if request.param is None:
        @deprecated.classic.deprecated
        def foo1():
            pass
        return foo1
    else:
        args, kwargs = request.param
        @deprecated.classic.deprecated(*args, **kwargs)
        def foo1():
            pass
        return foo1

@pytest.fixture(
    scope="module",
    params=[
        None,
        """This function adds *x* and *y*.""",
        """
        This function adds *x* and *y*.

        :param x: number *x*
        :param y: number *y*
        :return: sum = *x* + *y*
        """,
    ],
    ids=["no_docstring", "short_docstring", "long_docstring"],
)
def docstring(request):
    """Provides various function/class docstrings for Sphinx tests."""
    return request.param


@pytest.fixture(scope="module", params=['versionadded', 'versionchanged', 'deprecated'])
def directive(request):
    """Provides different Sphinx directive types."""
    return request.param


# Test basic function deprecation with a variety of arguments.
# noinspection PyShadowingNames
def test_classic_deprecated_function__warns(classic_deprecated_function):
    """
    Tests that a simple deprecated function issues a warning.
    This test is parameterized to cover various decorator arguments.
    """
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        classic_deprecated_function()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated function (or staticmethod)" in str(warn.message)
    assert warn.filename == __file__ or warn.category is WrongStackLevelWarning, 'Incorrect warning stackLevel'


# Test the injection of Sphinx directives into docstrings.
# noinspection PyShadowingNames
@pytest.mark.parametrize(
    "reason, version, expected",
    [
        (
            'A good reason',
            '1.2.0',
            textwrap.dedent(
                """\
                .. {directive}:: {version}
                   {reason}
                """
            ),
        ),
        (
            None,
            '1.2.0',
            textwrap.dedent(
                """\
                .. {directive}:: {version}
                """
            ),
        ),
    ],
    ids=["reason&version", "version"],
)
def test_has_sphinx_docstring(docstring, directive, reason, version, expected):
    """
    Ensures that Sphinx directives are correctly added to a function's docstring.
    """
    def foo(x, y):
        return x + y
    foo.__doc__ = docstring

    decorator_factory = getattr(deprecated.sphinx, directive)
    decorator = decorator_factory(reason=reason, version=version)
    foo = decorator(foo)

    expected_doc = expected.format(directive=directive, version=version, reason=reason)
    current_doc = textwrap.dedent(foo.__doc__)
    assert current_doc.endswith(expected_doc)

    current_doc = current_doc.replace(expected_doc, '')
    if docstring:
        assert re.search("\n[ ]*\n$", current_doc, flags=re.DOTALL)
    else:
        assert current_doc == "\n"

    with warnings.catch_warnings(record=True) as warns:
        foo(1, 2)

    assert len(warns) == (1 if directive == 'deprecated' else 0)

# Test the use of a custom warning category.
def test_specific_warning_cls_is_used():
    """
    Tests that a custom warning category can be specified and is used.
    """
    @deprecated.classic.deprecated(category=MyDeprecationWarning)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        foo()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, MyDeprecationWarning)
