# Architecture Design

Below is a text-based representation of the file tree. 
```bash
├── tinydb
│   ├── database.py
│   ├── __init__.py
│   ├── middlewares.py
│   ├── mypy_plugin.py
│   ├── operations.py
│   ├── py.typed
│   ├── queries.py
│   ├── storages.py
│   ├── table.py
│   ├── utils.py
│   └── version.py
```

`__init__.py` :

`database.py` :

- `TinyDB`: The main class of TinyDB, responsible for managing storage, tables, and providing access to the default table. It acts as a wrapper around the underlying storage system and forwards unknown attribute accesses to the default table.

  - `table(name: str, **kwargs) -> Table`: Returns a table instance for the given table name. If the table does not yet exist in memory, it is created using the configured `table_class` and stored for future access. Additional keyword arguments are passed to the table constructor.

  - `tables() -> Set[str]`: Returns a set containing the names of all tables currently present in the database by reading the top-level keys from the storage backend. Returns an empty set if the storage is uninitialized or empty.

  - `drop_tables() -> None`: Deletes all tables from the database by overwriting the entire storage with an empty dictionary. This action is irreversible and also clears the internal `_tables` cache.

  - `drop_table(name: str) -> None`: Deletes a specific table from the database by removing its entry from the storage data. If the table exists in the internal `_tables` cache, it is also removed. This operation cannot be undone.

  - `storage -> Storage`: A property that returns the storage instance currently used by the database (e.g., `JSONStorage`).

  - `close() -> None`: Closes the database by marking it as closed and calling the `close()` method on the storage instance, which may release resources such as file handles.

  - `__enter__()`: Enables the use of `TinyDB` as a context manager. Returns the instance itself.

  - `__exit__(*args)`: Automatically calls `close()` when exiting a `with` block, ensuring proper cleanup if the database is still open.

  - `__getattr__(name)`: Forwards any attribute access not found on the `TinyDB` instance to the default table (named `_default` by default), enabling direct method calls like `db.insert(...)`.

  - `__len__() -> int`: Returns the number of documents in the default table by delegating to `len(default_table)`.

  - `__iter__() -> Iterator[Document]`: Returns an iterator over the documents in the default table, allowing iteration directly on the `TinyDB` instance.

- `TableBase`: A type hint alias created using `with_typehint(Table)` to improve IDE and static type checker support for `TinyDB`’s dynamic delegation to `Table`. It is not a functional component but aids in type inference.

`middlewares.py` :

- `Middleware`: The base class for all middleware components in TinyDB. It acts as a wrapper around a storage class, allowing interception and modification of read/write operations. Middlewares are designed to be chained and must call the parent constructor in their `__init__`.

  - `__init__(self, storage_cls)`: Initializes the middleware with a storage class (not an instance). The actual storage instance is created later via `__call__`.

  - `__call__(self, *args, **kwargs)`: Called by TinyDB to instantiate the underlying storage. It creates an instance of the wrapped storage class using the provided arguments and stores it in `self.storage`, then returns `self` to maintain the middleware chain.

  - `__getattr__(self, name)`: Forwards any attribute access not defined on the middleware to the underlying storage instance, ensuring transparency.

- `CachingMiddleware(Middleware)`: A middleware that adds write-through caching to improve performance by reducing disk I/O. It caches database reads and batches writes, flushing to disk only after a configurable number of modifications.

  - `__init__(self, storage_cls)`: Calls the parent constructor and initializes an empty cache (`self.cache = None`) and a write counter (`_cache_modified_count = 0`).

  - `read(self)`: Returns data from the internal cache. If the cache is empty (`None`), it reads from the underlying storage and populates the cache.

  - `write(self, data)`: Stores the given data in the cache and increments the modification counter. If the counter reaches `WRITE_CACHE_SIZE` (default: 1000), it automatically flushes the cache to disk.

  - `flush(self)`: Forces all cached data to be written to the underlying storage and resets the modification counter. Only writes if there are pending changes.

  - `close(self)`: Ensures any unwritten data is flushed to disk and then delegates the `close()` call to the underlying storage to release resources (e.g., file handles).

