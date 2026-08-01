# Architecture Design
Below is a text-based representation of the file tree.

```text
.
├── voluptuous
    ├── error.py
    ├── humanize.py
    ├── __init__.py
    ├── py.typed
    ├── schema_builder.py
    ├── tests
    │   ├── __init__.py
    │   ├── tests.md
    │   └── tests.py
    ├── util.py
    └── validators.py
```
## `validators.py`

- `truth(f)`: **Convenience decorator to convert truth functions into validators**. It wraps a function `f` and ensures that if `f(v)` returns a falsy value, a `ValueError` is raised, otherwise, it returns the original value `v`.
  - `check(v)`: The inner function created by the decorator that **calls the original function `f`** and raises `ValueError` if the result is false.

- `Coerce(object)`: **Coerce a value to a type**. If the type constructor throws a `ValueError`, `TypeError`, or `InvalidOperation`, the value will be marked as `Invalid`.
  - `__init__(self, type, msg)`: Initializes the validator with the target `type` or callable and an optional custom error `msg`.
  - `__call__(self, v)`: Attempts to **convert the value `v` to the target `type`** and returns the coerced value.
  - `__repr__(self)`: Returns the string representation of the validator.

- `IsTrue(v)`: **Assert that a value is true, in the Python sense**. Implicitly false values (like empty lists or `False`) will fail validation.

- `IsFalse(v)`: **Assert that a value is false, in the Python sense**. Only implicitly false values will pass validation.

- `Boolean(v)`: **Convert human-readable boolean values to a bool**. Accepted string values include '1', 'true', 'yes', 'on', 'enable' and their false counterparts. Non-string values are cast to `bool`.

- `_WithSubValidators(object)`: **Base class for validators that use sub-validators** (like `Any`, `All`, `SomeOf`). Provides methods for compiling and running the nested validators.
  - `__init__(self, *validators, msg, required, discriminant, **kwargs)`: Initializes the base validator with a list of `validators`, optional `msg`, `required` flag, and an optional `discriminant` function to filter validators based on input value.
  - `__voluptuous_compile__(self, schema)`: **Compiles the list of sub-validators** using the parent `Schema` instance, allowing nested schemas to be correctly processed.
  - `_run(self, path, value)`: **Runs the validation process** using the compiled sub-validators, applying the `discriminant` function if provided to select which validators to execute.
  - `__call__(self, v)`: **Executes the sub-validators** by wrapping them in temporary `Schema` instances (used primarily for non-compiled use cases).
  - `__repr__(self)`: Returns a string representation, including the class name and sub-validators.
  - `_exec(self, funcs, v, path)`: **Abstract method** (must be implemented by subclasses) to execute the core logic for running the list of compiled validator functions (`funcs`).

- `Any(_WithSubValidators)`: **Use the first validated value**. The input value must pass at least one of the defined sub-validators.
  - `_exec(self, funcs, v, path)`: Executes sub-validators sequentially, **returns the value from the first one that passes**, and raises `AnyInvalid` if none pass. (Alias: `Or`).

- `Union(_WithSubValidators)`: **Use the first validated value among those selected by discriminant**. A custom function (`discriminant`) filters the sub-validators to check based on the input value.
  - `_exec(self, funcs, v, path)`: Executes the selected sub-validators sequentially, returns the value from the first one that passes, and raises an `AnyInvalid` error if none pass. (Alias: `Switch`).

- `All(_WithSubValidators)`: **Value must pass all validators**. The output of each validator is passed as input to the next.
  - `_exec(self, funcs, v, path)`: Executes all sub-validators sequentially, passing the result of one as input to the next, and raises an `AllInvalid` error if any fails. (Alias: `And`).

- `Match(object)`: Value must be a string that **matches the regular expression**.
  - `__init__(self, pattern, msg)`: Initializes with the regex `pattern` (string or compiled `re.Pattern`) and an optional `msg`.
  - `__call__(self, v)`: Attempts to **match the pattern against the input value `v`**.
  - `__repr__(self)`: Returns the string representation.

