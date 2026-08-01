# Architecture Design
Below is a text-based representation of the file tree.
```text
.
├── portalocker
│   ├── __about__.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── portalocker.py
│   ├── py.typed
│   ├── redis.py
│   ├── types.py
│   └── utils.py
```

## `__about__.py`

`__about__.py` :

- `_read_pyproject_version(path)`: Reads and extracts the package version from a local `pyproject.toml` file if available.  
  Uses a lightweight regex-based parser to find the `[project]` table and return the `version` value, avoiding external dependencies.  
  Returns `None` if the version cannot be determined.

- `get_version()`: Determines the runtime version of the `portalocker` package.  

## `__init__.py` :

- This module defines the public interface of the Portalocker package, which provides cross-platform file locking utilities and related synchronization primitives. It imports internal components, re-exports key classes and functions, defines constants for lock modes, and exposes metadata about the package.

## `__main__.py`

- `main(argv: typing.Sequence[str] | None = None) -> None`: The main function for the command-line interface, which sets up an argument parser for the `combine` subcommand and executes the corresponding function.
  
- `_read_file(path: pathlib.Path, seen_files: set[pathlib.Path]) -> typing.Iterator[str]`: Recursively reads the content of a Python file, handles and resolves relative imports by yielding content from imported files, and removes the `__future__` import statement.

- `_clean_line(line: str, names: set[str]) -> str`: Cleans up a line of code by replacing imported module names (e.g., `some_import.spam` becomes `spam`) and removing useless self-assignments (e.g., `spam = spam`).

- `combine(args: argparse.Namespace) -> None`: Combines all Python source files into a single `portalocker.py` file, prepending the `README.rst` and `LICENSE` content as docstrings, and optionally runs `ruff` for formatting and linting.

## `constants.py`

- `LockFlags(enum.IntFlag)`: An enumeration (IntFlag) class that defines the available locking constants:
  - `EXCLUSIVE`: exclusive lock.
  - `SHARED`: shared lock.
  - `NON_BLOCKING`: non-blocking flag.
  - `UNBLOCK`: unlock (primarily for internal use).

---

## `exceptions.py`

- `BaseLockException(*args, fh=None, **kwargs)`: The base exception for all lock-related errors.  

- `LockException`: Subclass of `BaseLockException` representing general lock errors. Can be raised when any locking operation fails.

- `AlreadyLocked`: Subclass of `LockException` raised when attempting to acquire a lock on a resource that is already locked by another process.

- `FileToLarge`: Subclass of `LockException` raised when attempting to lock a file that exceeds allowed size limits.


## `portalocker.py` :

- `LockCallable`: Protocol defining the signature of a callable used to lock a file. Accepts a `FileArgument` and `LockFlags`.

- `UnlockCallable`: Protocol defining the signature of a callable used to unlock a file. Accepts a `FileArgument`.

- `BaseLocker`: Abstract base class for locker implementations.
  - `lock(file_obj, flags)`: Abstract method to acquire a lock on the given file with the specified flags.
  - `unlock(file_obj)`: Abstract method to release a lock on the given file.

- `_prepare_windows_file(file_obj)`: Prepares a Windows file object for locking by obtaining its file descriptor, saving current position if an IO object, and returning context.

- `_restore_windows_file_pos(file_io_obj, original_pos)`: Restores the saved file position for a Windows IO object after locking/unlocking.

- `Win32Locker(BaseLocker)`: Implements file locking using Win32 API (`LockFileEx`/`UnlockFileEx`).
  - `_get_os_handle(fd)`: Returns the Windows OS handle for a given file descriptor.
  - `lock(file_obj, flags)`: Locks a file using the Win32 API.
  - `unlock(file_obj)`: Unlocks a file using the Win32 API.

- `MsvcrtLocker(BaseLocker)`: Implements file locking using `msvcrt.locking` for exclusive locks and Win32 API for shared locks.
  - `lock(file_obj, flags)`: Locks a file; uses `msvcrt.locking` for exclusive locks or falls back to `Win32Locker` for shared locks.
  - `unlock(file_obj)`: Unlocks a file; falls back to `Win32Locker` if `msvcrt.unlock` fails.

