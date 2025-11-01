## UML Class Diagram

```mermaid
classDiagram
  class LogFile {
    contains_events_for_timeframe(from_date, to_date)
    filename()
    has_valid_filename()
    records()
    timestamp()
  }
  class Record {
    assumed_role_arn : NoneType
    event_name
    event_source
    event_time : NoneType
    raw_source : NoneType
    resource_arns : list
    to_statement()
  }
  class Action {
    action
    prefix
    json_repr()
    matching_actions(allowed_prefixes)
  }
  class BaseElement {
    json_repr()*
  }
  class IAMJSONEncoder {
    default(o)
  }
  class PolicyDocument {
    Statement
    Version : str
    json_repr()
    to_json()
  }
  class Statement {
    Action
    Effect
    Resource
    json_repr()
    merge(other)
  }
  class CloudTrailAPIRecordSource {
    load_from_api(from_date, to_date)
  }
  class LocalDirectoryRecordSource {
    last_event_timestamp_in_dir()
    load_from_dir(from_date, to_date)
  }
  Action --|> BaseElement
  PolicyDocument --|> BaseElement
  Statement --|> BaseElement
```
## UML Package Diagram

```mermaid
classDiagram
  class trailscraper {
  }
  class boto_service_definitions {
  }
  class cli {
  }
  class cloudtrail {
  }
  class collection_utils {
  }
  class guess {
  }
  class iam {
  }
  class policy_generator {
  }
  class record_sources {
  }
  class cloudtrail_api_record_source {
  }
  class local_directory_record_source {
  }
  class s3_download {
  }
  class time_utils {
  }
  cli --> trailscraper
  cli --> cloudtrail
  cli --> guess
  cli --> iam
  cli --> policy_generator
  cli --> cloudtrail_api_record_source
  cli --> local_directory_record_source
  cli --> s3_download
  cli --> time_utils
  cloudtrail --> boto_service_definitions
  cloudtrail --> iam
  guess --> iam
  policy_generator --> cloudtrail
  policy_generator --> iam
  cloudtrail_api_record_source --> cloudtrail
  local_directory_record_source --> cloudtrail
  s3_download --> collection_utils
```