- `Replace(object)`: **Performs regex substitution** on a string value.
  - `__init__(self, pattern, substitution, msg)`: Initializes with the regex `pattern`, the `substitution` string, and an optional `msg`.
  - `__call__(self, v)`: **Returns the string after performing the substitution**.
  - `__repr__(self)`: Returns the string representation.

- `_url_validation(v)`: An internal helper function that **parses a string as a URL** and raises `UrlInvalid` if it is missing a scheme or a network location (`netloc`).

- `Email(v)`: **Verify that the value is a valid email address** by checking both the user and domain parts against standard regex patterns.

- `FqdnUrl(v)`: **Verify that the value is a fully qualified domain name URL** (must contain a domain name/dot in the `netloc`).

- `Url(v)`: **Verify that the value is a URL** that includes a scheme and a network location.

- `IsFile(v)`: **Verify the file exists** and the path points to a file on the filesystem.

- `IsDir(v)`: **Verify the directory exists** and the path points to a directory on the filesystem.

- `PathExists(v)`: **Verify the path exists**, regardless of whether it is a file or a directory.

- `Maybe(validator, msg)`: **Validate that the object matches the given validator or is `None`**. It is a convenience function that returns an `Any(None, validator)`.

- `Range(object)`: **Limit a value to a range** by checking if it is between `min` and `max` (inclusive or exclusive).
  - `__init__(self, min, max, min_included, max_included, msg)`: Initializes with the range bounds, flags for inclusivity, and an optional error `msg`.
  - `__call__(self, v)`: **Checks if the input value `v` is within the defined range**.
  - `__repr__(self)`: Returns the string representation.

- `Clamp(object)`: **Clamp a value to a range**. If the value is below `min` or above `max`, it is coerced to the boundary value; otherwise, it is returned unchanged.
  - `__init__(self, min, max, msg)`: Initializes with the inclusive `min` and `max` values and an optional error `msg`.
  - `__call__(self, v)`: **Coerces the input value `v` to fit within the `min` and `max` bounds**.
  - `__repr__(self)`: Returns the string representation.

- `Length(object)`: **The length of a value must be in a certain range**. Checks `len(v)` against `min` and `max` boundaries.
  - `__init__(self, min, max, msg)`: Initializes with the inclusive `min` and `max` lengths and an optional `msg`.
  - `__call__(self, v)`: **Checks the length of the input value `v`**.
  - `__repr__(self)`: Returns the string representation.

- `Datetime(object)`: **Validate that the value matches the datetime format** and coerces the string to a `datetime.datetime` object.
  - `__init__(self, format, msg)`: Initializes with the `strftime` `format` string and an optional `msg`.
  - `__call__(self, v)`: **Parses the string `v` into a `datetime.datetime` object** based on the specified format.
  - `__repr__(self)`: Returns the string representation.

- `Date(Datetime)`: **Validate that the value matches the date format** and coerces the string to a `datetime.date` object (inherits from `Datetime` with a different default format).
  - `__call__(self, v)`: **Parses the string `v` into a `datetime.date` object** based on the specified format.
  - `__repr__(self)`: Returns the string representation.

- `In(object)`: **Validate that a value is in a collection** (`container`).
  - `__init__(self, container, msg)`: Initializes with the required `container` and an optional `msg`.
  - `__call__(self, v)`: **Checks if the input value `v` is an element of the container**.
  - `__repr__(self)`: Returns the string representation.

- `NotIn(object)`: **Validate that a value is not in a collection** (`container`).
  - `__init__(self, container, msg)`: Initializes with the disallowed `container` and an optional `msg`.
  - `__call__(self, v)`: **Checks if the input value `v` is not an element of the container**.
  - `__repr__(self)`: Returns the string representation.

