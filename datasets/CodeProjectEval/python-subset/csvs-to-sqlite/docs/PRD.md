# PRD Document for csvs-to-sqlite

## Introduction

The purpose of this project is to develop a command-line utility that converts CSV (Comma-Separated Values) files into SQLite databases. The repository provides a comprehensive tool for data transformation, supporting various input formats and offering extensive customization options for database schema generation. This tool is designed for developers, data scientists, and end users who need to work with CSV data in a relational database format.

## Goals

The objective of this project is to provide a robust, flexible command-line interface for converting CSV files into SQLite databases with automatic type inference, support for multiple input sources, and advanced features like full-text search indexing and foreign key relationships. The tool should handle various CSV formats, support batch processing, and enable users to customize the resulting database schema according to their needs.

## Features and Functionalities

The following features and functionalities are expected in the project:

### Data Import
- Ability to convert single or multiple CSV files into SQLite database tables
- Ability to process entire directories containing CSV files recursively
- Ability to handle TSV (tab-separated values) files with custom field separators
- Ability to control field quoting behavior using CSV quoting constants (QUOTE_MINIMAL, QUOTE_ALL, QUOTE_NONNUMERIC, QUOTE_NONE)
- Ability to skip lines with too many fields instead of stopping the import
- Ability to replace existing tables in the database

### Schema Customization
- Ability to specify custom table names instead of using CSV filenames
- Ability to define custom database schema using shape parameter (format: `csvcol:dbcol(TYPE),...`)
- Ability to import all columns as text strings by default with `--just-strings` option
- Ability to automatically infer column data types (INTEGER, REAL, TEXT) from CSV content

### Data Transformation
- Ability to extract columns into separate lookup tables with foreign key relationships
- Ability to parse date columns into ISO formatted dates
- Ability to parse datetime columns into ISO formatted datetimes
- Ability to specify custom date/datetime format strings for parsing

### Database Optimization
- Ability to define primary keys on one or more columns
- Ability to create full-text search indexes on specified columns
- Ability to add single or compound indexes on columns
- Ability to control whether to add indexes on foreign key columns created via extraction
- Ability to control whether to add full-text indexes on extracted values

### Metadata Enhancement
- Ability to add a column populated with the source CSV filename
- Ability to populate columns with fixed string values
- Ability to populate columns with fixed integer values
- Ability to populate columns with fixed float values

## Technical Constraints

- The repository should use Python as the primary programming language
- The repository should provide a command-line interface using the Click library
- The repository should use Pandas for CSV data processing and type inference

## Requirements

### Dependencies

- `click>=7.0` - Command-line interface framework
- `dateparser>=1.0` - Date parsing library
- `pandas>=1.0` - Data manipulation and CSV processing
- `py-lru-cache~=0.1.4` - LRU cache implementation
- `six` - Python 2 and 3 compatibility utilities

### Development Dependencies

- `pytest` - Testing framework
- `pytest-cov` - Test coverage plugin for pytest
- `cogapp` - Code generation tool

## Usage

### Basic Conversion

To convert a single CSV file to SQLite:
```bash
csvs-to-sqlite myfile.csv mydatabase.db
```

To convert multiple CSV files:
```bash
csvs-to-sqlite one.csv two.csv bundle.db
```

To process all CSV files in a directory:
```bash
csvs-to-sqlite ~/path/to/directory all-my-csvs.db
```

### Advanced Usage Examples

Convert with custom table name:
```bash
csvs-to-sqlite myfile.csv mydatabase.db -t custom_table_name
```

Convert TSV file:
```bash
csvs-to-sqlite my-file.tsv my-file.db -s $'\t'
```

Extract columns into lookup tables:
```bash
csvs-to-sqlite data.csv output.db -c state:States:state_name
```

Add filename column and fixed columns:
```bash
csvs-to-sqlite data.csv output.db \
  --filename-column source \
  --fixed-column category "sales" \
  --fixed-column-int year 2024
```

Create full-text search index:
```bash
csvs-to-sqlite data.csv output.db -f description -f title
```

## Command Line Configuration Arguments

```
Usage: csvs-to-sqlite [OPTIONS] PATHS... DBNAME

  PATHS: paths to individual .csv files or to directories containing .csvs

  DBNAME: name of the SQLite database file to create

Options:
  -s, --separator TEXT            Field separator in input .csv
  -q, --quoting INTEGER           Control field quoting behavior per
                                  csv.QUOTE_* constants. Use one of
                                  QUOTE_MINIMAL (0), QUOTE_ALL (1),
                                  QUOTE_NONNUMERIC (2) or QUOTE_NONE (3).
  --skip-errors                   Skip lines with too many fields instead of
                                  stopping the import
  --replace-tables                Replace tables if they already exist
  -t, --table TEXT                Table to use (instead of using CSV filename)
  -c, --extract-column TEXT       One or more columns to 'extract' into a
                                  separate lookup table. If you pass a simple
                                  column name that column will be replaced
                                  with integer foreign key references to a new
                                  table of that name. You can customize the
                                  name of the table like so:
                                  state:States:state_name
                                  
                                  This will pull unique values from the
                                  'state' column and use them to populate a
                                  new 'States' table, with an id column
                                  primary key and a state_name column
                                  containing the strings from the original
                                  column.
  -d, --date TEXT                 One or more columns to parse into ISO
                                  formatted dates
  -dt, --datetime TEXT            One or more columns to parse into ISO
                                  formatted datetimes
  -df, --datetime-format TEXT     One or more custom date format strings to
                                  try when parsing dates/datetimes
  -pk, --primary-key TEXT         One or more columns to use as the primary
                                  key
  -f, --fts TEXT                  One or more columns to use to populate a
                                  full-text index
  -i, --index TEXT                Add index on this column (or a compound
                                  index with -i col1,col2)
  --shape TEXT                    Custom shape for the DB table - format is
                                  csvcol:dbcol(TYPE),...
  --filename-column TEXT          Add a column with this name and populate
                                  with CSV file name
  --fixed-column <TEXT TEXT>...   Populate column with a fixed string
  --fixed-column-int <TEXT INTEGER>...
                                  Populate column with a fixed integer
  --fixed-column-float <TEXT FLOAT>...
                                  Populate column with a fixed float
  --no-index-fks                  Skip adding index to foreign key columns
                                  created using --extract-column (default is
                                  to add them)
  --no-fulltext-fks               Skip adding full-text index on values
                                  extracted using --extract-column (default is
                                  to add them)
  --just-strings                  Import all columns as text strings by
                                  default (and, if specified, still obey
                                  --shape, --date/datetime, and --datetime-
                                  format)
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

## Terms/Concepts Explanation

**CSV (Comma-Separated Values)**: A plain text file format that stores tabular data where each line represents a row and fields are separated by commas (or other delimiters).

**SQLite**: A lightweight, file-based relational database management system that stores the entire database in a single file.

**Foreign Key**: A database constraint that establishes a relationship between two tables by referencing the primary key of another table.

**Full-Text Search (FTS)**: A database indexing technique that enables efficient searching of text content within columns.

**Type Inference**: The automatic detection of data types (INTEGER, REAL, TEXT) based on the content of CSV columns.

**Lookup Table**: A normalized database table that stores unique values referenced by foreign keys from other tables, reducing data redundancy.