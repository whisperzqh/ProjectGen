## UML Class Diagram

```mermaid
classDiagram
  class Accessor {
    key
    parse_key(key)
  }
  class MLLPClient {
    encoding : str
    socket : socket
    close()
    send(data)
    send_message(message)
  }
  class MLLPException {
  }
  class Batch {
    header
    trailer
    create_header()
    create_trailer()
  }
  class Component {
  }
  class Container {
    esc : str
    factory
    separator
    separators : str
    create_batch(seq)
    create_component(seq)
    create_field(seq)
    create_file(seq)
    create_message(seq)
    create_repetition(seq)
    create_segment(seq)
  }
  class Factory {
    create_batch
    create_component
    create_field
    create_file
    create_message
    create_repetition
    create_segment
  }
  class Field {
  }
  class File {
    header
    trailer
    create_header()
    create_trailer()
  }
  class Message {
    assign_field(value, segment, segment_num, field_num, repeat_num, component_num, subcomponent_num)
    create_ack(ack_code, message_id, application, facility)
    escape(field, app_map)
    extract_field(segment, segment_num, field_num, repeat_num, component_num, subcomponent_num)
    segment(segment_id)
    segments(segment_id)
    unescape(field, app_map)
  }
  class Repetition {
  }
  class Segment {
    assign_field(value, field_num, repeat_num, component_num, subcomponent_num)
    extract_field(segment_num, field_num, repeat_num, component_num, subcomponent_num)
  }
  class Sequence {
  }
  class _UTCOffset {
    minutes : int
    dst(dt)
    tzname(dt)
    utcoffset(dt)
  }
  class HL7Exception {
  }
  class MalformedBatchException {
  }
  class MalformedFileException {
  }
  class MalformedSegmentException {
  }
  class ParseException {
  }
  class InvalidBlockError {
  }
  class HL7StreamProtocol {
    connection_made(transport)
  }
  class HL7StreamReader {
    encoding
    encoding_errors
    readmessage()
  }
  class HL7StreamWriter {
    encoding
    encoding_errors
    writemessage(message)
  }
  class MLLPStreamReader {
    readblock()
  }
  class MLLPStreamWriter {
    writeblock(data)
  }
  class _ParsePlan {
    containers
    esc
    factory
    separator
    separators
    applies(text)
    container(data)
    next()
  }
  Batch --|> Container
  Component --|> Container
  Container --|> Sequence
  Field --|> Container
  File --|> Container
  Message --|> Container
  Repetition --|> Container
  Segment --|> Container
  MalformedBatchException --|> HL7Exception
  MalformedFileException --|> HL7Exception
  MalformedSegmentException --|> HL7Exception
  ParseException --|> HL7Exception
  HL7StreamReader --|> MLLPStreamReader
  HL7StreamWriter --|> MLLPStreamWriter
  Container --> Factory : factory
  Batch --o Factory : create_batch
  Component --o Factory : create_component
  Field --o Factory : create_field
  File --o Factory : create_file
  Message --o Factory : create_message
  Repetition --o Factory : create_repetition
  Segment --o Factory : create_segment
```

## UML Package Diagram

```mermaid
classDiagram
  class hl7 {
  }
  class accessor {
  }
  class client {
  }
  class containers {
  }
  class datatypes {
  }
  class exceptions {
  }
  class mllp {
  }
  class exceptions {
  }
  class streams {
  }
  class parser {
  }
  class util {
  }
  hl7 --> accessor
  hl7 --> containers
  hl7 --> datatypes
  hl7 --> exceptions
  hl7 --> parser
  hl7 --> util
  client --> hl7
  containers --> accessor
  containers --> exceptions
  containers --> util
  mllp --> exceptions
  mllp --> streams
  streams --> exceptions
  streams --> parser
  parser --> containers
  parser --> exceptions
  parser --> util
```