"""
Tests for the ``simpy.events.Process`` with scaled time values.
"""
import pytest
from simpy import Interrupt

def test_error_and_interrupted_join(env):
    """Newly constructed test"""
    def child_a(env, process):
        process.interrupt()
        return
        yield  # Dummy yield

    def child_b(env):
        raise AttributeError('eggs')
        yield  # Dummy yield

    def parent(env):
        env.process(child_a(env, env.active_process))
        b = env.process(child_b(env))

        try:
            yield b
        except Interrupt:
            pass

        yield env.timeout(0)

    env.process(parent(env))
    pytest.raises(AttributeError, env.run)