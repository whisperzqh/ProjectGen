## UML Class Diagram

```mermaid
classDiagram
  class BoundClass {
    cls : Type[T]
    bind_early(instance: object) None
  }
  class EmptySchedule {
  }
  class Environment {
    active_process : Optional[Process]
    now : SimTime
    all_of(events: Iterable[Event]) AllOf
    any_of(events: Iterable[Event]) AnyOf
    event() Event
    peek() SimTime
    process(generator: ProcessGenerator) Process
    run(until: Optional[Union[SimTime, Event]]) Optional[Any]
    schedule(event: Event, priority: EventPriority, delay: SimTime) None
    step() None
    timeout(delay: SimTime, value: Optional[Any]) Timeout
  }
  class StopSimulation {
    callback(event: Event) None
  }
  class AllOf {
  }
  class AnyOf {
  }
  class Condition {
    all_events(events: Tuple[Event, ...], count: int) bool
    any_events(events: Tuple[Event, ...], count: int) bool
  }
  class ConditionValue {
    events : List[Event]
    items() Iterator[Tuple[Event, Any]]
    keys() Iterator[Event]
    todict() Dict[Event, Any]
    values() Iterator[Any]
  }
  class Event {
    callbacks : List
    defused : bool
    env
    ok : bool
    processed : bool
    triggered : bool
    value : Optional[Any]
    fail(exception: Exception) Event
    succeed(value: Optional[Any]) Event
    trigger(event: Event) None
  }
  class Initialize {
    callbacks : List
    env
  }
  class Interruption {
    callbacks : List
    env
    process
  }
  class Process {
    callbacks : List
    env
    is_alive : bool
    name : str
    target : Event
    interrupt(cause: Optional[Any]) None
  }
  class Timeout {
    callbacks : List
    env
  }
  class Interrupt {
    cause : Optional[Any]
  }
  class SimPyException {
  }
  class BaseResource {
    GetQueue : ClassVar[Type[MutableSequence]]
    PutQueue : ClassVar[Type[MutableSequence]]
    capacity : Union[float, int]
    get_queue : MutableSequence[GetType]
    put_queue : MutableSequence[PutType]
    get() Get
    put() Put
  }
  class Get {
    proc
    resource : ResourceType
    cancel() None
  }
  class Put {
    proc : Optional[Process]
    resource : ResourceType
    cancel() None
  }
  class Container {
    level : ContainerAmount
    get(amount: ContainerAmount) ContainerGet
    put(amount: ContainerAmount) ContainerPut
  }
  class ContainerGet {
    amount : Union
  }
  class ContainerPut {
    amount : Union
  }
  class Preempted {
    by : Optional[Process]
    resource
    usage_since : Optional[SimTime]
  }
  class PreemptiveResource {
    users : List[PriorityRequest]
  }
  class PriorityRequest {
    key : tuple
    preempt : bool
    priority : int
    time
  }
  class PriorityResource {
    GetQueue : list
    PutQueue
    release(request: PriorityRequest) Release
    request(priority: int, preempt: bool) PriorityRequest
  }
  class Release {
    request
  }
  class Request {
    resource
    usage_since : Optional[SimTime]
  }
  class Resource {
    count : int
    queue : list
    users : List[Request]
    release(request: Request) Release
    request() Request
  }
  class SortedQueue {
    maxlen : Optional[int]
    append(item: Any) None
  }
  class FilterStore {
    get(filter: Callable[[Any], bool]) FilterStoreGet
  }
  class FilterStoreGet {
    filter : Callable[[Any], bool]
  }
  class PriorityItem {
    item : Any
    priority : Any
  }
  class PriorityStore {
  }
  class Store {
    items : List[Any]
    get() StoreGet
    put(item: Any) StorePut
  }
  class StoreGet {
  }
  class StorePut {
    item : Any
  }
  class RealtimeEnvironment {
    env_start : Union
    factor : float
    real_start
    strict : bool
    step() None
    sync() None
  }
  AllOf --|> Condition
  AnyOf --|> Condition
  Condition --|> Event
  Initialize --|> Event
  Interruption --|> Event
  Process --|> Event
  Timeout --|> Event
  Interrupt --|> SimPyException
  Get --|> Event
  Put --|> Event
  Container --|> BaseResource
  ContainerGet --|> Get
  ContainerPut --|> Put
  PreemptiveResource --|> PriorityResource
  PriorityRequest --|> Request
  PriorityResource --|> Resource
  Release --|> Get
  Request --|> Put
  Resource --|> BaseResource
  FilterStore --|> Store
  FilterStoreGet --|> StoreGet
  PriorityStore --|> Store
  Store --|> BaseResource
  StoreGet --|> Get
  StorePut --|> Put
  RealtimeEnvironment --|> Environment
  ConditionValue --> Event : events
  Put --> Process : proc
  Resource --> Request : users
  Request --> Resource : resource
  BoundClass --* Environment : process
  BoundClass --* Environment : timeout
  BoundClass --* Environment : event
  BoundClass --* Environment : all_of
  BoundClass --* Environment : any_of
  BoundClass --* BaseResource : put
  BoundClass --* BaseResource : get
  BoundClass --* Container : put
  BoundClass --* Container : get
  BoundClass --* PriorityResource : request
  BoundClass --* PriorityResource : release
  BoundClass --* Resource : request
  BoundClass --* Resource : release
  BoundClass --* FilterStore : get
  BoundClass --* Store : put
  BoundClass --* Store : get
  Environment --o Event : env
  Environment --o Initialize : env
  Environment --o Process : env
  Environment --o Timeout : env
  Process --o Interruption : process
  Process --o Preempted : by
  Request --o Release : request
  Resource --o Preempted : resource
  SortedQueue --o PriorityResource : PutQueue
```
## UML Package Diagram

```mermaid
classDiagram
  class simpy {
  }
  class core {
  }
  class events {
  }
  class exceptions {
  }
  class resources {
  }
  class base {
  }
  class container {
  }
  class resource {
  }
  class store {
  }
  class rt {
  }
  class test {
  }
  class util {
  }
  simpy --> core
  simpy --> events
  simpy --> exceptions
  simpy --> container
  simpy --> resource
  simpy --> store
  simpy --> rt
  core --> events
  events --> exceptions
  base --> core
  base --> events
  container --> core
  container --> resources
  container --> base
  resource --> core
  resource --> resources
  resource --> base
  store --> core
  store --> resources
  store --> base
  rt --> core
  test --> simpy
  util --> core
  util --> events
  events ..> core
  resource ..> events
```

