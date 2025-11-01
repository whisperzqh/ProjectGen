# Architecture Design

Below is a text-based representation of the file tree.

``` bash
├── simpy
│   ├── core.py
│   ├── events.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── py.typed
│   ├── resources
│   │   ├── base.py
│   │   ├── container.py
│   │   ├── __init__.py
│   │   ├── resource.py
│   │   └── store.py
│   ├── rt.py
│   ├── test.py
│   └── util.py
```

`util.py`:

- `start_delayed(env, generator, delay)`: Returns a helper process that starts another process for the given generator after a specified delay. Raises a ValueError if the delay is not positive.

- `subscribe_at(event)`: Registers at the given event to receive an interrupt when it occurs. Commonly used to get notified when a process terminates. Raises a RuntimeError if the event has already occurred.

`rt.py`:

- `RealtimeEnvironment(initial_time=0, factor=1.0, strict=True)`: A class that provides an execution environment for event-based simulations synchronized with real-time (wall-clock time). Time steps are scaled by the specified factor, and strict mode can enforce timing constraints.

  - `factor` (property): The scaling factor of the real-time, determining how simulation time relates to wall-clock time.
  - `strict` (property): The running mode of the environment. When True, `step()` will raise a RuntimeError if event processing is too slow.
  
  - `sync()`: Synchronizes the internal simulation time with the current wall-clock time to prevent timing errors when there are delays between environment creation and execution.
  
  - `step()`: Processes the next event after waiting for the appropriate real-time delay (scaled by factor). In strict mode, raises RuntimeError if processing takes longer than allowed.

`exceptions.py`:

- `SimPyException`: Base class for all SimPy-specific exceptions.

- `Interrupt(cause)`: Exception thrown into a process when it is interrupted. Contains information about the interrupt cause.

  - The instance property `cause` returns the reason for the interrupt, or None if no cause was provided.

`events.py`:

- `Event(env)`: The base class for all events in SimPy. Represents an event that may happen at some point in time, with states for triggered, processed, successful, or failed.

  - `triggered` (property): Becomes True when the event has been triggered and callbacks are about to be invoked.
  - `processed` (property): Becomes True when the event has been processed and callbacks have been invoked.
  - `ok` (property): Indicates if the event was triggered successfully (True for succeed(), False for fail()).
  - `defused` (property): When set to True, prevents a failed event's exception from being re-raised.
  - `value` (property): The value of the event once it becomes available after triggering.
  - `trigger(event)`: Triggers this event with the state and value of another event.
  - `succeed(value)`: Marks the event as successful, sets its value, and schedules it for processing.
  - `fail(exception)`: Marks the event as failed, sets an exception as its value, and schedules it for processing.

- `Timeout(env, delay, value)`: An event that gets automatically triggered after a specified delay has passed. Raises ValueError for negative delays.

- `Initialize(env, process)`: Internal event used to initialize a process. Automatically triggered when created and scheduled with URGENT priority.

- `Interruption(process, cause)`: Internal event that immediately schedules an Interrupt exception to be thrown into the specified process. Automatically triggered when created.

- `Process(env, generator)`: Represents a process that executes an event-yielding generator. Can be interrupted during execution.

  - `target` (property): The event that the process is currently waiting for.
  - `name` (property): The name of the function used to start the process.
  - `is_alive` (property): True until the process generator exits.
  - `interrupt(cause)`: Interrupts this process with an optional cause.

- `ConditionValue()`: Holds the result of a Condition event, providing dict-like access to triggered events and their values.

- `Condition(env, evaluate, events)`: An event that triggers when a condition function returns True on a list of events. The value is a ConditionValue containing occurred events.

  - `all_events(events, count)`: Static method that returns True if all events have been triggered.
  - `any_events(events, count)`: Static method that returns True if at least one event has been triggered.

- `AllOf(env, events)`: A Condition event that triggers when all of the provided events have been successfully triggered.

- `AnyOf(env, events)`: A Condition event that triggers when any of the provided events has been successfully triggered.

- `_describe_frame(frame)`: Helper function that prints filename, line number, and function name of a stack frame for error reporting.

`core.py`:

- `BoundClass(cls)`: A descriptor class that allows classes to behave like methods when accessed as instance attributes.

  - `bind_early(instance)`: Static method that binds all BoundClass attributes of an instance's class to the instance itself to improve performance.

- `EmptySchedule`: Exception thrown by an Environment when there are no further events to be processed.

- `StopSimulation`: Exception that indicates the simulation should stop immediately.

  - `callback(event)`: Class method used as a callback in Environment.run() to stop the simulation when the until event occurs.