- `lock(file, flags)`: Public function that locks a file using the configured `LOCKER`.

- `unlock(file)`: Public function that unlocks a file using the configured `LOCKER`.

- `PosixLocker(BaseLocker)`: Implements file locking using POSIX mechanisms (`fcntl`).
  - `locker(self) -> Callable[[Union[int, types.HasFileno], int], Any]`: Returns the function responsible for performing file locking operations. 
  - `_get_fd(file_obj)`: Returns the file descriptor from a file object or object implementing `fileno()`.
  - `lock(file_obj, flags)`: Acquires a lock on a POSIX file. Raises `AlreadyLocked` or `LockException` on errors.
  - `unlock(file_obj)`: Releases a lock on a POSIX file.

- `FlockLocker(PosixLocker)`: POSIX locker using `fcntl.flock`.

- `LockfLocker(PosixLocker)`: POSIX locker using `fcntl.lockf`.

- `lock(file, flags)`: Public POSIX function to lock a file using `_posix_locker_instance`.

- `unlock(file)`: Public POSIX function to unlock a file using `_posix_locker_instance`.


## `redis.py`

- `PubSubWorkerThread(redis.client.PubSubWorkerThread)`: Subclass of the Redis client's `PubSubWorkerThread`. This custom thread is designed to interrupt the main thread if an exception occurs during its run cycle, ensuring that errors in the background pubsub connection are noticed.
  - `run(self) -> None`: The thread's main loop. It calls the base class's `run` method and, if any exception is caught, calls `_thread.interrupt_main()` to propagate the error to the main program thread.

- `RedisLock(utils.LockBase)`: An extremely reliable **distributed lock** based on the Redis Pub/Sub system and implemented with a keep-alive thread. This method is preferred over key/value-based locks because if the connection is lost (due to network issues or process crashes), the pubsub subscription immediately terminates, which automatically unlocks the resource.
  - `__init__(self, channel: str, connection: redis.client.Redis[str] | None = None, timeout: float | None = None, check_interval: float | None = None, fail_when_locked: bool | None = False, thread_sleep_time: float = DEFAULT_THREAD_SLEEP_TIME, unavailable_timeout: float = DEFAULT_UNAVAILABLE_TIMEOUT, redis_kwargs: dict[str, typing.Any] | None = None) -> None`: Initializes the Redis lock with the unique channel name for locking, connection details, and various timeout/retry settings.
  - `get_connection(self) -> redis.client.Redis[str]`: Retrieves the Redis connection instance, creating it using the provided keyword arguments if it does not already exist.
  - `channel_handler(self, message: dict[str, str]) -> None`: The callback function executed by the PubSub worker thread upon receiving a message. It processes 'ping' messages by publishing a response containing a timestamp back to a specified response channel.
  - `client_name(self) -> str`: A property that returns the uniquely generated Redis client name used for identifying the lock holder (format: `{channel}-lock`).
  - `_timeout_generator(self, timeout: float | None, check_interval: float | None) -> typing.Iterator[int]`: An internal method that generates time steps for waiting loops. It yields values repeatedly over the specified `timeout` and sleeps for a random duration based on `check_interval` to prevent busy waiting.
  - `acquire(self, timeout: float | None = None, check_interval: float | None = None, fail_when_locked: bool | None = None) -> RedisLock`: Attempts to acquire the distributed lock. It checks for existing subscribers and uses `check_or_kill_lock` if a lock is found. If no lock is found, it subscribes to the channel and starts the `PubSubWorkerThread` to claim the lock.
  - `check_or_kill_lock(self, connection: redis.client.Redis[str], timeout: float) -> bool | None`: Checks the availability of a conflicting lock holder by sending a 'ping' message to the channel and waiting for a response. If a response is received, the lock holder is available and `True` is returned. If the check times out, the function attempts to kill the unavailable Redis client using its client name and returns `None`.
  - `release(self) -> None`: Releases the lock by stopping the keep-alive thread, unsubscribing from the channel, and closing the pubsub connection.
  - `__del__(self) -> None`: The destructor, which ensures that `self.release()` is called upon object deletion to clean up resources.


