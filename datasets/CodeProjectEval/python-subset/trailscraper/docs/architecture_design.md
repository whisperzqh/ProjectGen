# Architecture Design

Below is a text-based representation of the file tree.

``` bash
├── trailscraper
│   ├── boto_service_definitions.py
│   ├── cli.py
│   ├── cloudtrail.py
│   ├── collection_utils.py
│   ├── guess.py
│   ├── iam.py
│   ├── __init__.py
│   ├── known-iam-actions.txt
│   ├── policy_generator.py
│   ├── record_sources
│   │   ├── cloudtrail_api_record_source.py
│   │   ├── __init__.py
│   │   └── local_directory_record_source.py
│   ├── s3_download.py
│   └── time_utils.py
```

`boto_service_definitions.py`:

- `boto_service_definition_files()`: Returns a list of file paths to all service definition files (named `service-*.json`) provided by the `botocore` library, located within its installed data directory.

- `service_definition_file(servicename)`: Returns the file path to the most recent (lexicographically last) service definition file for the specified AWS service name by scanning all matching `service-*.json` files under the service’s directory in `botocore`'s data folder.

- `operation_definition(servicename, operationname)`: Loads the service definition file for the given AWS service and returns the JSON object describing the specified operation, as defined under the `'operations'` key in the service model.

`cli.py` :

- `root_group(verbose)`: The main Click command group for the Trailscraper CLI. Sets up logging verbosity and serves as the entry point for all subcommands. Displays the tool’s version when requested.

- `download(bucket, prefix, org_id, account_id, region, log_dir, from_s, to_s, wait, parallelism)`: Downloads AWS CloudTrail log files from a specified S3 bucket and prefix, filtered by organization ID, account ID(s), and region(s), within a given time range. Optionally waits until logs include events up to the specified end time.

- `select(log_dir, filter_assumed_role_arn, use_cloudtrail_api, from_s, to_s)`: Retrieves and filters CloudTrail records either from local log files or directly via the CloudTrail API, based on assumed role ARNs and a time window, then outputs matching records in JSON format.

- `generate()`: Reads CloudTrail records from standard input (STDIN) in JSON format and generates a minimal IAM policy that permits all observed API actions.

- `guess(only)`: Reads an IAM policy from STDIN and extends it by guessing additional related actions (e.g., adding "Describe*" actions when "List*" are present), optionally restricted to specified action prefixes.

- `last_event_timestamp(log_dir)`: Scans local CloudTrail log files and prints the timestamp of the most recent event found.

`cloudtrail.py` :

- `Record(event_source, event_name, resource_arns, assumed_role_arn, event_time, raw_source)`: Represents a single AWS CloudTrail log event. Encapsulates metadata such as the service invoked, action performed, associated resources, identity context, and timestamp.

  - The method `to_statement()` converts the record into a corresponding IAM policy statement that would permit the observed action. Handles special cases for services like S3, KMS, STS, and API Gateway.
  - The method `_source_to_iam_prefix()` maps CloudTrail event sources (e.g., `s3.amazonaws.com`) to their IAM service prefixes (e.g., `s3`), with overrides for known special cases.
  - The method `_event_name_to_iam_action()` normalizes CloudTrail event names to standard IAM action names, applying service-specific mappings and regex-based transformations.
  - The method `_to_api_gateway_statement()` constructs a precise IAM statement for API Gateway events using service definition metadata to determine HTTP method and resource path.

- `LogFile(path)`: Represents a single gzipped CloudTrail log file on disk.

  - The method `timestamp()` extracts the delivery timestamp from the log filename using a high-performance substring approach.
  - The method `filename()` returns the base name of the log file.
  - The method `has_valid_filename()` checks whether the filename matches the expected CloudTrail log naming pattern.
  - The method `records()` decompresses and parses the JSON log file into a list of `Record` objects, handling I/O errors gracefully.
  - The method `contains_events_for_timeframe(from_date, to_date)` heuristically determines if the log file may contain events within the specified time window (allowing a 1-hour buffer).

- `_resource_arns(json_record)`: Extracts a list of ARNs from the `resources` field of a raw CloudTrail JSON record.