- `Environment(initial_time=0)`: The core execution environment for event-based simulations, managing the simulation timeline and event processing.

  - `now` (property): Returns the current simulation time.
  - `active_process` (property): Returns the currently active process in the environment.
  
  - `process(generator)`: Creates and returns a new Process instance for the given generator.
  - `timeout(delay=0, value=None)`: Returns a new Timeout event with the specified delay and optional value.
  - `event()`: Returns a new Event instance for process synchronization.
  - `all_of(events)`: Returns an AllOf condition that triggers when all provided events have been triggered.
  - `any_of(events)`: Returns an AnyOf condition that triggers when any of the provided events has been triggered.
  
  - `schedule(event, priority=NORMAL, delay=0)`: Schedules an event with the given priority and delay.
  - `peek()`: Returns the time of the next scheduled event, or Infinity if no events are scheduled.
  - `step()`: Processes the next scheduled event in the queue. Raises EmptySchedule if no events are available.
  - `run(until=None)`: Executes the simulation until the specified criterion is met (either a time limit, event, or when no events remain).

`__init__.py`:

- `_compile_toc(entries, section_marker)`: A helper function that compiles a list of sections with objects into Sphinx-formatted autosummary directives for documentation generation.

`resources/base.py`:

- `Put(resource)`: Generic event for requesting to put something into a resource. Can be used as a context manager to automatically cancel the request on exceptions.
  - `__enter__()`: Context manager entry method.
  - `__exit__(exc_type, exc_value, traceback)`: Context manager exit method that cancels the request.
  - `cancel()`: Cancels this put request if it hasn't been triggered yet.

- `Get(resource)`: Generic event for requesting to get something from a resource. Can be used as a context manager to automatically cancel the request on exceptions.
  - `__enter__()`: Context manager entry method.
  - `__exit__(exc_type, exc_value, traceback)`: Context manager exit method that cancels the request.
  - `cancel()`: Cancels this get request if it hasn't been triggered yet.

- `BaseResource(env, capacity)`: Abstract base class for shared resources supporting put and get operations.
  - `capacity`: Property that returns the maximum capacity of the resource.
  - `put()`: Request to put something into the resource (returns Put event).
  - `get()`: Request to get something from the resource (returns Get event).
  - `_do_put(event)`: Abstract method to perform the put operation (must be implemented by subclasses).
  - `_trigger_put(get_event)`: Processes put events in the queue by calling _do_put.
  - `_do_get(event)`: Abstract method to perform the get operation (must be implemented by subclasses).
  - `_trigger_get(put_event)`: Processes get events in the queue by calling _do_get.

`resources/container.py`:

- `ContainerPut(container, amount)`: Request to put a specific amount of matter into a container.
- `ContainerGet(container, amount)`: Request to get a specific amount of matter from a container.
- `Container(env, capacity, init)`: Resource for sharing homogeneous matter between processes.
  - `level`: Property that returns the current amount of matter in the container.
  - `put(amount)`: Request to put amount of matter into the container.
  - `get(amount)`: Request to get amount of matter out of the container.
  - `_do_put(event)`: Processes put requests when there's enough capacity.
  - `_do_get(event)`: Processes get requests when there's enough matter available.

`resources/resource.py`:

- `Preempted(by, usage_since, resource)`: Contains information about a preemption interrupt.
- `Request(resource)`: Request usage of a resource (subclass of Put).
  - `__exit__(exc_type, exc_value, traceback)`: Context manager exit that releases the resource.
- `Release(resource, request)`: Releases usage of a resource granted by a request (subclass of Get).
- `PriorityRequest(resource, priority, preempt)`: Request with priority and preemption support.
- `SortedQueue(maxlen)`: Queue for sorting events by their priority key.
  - `append(item)`: Sorts item into the queue.
- `Resource(env, capacity)`: Resource with capacity usage slots.
  - `count`: Property returning number of current users.
  - `request()`: Request a usage slot.
  - `release(request)`: Release a usage slot.
  - `_do_put(event)`: Grants resource access if capacity available.
  - `_do_get(event)`: Removes user from resource and triggers release event.
- `PriorityResource(env, capacity)`: Resource supporting prioritized requests.
  - `request(priority, preempt)`: Request with priority (preempt flag ignored).
  - `release(request)`: Release a prioritized request.
- `PreemptiveResource(env, capacity)`: PriorityResource with preemption support.
  - `_do_put(event)`: Handles preemption logic before processing request.

`resources/store.py`:

- `StorePut(store, item)`: Request to put an item into a store.
- `StoreGet(store)`: Request to get an item from a store.
- `FilterStoreGet(store, filter)`: Request to get an item matching a filter function.
- `Store(env, capacity)`: Resource for storing objects in FIFO order.
  - `put(item)`: Request to put an item into the store.
  - `get()`: Request to get an item from the store.
  - `_do_put(event)`: Processes put requests when store has capacity.
  - `_do_get(event)`: Processes get requests when items are available.
- `PriorityItem(priority, item)`: Container for items with comparable priorities.
- `PriorityStore(env, capacity)`: Store that maintains items in priority order.
  - `_do_put(event)`: Adds item using heap push.
  - `_do_get(event)`: Removes item using heap pop.
- `FilterStore(env, capacity)`: Store supporting filtered get requests.
  - `get(filter)`: Request to get an item matching the filter.
  - `_do_get(event)`: Processes get requests by applying filter to available items.