- `Contains(object)`: **Validate that the given schema element is in the sequence being validated**.
  - `__init__(self, item, msg)`: Initializes with the required `item` that must be present in the container, and an optional `msg`.
  - `__call__(self, v)`: **Checks if the required `item` is present in the input container `v`**.
  - `__repr__(self)`: Returns the string representation.

- `ExactSequence(object)`: **Matches each element in a sequence against the corresponding element in the validators** and requires the sequence length to match the number of validators.
  - `__init__(self, validators, msg, **kwargs)`: Initializes with the iterable of `validators`, an optional `msg`, and other schema constructor arguments.
  - `__call__(self, v)`: **Validates the sequence `v`** for correct length and validates each element against its corresponding schema/validator.
  - `__repr__(self)`: Returns the string representation.

- `Unique(object)`: **Ensure an iterable does not contain duplicate items**.
  - `__init__(self, msg)`: Initializes with an optional error `msg`.
  - `__call__(self, v)`: **Checks if all items in the iterable `v` are unique** (and hashable).
  - `__repr__(self)`: Returns the string representation.

- `Equal(object)`: **Ensure that value matches target** using exact equality (`==`).
  - `__init__(self, target, msg)`: Initializes with the exact `target` value to compare against and an optional `msg`.
  - `__call__(self, v)`: **Checks if the input value `v` is equal to the `target`**.
  - `__repr__(self)`: Returns the string representation.

- `Unordered(object)`: **Ensures a sequence contains the validated values in an unspecified order**.
  - `__init__(self, validators, msg, **kwargs)`: Initializes with the list of required `validators`, an optional `msg`, and other schema constructor arguments.
  - `__call__(self, v)`: **Checks if the input sequence `v` has the same length as the validators** and if every element in `v` is successfully validated by *one* of the schemas.
  - `__repr__(self)`: Returns the string representation.

- `Number(object)`: **Verify the number of digits (Precision) and decimal places (Scale)** of a numeric value provided as a string.
  - `__init__(self, precision, scale, msg, yield_decimal)`: Initializes with optional `precision`, `scale`, `msg`, and a flag to `yield_decimal` instead of the original string input.
  - `__call__(self, v)`: **Validates the precision and scale** of the number representation `v`.
  - `__repr__(self)`: Returns the string representation.
  - `_get_precision_scale(self, number)`: An internal helper to **calculate the precision and scale of a given number** (provided as a string) by converting it to a `Decimal` object and returns a tuple of (precision, scale, Decimal).

- `SomeOf(_WithSubValidators)`: **Value must pass at least some validations**, determined by the given `min_valid` and/or `max_valid` parameters.
  - `__init__(self, validators, min_valid, max_valid, **kwargs)`: Initializes with the list of sub-validators, and the inclusive minimum and maximum number of required successful validations.
  - `_exec(self, funcs, v, path)`: **Executes all sub-validators, counts the passes**, and raises `NotEnoughValid` or `TooManyValid` if the count is outside the allowed range.
  - `__repr__(self)`: Returns the string representation.


## `util.py` :

- `Lower(v: str) -> str`: **Transform a string to lower case**.

- `Upper(v: str) -> str`: **Transform a string to upper case**.

- `Capitalize(v: str) -> str`: **Capitalise a string**.

- `Title(v: str) -> str`: **Title case a string**.

- `Strip(v: str) -> str`: **Strip whitespace from a string**.

- `DefaultTo(object)`: **Sets a value to default\_value if none provided**.
  - `__init__(self, default_value, msg: typing.Optional[str] = None) -> None`: Initializes the validator, preparing the `default_value` as a callable factory.
  - `__call__(self, v)`: Returns the default value if the input `v` is `None`; otherwise, returns `v` unchanged.
  - `__repr__(self)`: Returns a string representation of the validator, showing the factory's default value.

