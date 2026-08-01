# PRD Document for voluptuous

## Introduction

The purpose of this project is to develop a Python data validation library that provides a declarative schema definition system for validating and transforming complex data structures. The repository provides a comprehensive validation framework with support for nested structures, custom validators, and detailed error reporting. This tool is designed for Python developers who need to validate configuration files, API inputs, user data, or any structured data against predefined schemas.

## Goals

The objective of this project is to provide a robust, flexible validation system that allows developers to define schemas declaratively, validate data structures with automatic type checking and transformation, and receive detailed error messages with precise path information. The library should support complex nested structures, custom validators, and provide both compile-time schema optimization and runtime validation. 

## Features and Functionalities

The following features and functionalities are expected in the project:

### Core Validation
- Ability to validate dictionaries with required and optional keys
- Ability to validate lists, tuples, and sequences with multiple validator options
- Ability to validate sets and frozensets 
- Ability to validate scalar values (primitives, types, callables)
- Ability to validate nested data structures recursively 

### Schema Definition
- Ability to define schemas using Python dictionaries, lists, tuples, and sets 
- Ability to mark dictionary keys as `Required`, `Optional`, `Exclusive`, `Inclusive`, or `Remove` 
- Ability to control extra key handling with `PREVENT_EXTRA`, `ALLOW_EXTRA`, or `REMOVE_EXTRA` 
- Ability to use `Extra` marker for wildcard key matching  
- Ability to use `Self` token for recursive schema references  

### Built-in Validators
- Ability to validate with type checking (int, str, bool, etc.)
- Ability to validate dates and datetimes with custom formats 
- Ability to validate email addresses 
- Ability to validate URLs  
- Ability to validate ranges and clamp values 
- Ability to validate string patterns with regex matching  
- Ability to validate file and directory paths 

### Composite Validators
- Ability to combine validators with `All` (all must pass) 
- Ability to combine validators with `Any` (at least one must pass)
- Ability to use `Union` for type unions 
- Ability to use `SomeOf` for partial validation 

### Data Transformation
- Ability to coerce values to specific types  
- Ability to transform strings (capitalize, lower, upper, strip, title) 
- Ability to replace values conditionally 
- Ability to remove keys from output 

### Error Handling
- Ability to collect multiple validation errors 
- Ability to track error paths through nested structures 
- Ability to provide custom error messages 
- Ability to humanize error messages 

### Schema Extension
- Ability to extend existing schemas  
- Ability to infer schemas from concrete data 

## Technical Constraints

- The repository should use Python as the primary programming language
- The repository should support Python 3.6+ 
- The repository should provide a two-phase compilation and validation architecture for performance 

## Requirements

### Dependencies

The library has minimal external dependencies and primarily uses Python standard library components.<cite/>

### Development Dependencies

- `pytest` - Testing framework

## Contribution to Documentation

Documentation is built using `Sphinx`. You can install it by

    pip install -r requirements.txt

For building `sphinx-apidoc` from scratch you need to set PYTHONPATH to `voluptuous/voluptuous` repository.

## Usage

### Basic Validation

Define a schema and validate data:
```python
from voluptuous import Schema

schema = Schema({'name': str, 'age': int})
schema({'name': 'John', 'age': 30})  # Valid
``` 

### Dictionary Validation with Markers

Use `Required` and `Optional` markers:
```python
from voluptuous import Schema, Required, Optional

schema = Schema({
    Required('name'): str,
    Optional('age'): int
})
```

### Sequence Validation

Validate lists with multiple possible validators:
```python
schema = Schema(['one', 'two', int])
schema(['one'])  # Valid
schema([1])      # Valid
``` 

### Date and Datetime Validation

Validate dates with custom formats:
```python
from voluptuous import Schema, Date, Datetime

schema = Schema({
    'date': Date('%Y%m%d'),
    'datetime': Datetime()
})
``` 

### Composite Validators

Combine multiple validators:
```python
from voluptuous import Schema, All, Range

schema = Schema(All(int, Range(min=0, max=100)))
```

### Error Handling

Handle validation errors with path information:
```python
from voluptuous import Schema, MultipleInvalid

schema = Schema({'key': int})
try:
    schema({'key': 'not an int'})
except MultipleInvalid as e:
    print(e.errors[0].path)  # ['key']
```

## Terms/Concepts Explanation

**Schema**: A declarative definition of the expected structure and types of data, compiled into optimized validator functions. 

**Validator**: A callable that validates and optionally transforms a value, raising `Invalid` on validation failure.

**Marker**: A wrapper object (`Required`, `Optional`, `Exclusive`, `Inclusive`, `Remove`) that adds metadata to schema keys.  

**Compilation Phase**: The one-time process of transforming a schema definition into optimized validator functions. 

**Validation Phase**: The runtime execution of compiled validators against input data. 

**Path Tracking**: The mechanism for tracking the current location in nested data structures for precise error reporting. 

**Extra Keys**: Dictionary keys not defined in the schema, handled according to `PREVENT_EXTRA`, `ALLOW_EXTRA`, or `REMOVE_EXTRA` settings. 