## `utils.py` :

- `coalesce(*args, test_value=None)`:  
  Returns the first argument that is **not equal to `test_value`** (checked by identity), or `None` if all values match `test_value`. Commonly used to choose the first non-null or default value.

- `open_atomic(filename, binary=True)`:  
  Opens a file for **atomic writing** — writes data to a temporary file and atomically renames it to the target filename upon completion. Guarantees that readers never see a partially written file.

---

### Class: `LockBase`
Abstract base class defining a **standard interface for file locking mechanisms** with timeout, interval, and context management support.

  - `__init__(timeout=None, check_interval=None, fail_when_locked=None)`:  
    Initializes base lock parameters including timeout duration, interval between lock checks, and behavior on immediate lock failure.

  - `acquire(timeout=None, check_interval=None, fail_when_locked=None)`:  
    *(Abstract)* Attempts to acquire a lock, possibly waiting until timeout expires.

  - `_timeout_generator(timeout, check_interval)`:  
    Internal generator that yields attempt counters and enforces waiting intervals until the specified timeout is reached.

  - `release()`:  
    *(Abstract)* Releases the current lock.

  - `__enter__()`:  
    Context manager entry; automatically calls `acquire()` and returns the locked file handle.

  - `__exit__(exc_type, exc_value, traceback)`:  
    Context manager exit; automatically releases the lock when the block finishes.

  - `__delete__(instance)`:  
    Ensures that releasing occurs when the lock object is deleted.

  - `__del__()`:  
    Destructor ensuring cleanup of the lock resource upon garbage collection.

---

### Class: `Lock`
Manages **file-based locking with configurable timeout and blocking behavior**.

  - `__init__(filename, mode='a', timeout=None, check_interval=DEFAULT_CHECK_INTERVAL, fail_when_locked=False, flags=LOCK_METHOD, **file_open_kwargs)`:  
    Initializes the lock object with file path, mode, timeout, and locking flags. Supports truncation if opened in write mode.

  - `acquire(timeout=None, check_interval=None, fail_when_locked=None)`:  
    Attempts to acquire an exclusive file lock within a timeout window. Raises `AlreadyLocked` or `LockException` when acquisition fails.

  - `release()`:  
    Releases the current file lock and closes the file handle safely, suppressing exceptions from cleanup.

  - `_get_fh()`:  
    Opens and returns a file handle using the stored filename and mode.

  - `_get_lock(fh)`:  
    Attempts to apply a lock on the given file handle via `portalocker.lock()`. Returns the locked file handle.

  - `_prepare_fh(fh)`:  
    Truncates the file to zero bytes if required and prepares it for writing.

---

### Class: `RLock`
A **reentrant lock** allowing the same process or thread to acquire the same file lock multiple times before releasing it.

  - `__init__(filename, mode='a', timeout=DEFAULT_TIMEOUT, check_interval=DEFAULT_CHECK_INTERVAL, fail_when_locked=False, flags=LOCK_METHOD)`:  
    Initializes a reentrant file lock instance, maintaining an internal counter for acquisitions.

  - `acquire(timeout=None, check_interval=None, fail_when_locked=None)`:  
    Acquires the lock, incrementing the internal counter each time. Returns immediately if already held.

  - `release()`:  
    Decrements the acquisition count and releases the actual file lock only when the count reaches zero.

---

### Class: `TemporaryFileLock`
A **temporary file lock** that automatically cleans up its lock file upon process exit.

  - `__init__(filename='.lock', timeout=DEFAULT_TIMEOUT, check_interval=DEFAULT_CHECK_INTERVAL, fail_when_locked=True, flags=LOCK_METHOD)`:  
    Creates a temporary file lock and registers an automatic release on program exit.

  - `release()`:  
    Releases the lock and removes the associated temporary file, retrying on transient permission errors (useful for Windows file systems).

---