- `SetTo(object)`: **Set a value, ignoring any previous value**.
  - `__init__(self, value) -> None`: Initializes the validator, preparing the fixed `value` as a callable factory.
  - `__call__(self, v)`: Returns the fixed value set during initialization, ignoring the input `v`.
  - `__repr__(self)`: Returns a string representation of the validator, showing the fixed value it sets.

- `Set(object)`: **Convert a list into a set**.
  - `__init__(self, msg: typing.Optional[str] = None) -> None`: Initializes the validator with an optional custom error message.
  - `__call__(self, v)`: Attempts to **convert the input value `v` into a `set`**; raises `TypeInvalid` if the conversion fails (e.g., due to unhashable elements).
  - `__repr__(self)`: Returns the string representation `'Set()'`.

- `Literal(object)`: A validator that **checks for exact equality with a literal value**.
  - `__init__(self, lit) -> None`: Initializes the validator with the literal value (`lit`) to compare against.
  - `__call__(self, value, msg: typing.Optional[str] = None)`: **Checks if the input `value` is exactly equal to the stored literal** (`self.lit`); raises `LiteralInvalid` if they do not match, or returns the literal if they do.
  - `__str__(self)`: Returns the string representation of the literal value.
  - `__repr__(self)`: Returns the official string representation of the literal value.

## `schema_builder.py`

- `_isnamedtuple(obj)`: A utility function to **check if an object is a `collections.namedtuple`**.

- `Undefined(object)`: A class representing an explicitly **undefined value**, typically used for un-set parameters or default values.
  - `__nonzero__(self)`: Returns `False` for Python 2 compatibility (for boolean evaluation).
  - `__repr__(self)`: Returns the string representation `'...'`.

- `Self() -> None`: A placeholder function intended to allow a schema to **recursively reference itself**. It raises a `SchemaError` if called directly.

- `default_factory(value) -> DefaultFactory`: Converts a concrete value into a callable factory function (a lambda that returns the value) unless the value is already `UNDEFINED` or a callable.

- `raises(exc, msg: typing.Optional[str] = None, regex: typing.Optional[re.Pattern] = None) -> Generator[None, None, None]`: **Context manager for testing** that asserts a specific exception (`exc`) is raised within its block, optionally checking the exception message (`msg`) or matching it against a regular expression (`regex`).

- `message(msg, cls)`: **Decorator to associate a custom error message** (`msg`) and an optional specific error class (`cls`) with a validator function.

- `_args_to_dict(func, args)`: A utility function to **map positional arguments (`args`) back to their corresponding function argument names** defined in `func`.

- `_merge_args_with_kwargs(args_dict, kwargs)`: A utility function to **merge a dictionary of positional arguments (`args_dict`) with a dictionary of keyword arguments (`kwargs`)**, giving precedence to values from `kwargs`.

- `Schema(object)`: **The core validation schema class**. It is the main entry point for defining validation rules and performing validation.
  - `__init__(self, schema, required, extra)`: Initializes the schema, compiling the validation structure (`schema`) and setting behavior for field necessity (`required`) and handling of extra keys (`extra`).
  - `infer(cls, data, **kwargs)`: Class method to **create a new Schema by inferring types** from a concrete data structure (like a Python dictionary or list).
  - `__eq__(self, other)`: Checks for **equality** between two `Schema` instances by comparing their underlying validation structures and configuration.
  - `__ne__(self, other)`: Checks for **inequality** between two `Schema` instances.
  - `__str__(self)`: Returns a simple string representation of the underlying schema structure.
  - `__repr__(self)`: Returns a detailed string representation of the `Schema` object, including configuration settings.
  - `__call__(self, data)`: The primary method to **validate data against this schema**, returning the validated (and possibly transformed) data or raising an exception.
  - `_compile(self, schema)`: **Compiles the schema structure** into a callable validation function/tree for efficient repeated use.
  - `_compile_mapping(self, schema, invalid_msg)`: Creates a validator function for **dictionary-like structures**, handling key validation, required/optional fields, and extra keys.
  - `_compile_object(self, schema)`: Creates a validator function for an **object** (instance of a class), validating its attributes based on the schema.
  - `_compile_dict(self, schema)`: Creates a validator function specifically for a `dict` (dictionary) type.
  - `_compile_list(self, schema)`: Creates a validator function for a `list`.
  - `_compile_tuple(self, schema)`: Creates a validator function for a `tuple`.
  - `_compile_set(self, schema)`: Creates a validator function for a `set` or `frozenset`.
  - `_compile_scalar(schema)`: Creates a validator function for a single, non-collection schema element (e.g., a type, a literal value, or a simple callable validator).
  - `_compile_key(self, key)`: Compiles a **key validator** (e.g., a bare key, `Required`, or `Optional`) into a callable function.
  - `_get_key_from_data(self, key, data)`: Searches for a key in the data that **matches the compiled key validator**, used for flexible key matching (e.g., for regex keys).

