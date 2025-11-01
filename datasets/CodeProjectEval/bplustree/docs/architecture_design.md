# Architecture Design

Below is a text-based representation of the file tree.

```text
├── bplustree
│   ├── const.py
│   ├── entry.py
│   ├── __init__.py
│   ├── memory.py
│   ├── node.py
│   ├── serializer.py
│   ├── tree.py
│   └── utils.py
```

## `bplustree/__init__.py`

This file contains only imports and exports, no functions or methods.

## `bplustree/const.py`

This file contains only constants and a namedtuple definition, no functions or methods.

## `bplustree/utils.py`

### Module-level functions

- `pairwise(iterable)`:Iterate over elements two by two, yielding consecutive pairs (s0,s1), (s1,s2), (s2,s3), etc.

- `iter_slice(iterable, n)`: Yield slices of size n from a bytes object and indicate if each slice is the last one.

## `bplustree.py` :

### `BPlusTree` Class:  
  Initializes a new **B+ Tree** instance with the given configuration.  
  If the file exists, it loads metadata and reconstructs the tree; otherwise, it initializes a new empty tree structure.

  - `_filename`: Path to the storage file.  
  - `_tree_conf`: Holds structural and serializer configuration for the tree.  
  - `_mem`: Interface for file-based memory management (`FileMemory`).  
  - `_root_node_page`: Page number of the current root node.  
  - `_is_open`: Indicates whether the tree is currently open.  
  - Node and record types (`LonelyRootNode`, `LeafNode`, `InternalNode`, etc.) are assigned dynamically using partials.

### Public API
- `__init__(filename, page_size=4096, order=100, key_size=8, value_size=32, cache_size=64, serializer=None)`:  
  Initializes a new **B+ Tree** instance.  
  If the specified file already contains a serialized tree, its metadata is loaded; otherwise, a new empty tree is created.  
  Configures memory layout and node/record constructors.

  **Args:**
  - `filename (str)`: Path to the file used for persistent storage.  
  - `page_size (int)`: Size of each disk page in bytes (default: 4096).  
  - `order (int)`: Maximum number of children per node.  
  - `key_size (int)`: Fixed size for each serialized key.  
  - `value_size (int)`: Maximum in-page size for values before overflow.  
  - `cache_size (int)`: Number of pages kept in memory for fast access.  
  - `serializer (Serializer, optional)`: Handles encoding/decoding of keys. Defaults to `IntSerializer`.

- `close()`:  
  Safely closes the tree and commits any pending write operations.  
  Prevents redundant closure attempts and logs when already closed.

- `__enter__()`:  
  Enables the tree to be used as a context manager (e.g., `with BPlusTree(...) as tree:`).  
  Returns the current instance.

- `__exit__(exc_type, exc_val, exc_tb)`:  
  Ensures the tree is closed when exiting the context block.

- `checkpoint()`:  
  Performs a **checkpoint operation**, flushing write-ahead logs and synchronizing in-memory data with the disk.

- `insert(key, value, replace=False)`:  
  Inserts a new `(key, value)` pair into the B+ Tree.  
  - If `replace=False` and the key already exists, raises a `ValueError`.  
  - If the value exceeds the configured `value_size`, overflow pages are created to store the data.

- `batch_insert(iterable)`:  
  Efficiently inserts multiple `(key, value)` pairs in ascending key order within a single transaction.  
  Significantly faster than repeated single inserts.  
  Raises `ValueError` if the keys are not sorted or overlap existing keys.

- `get(key, default=None) -> bytes`:  
  Retrieves the value associated with the specified key.  
  Returns `default` if the key is not found.

- `__contains__(item)`:  
  Checks whether a given key exists in the tree.

- `__setitem__(key, value)`:  
  Syntactic sugar for insertion with replacement (`tree[key] = value`).

- `__getitem__(item)`:  
  Retrieves a single value or a dictionary of key-value pairs if a slice is provided.  
  Raises `KeyError` if the key does not exist.

- `__len__()`:  
  Returns the total number of records stored in the B+ Tree by traversing all leaf nodes.

- `__length_hint__()`:  
  Provides an estimated number of records in the tree based on heuristics (used for optimization in Python built-ins).

- `__iter__(slice_=None)`:  
  Returns an iterator over the keys in the tree.  
  Optionally supports slicing (start/stop).

- `keys = __iter__`:  
  Alias for `__iter__`, allowing iteration over keys.

