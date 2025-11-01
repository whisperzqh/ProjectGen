## UML Class Diagram
```mermaid
classDiagram
  class LockFlags {
    name
  }
  class AlreadyLocked {
  }
  class BaseLockException {
    LOCK_FAILED
    fh : NoneType
    strerror : Optional[typing.Optional[str]]
  }
  class FileToLarge {
  }
  class LockException {
  }
  class BaseLocker {
    lock(file_obj: types.FileArgument, flags: LockFlags)* None
    unlock(file_obj: types.FileArgument)* None
  }
  class FlockLocker {
    LOCKER
  }
  class LockCallable {
  }
  class LockfLocker {
    LOCKER
  }
  class MsvcrtLocker {
    lock(file_obj: types.FileArgument, flags: LockFlags) None
    unlock(file_obj: types.FileArgument) None
  }
  class PosixLocker {
    locker
    lock(file_obj: PosixFileArgument, flags: LockFlags) None
    unlock(file_obj: PosixFileArgument) None
  }
  class UnlockCallable {
  }
  class Win32Locker {
    lock(file_obj: types.FileArgument, flags: LockFlags) None
    unlock(file_obj: types.FileArgument) None
  }
  class PubSubWorkerThread {
    run() None
  }
  class RedisLock {
    DEFAULT_REDIS_KWARGS : typing.ClassVar[dict[str, typing.Any]]
    channel : str
    client_name
    close_connection : bool
    connection : redis.client.Redis[str] | None
    pubsub : redis.client.PubSub | None
    redis_kwargs : dict[str, typing.Any]
    thread : PubSubWorkerThread | None
    thread_sleep_time : float
    timeout : float
    unavailable_timeout : float
    acquire(timeout: float | None, check_interval: float | None, fail_when_locked: bool | None) RedisLock
    channel_handler(message: dict[str, str]) None
    check_or_kill_lock(connection: redis.client.Redis[str], timeout: float) bool | None
    get_connection() redis.client.Redis[str]
    release() None
  }
  class FileOpenKwargs {
    buffering : int | None
    closefd : bool | None
    encoding : str | None
    errors : str | None
    newline : str | None
    opener : typing.Callable[[str, int], int] | None
  }
  class HasFileno {
    fileno() int
  }
  class BoundedSemaphore {
    directory : str
    filename_pattern : str
    lock : Lock | None
    maximum : int
    name : str
    acquire(timeout: float | None, check_interval: float | None, fail_when_locked: bool | None) Lock | None
    get_filename(number: int) pathlib.Path
    get_filenames() typing.Sequence[pathlib.Path]
    get_random_filenames() typing.Sequence[pathlib.Path]
    release() None
    try_lock(filenames: typing.Sequence[Filename]) bool
  }
  class Lock {
    check_interval : float
    fail_when_locked : bool
    fh : types.IO | None
    file_open_kwargs : dict[str, typing.Any]
    filename : str
    flags
    mode : str
    timeout : float
    truncate : bool
    acquire(timeout: float | None, check_interval: float | None, fail_when_locked: bool | None) typing.IO[typing.AnyStr]
    release() None
  }
  class LockBase {
    check_interval : float
    fail_when_locked : bool
    timeout : float
    acquire(timeout: float | None, check_interval: float | None, fail_when_locked: bool | None)* typing.IO[typing.AnyStr]
    release()* None
  }
  class NamedBoundedSemaphore {
  }
  class PidFileLock {
    acquire(timeout: float | None, check_interval: float | None, fail_when_locked: bool | None) typing.IO[typing.AnyStr]
    read_pid() int | None
    release() None
  }
  class RLock {
    acquire(timeout: float | None, check_interval: float | None, fail_when_locked: bool | None) typing.IO[typing.AnyStr]
    release() None
  }
  class TemporaryFileLock {
    release() None
  }
  AlreadyLocked --|> LockException
  FileToLarge --|> LockException
  LockException --|> BaseLockException
  FlockLocker --|> PosixLocker
  LockfLocker --|> PosixLocker
  MsvcrtLocker --|> BaseLocker
  PosixLocker --|> BaseLocker
  Win32Locker --|> BaseLocker
  RedisLock --|> LockBase
  BoundedSemaphore --|> LockBase
  Lock --|> LockBase
  NamedBoundedSemaphore --|> BoundedSemaphore
  PidFileLock --|> TemporaryFileLock
  RLock --|> Lock
  TemporaryFileLock --|> Lock
  LockFlags --* Lock : flags
  PubSubWorkerThread --* RedisLock : thread
  Lock --* BoundedSemaphore : lock
```
## UML Package Diagram
```mermaid
classDiagram
  class portalocker {
  }
  class __about__ {
  }
  class __main__ {
  }
  class constants {
  }
  class exceptions {
  }
  class portalocker {
  }
  class redis {
  }
  class types {
  }
  class utils {
  }
  portalocker --> redis
  portalocker --> utils
  utils --> types
```
