## UML Class Diagram
```mermaid
classDiagram
  class AllInvalid {
  }
  class AnyInvalid {
  }
  class BooleanInvalid {
  }
  class CoerceInvalid {
  }
  class ContainsInvalid {
  }
  class DateInvalid {
  }
  class DatetimeInvalid {
  }
  class DictInvalid {
  }
  class DirInvalid {
  }
  class EmailInvalid {
  }
  class Error {
  }
  class ExactSequenceInvalid {
  }
  class ExclusiveInvalid {
  }
  class FalseInvalid {
  }
  class FileInvalid {
  }
  class InInvalid {
  }
  class InclusiveInvalid {
  }
  class Invalid {
    error_message
    error_type : Optional[typing.Optional[str]]
    msg
    path
    prepend(path: typing.List[typing.Hashable]) None
  }
  class LengthInvalid {
  }
  class LiteralInvalid {
  }
  class MatchInvalid {
  }
  class MultipleInvalid {
    error_message
    errors : list
    msg
    path
    add(error: Invalid) None
    prepend(path: typing.List[typing.Hashable]) None
  }
  class NotEnoughValid {
  }
  class NotInInvalid {
  }
  class ObjectInvalid {
  }
  class PathInvalid {
  }
  class RangeInvalid {
  }
  class RequiredFieldInvalid {
  }
  class ScalarInvalid {
  }
  class SchemaError {
  }
  class SequenceTypeInvalid {
  }
  class TooManyValid {
  }
  class TrueInvalid {
  }
  class TypeInvalid {
  }
  class UrlInvalid {
  }
  class ValueInvalid {
  }
  class Exclusive {
    group_of_exclusion : str
  }
  class Inclusive {
    group_of_inclusion : str
  }
  class Marker {
    description : typing.Any | None
    msg : Optional[typing.Optional[str]]
    schema
  }
  class Msg {
    cls : Optional[typing.Optional[typing.Type[Error]]]
    msg : str
    schema
  }
  class Object {
    cls : object
  }
  class Optional {
    default
  }
  class Remove {
  }
  class Required {
    default
  }
  class Schema {
    extra : int
    required : bool
    schema
    extend(schema: Schemable, required: typing.Optional[bool], extra: typing.Optional[int]) Schema
    infer(data) Schema
  }
  class Undefined {
  }
  class VirtualPathComponent {
  }
  class DefaultTo {
    default_value
    msg : Optional[typing.Optional[str]]
  }
  class Literal {
    lit
  }
  class Set {
    msg : Optional[typing.Optional[str]]
  }
  class SetTo {
    value
  }
  class All {
  }
  class Any {
  }
  class Clamp {
    max : SupportsAllComparisons | None
    min : SupportsAllComparisons | None
    msg : Optional[typing.Optional[str]]
  }
  class Coerce {
    msg : Optional[typing.Optional[str]]
    type : typing.Union[type, typing.Callable]
    type_name
  }
  class Contains {
    item
    msg : Optional[typing.Optional[str]]
  }
  class Date {
    DEFAULT_FORMAT : str
  }
  class Datetime {
    DEFAULT_FORMAT : str
    format : str
    msg : Optional[typing.Optional[str]]
  }
  class Equal {
    msg : Optional[typing.Optional[str]]
    target
  }
  class ExactSequence {
    msg : Optional[typing.Optional[str]]
    validators : typing.Iterable[Schemable]
  }
  class In {
    container : typing.Container | typing.Iterable
    msg : Optional[typing.Optional[str]]
  }
  class Length {
    max : SupportsAllComparisons | None
    min : SupportsAllComparisons | None
    msg : Optional[typing.Optional[str]]
  }
  class Match {
    msg : Optional[typing.Optional[str]]
    pattern : typing.Union[re.Pattern, str]
  }
  class NotIn {
    container : Iterable
    msg : Optional[typing.Optional[str]]
  }
  class Number {
    msg : Optional[typing.Optional[str]]
    precision : Optional[typing.Optional[int]]
    scale : Optional[typing.Optional[int]]
    yield_decimal : bool
  }
  class Range {
    max : SupportsAllComparisons | None
    max_included : bool
    min : SupportsAllComparisons | None
    min_included : bool
    msg : Optional[typing.Optional[str]]
  }
  class Replace {
    msg : Optional[typing.Optional[str]]
    pattern : typing.Union[re.Pattern, str]
    substitution : str
  }
  class SomeOf {
    max_valid
    min_valid : int
  }
  class Union {
  }
  class Unique {
    msg : Optional[typing.Optional[str]]
  }
  class Unordered {
    msg : Optional[typing.Optional[str]]
    validators : typing.Iterable[Schemable]
  }
  class _WithSubValidators {
    discriminant : NoneType
    msg : NoneType
    required : bool
    schema
    validators : tuple
  }
  AllInvalid --|> Invalid
  AnyInvalid --|> Invalid
  BooleanInvalid --|> Invalid
  CoerceInvalid --|> Invalid
  ContainsInvalid --|> Invalid
  DateInvalid --|> Invalid
  DatetimeInvalid --|> Invalid
  DictInvalid --|> Invalid
  DirInvalid --|> Invalid
  EmailInvalid --|> Invalid
  ExactSequenceInvalid --|> Invalid
  ExclusiveInvalid --|> Invalid
  FalseInvalid --|> Invalid
  FileInvalid --|> Invalid
  InInvalid --|> Invalid
  InclusiveInvalid --|> Invalid
  Invalid --|> Error
  LengthInvalid --|> Invalid
  LiteralInvalid --|> Invalid
  MatchInvalid --|> Invalid
  MultipleInvalid --|> Invalid
  NotEnoughValid --|> Invalid
  NotInInvalid --|> Invalid
  ObjectInvalid --|> Invalid
  PathInvalid --|> Invalid
  RangeInvalid --|> Invalid
  RequiredFieldInvalid --|> Invalid
  ScalarInvalid --|> Invalid
  SchemaError --|> Error
  SequenceTypeInvalid --|> Invalid
  TooManyValid --|> Invalid
  TrueInvalid --|> Invalid
  TypeInvalid --|> Invalid
  UrlInvalid --|> Invalid
  ValueInvalid --|> Invalid
  Exclusive --|> Optional
  Inclusive --|> Optional
  Optional --|> Marker
  Remove --|> Marker
  Required --|> Marker
  All --|> _WithSubValidators
  Any --|> _WithSubValidators
  Date --|> Datetime
  SomeOf --|> _WithSubValidators
  Union --|> _WithSubValidators
  Schema --* Msg : schema
  Undefined --* Optional : default
  Undefined --* Required : default
  Schema --o _WithSubValidators : schema

```

## UML Package Diagram
```mermaid
classDiagram
  class voluptuous {
  }
  class error {
  }
  class humanize {
  }
  class schema_builder {
  }
  class util {
  }
  class validators {
  }
  voluptuous --> error
  voluptuous --> schema_builder
  voluptuous --> util
  voluptuous --> validators
  humanize --> voluptuous
  humanize --> error
  humanize --> schema_builder
  schema_builder --> voluptuous
  schema_builder --> error
  util --> voluptuous
  util --> error
  util --> schema_builder
  util --> validators
  validators --> error
  validators --> schema_builder
```
