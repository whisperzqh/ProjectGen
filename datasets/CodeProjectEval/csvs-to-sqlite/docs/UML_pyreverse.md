## UML Class Diagram

```mermaid
classDiagram
  class LoadCsvError {
  }
  class LookupTable {
    cache : LRUCacheDict
    conn
    fts_table_name
    index_fts
    table_name
    value_column
    ensure_table_exists()
    id_for_value(value)
  }
  class PathOrURL {
    convert(value, param, ctx)
  }
```

## UML Package Diagram

```mermaid
classDiagram
  class csvs_to_sqlite {
  }
  class cli {
  }
  class utils {
  }
  cli --> utils
```