- `_assumed_role_arn(json_record)`: Extracts the ARN of the assumed IAM role from the `userIdentity` section of a CloudTrail record, if applicable.

- `_parse_record(json_record)`: Converts a raw CloudTrail JSON event into a `Record` object, parsing the event time and handling missing keys gracefully with logging.

- `parse_records(json_records)`: Transforms a list of raw CloudTrail JSON records into a list of validated `Record` objects, filtering out any that fail to parse.

- `_by_timeframe(from_date, to_date)`: Returns a predicate function that checks whether a `Record`’s event time falls within the specified inclusive time range.

- `_by_role_arns(arns_to_filter_for)`: Returns a predicate function that checks whether a `Record` was executed under one of the specified assumed role ARNs (or passes if no filter is provided).

- `filter_records(records, arns_to_filter_for, from_date, to_date)`: Filters a list of `Record` objects based on assumed role ARN and time window. Logs a warning if no records match but input records exist.

`collection_utils.py`:

- `consume(iterator)`: Consumes all items in the given iterator without storing them, typically used to trigger side effects (e.g., lazy evaluation or I/O operations). Implemented efficiently using `collections.deque(iterator, maxlen=0)` as recommended in the itertools recipes.

`guess.py` :

- `_guess_actions(actions, allowed_prefixes)`: For a given list of IAM actions, returns a flattened list of related actions (e.g., "Describe*" or "List*") that match any of the specified verb prefixes (like "Describe", "Get", etc.), using each action’s `matching_actions` method.

- `_extend_statement(statement, allowed_prefixes)`: Attempts to extend a single IAM policy statement by guessing additional related actions based on the allowed prefixes. If new actions are found, it returns both the original statement and a new broad statement (with `"*"` resource) containing the guessed actions; otherwise, it returns only the original statement.

- `guess_statements(policy, allowed_prefixes)`: Takes an IAM `PolicyDocument` and a list of allowed action prefixes (e.g., `["Describe", "List"]`) and returns a new policy that includes the original statements plus additional statements with guessed related actions. This is used to suggest permissions that are commonly used together with observed actions.

`iam.py` :

- `BaseElement`: Abstract base class for IAM policy elements. Provides default implementations for equality, hashing, string representation, and JSON serialization via the `json_repr()` method, which subclasses must implement.

- `Action(prefix, action)`: Represents a single IAM action (e.g., `s3:GetObject`).

  - The method `json_repr()` returns the action as a string in `"prefix:action"` format.
  - The method `_base_action()` strips common IAM verb prefixes (like "Describe", "List") and plural "s" to derive a canonical base name for the action.
  - The method `matching_actions(allowed_prefixes)` returns a list of related IAM actions (e.g., "Describe*", "List*") that share the same base resource but differ in verb prefix, filtered to only include actions known to exist in AWS IAM.

- `Statement(Action, Effect, Resource)`: Represents a single statement in an IAM policy.

  - The method `json_repr()` returns a dictionary representation compatible with AWS IAM policy syntax.
  - The method `merge(other)` combines two statements with the same effect by merging their actions and resources, deduplicating and sorting the results.
  - Implements rich comparison (`__lt__`) to enable sorting of statements by effect, actions, and resources.

- `PolicyDocument(Statement, Version)`: Represents a full IAM policy document.

  - The method `json_repr()` returns a dictionary with `Version` and `Statement` keys.
  - The method `to_json()` serializes the policy to a formatted JSON string suitable for use with AWS IAM.

- `IAMJSONEncoder`: A custom JSON encoder that uses the `json_repr()` method of `BaseElement` subclasses to serialize IAM policy objects.

- `_parse_action(action)`: Parses a string like `"s3:GetObject"` into an `Action` object by splitting on the colon.

- `_parse_statement(statement)`: Converts a dictionary representing a single IAM policy statement into a `Statement` object, parsing its actions into `Action` instances.

- `_parse_statements(json_data)`: Converts a list of IAM policy statement dictionaries into a list of `Statement` objects.

- `parse_policy_document(stream)`: Reads a JSON IAM policy from a file-like object or string and returns a `PolicyDocument` instance.

- `all_known_iam_permissions()`: Reads the bundled `known-iam-actions.txt` file and returns a set of all known AWS IAM actions as strings (e.g., `"s3:GetObject"`).

