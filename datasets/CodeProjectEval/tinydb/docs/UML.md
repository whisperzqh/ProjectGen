## UML Class Diagram

```mermaid
classDiagram
    class TinyDB {
        -_storage: Storage
        -_tables: Dict[str, Table]
        -_opened: bool
        +table_class: Type[Table]
        +default_table_name: str
        +default_storage_class: Type[Storage]
        +__init__(*args, **kwargs)
        +table(name: str) Table
        +tables() Set[str]
        +drop_table(name: str)
        +drop_tables()
        +close()
        +storage: Storage
    }
    
    class Table {
        -name: str
        -_storage: Storage
        -_query_cache: LRUCache
        -_next_id: Optional[int]
        +document_class: Type[Document]
        +document_id_class: Type[int]
        +insert(document: Mapping) int
        +insert_multiple(documents: Iterable) List[int]
        +all() List[Document]
        +search(cond: QueryLike) List[Document]
        +get(cond: QueryLike) Optional[Document]
        +update(fields, cond: QueryLike) List[int]
        +upsert(document, cond: QueryLike) List[int]
        +remove(cond: QueryLike) List[int]
        +truncate()
        +count(cond: QueryLike) int
        +clear_cache()
        -_read_table() Dict
        -_update_table(updater: Callable)
        -_get_next_id() int
    }
    
    class Document {
        +doc_id: int
        +__init__(value: Mapping, doc_id: int)
    }
    
    class Storage {
        <<interface>>
        +read() Optional[Dict]
        +write(data: Dict)
        +close()
    }
    
    class JSONStorage {
        -_handle: file
        -_mode: str
        +__init__(path: str, **kwargs)
        +read() Dict
        +write(data: Dict)
        +close()
    }
    
    class MemoryStorage {
        +memory: Optional[Dict]
        +read() Dict
        +write(data: Dict)
    }
    
    class Middleware {
        -_storage_cls: Type[Storage]
        +storage: Storage
        +__init__(storage_cls)
        +__call__(*args, **kwargs)
        +__getattr__(name)
    }
    
    class CachingMiddleware {
        +WRITE_CACHE_SIZE: int
        +cache: Optional[Dict]
        -_cache_modified_count: int
        +read() Dict
        +write(data: Dict)
        +flush()
        +close()
    }
    
    class Query {
        -_path: Tuple
        -_test: Callable
        -_hash: Optional[Tuple]
        +__getattr__(item: str) Query
        +__eq__(other) QueryInstance
        +__ne__(other) QueryInstance
        +__lt__(other) QueryInstance
        +__le__(other) QueryInstance
        +__gt__(other) QueryInstance
        +__ge__(other) QueryInstance
        +exists() QueryInstance
        +matches(regex) QueryInstance
        +test(func) QueryInstance
    }
    
    class QueryInstance {
        -_test: Callable
        -_hash: Optional[Tuple]
        +__call__(value: Mapping) bool
        +__and__(other: QueryInstance) QueryInstance
        +__or__(other: QueryInstance) QueryInstance
        +__invert__() QueryInstance
        +is_cacheable() bool
    }
    
    TinyDB "1" --> "*" Table : manages
    TinyDB "1" --> "1" Storage : uses
    Table "1" --> "*" Document : contains
    Table "1" --> "1" Storage : uses
    Document --|> dict : extends
    Storage <|-- JSONStorage : implements
    Storage <|-- MemoryStorage : implements
    Middleware --|> Storage : implements
    Middleware "1" o-- "1" Storage : wraps
    CachingMiddleware --|> Middleware : extends
    Query --|> QueryInstance : extends
    Table ..> Query : uses for filtering
```

## UML Package Diagram

```mermaid
graph TD
    subgraph "tinydb Package"
        database["database.py<br/>TinyDB class"]
        table["table.py<br/>Table, Document"]
        queries["queries.py<br/>Query, QueryInstance"]
        storages["storages.py<br/>Storage, JSONStorage, MemoryStorage"]
        middlewares["middlewares.py<br/>Middleware, CachingMiddleware"]
        utils["utils.py<br/>LRUCache, utilities"]
        init["__init__.py<br/>Public API exports"]
    end
    
    subgraph "External Dependencies"
        json["json module"]
        typing["typing module"]
    end
    
    init --> database
    init --> table
    init --> queries
    init --> storages
    
    database --> table
    database --> storages
    database --> utils
    
    table --> queries
    table --> storages
    table --> utils
    
    middlewares --> storages
    
    storages --> json
    
    database --> typing
    table --> typing
    queries --> typing
    middlewares --> typing
```

## UML Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant TinyDB
    participant Table
    participant Storage
    participant Middleware
    
    Note over Client,Storage: Database Initialization
    Client->>TinyDB: TinyDB(path, storage=CachingMiddleware(JSONStorage))
    TinyDB->>Middleware: __init__(JSONStorage)
    TinyDB->>Middleware: __call__(path)
    Middleware->>Storage: JSONStorage(path)
    Middleware-->>TinyDB: middleware instance
    
    Note over Client,Storage: Insert Operation
    Client->>TinyDB: insert(document)
    TinyDB->>Table: table(default_table_name)
    TinyDB->>Table: insert(document)
    Table->>Table: _get_next_id()
    Table->>Storage: read()
    Storage-->>Table: current data
    Table->>Table: add document with ID
    Table->>Storage: write(updated data)
    Table->>Table: clear_cache()
    Table-->>Client: document_id
    
    Note over Client,Storage: Search Operation
    Client->>TinyDB: search(Query)
    TinyDB->>Table: search(Query)
    Table->>Table: check query_cache
    alt Cache miss
        Table->>Storage: read()
        Storage-->>Table: table data
        Table->>Table: filter with Query
        Table->>Table: update cache
    end
    Table-->>Client: List[Document]
    
    Note over Client,Storage: Update Operation
    Client->>TinyDB: update(fields, Query)
    TinyDB->>Table: update(fields, Query)
    Table->>Table: _update_table(updater)
    Table->>Storage: read()
    Storage-->>Table: all tables data
    Table->>Table: modify matching documents
    Table->>Storage: write(updated data)
    Table->>Table: clear_cache()
    Table-->>Client: List[doc_ids]
    
    Note over Client,Storage: Close Operation
    Client->>TinyDB: close()
    TinyDB->>Storage: close()
    alt Middleware with cache
        Storage->>Storage: flush()
        Storage->>Storage: close file handles
    end
```