`mypy_plugin.py` :

- `TinyDBPlugin(Plugin)`: A MyPy plugin class that enhances type checking for TinyDB, specifically to support the `with_typehint` utility used for dynamic class aliasing with proper type inference.

  - `__init__(self, options: Options)`: Initializes the plugin with MyPy options and sets up an internal dictionary `named_placeholders` (currently unused but reserved for potential future use).

  - `get_dynamic_class_hook(self, fullname: str) -> Optional[Callable[[DynamicClassDefContext], None]]`: Registers a dynamic class definition hook for the function `tinydb.utils.with_typehint`. When MyPy encounters this function during type checking, the hook ensures that the resulting alias (e.g., `TableBase`) is treated as a proper type alias of the original class (e.g., `Table`), enabling accurate type inference in IDEs and static analysis tools.

    - The inner `hook(ctx: DynamicClassDefContext)` function:
      - Extracts the class passed as the first argument to `with_typehint`.
      - Verifies it is a `NameExpr` (i.e., a named class reference).
      - Looks up the fully qualified type in MyPy’s symbol table.
      - Registers the new alias (e.g., `TableBase`) in the current scope with the same type information as the original class.

- `plugin(_version: str)`: The entry point function required by MyPy to load the plugin. It returns the `TinyDBPlugin` class so MyPy can instantiate it during type checking.

`operations.py` :

- `delete(field)`: Returns a transformation function that deletes the specified field from a document. Used in `db.update()` to remove a key from matching documents.

- `add(field, n)`: Returns a transformation function that adds the value `n` to the specified numeric field in a document. Used in `db.update()` to increment a field by a given amount.

- `subtract(field, n)`: Returns a transformation function that subtracts the value `n` from the specified numeric field in a document. Used in `db.update()` to decrement a field by a given amount.

- `set(field, val)`: Returns a transformation function that sets the specified field in a document to the given value `val`. Used in `db.update()` to assign a new value to a field.

- `increment(field)`: Returns a transformation function that increments the specified numeric field in a document by 1. Equivalent to `add(field, 1)`.

- `decrement(field)`: Returns a transformation function that decrements the specified numeric field in a document by 1. Equivalent to `subtract(field, 1)`.

`queries.py` :

- `is_sequence(obj)`: A helper function that checks whether an object is iterable (i.e., has an `__iter__` method). Used internally to determine if a field value is a list or similar sequence type.

- `QueryLike(Protocol)`: A typing protocol that defines the interface for query-like objects. Any object conforming to this protocol must be callable (accepting a `Mapping` and returning `bool`) and hashable. This enables MyPy to correctly type-check query usage in TinyDB.

- `QueryInstance`: Represents a fully constructed, executable query. It encapsulates a test function and a hashable descriptor for caching and comparison. Query instances are generated by the `Query` class and support logical operations.

  - `__init__(self, test: Callable[[Mapping], bool], hashval: Optional[Tuple])`: Initializes the query instance with a test function and an optional hashable value used for caching and equality.

  - `is_cacheable(self) -> bool`: Returns `True` if the query has a stable hash value and can be safely cached.

  - `__call__(self, value: Mapping) -> bool`: Executes the query against a document (dictionary-like object) and returns `True` if it matches.

  - `__hash__(self) -> int`: Returns a stable hash based on the internal `hashval`, enabling use as dictionary keys in query caches.

  - `__repr__(self)`: Returns a string representation showing the internal hash structure.

  - `__eq__(self, other)`: Compares two query instances for equality based on their `hashval`.

  - `__and__(self, other: 'QueryInstance') -> 'QueryInstance'`: Combines two queries with logical AND. Produces a cacheable query if both operands are cacheable.

  - `__or__(self, other: 'QueryInstance') -> 'QueryInstance'`: Combines two queries with logical OR. Produces a cacheable query if both operands are cacheable.

  - `__invert__(self) -> 'QueryInstance'`: Inverts the query logic using logical NOT. Preserves cacheability if the original is cacheable.

