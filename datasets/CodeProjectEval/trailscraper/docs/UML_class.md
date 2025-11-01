## UML Class Diagram

```mermaid
classDiagram
    class BaseElement {
        +json_repr()
        +__eq__(other)
        +__ne__(other)
        +__hash__()
        +__repr__()
    }
    
    class Action {
        +string prefix
        +string action
        +json_repr()
        +_base_action()
        +matching_actions(allowed_prefixes)
    }
    
    class Statement {
        +list Action
        +string Effect
        +list Resource
        +json_repr()
        +merge(other)
        +__lt__(other)
    }
    
    class PolicyDocument {
        +string Version
        +list Statement
        +json_repr()
        +to_json()
    }
    
    class Record {
        +string event_source
        +string event_name
        +list resource_arns
        +string assumed_role_arn
        +datetime event_time
        +dict raw_source
        +_source_to_iam_prefix()
        +_event_name_to_iam_action()
        +_to_api_gateway_statement()
        +to_statement()
    }
    
    class LogFile {
        +string _path
        +timestamp()
        +filename()
        +has_valid_filename()
        +records()
        +contains_events_for_timeframe(from_date, to_date)
    }
    
    class LocalDirectoryRecordSource {
        +string _log_dir
        +_valid_log_files()
        +load_from_dir(from_date, to_date)
        +last_event_timestamp_in_dir()
    }
    
    class CloudTrailAPIRecordSource {
        +boto3_client _client
        +load_from_api(from_date, to_date)
    }
    
    class IAMJSONEncoder {
        +default(o)
    }
    
    BaseElement <|-- Action
    BaseElement <|-- Statement
    BaseElement <|-- PolicyDocument
    PolicyDocument "1" *-- "many" Statement
    Statement "1" *-- "many" Action
    LogFile "1" --> "many" Record : creates
    LocalDirectoryRecordSource "1" --> "many" LogFile : processes
    CloudTrailAPIRecordSource --> Record : creates
    Record --> Statement : converts to
    Statement --> PolicyDocument : aggregated into
    IAMJSONEncoder --> BaseElement : serializes
```
## UML Package Diagram

```mermaid
graph TB
    subgraph "CLI Layer"
        CLI["cli.py<br/>Command Line Interface"]
    end
    
    subgraph "Core Processing Modules"
        CLOUDTRAIL["cloudtrail.py<br/>Record, LogFile, Parsing"]
        IAM["iam.py<br/>Action, Statement, PolicyDocument"]
        POLICY_GEN["policy_generator.py<br/>generate_policy()"]
        GUESS["guess.py<br/>guess_statements()"]
    end
    
    subgraph "record_sources Package"
        RS_INIT["__init__.py"]
        LOCAL_SRC["local_directory_record_source.py<br/>LocalDirectoryRecordSource"]
        API_SRC["cloudtrail_api_record_source.py<br/>CloudTrailAPIRecordSource"]
    end
    
    subgraph "Utility Modules"
        S3_DOWNLOAD["s3_download.py<br/>S3 Download Functions"]
        TIME_UTILS["time_utils.py<br/>Time Parsing"]
        COLLECTION_UTILS["collection_utils.py<br/>Collection Helpers"]
        BOTO_DEFS["boto_service_definitions.py<br/>Service Definitions"]
    end
    
    subgraph "External Dependencies"
        BOTO3["boto3<br/>AWS SDK"]
        CLICK["click<br/>CLI Framework"]
        TOOLZ["toolz<br/>Functional Utils"]
    end
    
    CLI --> LOCAL_SRC
    CLI --> API_SRC
    CLI --> S3_DOWNLOAD
    CLI --> POLICY_GEN
    CLI --> GUESS
    CLI --> TIME_UTILS
    CLI --> CLICK
    
    LOCAL_SRC --> CLOUDTRAIL
    API_SRC --> CLOUDTRAIL
    API_SRC --> BOTO3
    
    CLOUDTRAIL --> IAM
    POLICY_GEN --> CLOUDTRAIL
    POLICY_GEN --> IAM
    GUESS --> IAM
    
    S3_DOWNLOAD --> BOTO3
    S3_DOWNLOAD --> TIME_UTILS
    
    LOCAL_SRC --> TOOLZ
    CLOUDTRAIL --> COLLECTION_UTILS
    CLOUDTRAIL --> BOTO_DEFS
``` 