### Class: `PidFileLock`
A **PID-based file lock** that writes the current process ID to a lock file and allows querying which process holds it.

  - `__init__(filename='.pid', timeout=DEFAULT_TIMEOUT, check_interval=DEFAULT_CHECK_INTERVAL, fail_when_locked=True, flags=LOCK_METHOD)`:  
    Initializes the PID file lock, using an internal sidecar lock file to avoid conflicts on mandatory locking systems.

  - `acquire(timeout=None, check_interval=None, fail_when_locked=None)`:  
    Acquires the lock, writing the current process ID to the PID file.

  - `read_pid()`:  
    Reads and returns the process ID from the lock file if it exists; returns `None` if unavailable.

  - `__enter__()`:  
    Context manager entry that returns `None` if the lock is acquired, or the PID of the process holding it otherwise.

  - `__exit__(exc_type, exc_value, traceback)`:  
    Releases the PID file and its sidecar lock on context exit.

  - `release()`:  
    Releases both the PID file and the internal lock, removing both files.

---

### Class: `BoundedSemaphore`
Implements a **bounded semaphore** using multiple file locks to limit concurrent processes across systems.

  - `__init__(maximum, name='bounded_semaphore', filename_pattern='{name}.{number:02d}.lock', directory=tempfile.gettempdir(), timeout=None, check_interval=None, fail_when_locked=True)`:  
    Initializes a semaphore with a maximum concurrency level and lock file naming convention.

  - `get_filenames()`:  
    Returns a list of all lock file paths managed by the semaphore.

  - `get_random_filenames()`:  
    Returns the lock file list in a random order to minimize contention.

  - `get_filename(number)`:  
    Generates a lock filename for the specified index number.

  - `acquire(timeout=None, check_interval=None, fail_when_locked=None)`:  
    Attempts to acquire one of the available lock slots. Raises `AlreadyLocked` if all are occupied and `fail_when_locked` is `True`.

  - `try_lock(filenames)`:  
    Tries to acquire one lock among the provided filenames. Returns `True` if successful.

  - `release()`:  
    Releases the held lock and resets the internal reference.

### Class: `NamedBoundedSemaphore`
An improved version of `BoundedSemaphore` that **uses unique, named lock files** to avoid conflicts between unrelated processes.

  - `__init__(maximum, name=None, filename_pattern='{name}.{number:02d}.lock', directory=tempfile.gettempdir(), timeout=None, check_interval=None, fail_when_locked=True)`:  
    Creates a uniquely named semaphore if none is provided, ensuring process-safe locking across systems.


## `types.py` :

- `Mode`:  
  A `typing.Literal` that defines all valid file open modes supported by Python, including text (`'r'`, `'w'`, `'a'`, `'x'`, etc.) and binary (`'rb'`, `'wb'`, `'ab'`, `'xb'`, etc.) variants, as well as combined read/write and universal newline options.  
  This ensures type safety and clarity when specifying file modes throughout the project.

- `Filename`:  
  A type alias representing a file path, which can be either a `str` or a `pathlib.Path` object.

- `IO`:  
  A type alias representing a file-like object that supports I/O operations.  
  It may be either `typing.IO[str]` for text streams or `typing.IO[bytes]` for binary streams.

- `FileOpenKwargs`:  
  A `TypedDict` defining keyword arguments for Python’s built-in `open()` function, including:
  - `buffering`: Buffering policy for the file object.  
  - `encoding`: Text encoding used for reading or writing.  
  - `errors`: Specifies how encoding and decoding errors are handled.  
  - `newline`: Controls how universal newlines work in text mode.  
  - `closefd`: Determines whether the underlying file descriptor should be closed.  
  - `opener`: Custom callable used to open the file descriptor.

- `HasFileno`:  
  A `typing.Protocol` defining an interface for objects that implement a `fileno()` method, returning an integer file descriptor.  
  Commonly used to type-hint objects that can be passed to `fcntl.flock` or similar system-level I/O functions.

  - `fileno(self) -> int`: Returns the file descriptor associated with the object.

- `FileArgument`:  
  A type alias representing any valid object that can be used as a file argument in lock/unlock operations.  
  It may be:
  - A `typing.IO` object (text or binary stream)  
  - An `io.TextIOWrapper`  
  - An integer file descriptor  
  - An object implementing the `HasFileno` protocol.