- `Query(QueryInstance)`: A query builder class that constructs `QueryInstance` objects through attribute access or indexing. Supports fluent query construction like `Query().name == 'John'`.

  - `__init__(self)`: Initializes an empty query path and sets a placeholder test function that raises an error if evaluated prematurely.

  - `__repr__(self)`: Returns a string like `Query()` for clarity.

  - `__hash__(self)`: Delegates to the parent `QueryInstance.__hash__`.

  - `__getattr__(self, item: str)`: Dynamically extends the query path by treating attribute access (e.g., `.name`) as a field lookup in documents.

  - `__getitem__(self, item: str)`: Provides alternative syntax for field access (e.g., `['name']`) that behaves identically to `__getattr__`.

  - `_generate_test(self, test: Callable[[Any], bool], hashval: Tuple, allow_empty_path: bool = False) -> QueryInstance`: Internal helper that builds a `QueryInstance` by first traversing the query path in a document and then applying the given test function.

  - `__eq__(self, rhs: Any)`: Creates a query that tests for equality of a field value with `rhs`.

  - `__ne__(self, rhs: Any)`: Creates a query that tests for inequality of a field value with `rhs`.

  - `__lt__(self, rhs: Any)`: Creates a query that tests if a field value is less than `rhs`.

  - `__le__(self, rhs: Any)`: Creates a query that tests if a field value is less than or equal to `rhs`.

  - `__gt__(self, rhs: Any)`: Creates a query that tests if a field value is greater than `rhs`.

  - `__ge__(self, rhs: Any)`: Creates a query that tests if a field value is greater than or equal to `rhs`.

  - `exists(self) -> QueryInstance`: Creates a query that checks whether the specified field exists in the document.

  - `matches(self, regex: str, flags: int = 0) -> QueryInstance`: Creates a query that matches the entire field value against a regular expression using `re.match`.

  - `search(self, regex: str, flags: int = 0) -> QueryInstance`: Creates a query that checks if the field value contains a substring matching a regular expression using `re.search`.

  - `test(self, func: Callable[[Any], bool], *args) -> QueryInstance`: Creates a query that applies a user-defined test function to the field value, optionally with extra arguments.

  - `any(self, cond: Union[QueryInstance, List[Any]]) -> QueryInstance`: Creates a query that checks if any element in a list-valued field satisfies a condition (either another query or membership in a list).

  - `all(self, cond: Union[QueryInstance, List[Any]]) -> QueryInstance`: Creates a query that checks if all elements in a list-valued field satisfy a condition (either another query or are contained in a given list).

  - `one_of(self, items: List[Any]) -> QueryInstance`: Creates a query that checks if the field value is present in a given list of allowed values.

  - `fragment(self, document: Mapping) -> QueryInstance`: Creates a query that checks if the document contains at least the key-value pairs specified in `document` (i.e., a partial match or "fragment").

  - `noop(self) -> QueryInstance`: Returns a query that always evaluates to `True`. Useful as a neutral element when building queries dynamically.

  - `map(self, fn: Callable[[Any], Any]) -> 'Query'`: Extends the query path by applying a callable transformation to the current value during traversal. This is useful for custom field processing. Note: queries using `map` are not cacheable.

- `where(key: str) -> Query`: A convenience function that returns `Query()[key]`, enabling a more concise syntax for simple field queries (e.g., `where('name') == 'John'`).

`storages.py` :

- `touch(path: str, create_dirs: bool)`: A utility function that ensures a file exists at the given `path`. If `create_dirs` is `True`, it also creates any missing parent directories. The file is created by opening it in append mode (`'a'`), which does not alter existing content.

- `Storage`: An abstract base class defining the interface for all storage backends in TinyDB. Subclasses must implement `read()` and `write()`; `close()` is optional.

  - `read(self) -> Optional[Dict[str, Dict[str, Any]]]`: Abstract method that reads and deserializes the database state. Must return `None` if the storage is empty or uninitialized.

  - `write(self, data: Dict[str, Dict[str, Any]]) -> None`: Abstract method that serializes and writes the full database state to the storage medium.

  - `close(self) -> None`: Optional method for cleaning up resources (e.g., closing file handles). The default implementation does nothing.

