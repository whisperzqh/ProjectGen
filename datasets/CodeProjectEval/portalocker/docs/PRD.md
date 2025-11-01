# PRD Document for portalocker

## Introduction

The purpose of this project is to develop a cross-platform Python library that provides file locking capabilities for process synchronization and distributed systems. The repository wraps platform-specific file locking mechanisms (Windows `msvcrt.locking`/Win32 APIs and POSIX `fcntl.flock`) into a unified API that works seamlessly across Windows, Linux, macOS, and other Unix-like systems. This tool is designed for Python developers, system administrators, and distributed systems engineers who need reliable mechanisms to coordinate file access across multiple processes, threads, and systems.
## Goals

The objective of this project is to provide a robust, production-stable library for cross-platform file locking with automatic platform detection, support for multiple lock types (exclusive, shared, non-blocking), and advanced features like distributed Redis-based locking and atomic file operations.The library should handle platform differences transparently, support reentrant locks and semaphores, and enable users to implement reliable concurrent access patterns with minimal code. 

## Features and Functionalities

The following features and functionalities are expected in the project:

### Core File Locking
- Ability to acquire exclusive locks (`LOCK_EX`) for single-process write access 
- Ability to acquire shared locks (`LOCK_SH`) for multi-reader scenarios 
- Ability to use non-blocking locks (`LOCK_NB`) for immediate failure when lock unavailable 
- Ability to automatically detect and use platform-specific locking mechanisms (Windows vs POSIX) 
- Ability to specify lock timeouts for automatic release 
- Ability to unlock files explicitly or via context managers 

### High-Level Lock Utilities
- Ability to use `Lock` context manager for basic file-based locking with timeout support 
- Ability to use `RLock` for reentrant locks allowing same process to acquire multiple times 
- Ability to use `TemporaryFileLock` with automatic cleanup of lock files 
- Ability to use `BoundedSemaphore` for cross-process semaphore limiting concurrent access 
- Ability to handle lock acquisition failures with proper exception handling 

### Distributed Locking
- Ability to use Redis-based distributed locking for multi-system coordination 
- Ability to receive immediate unlock notifications via Redis Pub/Sub mechanism 
- Ability to handle network failures with automatic unlock on connection loss 
- Ability to use compatible API between file-based and Redis-based locks 

### Atomic Operations
- Ability to perform atomic file writes using `open_atomic()` function 
- Ability to prevent partial reads during file updates 

### Platform Abstraction
- Ability to use consistent API across Windows and POSIX systems 
- Ability to fall back to alternative locking mechanisms when primary method unavailable 
- Ability to handle platform-specific edge cases transparently 

## Technical Constraints

- The repository should use Python as the primary programming language 
- The repository should support Python 3.9 through 3.13 
- The repository should support CPython, PyPy, and IronPython implementations  
- The repository should have no external dependencies except `pywin32>=226` on Windows 
- The repository should maintain 100% test coverage 
- The repository should provide type hints and pass strict type checking 

## Requirements

### Dependencies

**Core Dependencies:**
- `pywin32>=226` (Windows only) - Windows-specific file locking APIs 

**Optional Dependencies:**
- `redis` - Redis-based distributed locking support 

### Development Dependencies

**Testing:**
- `pytest>=5.4.1` - Testing framework 
- `pytest-cov>=2.8.1` - Test coverage plugin 
- `pytest-mypy>=0.8.0` - MyPy integration for pytest 
- `coverage-conditional-plugin>=0.9.0` - Platform-specific coverage rules 

**Code Quality:**
- `mypy>=1.15.0` - Static type checker 
- `pyright>=1.1.401` - Alternative type checker 
- `ruff>=0.11.11` - Linting and formatting 
- `lefthook>=1.11.13` - Git hooks management 

**Build and Documentation:**
- `tox>=4.26.0` - Test environment management 
- `sphinx` - Documentation generation 

## Usage

### Basic File Locking

Lock a file exclusively:
```python
import portalocker

with portalocker.Lock('myfile.txt', 'r+', timeout=10) as fh:
    fh.write('data')
```

