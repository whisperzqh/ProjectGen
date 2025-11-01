Below is a text-based representation of the file tree.

```
├── deprecated
│   ├── classic.py
│   ├── __init__.py
│   └── sphinx.py
```


## `__init__.py`

- `__version__`: Package version string (currently "1.2.18") 
- `__author__`: Package author information 
- `__date__`: Last update date 
- `deprecated`: Imported from `deprecated.classic`, the main decorator for marking code as deprecated 

## `classic.py`

- `ClassicAdapter`: A wrapper adapter class that inherits from `wrapt.AdapterFactory` to emit deprecation warnings when decorated functions, methods, or classes are used 

  - `__init__(self, reason="", version="", action=None, category=DeprecationWarning, extra_stacklevel=0)`: Constructs a wrapper adapter with parameters for the deprecation message, version number, warning filter action, warning category class, and additional stack levels to skip
  
  - `get_deprecated_msg(self, wrapped, instance)`: Generates the deprecation warning message based on the type of wrapped entity (class, function, method, static method, or class method) 
  
  - `__call__(self, wrapped)`: Decorates a class or function by wrapping it to emit deprecation warnings; for classes, patches the `__new__` method; for routines, uses `wrapt.decorator` 

- `deprecated(*args, **kwargs)`: A decorator factory that marks functions, methods, or classes as deprecated and emits warnings when they are used; supports parameters including `reason`, `version`, `action`, `category`, `extra_stacklevel`, and `adapter_cls` 

## `sphinx.py`

- `SphinxAdapter`: Extends `ClassicAdapter` to add Sphinx documentation directives (`versionadded`, `versionchanged`, `deprecated`) to docstrings while optionally emitting runtime deprecation warnings 

  - `__init__(self, directive, reason="", version="", action=None, category=DeprecationWarning, extra_stacklevel=0, line_length=70)`: Constructs a Sphinx adapter with a required directive type ("versionadded", "versionchanged", or "deprecated"), version number (required), and optional parameters for reason, warning control, and text wrapping 
  
  - `__call__(self, wrapped)`: Adds the Sphinx directive to the docstring of the decorated class or function; for "versionadded" and "versionchanged", only modifies the docstring; for "deprecated", also adds warning emission via parent class

  - `get_deprecated_msg(self, wrapped, instance)`: Overrides parent method to strip Sphinx cross-reference syntax (like `:function:`, `:py:func:`) from warning messages before displaying them to users 

- `versionadded(reason="", version="", line_length=70)`: A decorator that inserts a "versionadded" Sphinx directive into function/class docstrings to document when a feature was added; does not emit runtime warnings 

- `versionchanged(reason="", version="", line_length=70)`: A decorator that inserts a "versionchanged" Sphinx directive into function/class docstrings to document when a feature was modified; does not emit runtime warnings 

- `deprecated(reason="", version="", line_length=70, **kwargs)`: A decorator that inserts a "deprecated" Sphinx directive into function/class docstrings and emits runtime deprecation warnings; supports additional keyword arguments for `action`, `category`, and `extra_stacklevel`