- `JSONStorage(Storage)`: A concrete storage implementation that persists data in a JSON file on disk.

  - `__init__(self, path: str, create_dirs=False, encoding=None, access_mode='r+', **kwargs)`: Initializes the storage with a file path and optional settings. Creates the file (and parent directories if `create_dirs=True`) when the access mode permits writing. Issues a warning if an unsafe access mode (e.g., `'w'`) is used.

  - `close(self) -> None`: Closes the underlying file handle.

  - `read(self) -> Optional[Dict[str, Dict[str, Any]]]`: Reads the JSON file. Returns `None` if the file is empty; otherwise, returns the parsed JSON as a dictionary.

  - `write(self, data: Dict[str, Dict[str, Any]]) -> None`: Writes the given data to the file as JSON. Overwrites the file contents, flushes to disk, and truncates any leftover data to prevent corruption.

- `MemoryStorage(Storage)`: An in-memory storage implementation useful for testing or temporary databases. Data is not persisted across sessions.

  - `__init__(self)`: Initializes an empty `memory` attribute to hold the database state.

  - `read(self) -> Optional[Dict[str, Dict[str, Any]]]`: Returns the current in-memory data (or `None` if never written).

  - `write(self, data: Dict[str, Dict[str, Any]]) -> None`: Stores a copy of the provided data in memory, replacing any previous state.

`table.py` :

- `Document(dict)`: A subclass of `dict` that represents a document in the database and additionally stores its document ID as the `doc_id` attribute.

  - `__init__(self, value: Mapping, doc_id: int)`: Initializes the document with the given data (`value`) and assigns the provided `doc_id`.

- `Table`: Represents a single table in a TinyDB database, providing methods to insert, update, search, and remove documents.

  - `__init__(self, storage: Storage, name: str, cache_size: int = 10, persist_empty: bool = False)`: Initializes a new table with the given name and storage backend. Sets up a query cache and optionally persists an empty table immediately if `persist_empty=True`.

  - `__repr__(self)`: Returns a string representation of the table showing its name, document count, and storage backend.

  - `name -> str`: Property that returns the table’s name.

  - `storage -> Storage`: Property that returns the storage instance used by this table.

  - `insert(self, document: Mapping) -> int`: Inserts a single document into the table and returns its assigned document ID. If the input is a `Document` instance, its `doc_id` is respected.

  - `insert_multiple(self, documents: Iterable[Mapping]) -> List[int]`: Inserts multiple documents and returns a list of their assigned document IDs.

  - `all(self) -> List[Document]`: Returns a list of all documents in the table.

  - `search(self, cond: QueryLike) -> List[Document]`: Searches for all documents matching the given query condition. Uses a query cache for performance; only cacheable queries are stored.

  - `get(self, cond: Optional[QueryLike] = None, doc_id: Optional[int] = None, doc_ids: Optional[List] = None) -> Optional[Union[Document, List[Document]]]`: Retrieves one or more documents by query, single ID, or list of IDs. Returns `None` if no match is found (except for `doc_ids`, which returns a list).

  - `contains(self, cond: Optional[QueryLike] = None, doc_id: Optional[int] = None) -> bool`: Checks whether a document matching the given condition or ID exists in the table.

  - `update(self, fields: Union[Mapping, Callable[[Mapping], None]], cond: Optional[QueryLike] = None, doc_ids: Optional[Iterable[int]] = None) -> List[int]`: Updates documents matching a query or list of IDs. The `fields` argument can be a dictionary of updates or a callable that modifies the document in place. Returns a list of updated document IDs.

  - `update_multiple(self, updates: Iterable[Tuple[Union[Mapping, Callable], QueryLike]]) -> List[int]`: Applies multiple update operations, each consisting of update data/function and a query condition. Returns a list of affected document IDs.

  - `upsert(self, document: Mapping, cond: Optional[QueryLike] = None) -> List[int]`: Updates documents matching the condition if they exist; otherwise, inserts the document as new. If the document is a `Document` with a `doc_id`, it attempts to update that specific document.

  - `remove(self, cond: Optional[QueryLike] = None, doc_ids: Optional[Iterable[int]] = None) -> List[int]`: Removes documents matching a query or a list of document IDs. Returns the list of removed document IDs.

  - `truncate(self) -> None`: Removes all documents from the table and resets the internal document ID counter.

  - `count(self, cond: QueryLike) -> int`: Counts the number of documents matching the given query by delegating to `search()` and returning the length of the result.

  - `clear_cache(self) -> None`: Clears the internal query result cache.

  - `__len__(self) -> int`: Returns the total number of documents in the table.

  - `__iter__(self) -> Iterator[Document]`: Returns an iterator over all documents in the table, yielding each as a `Document` instance.

  - `_get_next_id(self) -> int`: Determines and returns the next available document ID, either from an internal counter or by scanning existing IDs in the table.

  - `_read_table(self) -> Dict[str, Mapping]`: Reads the raw table data from storage without converting document IDs or wrapping documents in the `Document` class.

  - `_update_table(self, updater: Callable[[Dict[int, Mapping]], None]) -> None`: Performs a read-modify-write cycle on the table:
    - Reads the full database from storage.
    - Extracts this table’s data and converts document IDs to the configured ID type.
    - Applies the `updater` function to modify the table.
    - Converts IDs back to strings (for JSON compatibility) and writes the updated database back.
    - Clears the query cache afterward to ensure consistency.

