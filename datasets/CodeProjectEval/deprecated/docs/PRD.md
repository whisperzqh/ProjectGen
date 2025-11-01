# PRD Document for Deprecated

## Introduction

The purpose of this project is to develop a Python decorator library that provides a standardized way to mark deprecated code elements (functions, methods, classes) in Python codebases. The repository provides decorators that emit warnings when deprecated code is used and integrates with Sphinx documentation to automatically generate deprecation notices. This tool is designed for library maintainers, framework developers, and software engineers who need to manage API evolution while maintaining backward compatibility.

## Goals

The objective of this project is to provide a simple, Pythonic decorator-based solution for deprecating code elements with automatic warning generation and documentation integration. The tool should support both runtime deprecation warnings and compile-time documentation generation through Sphinx directives, enabling developers to communicate API changes effectively to their users. 

## Features and Functionalities

The following features and functionalities are expected in the project:

### Deprecation Warnings
- Ability to mark functions as deprecated using the `@deprecated` decorator  
- Ability to mark class methods as deprecated
- Ability to specify the version when deprecation was introduced 
- Ability to provide a custom reason message explaining the deprecation 
- Ability to emit `DeprecationWarning` at runtime when deprecated code is called

### Sphinx Documentation Integration
- Ability to use `@deprecated` decorator from `deprecated.sphinx` module for documentation 
- Ability to use `@versionadded` decorator to mark new functionality
- Ability to use `@versionchanged` decorator to mark modified functionality  
- Ability to automatically generate Sphinx directives in docstrings 
- Ability to display deprecation information in `help()` output 

## Technical Constraints

- The repository should use Python as the primary programming language 
- The repository should support Python 2.7 and Python 3.4+  
- The repository should be platform-independent 
- The repository should use the `wrapt` library for robust decorator implementation  

## Requirements

### Dependencies

- `wrapt < 2, >= 1.10` - Decorator infrastructure library providing correct function wrapping with signature preservation

### Development Dependencies

- `tox` - Multi-environment testing automation  
- `PyTest` - Testing framework
- `PyTest-Cov` - Test coverage plugin for pytest
- `bump2version < 1` - Version management tool
- `setuptools` - Required for Python 3.12+ compatibility

## Usage

### Basic Deprecation

To mark a function as deprecated:
```python
from deprecated import deprecated

@deprecated(version='1.2.1', reason="You should use another function")
def some_old_function(x, y):
    return x + y
```

To mark a class method as deprecated:
```python
class SomeClass(object):
    @deprecated(version='1.3.0', reason="This method is deprecated")
    def some_old_method(self, x, y):
        return x + y
```

### Sphinx Documentation Integration

To integrate with Sphinx documentation:
```python
from deprecated.sphinx import deprecated
from deprecated.sphinx import versionadded
from deprecated.sphinx import versionchanged

@versionadded(version='1.0', reason="This function is new")
def function_one():
    '''This is the function one'''

@versionchanged(version='1.0', reason="This function is modified")
def function_two():
    '''This is the function two'''

@deprecated(version='1.0', reason="This function will be removed soon")
def function_three():
    '''This is the function three'''
```

## Installation

### Standard Installation

```bash
pip install Deprecated
```

### System Package Installation (Fedora/RHEL)

```bash
sudo dnf install python3-deprecated
```

## Terms/Concepts Explanation

**Decorator**: A Python design pattern that allows modification of function or class behavior by wrapping them with additional functionality without changing their source code.

**DeprecationWarning**: A built-in Python warning category used to signal that a feature is deprecated and may be removed in future versions.  

**Sphinx**: A documentation generation tool that creates intelligent and beautiful documentation from reStructuredText source files, commonly used for Python projects.

**wrapt**: A Python library that provides decorators, wrappers and monkey patching with correct preservation of function signatures and metadata. 

**Version Directive**: Sphinx directives like `.. deprecated::`, `.. versionadded::`, and `.. versionchanged::` that document API changes in generated documentation. 