- `items(slice_=None) -> Iterator[tuple]`:  
  Iterates over `(key, value)` pairs, optionally within a specified key range.

- `values(slice_=None) -> Iterator[bytes]`:  
  Iterates over values, optionally within a specified key range.

- `__bool__()`:  
  Returns `True` if the tree contains at least one record; otherwise `False`.

- `__repr__()`:  
  Returns a concise string representation of the tree, including the filename and configuration.

### Internal Methods (Implementation Details)

- `_initialize_empty_tree()`:  
  Creates a new tree with a single `LonelyRootNode` when no metadata is found.  
  Writes the initial metadata to disk.

- `_create_partials()`:  
  Initializes **partial constructors** for tree node and record classes (`LeafNode`, `RootNode`, `Record`, `Reference`, etc.) using the tree configuration for automatic parameter binding.

- `_root_node -> Union[LonelyRootNode, RootNode]`:  
  Property returning the current root node object from memory.

- `_left_record_node -> Union[LonelyRootNode, LeafNode]`:  
  Property returning the **leftmost leaf node** (the first record node in key order).

- `_iter_slice(slice_: slice) -> Iterator[Record]`:  
  Internal generator that iterates through records in the specified key range (`start`, `stop`, `step`).  
  Raises `ValueError` for invalid or backward slices.

- `_search_in_tree(key, node) -> Node`:  
  Recursively searches the tree for the node that should contain the specified key.  
  Traverses internal nodes down to leaf or root nodes.

- `_split_leaf(old_node: Node)`:  
  **Splits a full leaf node** into two, redistributing entries and linking them via `next_page`.  
  If the split occurs at the root, a new root node is created.

- `_split_parent(old_node: Node)`:  
  **Splits a full internal node** when it exceeds the allowed capacity.  
  Promotes the median reference to the parent or creates a new root as needed.

- `_create_new_root(reference: Reference)`:  
  Creates a new root node after a split, inserting the given reference to connect the new child nodes.  
  Updates metadata to persist the new root page.

- `_create_overflow(value: bytes) -> int`:  
  Handles **large value storage** by splitting it across multiple overflow pages.  
  Each page contains a pointer to the next page, ensuring sequential reading.

- `_read_from_overflow(first_overflow_page) -> bytes`:  
  Reconstructs the full byte sequence stored in overflow pages by sequentially reading and concatenating payloads.

- `_get_value_from_record(record: Record) -> bytes`:  
  Returns the full value for a record — either from the in-page data or by reading linked overflow pages.

## `bplustree/entry.py`

### `Entry` class (abstract base class)

- `load(data)`: Abstract method that deserializes bytes into an entry object .

- `dump()`: Abstract method that serializes an entry object to bytes .

- `__eq__(other)`: Compares entries by their keys for equality .

- `__lt__(other)`: Compares entries by their keys for less-than ordering .

- `__le__(other)`: Compares entries by their keys for less-than-or-equal ordering .

- `__gt__(other)`: Compares entries by their keys for greater-than ordering .

- `__ge__(other)`: Compares entries by their keys for greater-than-or-equal ordering .

### `Record` class

- `__init__(tree_conf, key=None, value=None, data=None, overflow_page=None)`: Initializes a Record entry with key-value data, calculating the fixed entry length and optionally loading from serialized data .

- `load(data)`: Deserializes bytes into a Record, extracting the key using the serializer, the value (or overflow page reference), and validating lengths .

- `dump()`: Serializes the Record to bytes, including used key/value lengths, the serialized key, the value (or empty if overflow), and the overflow page reference .

- `__repr__()`: Returns a string representation showing the key and either the value preview, overflow status, or unknown value status .

### `Reference` class

- `__init__(tree_conf, key=None, before=None, after=None, data=None)`: Initializes a Reference entry with a key and page pointers (before/after), calculating the fixed entry length and optionally loading from serialized data .

- `load(data)`: Deserializes bytes into a Reference, extracting the before page number, the key using the serializer, and the after page number .

- `dump()`: Serializes the Reference to bytes, including the before page, used key length, the serialized key, and the after page .

- `__repr__()`: Returns a string representation showing the key, before page, and after page .

## `bplustree/node.py`

### `Node` class (abstract base class)

- `__init__(tree_conf, data=None, page=None, parent=None, next_page=None)`: Initializes a node with configuration, empty entries list, page metadata, and optionally loads from serialized data .

