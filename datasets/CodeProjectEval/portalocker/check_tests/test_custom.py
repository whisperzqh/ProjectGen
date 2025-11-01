"""Tests for PidFileLock class (version 2, modified test data)."""

import multiprocessing
import os
import tempfile
import time
from pathlib import Path
from typing import Optional
from unittest import mock

from portalocker import utils


def test_pidfilelock_creation_v2():
    """Test basic PidFileLock creation with modified data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'pidfilelock_creation_v2.lock'
        lock = utils.PidFileLock(str(lock_file))
        assert lock.filename == str(lock_file)
        assert not lock._acquired_lock


def test_pidfilelock_acquire_writes_pid_v2():
    """Test that acquiring the lock writes the current PID (modified data)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'pidfilelock_acquire_writes_pid_v2.lock'
        lock = utils.PidFileLock(str(lock_file))

        try:
            lock.acquire()
            assert lock._acquired_lock

            with open(lock_file) as f:
                written_pid = int(f.read().strip())
            assert written_pid == os.getpid()
        finally:
            lock.release()

'''
def test_pidfilelock_context_manager_success_v2():
    """Test context manager success (modified data)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'pidfilelock_context_manager_success_v2.lock'
        lock = utils.PidFileLock(str(lock_file))

        with lock as result:
            assert result is None
            assert lock._acquired_lock

            with open(lock_file) as f:
                written_pid = int(f.read().strip())
            assert written_pid == os.getpid()

        assert not lock._acquired_lock
        assert not os.path.exists(lock_file)


def test_read_pid_empty_file_v2():
    """Test reading PID from empty file (modified data)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'read_pid_empty_v2.lock'
        lock_file.touch()
        lock = utils.PidFileLock(str(lock_file))
        assert lock.read_pid() is None
'''

def test_read_pid_invalid_content_v2():
    """Test reading PID from invalid file content (modified data)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'read_pid_invalid_v2.lock'
        with open(lock_file, 'w') as f:
            f.write('xyz_invalid_pid')

        lock = utils.PidFileLock(str(lock_file))
        assert lock.read_pid() is None


def test_read_pid_valid_content_v2():
    """Test reading PID from valid file content (modified data)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'read_pid_valid_v2.lock'
        test_pid = 54321
        with open(lock_file, 'w') as f:
            f.write(str(test_pid))

        lock = utils.PidFileLock(str(lock_file))
        assert lock.read_pid() == test_pid


@mock.patch('builtins.open', side_effect=OSError('Access denied'))
def test_read_pid_permission_error_v2(mock_open):
    """Test reading PID when file cannot be opened (modified data)."""
    lock = utils.PidFileLock('read_pid_permission_error_v2.lock')
    assert lock.read_pid() is None


def test_release_without_acquire_v2():
    """Test releasing without acquiring first (modified data)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'release_without_acquire_v2.lock'
        lock = utils.PidFileLock(str(lock_file))
        lock.release()
        assert not lock._acquired_lock


def test_multiple_context_manager_entries_v2():
    """Test multiple context manager entries (modified data)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'multiple_context_entries_v2.lock'
        lock = utils.PidFileLock(str(lock_file))

        with lock as result1:
            assert result1 is None

            lock2 = utils.PidFileLock(str(lock_file))
            with lock2 as result2:
                assert result2 == os.getpid()


def test_inheritance_from_temporaryfilelock_v2():
    """Test inheritance from TemporaryFileLock (modified data)."""
    lock = utils.PidFileLock()
    assert isinstance(lock, utils.TemporaryFileLock)
    assert isinstance(lock, utils.Lock)
    assert isinstance(lock, utils.LockBase)


def test_custom_parameters_v2():
    """Test PidFileLock with modified custom parameters."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'custom_parameters_v2.lock'
        lock = utils.PidFileLock(
            filename=str(lock_file),
            timeout=5.0,
            check_interval=0.05,
            fail_when_locked=True,
        )

        assert lock.filename == str(lock_file)
        assert lock.timeout == 5.0
        assert lock.check_interval == 0.05
        assert lock.fail_when_locked is True


def _worker_function_v2(lock_file_path, result_queue, should_succeed):
    """Worker function for multiprocessing tests (modified data)."""
    try:
        lock = utils.PidFileLock(lock_file_path)
        with lock as result:
            if should_succeed:
                result_queue.put(('acquired', result, os.getpid()))
                time.sleep(0.3)
            else:
                result_queue.put(('waiting', result, os.getpid()))
    except Exception as e:
        result_queue.put(('error', str(e), os.getpid()))


def test_multiprocess_locking_v2():
    """Test multiprocess locking with modified data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_file = Path(tmpdir) / 'multiprocess_locking_v2.lock'
        result_queue: multiprocessing.Queue[tuple[str, Optional[int], int]] = (
            multiprocessing.Queue()
        )

        p1 = multiprocessing.Process(
            target=_worker_function_v2, args=(str(lock_file), result_queue, True)
        )
        p1.start()
        time.sleep(0.1)

        p2 = multiprocessing.Process(
            target=_worker_function_v2, args=(str(lock_file), result_queue, False)
        )
        p2.start()

        try:
            result1 = result_queue.get(timeout=2)
            result2 = result_queue.get(timeout=2)

            assert result1[0] == 'acquired'
            assert result1[1] is None
            pid1 = result1[2]

            assert result2[0] == 'waiting'
            assert result2[1] == pid1
        finally:
            p1.join(timeout=2)
            p2.join(timeout=2)
            if p1.is_alive():
                p1.terminate()
            if p2.is_alive():
                p2.terminate()

