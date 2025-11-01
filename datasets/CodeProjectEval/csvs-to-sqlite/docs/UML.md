## UML Class Diagram

```mermaid
classDiagram
    class CLI {
        +cli()
        +parse_args()
        +process_csv_files()
    }
    
    class LookupTable {
        -conn: Connection
        -table_name: str
        -value_column: str
        -fts_table_name: str
        -index_fts: bool
        -cache: LRU
        +ensure_table_exists()
        +id_for_value(value) int
    }
    
    class CSVProcessor {
        +load_csv()
        +refactor_dataframes()
        +to_sql_with_foreign_keys()
        +apply_shape()
        +parse_shape()
    }
    
    class DatabaseManager {
        +table_exists()
        +drop_table()
        +create_fts_table()
    }
    
    CLI --> CSVProcessor : uses
    CSVProcessor --> LookupTable : creates
    CSVProcessor --> DatabaseManager : uses
    LookupTable --> DatabaseManager : writes to
```

## UML Package Diagram

```mermaid
graph TD
    A["csvs_to_sqlite.cli"] --> B["csvs_to_sqlite.utils"]
    B --> C["pandas"]
    B --> D["sqlite3"]
    B --> E["lru"]
    B --> F["dateparser"]
    A --> G["click"]
    
    subgraph "External Dependencies"
        C
        D
        E
        F
        G
    end
    
    subgraph "Core Package"
        A
        B
    end
```

## UML Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant CSVProcessor
    participant LookupTable
    participant SQLite
    
    User->>CLI: csvs-to-sqlite -c column:table data.csv db.db
    CLI->>CSVProcessor: load_csv(filepath)
    CSVProcessor->>CSVProcessor: parse CSV with pandas
    CSVProcessor-->>CLI: DataFrame
    
    CLI->>CSVProcessor: refactor_dataframes(conn, dfs, foreign_keys)
    
    loop For each extracted column
        CSVProcessor->>LookupTable: new LookupTable(conn, table, column)
        LookupTable->>SQLite: ensure_table_exists()
        
        loop For each value in column
            CSVProcessor->>LookupTable: id_for_value(value)
            alt Value in cache
                LookupTable-->>CSVProcessor: cached_id
            else Value not in cache
                LookupTable->>SQLite: SELECT or INSERT value
                SQLite-->>LookupTable: id
                LookupTable->>LookupTable: cache.set(value, id)
                LookupTable-->>CSVProcessor: id
            end
        end
    end
    
    CSVProcessor-->>CLI: refactored DataFrames
    CLI->>CSVProcessor: to_sql_with_foreign_keys()
    CSVProcessor->>SQLite: CREATE TABLE with FK constraints
    CSVProcessor->>SQLite: INSERT data
    SQLite-->>User: Database created
```