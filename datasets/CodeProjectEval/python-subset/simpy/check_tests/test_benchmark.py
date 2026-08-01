"""
Minimal benchmark tests for SimPy: only Store and Resource simulations.
"""
import pytest
import simpy


@pytest.mark.benchmark(group='simulation')
def test_store_sim(benchmark):
    """Newly constructed test"""
    def producer(env, store, n):
        for i in range(n):
            yield env.timeout(2)
            yield store.put(i)

    def consumer(env, store):
        while True:
            yield store.get()
            yield env.timeout(3)

    def sim():
        env = simpy.Environment()
        store = simpy.Store(env, capacity=8)
        for _ in range(3):
            env.process(producer(env, store, 15))
        for _ in range(5):
            env.process(consumer(env, store))
        env.run()
        return next(env._eid)

    num_events = benchmark(sim)
    assert num_events == 191  


@pytest.mark.benchmark(group='simulation')
def test_resource_sim(benchmark):
    """Newly constructed test"""
    def worker(env, resource):
        while True:
            with resource.request() as req:
                yield req
                yield env.timeout(2)

    def sim():
        env = simpy.Environment()
        resource = simpy.Resource(env, capacity=4)
        for _ in range(8):
            env.process(worker(env, resource))
        env.run(until=25)
        return next(env._eid)

    num_events = benchmark(sim)
    assert num_events == 161  

@pytest.mark.benchmark(group='simulation')
def test_container_sim(benchmark):
    """Newly constructed test"""
    def producer(env, container, full_event):
        while container.level < container.capacity:
            space = container.capacity - container.level
            to_put = min(3, space)
            yield container.put(to_put)
            if container.level == container.capacity:
                full_event.succeed()
            yield env.timeout(0.1)

    def sim():
        env = simpy.Environment()
        container = simpy.Container(env, capacity=20)
        full_event = env.event()
        env.process(producer(env, container, full_event))
        env.run(until=full_event)
        return next(env._eid)

    num_events = benchmark(sim)
    assert num_events == 16 