- `_iterate_mapping_candidates(compiled_schema) -> typing.Generator`: A generator that yields **key and validator pairs** from a compiled mapping schema in a specific order (first non-callable, then callable keys).

- `_iterate_object(data) -> typing.Generator`: A generator that yields **key/value pairs of an object's public attributes** (those not starting with `_`).

- `Marker(object)`: The abstract base class for `Required`, `Optional`, and `Remove`, defining shared initialization and key validation logic.
  - `__init__(self, schema, default, msg)`: Initializes with the key's schema, optional default value, and an optional custom error message.
  - `__call__(self, path, v)`: **Validates the key against the marker's schema** and handles default values if the marker allows it.

- `Required(Marker)`: A marker class that designates a key as **required**.
  - `__init__(self, schema, default, msg)`: Initializes the marker with the key's schema, optional default value, and an optional custom error message.
  - `__repr__(self)`: Returns a string representation.
  - `__voluptuous_compile__(self, schema)`: Compiles the underlying key schema for use within the `Required` marker.

- `Optional(Marker)`: A marker class that designates a key as **optional**.
  - `__init__(self, schema, default, msg)`: Initializes the marker with the key's schema, optional default value, and an optional custom error message.
  - `__repr__(self)`: Returns a string representation.
  - `__voluptuous_compile__(self, schema)`: Compiles the underlying key schema for use within the `Optional` marker.

- `Remove(Marker)`: A marker class that designates a key to be **removed from the output** if it is present in the input data.
  - `__init__(self, schema)`: Initializes the marker with the key's schema.
  - `__repr__(self)`: Returns a string representation.
  - `__voluptuous_compile__(self, schema)`: Compiles the underlying key schema for use within the `Remove` marker.
  - `__call__(self, v)`: Returns the internal `Remove` sentinel value, signaling the calling validator to remove the key.

- `Object(Schema)`: Defines a schema that validates the **attributes of an object** (an instance of a specific class).
  - `__init__(self, schema, cls, msg, **kwargs)`: Initializes with the attribute schema, an optional expected class (`cls`), an optional message, and other schema arguments.
  - `__repr__(self)`: Returns a string representation.
  - `__voluptuous_compile__(self, schema)`: Compiles the object schema.

- `validate(*a, **kw) -> typing.Callable`: A **decorator for validating arguments and/or the return value of a function** against a given schema.
  - `validate_schema_decorator(func)`: The inner function created by the decorator that **wraps the target function** with input and output validation logic.
  - `func_wrapper(*args, **kwargs)`: The final wrapped function that **performs input validation**, calls the original function, and then **performs output validation**.

## `humanize.py`

- `_nested_getitem(data: typing.Any, path: typing.List[typing.Hashable]) -> typing.Optional[typing.Any]`: A utility function to **safely retrieve a value from a nested data structure** using a list of keys (`path`), returning `None` if the item cannot be retrieved or an index/key error occurs.

