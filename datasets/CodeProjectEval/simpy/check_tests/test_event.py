import re
import pytest
import simpy


def test_triggered(env):
    """Newly constructed test"""
    """Test consuming an event that was succeeded before process started."""
    def pem(env, event):
        value = yield event
        return value

    event = env.event()
    event.succeed('pre_succeeded')

    result = env.run(env.process(pem(env, event)))
    assert result == 'pre_succeeded'