- `known_iam_actions(prefix)`: Returns a list of `Action` objects corresponding to all known IAM actions for a given service prefix (e.g., `"ec2"`), using `all_known_iam_permissions()` and grouping by prefix.

`policy_generator.py` :

- `_combine_statements_by(key)`: Returns a function that groups a list of IAM `Statement` objects by a specified key (e.g., resource list or action list) and merges statements within each group using the `Statement.merge()` method. This enables consolidation of overlapping permissions.

- `generate_policy(selected_records)`: Takes a list of `Record` objects from CloudTrail and generates a minimal, consolidated IAM policy document. It converts each record to a policy statement, filters out `None` results (e.g., from ignored events like `sts:GetCallerIdentity`), merges statements first by shared resources and then by shared actions, and finally sorts the resulting statements for deterministic output.

`s3_download.py` :

- `_s3_key_prefix(prefix, date, account_id, region)`: Constructs the S3 key prefix for standard (non-organization) CloudTrail logs based on the given account ID, region, and date.

- `_s3_key_prefix_for_org_trails(prefix, date, org_id, account_id, region)`: Constructs the S3 key prefix for CloudTrail logs from AWS Organizations, which include an additional organizational ID segment in the path.

- `_s3_key_prefixes(prefix, org_ids, account_ids, regions, from_date, to_date)`: Generates a complete list of S3 key prefixes covering all combinations of accounts, regions, and days within the specified time range. Supports both standard and organization-enabled trails.

- `_s3_download_recursive(bucket, prefixes, target_dir, parallelism)`: Recursively lists and downloads CloudTrail log files from an S3 bucket that match any of the provided prefixes. Uses a thread-local S3 client for thread safety and downloads files in parallel using a `ThreadPoolExecutor`. Skips files that already exist locally.

  - The nested function `get_s3_client()` ensures each thread has its own boto3 S3 client.
  - The nested function `_download_file(key)` downloads a single S3 object to the local filesystem.
  - The nested function `_starts_with_prefix(potential_prefix)` checks if a given S3 prefix matches any of the target prefixes (used during recursive listing).
  - The nested function `_list_files_to_download(current_prefix)` recursively traverses S3 "directories" (common prefixes) and collects all leaf objects that fall under the specified target prefixes.

- `download_cloudtrail_logs(target_dir, bucket, cloudtrail_prefix, org_ids, account_ids, regions, from_date, to_date, parallelism)`: Public entry point that orchestrates the download of CloudTrail logs from S3 by first computing all relevant S3 key prefixes and then invoking the recursive downloader.

`time_utils.py`:

- `parse_human_readable_time(time_string)`: Parse human readable strings (e.g. "now", "2017-01-01" and "one hour ago") into datetime.

`record_source/cloudtrail_api_record_source.py`:

- `CloudTrailAPIRecordSource()`: A class to represent CloudTrail records from the CloudTrail lookup_events API.

  - `__init__(self)`: Initializes a CloudTrailAPIRecordSource instance by creating a boto3 CloudTrail client.

  - `load_from_api(self, from_date, to_date)`: Loads the last 10 hours of CloudTrail events from the API.  
    Queries the CloudTrail `lookup_events` API using pagination between the specified `from_date` and `to_date`, parses each raw event using `_parse_record`, and returns a list of parsed CloudTrail records.

`record_source/local_directory_record_source.py`:

- `LocalDirectoryRecordSource(log_dir)`: A class to represent CloudTrail records stored on disk.

  - `__init__(self, log_dir)`: Initializes a LocalDirectoryRecordSource instance with the specified local directory path containing CloudTrail log files.

  - `_valid_log_files(self)`: Returns an iterable of `LogFile` objects representing files in the log directory with valid CloudTrail log filenames.  
    Invalid filenames are logged as warnings and excluded from the result.

  - `load_from_dir(self, from_date, to_date)`: Loads all CloudTrail records from valid log files in the directory that contain events within the specified time range (`from_date` to `to_date`).

  - `last_event_timestamp_in_dir(self)`: Return the timestamp of the most recent event in the given directory.  
    It identifies the most recent log file by filename timestamp, then finds the latest event within that file’s records.