- `humanize_error(data, validation_error: Invalid, max_sub_error_length: int = MAX_VALIDATION_ERROR_ITEM_LENGTH) -> str`: **Provide a more helpful + complete validation error message** than that provided automatically. It includes the original error message, the error path, and a summary of the **offending input value**, handling both single (`Invalid`) and multiple (`MultipleInvalid`) errors.

- `validate_with_humanized_errors(data, schema: Schema, max_sub_error_length: int = MAX_VALIDATION_ERROR_ITEM_LENGTH) -> typing.Any`: A wrapper that **validates data against a schema** and, if validation fails with `Invalid` or `MultipleInvalid`, it **raises a new error with a human-readable message** that includes the context of the invalid data.

## `error.py`

- `Error(Exception)`: **Base validation exception**.

- `SchemaError(Error)`: An **error was encountered in the schema** itself (not the data being validated).

- `Invalid(Error)`: **The data was invalid**.
  - `__init__(self, message: str, path: typing.Optional[typing.List[typing.Hashable]] = None, error_message: typing.Optional[str] = None, error_type: typing.Optional[str] = None) -> None`: Initializes the validation error with a primary `message`, the optional `path` to the error, the raw `error_message`, and an optional `error_type`.
  - `msg(self) -> str`: Property that returns the **primary error message**.
  - `path(self) -> typing.List[typing.Hashable]`: Property that returns the **path to the error**, as a list of keys in the source data.
  - `error_message(self) -> str`: Property that returns the **actual underlying error message** that was raised, as a string.
  - `__str__(self) -> str`: Returns the string representation of the exception, detailing the error message, type, and the path in the data structure.
  - `prepend(self, path: typing.List[typing.Hashable]) -> None`: **Prepends a list of keys** to the front of the existing error path list.

- `MultipleInvalid(Invalid)`: Exception raised when **multiple validation errors** occur simultaneously.
  - `__init__(self, errors, msg, path, error_type)`: Initializes with a list of underlying `errors`, an optional message, path, and error type.
  - `__iter__(self)`: Allows **iteration over the list of underlying validation errors**.
  - `__len__(self)`: Returns the total **number of contained validation errors**.
  - `__str__(self)`: Returns a string representation that combines the messages of all underlying errors.
  - `prepend(self, path)`: Prepends a path to **all individual errors** contained within this multiple error instance.

- `RequiredFieldInvalid(Invalid)`: The **required field was not provided** in the data.

- `ObjectInvalid(Invalid)`: The object is **not of the expected class**.

- `ContainsInvalid(Invalid)`: The value **does not contain the specified element**.

- `TypeInvalid(Invalid)`: The value is **not of the expected type**.

- `CoerceInvalid(Invalid)`: Failed to **coerce value to type**.

- `AnyInvalid(Invalid)`: The value **did not pass any validator**.

- `AllInvalid(Invalid)`: The value **did not pass all validators**.

- `MatchInvalid(Invalid)`: The value **does not match the given regular expression**.

- `RangeInvalid(Invalid)`: The value is **not in given range**.

- `TrueInvalid(Invalid)`: The value is **not True** (in the Python sense).

- `FalseInvalid(Invalid)`: The value is **not False** (in the Python sense).

- `BooleanInvalid(Invalid)`: The value is **not a boolean**.

- `UrlInvalid(Invalid)`: The value is **not a URL**.

- `EmailInvalid(Invalid)`: The value is **not an email address**.

- `FileInvalid(Invalid)`: The value is **not a file**.

- `DirInvalid(Invalid)`: The value is **not a directory**.

- `PathInvalid(Invalid)`: The value is **not a path**.

- `LiteralInvalid(Invalid)`: The **literal values do not match** the expected value.

- `LengthInvalid(Invalid)`: Indicates an error related to the **length of a value**.

- `DatetimeInvalid(Invalid)`: The value is **not a formatted datetime string**.

- `DateInvalid(Invalid)`: The value is **not a formatted date string**.

- `InInvalid(Invalid)`: Indicates an error because a value is **not in the allowed set of values**.

