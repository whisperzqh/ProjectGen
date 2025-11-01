## UML Class Diagram

```mermaid
classDiagram
    class Environment {
        -_now: SimTime
        -_queue: List
        -_eid: count
        -_active_proc: Process
        +now: SimTime
        +active_process: Process
        +process(generator)
        +timeout(delay, value)
        +event()
        +schedule(event, priority, delay)
        +step()
        +run(until)
    }

    class RealtimeEnvironment {
        -env_start: SimTime
        -real_start: float
        -_factor: float
        -_strict: bool
        +factor: float
        +strict: bool
        +sync()
        +step()
    }

    class Event {
        +env: Environment
        +callbacks: List
        -_ok: bool
        -_value: Any
        +triggered: bool
        +processed: bool
        +ok: bool
        +value: Any
        +trigger(event)
        +succeed(value)
        +fail(exception)
    }

    class Timeout {
        -_delay: SimTime
    }

    class Process {
        -_generator: ProcessGenerator
        -_target: Event
        +target: Event
        +name: str
        +is_alive: bool
        +interrupt(cause)
        -_resume(event)
    }

    class Condition {
        -_evaluate: Callable
        -_events: Tuple
        -_count: int
        -_check(event)
        -_build_value(event)
    }

    class AllOf {
    }

    class AnyOf {
    }

    class BaseResource {
        -_env: Environment
        -_capacity: int
        +put_queue: List
        +get_queue: List
        +capacity: int
        +put()
        +get()
        -_do_put(event)
        -_do_get(event)
        -_trigger_put(event)
        -_trigger_get(event)
    }

    class Put {
        +resource: ResourceType
        +proc: Process
        +cancel()
    }

    class Get {
        +resource: ResourceType
        +proc: Process
        +cancel()
    }

    class Resource {
        +users: List
        +queue: List
        +count: int
        +request()
        +release(request)
    }

    class PriorityResource {
        +PutQueue: SortedQueue
    }

    class PreemptiveResource {
    }

    class Container {
        -_level: ContainerAmount
        +level: ContainerAmount
    }

    class Store {
        +items: List
    }

    class PriorityStore {
    }

    class FilterStore {
    }

    class SimPyException {
    }

    class Interrupt {
        +cause: Any
    }

    RealtimeEnvironment --|> Environment
    Timeout --|> Event
    Process --|> Event
    Condition --|> Event
    AllOf --|> Condition
    AnyOf --|> Condition
    Put --|> Event
    Get --|> Event
    Resource --|> BaseResource
    PriorityResource --|> Resource
    PreemptiveResource --|> PriorityResource
    Container --|> BaseResource
    Store --|> BaseResource
    PriorityStore --|> Store
    FilterStore --|> Store
    Interrupt --|> SimPyException
    
    Environment "1" --o "*" Event : manages
    Process "1" --> "1" Event : yields
    BaseResource "1" --> "*" Put : has
    BaseResource "1" --> "*" Get : has
```
## UML Package Diagram

```mermaid
graph TD
    simpy["simpy (main package)"]
    core["simpy.core"]
    events["simpy.events"]
    exceptions["simpy.exceptions"]
    rt["simpy.rt"]
    resources["simpy.resources"]
    base["simpy.resources.base"]
    resource["simpy.resources.resource"]
    container["simpy.resources.container"]
    store["simpy.resources.store"]

    simpy --> core
    simpy --> events
    simpy --> exceptions
    simpy --> rt
    simpy --> resources

    resources --> base
    resources --> resource
    resources --> container
    resources --> store

    events --> exceptions
    rt --> core
    base --> core
    base --> events
    resource --> base
    resource --> core
    container --> base
    container --> core
    store --> base
    store --> core
```