Lock with explicit lock/unlock:
```python
file = open('myfile.txt', 'r+')
portalocker.lock(file, portalocker.LOCK_EX)
# ... do work ...
portalocker.unlock(file)
```

### Advanced Usage Examples

Non-blocking lock:
```python
try:
    with portalocker.Lock('myfile.txt', 'r+', timeout=0) as fh:
        fh.write('data')
except portalocker.LockException:
    print('Could not acquire lock')
```

Reentrant lock:
```python
with portalocker.RLock('myfile.txt', 'r+') as fh:
    # Can acquire same lock multiple times in same process
    with portalocker.RLock('myfile.txt', 'r+') as fh2:
        fh.write('data')
```

Temporary file lock:
```python
with portalocker.TemporaryFileLock() as fh:
    # Lock file automatically cleaned up
    fh.write('temporary data')
```

Bounded semaphore:
```python
with portalocker.BoundedSemaphore(3, 'semaphore.lock') as sem:
    # Only 3 processes can enter this block simultaneously
    do_work()
```

Atomic file write:
```python
with portalocker.open_atomic('myfile.txt', 'w') as fh:
    fh.write('data')
    # File only visible to readers after context exits
```

Redis-based distributed lock:
```python
import portalocker

lock = portalocker.RedisLock('mykey', host='localhost')
with lock:
    # Distributed lock across multiple systems
    do_distributed_work()
```

## API Reference

### Lock Flags

- `LOCK_EX` - Exclusive lock (write access)
- `LOCK_SH` - Shared lock (read access)
- `LOCK_NB` - Non-blocking mode
- `LOCK_UN` - Unlock

### Core Functions

- `lock(file, flags)` - Acquire lock on file handle
- `unlock(file)` - Release lock on file handle
- `open_atomic(filename, mode)` - Open file for atomic writing

### Context Managers

- `Lock(filename, mode, timeout, flags)` - Basic file lock
- `RLock(filename, mode, timeout, flags)` - Reentrant lock
- `TemporaryFileLock(filename, timeout, flags)` - Auto-cleanup lock
- `BoundedSemaphore(max_count, filename, timeout)` - Process semaphore

### Exceptions

- `LockException` - Base exception for locking errors
- `AlreadyLocked` - Lock already held by another process

## Platform Support

### Operating Systems
- Windows (all versions)
- macOS / MacOS X 
- Linux 
- FreeBSD 
- Solaris 
- Other POSIX/Unix systems  

### Python Versions
- Python 3.9, 3.10, 3.11, 3.12, 3.13 
- CPython, PyPy, IronPython 

## Development and Testing

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=portalocker
```

Run type checking:
```bash
mypy .
pyright
```

Run linting:
```bash
ruff check
ruff format --check
```

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration with the following jobs: 

- **Linting and Documentation** - Runs ruff, mypy, pyright, codespell, and builds Sphinx docs
- **Type Checking** - Validates type hints across all platforms and Python versions  
- **Tests** - Executes pytest with Redis integration across matrix of OS and Python versions

AppVeyor provides additional Windows testing coverage. 

## Terms/Concepts Explanation

**File Locking**: An operating system mechanism that prevents multiple processes from simultaneously modifying the same file, ensuring data integrity in concurrent access scenarios. 

**Exclusive Lock (LOCK_EX)**: A lock type that grants write access to only one process at a time, blocking all other processes from reading or writing. 

**Shared Lock (LOCK_SH)**: A lock type that allows multiple processes to read a file simultaneously while preventing any process from writing. 

**Non-blocking Lock (LOCK_NB)**: A lock acquisition mode that immediately returns failure if the lock cannot be acquired, rather than waiting. 

**Reentrant Lock**: A lock that can be acquired multiple times by the same process without causing a deadlock, maintaining a count of acquisitions. 

**Context Manager**: A Python object that implements `__enter__` and `__exit__` methods, enabling automatic resource management with the `with` statement. 

**Atomic Operation**: An operation that completes entirely or not at all, with no intermediate state visible to other processes. 

**Distributed Lock**: A locking mechanism that coordinates access across multiple systems or servers, typically using a shared coordination service like Redis. 

**Bounded Semaphore**: A synchronization primitive that limits the number of processes that can access a resource simultaneously to a specified maximum count. 