`utils.py` :

- `with_typehint(baseclass: Type[T])`: A utility function that enables type checkers to treat a class as if it inherits from `baseclass` for the purpose of type inference, while at runtime it simply inherits from `object`. This is used to add type hints to dynamically constructed classes (e.g., `TableBase = with_typehint(Table)`). MyPy support is provided via a custom plugin (`mypy_plugin.py`).

- `LRUCache(abc.MutableMapping, Generic[K, V])`: A thread-unsafe, least-recently-used (LRU) cache implementation with a fixed capacity, backed by `collections.OrderedDict`. It behaves like a dictionary but automatically evicts the least recently accessed item when exceeding its capacity.

  - `__init__(self, capacity=None)`: Initializes the cache with an optional maximum capacity. If `None`, the cache is unbounded.

  - `lru -> List[K]`: Property that returns a list of keys in access order (least to most recent).

  - `length -> int`: Property that returns the current number of entries in the cache.

  - `clear(self) -> None`: Empties the cache.

  - `__len__(self) -> int`: Returns the number of items in the cache.

  - `__contains__(self, key) -> bool`: Checks if a key exists in the cache.

  - `__setitem__(self, key: K, value: V) -> None`: Adds or updates a key-value pair, marking it as most recently used.

  - `__delitem__(self, key: K) -> None`: Removes a key from the cache.

  - `__getitem__(self, key) -> V`: Retrieves a value by key, raising `KeyError` if not found, and marks the key as recently used.

  - `__iter__(self) -> Iterator[K]`: Returns an iterator over the cache keys.

  - `get(self, key: K, default: Optional[D] = None) -> Optional[Union[V, D]]`: Retrieves a value by key, returning `default` if not found, and moves the key to the end (most recent) if present.

  - `set(self, key: K, value: V)`: Inserts or updates a key-value pair. If the cache exceeds its capacity after insertion, the least recently used item (first in order) is removed.

- `FrozenDict(dict)`: An immutable dictionary subclass that supports hashing by freezing its contents. Used to make dictionary-based query components hashable for caching.

  - `__hash__(self) -> int`: Returns a hash computed from a sorted tuple of all key-value pairs.

  - `_immutable(self, *args, **kws)`: Helper method that raises a `TypeError` when any mutation is attempted.

  - `__setitem__`, `__delitem__`, `clear`, `setdefault`, `popitem`, `update`, `pop`: All overridden to raise `TypeError`, enforcing immutability.

- `freeze(obj)`: Recursively converts mutable objects into immutable, hashable equivalents:
  - `dict` → `FrozenDict` (with values also frozen),
  - `list` → `tuple` (with elements frozen),
  - `set` → `frozenset`,
  - Other types are returned unchanged.
  Used primarily to generate stable hashes for query objects containing nested data structures.

`version.py` :