I understand you're asking for UML diagrams for the voluptuous validation library. <cite/> Let me generate three types of diagrams: a class diagram showing the main classes and their relationships, a package relationship diagram, and a sequence diagram showing the validation flow. <cite/>

## UML Class Diagram

```mermaid
classDiagram
    class Schema {
        +dict schema
        +bool required
        +int extra
        +function _compiled
        +__init__(schema, required, extra)
        +__call__(data)
        +infer(data) Schema
        +extend(schema, required, extra) Schema
        -_compile(schema)
        -_compile_dict(schema)
        -_compile_mapping(schema, invalid_msg)
        -_compile_object(schema)
        -_compile_sequence(schema, seq_type)
        -_compile_tuple(schema)
        -_compile_list(schema)
        -_compile_set(schema)
        -_compile_scalar(schema)
    }
    
    class Marker {
        +schema
        +Schema _schema
        +str msg
        +description
        +__init__(schema_, msg, description)
        +__call__(v)
        +__str__()
        +__repr__()
        +__lt__(other)
        +__eq__(other)
    }
    
    class Optional {
        +default
        +__init__(schema, msg, default, description)
    }
    
    class Required {
        +default
        +__init__(schema, msg, default, description)
    }
    
    class Exclusive {
        +str group_of_exclusion
        +__init__(schema, group_of_exclusion, msg, description)
    }
    
    class Inclusive {
        +str group_of_inclusion
        +default
        +__init__(schema, group_of_inclusion, msg, description, default)
    }
    
    class Remove {
        +__init__(schema_, msg, description)
        +__call__(schema)
        +__repr__()
    }
    
    class Object {
        +cls
        +__init__(schema, cls)
    }
    
    class Msg {
        +schema
        +str msg
        +cls
        +__init__(schema, msg, cls)
        +__call__(v)
        +__repr__()
    }
    
    class Undefined {
        +__nonzero__()
        +__repr__()
    }
    
    class VirtualPathComponent {
        +__str__()
        +__repr__()
    }
    
    class _WithSubValidators {
        +list validators
        +str msg
        +bool required
        +discriminant
        +list _compiled
        +Schema schema
        +__init__(validators, msg, required, discriminant)
        +__voluptuous_compile__(schema)
        +_run(path, value)
        +__call__(v)
        +_exec(funcs, v, path)*
    }
    
    class Union {
        +_exec(funcs, v, path)
    }
    
    class ExactSequence {
        +list validators
        +str msg
        +__init__(validators, msg)
        +__call__(v)
        +__repr__()
    }
    
    class SomeOf {
        +int min_valid
        +int max_valid
        +__init__(validators, min_valid, max_valid)
        +_exec(funcs, v, path)
        +__repr__()
    }
    
    class Unordered {
        +list validators
        +str msg
        +list _schemas
        +__init__(validators, msg)
        +__call__(v)
        +__repr__()
    }
    
    Marker <|-- Optional
    Marker <|-- Required
    Marker <|-- Remove
    Optional <|-- Exclusive
    Optional <|-- Inclusive
    dict <|-- Object
    str <|-- VirtualPathComponent
    _WithSubValidators <|-- Union
    _WithSubValidators <|-- SomeOf
    Schema ..> Marker : uses
    Schema ..> Object : uses
    Marker ..> Schema : creates
    _WithSubValidators ..> Schema : compiles with
```
## Package Relationship Diagram

```mermaid
graph TB
    subgraph "voluptuous Package"
        init["__init__.py<br/>(Package Entry Point)"]
        schema["schema_builder.py<br/>(Core Schema & Markers)"]
        validators["validators.py<br/>(Validation Functions)"]
        error["error.py<br/>(Exception Classes)"]
        util["util.py<br/>(Utility Functions)"]
        humanize["humanize.py<br/>(Error Formatting)"]
    end
    
    subgraph "External Dependencies"
        typing["typing<br/>(Type Hints)"]
        collections["collections<br/>(Data Structures)"]
        datetime_mod["datetime<br/>(Date/Time)"]
        re["re<br/>(Regex)"]
    end
    
    init --> schema
    init --> validators
    init --> error
    init --> util
    init --> humanize
    
    schema --> error
    schema --> typing
    
    validators --> schema
    validators --> error
    validators --> typing
    validators --> datetime_mod
    validators --> re
    
    humanize --> error
    
    util --> error
```

## Sequence Diagram: Schema Validation Flow

```mermaid
sequenceDiagram
    participant User
    participant Schema
    participant _compile
    participant _compile_dict
    participant _compile_scalar
    participant validate_dict
    participant Marker
    
    User->>Schema: Schema({Required("name"): str, "age": int})
    activate Schema
    Schema->>Schema: __init__()
    Schema->>_compile: _compile(schema_dict)
    activate _compile
    
    _compile->>_compile: Check schema type
    _compile->>_compile_dict: isinstance(Mapping)
    activate _compile_dict
    
    _compile_dict->>_compile_dict: Extract Required markers
    _compile_dict->>_compile_dict: Build required_keys set
    _compile_dict->>_compile_dict: Build default_keys dict
    
    loop For each key-value pair
        _compile_dict->>_compile: _compile(key)
        _compile->>_compile_scalar: _compile_scalar(Required("name"))
        activate _compile_scalar
        _compile_scalar->>Marker: Compile marker schema
        _compile_scalar-->>_compile: key_validator
        deactivate _compile_scalar
        
        _compile_dict->>_compile: _compile(value)
        _compile->>_compile_scalar: _compile_scalar(str)
        activate _compile_scalar
        _compile_scalar-->>_compile: value_validator
        deactivate _compile_scalar
    end
    
    _compile_dict->>_compile_dict: Sort candidates by priority
    _compile_dict->>_compile_dict: Optimize into candidates_by_key
    _compile_dict->>_compile_dict: Create validate_dict closure
    _compile_dict-->>_compile: validate_dict function
    deactivate _compile_dict
    
    _compile-->>Schema: Store in self._compiled
    deactivate _compile
    Schema-->>User: Schema instance
    deactivate Schema
    
    User->>Schema: schema({"name": "Alice", "age": 30})
    activate Schema
    Schema->>validate_dict: self._compiled([], data)
    activate validate_dict
    
    validate_dict->>validate_dict: Check required keys present
    validate_dict->>validate_dict: Apply defaults if needed
    
    loop For each data key
        validate_dict->>validate_dict: Match against candidates_by_key
        validate_dict->>validate_dict: Validate key with key_validator
        validate_dict->>validate_dict: Validate value with value_validator
        validate_dict->>validate_dict: Add to output dict
    end
    
    validate_dict->>validate_dict: Check Exclusive groups
    validate_dict->>validate_dict: Check Inclusive groups
    validate_dict->>validate_dict: Handle extra keys per policy
    
    validate_dict-->>Schema: Validated data
    deactivate validate_dict
    Schema-->>User: {"name": "Alice", "age": 30}
    deactivate Schema
```