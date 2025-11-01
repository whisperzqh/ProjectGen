# Architecture Design

Below is a text-based representation of the file tree. 
```bash
├── csvs_to_sqlite
│   ├── __init__.py
│   ├── cli.py
│   └── utils.py
```

`__init__.py` :

`cli.py` :

- `cli()`: Main command-line interface function that orchestrates the entire CSV-to-SQLite conversion process. Accepts paths to CSV files or directories and a database name, processes command-line options, loads CSV files into pandas DataFrames, applies transformations (shape, dates, column extraction), creates lookup tables for foreign keys, writes data to SQLite with proper schema and constraints, and creates indexes and full-text search tables.

`utils.py` :

- `class LoadCsvError(Exception)`: Custom exception raised when CSV loading fails.

- `load_csv(filepath, separator, skip_errors, quoting, shape, encodings_to_try=("utf8", "latin-1"), just_strings=False)`: Load a CSV file into a pandas DataFrame with error handling and encoding detection. Tries multiple encodings (utf8, latin-1), handles different separators and quoting options, supports column filtering via shape parameter, and can force all columns to string type with just_strings parameter.

- `csvs_from_paths(paths)`: Process input paths (files, directories, or URLs) and return a dictionary mapping table names to file paths. Handles individual CSV files, recursively searches directories for CSV files, supports URLs, and resolves naming conflicts by adding numeric suffixes.

- `_is_url(possible_url)`: Check if a string is a valid URL by verifying its scheme against known URL schemes.

- `class PathOrURL(click.Path)`: Custom Click parameter type that handles both file paths and URLs. If the argument can be parsed as a URL, it will be treated as one; otherwise it behaves like click.Path.
    - `__init__(exists=False, file_okay=True, dir_okay=True, writable=False, readable=True, resolve_path=False, allow_dash=False, path_type=None)`: Initialize the PathOrURL type with standard Click.Path parameters.
    - `convert(value, param, ctx)`: Convert the value to either a URL or a path depending on its format.

- `class LookupTable`: Manages lookup tables for extracted columns with foreign key relationships.
    - `__init__(conn, table_name, value_column, index_fts)`: Initialize a LookupTable instance with database connection, table name, value column name, and FTS indexing flag. Creates an LRU cache for performance optimization.
    - `ensure_table_exists()`: Create the lookup table if it doesn't exist, with optional FTS index. Creates a table with id (INTEGER PRIMARY KEY) and value column (TEXT), and optionally creates a FTS virtual table for full-text search.
    - `__repr__()`: Return a string representation showing the table name and row count.
    - `id_for_value(value)`: Get or create an ID for a given value, with LRU caching for performance. Checks in-memory cache first, queries database if not cached, inserts new values and updates FTS index if needed.

- `refactor_dataframes(conn, dataframes, foreign_keys, index_fts)`: Process DataFrames to extract columns into lookup tables and replace values with foreign key IDs. Creates or reuses LookupTable instances and applies transformations to all matching columns across DataFrames.

- `table_exists(conn, table)`: Check if a table exists in the SQLite database.

- `drop_table(conn, table)`: Drop a table from the database.

- `get_create_table_sql(table_name, df, index=True, sql_type_overrides=None, primary_keys=None)`: Generate CREATE TABLE SQL statement with proper column types and primary keys. Creates temporary in-memory table to infer schema, handles integer/float type detection for nullable columns, supports custom primary key definitions, and returns both SQL and column list.

- `to_sql_with_foreign_keys(conn, df, name, foreign_keys, sql_type_overrides=None, primary_keys=None, index_fks=False)`: Write DataFrame to SQLite with foreign key constraints and indexes. Generates CREATE TABLE with foreign key constraints, optionally creates indexes on foreign key columns, and inserts DataFrame data.

- `best_fts_version()`: Detect the most advanced FTS version supported by SQLite (FTS5, FTS4, or FTS3). Tests each version in order and returns the first one that works.

- `generate_and_populate_fts(conn, created_tables, cols, foreign_keys)`: Create and populate full-text search virtual tables. Creates FTS virtual tables for specified columns, handles simple SELECT for non-foreign-key columns, builds complex JOIN queries for foreign key columns, and populates FTS tables with data.

- `parse_shape(shape)`: Parse the shape string format (e.g., "county:Cty,votes:Vts(REAL)") into structured definitions. Extracts column mappings, type overrides, and rename specifications.

- `apply_shape(df, shape)`: Apply shape transformations to a DataFrame in-place. Drops unwanted columns, renames columns according to mapping, and returns SQL type overrides for to_sql().

- `add_index(conn, table_name, index)`: Create an index on specified columns (supports compound indexes). Validates columns exist in table and creates single or compound indexes.

- `apply_dates_and_datetimes(df, date_cols, datetime_cols, datetime_formats)`: Convert date and datetime columns to ISO format strings. Uses dateparser library to parse various date formats and supports custom datetime format strings.
