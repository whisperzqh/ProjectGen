"""
Modified test cases for shared resources with new data.
Only includes newly constructed tests.
"""

import pytest
import simpy
from simpy.resources.resource import Preempted


def test_container(env, log):
    """Newly constructed test"""
    def putter(env, buf, log):
        yield env.timeout(2)  # start later
        while env.now < 8:
            yield buf.put(3)  # put 3 units
            log.append(('PUT', env.now))
            yield env.timeout(2)

    def getter(env, buf, log):
        yield buf.get(2)  # get 2 units
        log.append(('GET', env.now))
        yield env.timeout(1)
        yield buf.get(1)  # get 1 unit
        log.append(('GET', env.now))

    buf = simpy.Container(env, init=1, capacity=5)
    env.process(putter(env, buf, log))
    env.process(getter(env, buf, log))
    env.run(until=10)

    # Timeline:
    # t=0: buf=1 → get(2) blocks
    # t=2: put(3) → buf=4 → unblocks get(2) → buf=2, logs PUT and GET at t=2
    # t=3: get(1) succeeds → buf=1, logs GET at t=3
    # t=4: put(3) → buf=4, logs PUT at t=4
    assert log == [('PUT', 2), ('GET', 2), ('GET', 3), ('PUT', 4)]


def test_priority_store_item_priority(env):
    """Newly constructed test"""
    pstore = simpy.PriorityStore(env, 4)  # capacity 4
    log = []

    def getter(wait):
        yield env.timeout(wait)
        item = yield pstore.get()
        log.append(item)

    # Insert unsorted letters; PriorityStore retrieves in ascending order
    env.process(pstore.put(s) for s in 'zyxwvu')
    env.process(getter(1))
    env.process(getter(2))
    env.process(getter(3))
    env.run()
    # Expected order: 'u' < 'v' < 'w' < ...
    assert log == ['w', 'v', 'u']