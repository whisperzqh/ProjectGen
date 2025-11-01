## Introduction

This document outlines the product requirements for `TinyDB`, a lightweight document-oriented database optimized for simplicity and ease of use. The project aims to provide a simple yet powerful database solution for small Python applications that don't require the complexity of SQL databases or external database servers.

## Goals

The primary goal of TinyDB is to offer a tiny, document-oriented database that is optimized for developer happiness by providing a simple and clean API. It aims to assist developers building small applications by eliminating the need for external database servers or complex SQL configurations.

## Features and Functionalities

- **Document-Oriented Storage**: Store any document represented as Python `dict` objects, similar to MongoDB.

- **Rich Query Language**: Support for complex queries including field comparisons, logical operations (AND, OR, NOT), regex matching, and custom test functions.

- **Multiple Tables**: Ability to organize data into multiple named tables within a single database.

- **No External Dependencies**: Written in pure Python with no external dependencies from PyPI, using only the Python standard library.

- **Extensible Storage System**: Support for custom storage backends through a clean storage interface, with built-in JSON and memory storage options.

- **Middleware Support**: Ability to extend storage functionality through middleware, including built-in caching middleware for performance optimization.

- **Cross-Platform Compatibility**: Works on Python 3.8+ and PyPy3 across all operating systems.

- **Type Safety**: Includes MyPy type annotations for static type checking.

## Core Architecture

TinyDB follows a layered architecture with these main components:

- **TinyDB Class**: Main entry point managing storage and providing access to tables.
- **Table Class**: Handles CRUD operations (insert, search, get, update, remove, all) on document collections.
- **Query System**: Provides an intuitive query language for filtering documents.
- **Storage Interface**: Abstraction layer supporting different persistence mechanisms (JSON files, memory, custom).
- **Middleware Pattern**: Allows extending storage functionality (e.g., caching).

## Usage

```python
>>> from tinydb import TinyDB, Query
>>> db = TinyDB('/path/to/db.json')
>>> db.insert({'int': 1, 'char': 'a'})
>>> db.insert({'int': 1, 'char': 'b'})

# Query Language

>>> User = Query()
>>> # Search for a field value
>>> db.search(User.name == 'John')
[{'name': 'John', 'age': 22}, {'name': 'John', 'age': 37}]

>>> # Combine two queries with logical and
>>> db.search((User.name == 'John') & (User.age <= 30))
[{'name': 'John', 'age': 22}]

>>> # Combine two queries with logical or
>>> db.search((User.name == 'John') | (User.name == 'Bob'))
[{'name': 'John', 'age': 22}, {'name': 'John', 'age': 37}, {'name': 'Bob', 'age': 42}]

>>> # Negate a query with logical not
>>> db.search(~(User.name == 'John'))
[{'name': 'Megan', 'age': 27}, {'name': 'Bob', 'age': 42}]

>>> # Apply transformation to field with `map`
>>> db.search((User.age.map(lambda x: x + x) == 44))
>>> [{'name': 'John', 'age': 22}]

>>> # More possible comparisons:  !=  <  >  <=  >=
>>> # More possible checks: where(...).matches(regex), where(...).test(your_test_func)

# Tables

>>> table = db.table('name')
>>> table.insert({'value': True})
>>> table.all()
[{'value': True}]

# Using Middlewares

>>> from tinydb.storages import JSONStorage
>>> from tinydb.middlewares import CachingMiddleware
>>> db = TinyDB('/path/to/db.json', storage=CachingMiddleware(JSONStorage))
```

## Requirements

### Dependencies
- Python 3.8 or higher
- No external runtime dependencies (pure Python standard library)

### Development Dependencies
- pytest for testing
- sphinx for documentation
- MyPy for type checking

## Design and User Interface

As a backend library, TinyDB does not have a GUI. The interface is through Python classes and methods following Pythonic design principles for simplicity and readability. The API is designed to be intuitive and clean, with a focus on developer experience.