- `load(data)`: Deserializes a page of bytes into a node, extracting the next_page pointer and all entries .

- `dump()`: Serializes the node to a page of bytes, including the node type, used page length, next_page pointer, all entries, and padding .

- `can_add_entry` (property): Returns True if the node has space for another entry based on max_children constraint .

- `can_delete_entry` (property): Returns True if the node can lose an entry without violating min_children constraint .

- `smallest_key` (property): Returns the key of the first entry in the node .

- `smallest_entry` (property): Returns the first entry in the node .

- `biggest_key` (property): Returns the key of the last entry in the node .

- `biggest_entry` (property): Returns the last entry in the node .

- `num_children` (property, abstract): Abstract property that returns the number of children/entries the node has .

- `pop_smallest()`: Removes and returns the first entry from the node .

- `insert_entry(entry)`: Inserts an entry into the node in sorted order using binary search .

- `insert_entry_at_the_end(entry)`: Optimized insertion that appends an entry to the end when it's known to have the largest key .

- `remove_entry(key)`: Removes the entry with the specified key from the node .

- `get_entry(key)`: Retrieves the entry with the specified key, raising ValueError if not found .

- `_find_entry_index(key)`: Uses binary search to find the index of an entry with the given key, raising ValueError if not found .

- `split_entries()`: Splits the entries list in half, keeping the lower half in the node and returning the upper half .

- `from_page_data(tree_conf, data, page)` (class method): Factory method that reads the node type byte and constructs the appropriate node subclass .

- `__repr__()`: Returns a string representation showing the node class name, page number, and entry count .

- `__eq__(other)`: Compares nodes by class, page number, and entries for equality .

### `RecordNode` class

- `__init__(tree_conf, data=None, page=None, parent=None, next_page=None)`: Initializes a RecordNode by setting the entry class to Record and calling the parent constructor .

- `num_children` (property): Returns the number of entries in the node .

### `LonelyRootNode` class

- `__init__(tree_conf, data=None, page=None, parent=None)`: Initializes a LonelyRootNode with node type 1, min_children=0, max_children=order-1 .

- `convert_to_leaf()`: Converts this LonelyRootNode to a LeafNode, preserving entries and page number .

### `LeafNode` class

- `__init__(tree_conf, data=None, page=None, parent=None, next_page=None)`: Initializes a LeafNode with node type 4, min_children=⌈order/2⌉-1, max_children=order-1 .

### `ReferenceNode` class

- `__init__(tree_conf, data=None, page=None, parent=None)`: Initializes a ReferenceNode by setting the entry class to Reference and calling the parent constructor .

- `num_children` (property): Returns the number of entries plus one (since references have before/after pointers) .

- `insert_entry(entry)`: Inserts a Reference entry and maintains pointer consistency by updating adjacent entries' before/after pointers .

### `RootNode` class

- `__init__(tree_conf, data=None, page=None, parent=None)`: Initializes a RootNode with node type 2, min_children=2, max_children=order .

- `convert_to_internal()`: Converts this RootNode to an InternalNode, preserving entries and page number .

### `InternalNode` class

- `__init__(tree_conf, data=None, page=None, parent=None)`: Initializes an InternalNode with node type 3, min_children=⌈order/2⌉, max_children=order .

## `bplustree/serializer.py`

### `Serializer` class (abstract base class)

- `serialize(obj, key_size)`: Abstract method that serializes a key object to bytes .

- `deserialize(data)`: Abstract method that creates a key object from bytes .

- `__repr__()`: Returns a string representation with the class name .

### `IntSerializer` class

- `serialize(obj, key_size)`: Converts an integer to bytes using the configured endianness .

- `deserialize(data)`: Converts bytes back to an integer using the configured endianness .

### `StrSerializer` class

- `serialize(obj, key_size)`: Converts a string to UTF-8 encoded bytes, padded with null bytes to key_size .

- `deserialize(data)`: Converts UTF-8 encoded bytes back to a string, stripping null padding .

### `UUIDSerializer` class

- `serialize(obj, key_size)`: Converts a UUID object to its 16-byte binary representation .

- `deserialize(data)`: Converts 16 bytes back to a UUID object .

### `DatetimeUTCSerializer` class

- `__init__()`:  Initializes the serializer. Checks whether the `temporenc` library is available; if not, raises a `RuntimeError` indicating that the library is required for datetime serialization.

