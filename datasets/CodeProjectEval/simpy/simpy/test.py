# get_new_event_counts.py
import simpy

# --- Store Simulation ---
def test_store_sim():
    def producer(env, store, n):
        for i in range(n):
            yield env.timeout(2)
            yield store.put(i)
    def consumer(env, store):
        while True:
            yield store.get()
            yield env.timeout(3)
    env = simpy.Environment()
    store = simpy.Store(env, capacity=10)
    for _ in range(2):
        env.process(producer(env, store, 20))
    for _ in range(5):
        env.process(consumer(env, store))
    env.run()
    return next(env._eid)

# --- Resource Simulation ---
def test_resource_sim():
    def worker(env, resource):
        while True:
            with resource.request() as req:
                yield req
                yield env.timeout(2)
    env = simpy.Environment()
    resource = simpy.Resource(env, capacity=5)
    for _ in range(10):
        env.process(worker(env, resource))
    env.run(until=30)
    return next(env._eid)

# --- Container Simulation ---
def test_container_sim():
    def producer(env, container, full_event):
        while True:
            yield container.put(3)
            if container.level == container.capacity:
                full_event.succeed()
            yield env.timeout(2)
    def consumer(env, container):
        while True:
            yield container.get(3)
            yield env.timeout(5)
    env = simpy.Environment()
    container = simpy.Container(env, capacity=25)
    full_event = env.event()
    env.process(producer(env, container, full_event))
    for _ in range(2):
        env.process(consumer(env, container))
    env.run(until=full_event)
    return next(env._eid)

if __name__ == "__main__":
    print("Store simulation event count:", test_store_sim())
    print("Resource simulation event count:", test_resource_sim())
    print("Container simulation event count:", test_container_sim())