- `NotInInvalid(Invalid)`: Indicates an error because a value **is in the disallowed set of values**.

- `ExactSequenceInvalid(Invalid)`: Indicates an error where a sequence's **length or element types do not exactly match** the schema.

- `NotEnoughValid(Invalid)`: The value **did not pass enough validations** (used in `SomeOf`).

- `TooManyValid(Invalid)`: The value **passed more than expected validations** (used in `SomeOf`).

## `__init__.py`

The request asks to generate a list of functions/methods and their descriptions for the provided Python code snippet. However, the code snippet consists only of **import statements** from the **`voluptuous`** library and its submodules, along with a version and author attribution. It **does not define any new functions or classes**.

Therefore, I cannot extract any functions or methods from the provided snippet itself. The following response lists the top-level entities imported from the library, which are the primary building blocks for schema definition.

***

## `voluptuous` Imported Entities

The following entities are imported from the `voluptuous` library and are used to build and validate data schemas, as demonstrated in the examples:

- `Schema` (from `voluptuous.schema_builder`):
    - **Description:** The primary class used to define the validation schema for a Python data structure (e.g., `dict`, `list`). It validates the input data against the rules defined within its constructor.

- `All` (from `voluptuous.validators`):
    - **Description:** A validator that requires the input value to pass **all** of the validators it contains. The value is processed sequentially by each validator.

- `Any` (from `voluptuous.validators`):
    - **Description:** A validator that requires the input value to pass **at least one** of the validators it contains. Often used for type checking or enumerating valid literal values.

- `Coerce` (from `voluptuous.validators`):
    - **Description:** A validator that attempts to convert the input value to the specified type or call the specified callable (e.g., `str`, `int`) before further validation.

- `Required` (from `voluptuous.schema_builder`):
    - **Description:** A marker used within a schema dictionary to specify that a key is **mandatory**. It can also specify a default value if the key is missing.

- `Optional` (from `voluptuous.schema_builder`):
    - **Description:** A marker used within a schema dictionary to specify that a key is **optional**. It can also specify a default value if the key is missing.

- `Invalid` (from `voluptuous.error`):
    - **Description:** The base exception class raised by `voluptuous` when validation fails. It provides detailed error messages about why the data failed to match the schema.

- `MultipleInvalid` (from `voluptuous.error`):
    - **Description:** An exception raised when **multiple validation errors** occur simultaneously during schema processing, often by validators like `All`. It contains a list of individual `Invalid` exceptions.

- `REMOVE_EXTRA` (from `voluptuous.schema_builder`):
    - **Description:** A constant that, when passed as a keyword argument to `Schema`, instructs the validator to **remove keys** from the input data that are not defined in the schema.

- `PREVENT_EXTRA` (from `voluptuous.schema_builder`):
    - **Description:** A constant that, when passed as a keyword argument to `Schema`, instructs the validator to **raise an error** if the input data contains keys that are not defined in the schema.

- `ALLOW_EXTRA` (from `voluptuous.schema_builder`):
    - **Description:** A constant that, when passed as a keyword argument to `Schema`, instructs the validator to **allow extra keys** in the input data that are not defined in the schema (this is often the default behavior).

- `Length` (from `voluptuous.validators`):
    - **Description:** A validator that checks the length of a value (e.g., a string or list), often enforcing minimum or maximum bounds.

- `Range` (from `voluptuous.validators`):
    - **Description:** A validator that checks if a numeric value falls within a specified range, often enforcing minimum or maximum bounds.

- `url` (from `voluptuous.validators`):
    - **Description:** A built-in validator for ensuring a string value is a syntactically valid URL.

- `datetime` (from `voluptuous.validators`):
    - **Description:** A validator that parses a string into a Python `datetime` object based on a specified format.

- `Email` (from `voluptuous.validators`):
    - **Description:** A validator for ensuring a string value is a syntactically valid email address.