- `serialize(obj, key_size)`: Converts a UTC datetime object to bytes using the temporenc library.

- `deserialize(data)`: Converts bytes back to a UTC datetime object using the temporenc library.

## `bplustree/memory.py`

### `ReachedEndOfFile(Exception)` Class:  
  Custom exception raised when a read operation reaches the end of a file unexpectedly.

### Utility Functions

- `open_file_in_dir(path: str) -> Tuple[io.FileIO, Optional[int]]`:  
  Opens a file and its parent directory for read/write operations.  
  If the file does not exist, it is created. On non-Windows systems, the parent directory is opened for fsync operations to ensure metadata persistence.  
  On Windows, the directory is not opened as it is unnecessary for metadata sync.

- `write_to_file(file_fd: io.FileIO, dir_fileno: Optional[int], data: bytes, fsync: bool=True)`:  
  Writes binary data to a file descriptor, ensuring that the full content is written even if partial writes occur.  
  Optionally performs an `fsync` on both the file and directory to guarantee data persistence on disk.

- `fsync_file_and_dir(file_fileno: int, dir_fileno: Optional[int])`:  
  Synchronizes both the file and its parent directory to disk using `os.fsync()`.  
  Ensures that both file contents and filesystem metadata are flushed.

- `read_from_file(file_fd: io.FileIO, start: int, stop: int) -> bytes`:  
  Reads binary data from a file between byte positions `start` and `stop`.  
  Raises `ReachedEndOfFile` if the read reaches the end of the file unexpectedly.  
  Returns the exact number of bytes requested.

### `FakeCache` Class  
  A dummy cache implementation that does nothing.  
  Used when caching is disabled (`cache_size=0`) to maintain interface compatibility with `cachetools`.

  - `get(k)`: Placeholder method that always returns `None`.  
  - `__setitem__(key, value)`: Placeholder that ignores writes.  
  - `clear()`: Placeholder that performs no cache clearing.

### `FileMemory` Class

- `FileMemory(filename: str, tree_conf: TreeConf, cache_size: int=512)`:  
  Manages persistent memory storage for B+ Tree nodes and pages using a file-backed structure.  
  Provides transactional read/write operations with an integrated Write-Ahead Log (WAL).  
  Supports optional caching of deserialized nodes to improve performance.

  #### Instance Attributes:
  - `_filename`: Path to the tree data file.  
  - `_tree_conf`: Configuration object defining page and key/value structure.  
  - `_lock`: Reader-writer lock (`rwlock.RWLock`) for concurrent transaction safety.  
  - `_cache`: LRU cache or dummy cache for node reuse.  
  - `_fd`, `_dir_fd`: File and directory descriptors for I/O operations.  
  - `_wal`: Write-Ahead Log manager (`WAL`).  
  - `last_page`: The highest allocated page number in the tree file.

- `__init__(filename: str, tree_conf: TreeConf, cache_size: int=512)`:  
  Initializes a new instance of the `FileMemory` class, which manages persistent, file-based storage for B+ Tree pages and nodes.  
  The constructor sets up the file structure, caching layer, and write-ahead log (WAL) for crash-safe transactions.

- `get_node(page: int)`:  
  Retrieves a node object from disk or cache.  
  Deserializes page data into a `Node` if not cached.  
  Uses the WAL to check for modified (uncommitted) pages first.

- `set_node(node: Node)`:  
  Writes a node to the WAL and updates the cache.  
  Ensures that modifications are stored transactionally.

- `set_page(page: int, data: bytes)`:  
  Writes raw page data directly to the WAL.  
  Typically used for writing overflow pages.

- `get_page(page: int) -> bytes`:  
  Reads a page from the WAL if available, otherwise from the main tree file.

- `read_transaction`:  
  A context manager for safe concurrent **read operations**.  
  Acquires a read lock during its lifetime.

- `write_transaction`:  
  A context manager for atomic **write operations**.  
  Acquires a write lock, and commits or rolls back changes in the WAL on exit.  
  - On exception: Rolls back all uncommitted changes and clears the cache.  
  - On success: Commits changes to the WAL and releases the lock.

- `next_available_page -> int`:  
  Returns the next available page index and increments the internal counter.

- `get_metadata() -> tuple`:  
  Reads and returns metadata (root node page and `TreeConf` settings) from page 0 of the tree file.  
  Raises `ValueError` if the metadata is not yet initialized.

- `set_metadata(root_node_page: int, tree_conf: TreeConf)`:  
  Writes the root node page number and tree configuration to the first page of the file.  
  Ensures that metadata is persisted on disk via `fsync`.

- `close()`:  
  Performs a final checkpoint to flush data to disk, then closes all file and directory descriptors.

- `perform_checkpoint(reopen_wal=False)`:  
  Transfers all committed pages from the WAL back into the main tree file, ensuring data consistency.  
  Optionally reopens a new WAL file after checkpointing.

- `_read_page(page: int) -> bytes`:  
  Reads a full page of data from the tree file based on its page index.

- `_write_page_in_tree(page: int, data: Union[bytes, bytearray], fsync: bool=True)`:  
  Writes raw page data directly into the tree file at the specified position.  
  Used during checkpoint operations and metadata writes.

- `__repr__()`:  
  Returns a string representation of the `FileMemory` instance, including the filename.

### `FrameType` Enum

- `FrameType(enum.Enum)`:  
  Enumeration representing the types of frames used in the Write-Ahead Log (WAL):
  - `PAGE`: Represents a page modification frame.  
  - `COMMIT`: Indicates a transaction commit frame.  
  - `ROLLBACK`: Indicates a rollback frame.

---

### `WAL` Class

- `WAL(filename: str, page_size: int)`:  
  Implements a **Write-Ahead Log** mechanism to ensure data integrity during write transactions.  
  Tracks committed and uncommitted page modifications.  
  Enables recovery of uncommitted data if the tree was not closed properly.

  #### Instance Attributes:
  - `filename`: The WAL file name (appends `-wal` to the main tree filename).  
  - `_fd`, `_dir_fd`: File and directory descriptors for WAL I/O.  
  - `_page_size`: Page size in bytes.  
  - `_committed_pages`: Dictionary of committed page offsets.  
  - `_not_committed_pages`: Dictionary of uncommitted page offsets.  
  - `needs_recovery`: Boolean indicating whether recovery is required (based on existing WAL content).

- `__init__(filename: str, page_size: int)`:  
  Initializes a new instance of the `WAL` (Write-Ahead Log) class, which provides transactional durability for the B+ Tree by recording page modifications before they are written to the main tree file.  
  The constructor ensures that an existing WAL file is properly loaded and recovered if the previous process terminated unexpectedly.

- `checkpoint()`:  
  Transfers committed pages back to the tree file, closes the WAL, and deletes the WAL file.  
  Yields `(page_number, page_data)` pairs during the transfer process.

- `_create_header()`:  
  Writes the WAL file header, which includes the configured page size.  
  Ensures the header is synchronized to disk.

- `_load_wal()`:  
  Loads and validates the WAL file upon startup.  
  Reads the header and sequentially loads all frames.  
  Discards any uncommitted frames after recovery.

- `_load_next_frame()`:  
  Reads the next frame header and determines its type (`PAGE`, `COMMIT`, or `ROLLBACK`).  
  Advances the file pointer accordingly and indexes the frame for later reference.

- `_index_frame(frame_type: FrameType, page: int, page_start: int)`:  
  Updates internal tracking dictionaries based on frame type:  
  - `PAGE`: Adds to uncommitted pages.  
  - `COMMIT`: Moves uncommitted pages to committed.  
  - `ROLLBACK`: Clears uncommitted pages.

- `_add_frame(frame_type: FrameType, page: Optional[int]=None, page_data: Optional[bytes]=None)`:  
  Appends a new frame to the WAL file.  
  Validates page data size and writes the corresponding binary frame to disk.  
  Updates internal tracking after the write.

- `get_page(page: int) -> Optional[bytes]`:  
  Retrieves a page’s data from either uncommitted or committed frames.  
  Returns `None` if the page does not exist in the WAL.

- `set_page(page: int, page_data: bytes)`:  
  Adds a `PAGE` frame to the WAL for a modified page.  
  Used when nodes or pages are updated during a transaction.

- `commit()`:  
  Writes a `COMMIT` frame to persist all uncommitted pages.  
  No-op if there are no pending modifications.

- `rollback()`:  
  Writes a `ROLLBACK` frame to discard all uncommitted pages.  
  No-op if there are no pending modifications.

- `__repr__()`:  
  Returns a string representation of the WAL instance, including the WAL filename.