# Architecture Design

Below is a text-based representation of the file tree. 
```bash
├── hl7
│   ├── accessor.py
│   ├── client.py
│   ├── containers.py
│   ├── datatypes.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── mllp
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   └── streams.py
│   ├── parser.py
│   └── util.py
```

`accessor.py`:

- `Accessor`: A class that represents an accessor for an HL7 segment.

    - `Accessor.__new__(cls, segment, segment_num=1, field_num=None, repeat_num=None, component_num=None, subcomponent_num=None)`: Create a new instance of Accessor for *segment*. Index numbers start from 1.

    - `Accessor.key`: Return the string accessor key that represents this instance.

    - `Accessor.__str__()`: Return the string representation of the accessor, equivalent to its key.

    - `Accessor.parse_key(key)`: Create an Accessor by parsing an accessor key.

    The key is defined as:

        |   SEG[n]-Fn-Rn-Cn-Sn
        |       F   Field
        |       R   Repeat
        |       C   Component
        |       S   Sub-Component
        |
        |   *Indexing is from 1 for compatibility with HL7 spec numbering.*

    Example:

        |   PID.F1.R1.C2.S2 or PID.1.1.2.2
        |
        |   PID (default to first PID segment, counting from 1)
        |   F1  (first after segment id, HL7 Spec numbering)
        |   R1  (repeat counting from 1)
        |   C2  (component 2 counting from 1)
        |   S2  (component 2 counting from 1)

`client.py`:

- `MLLPException`: Exception raised for errors in MLLP communication.

- `MLLPClient`: A basic, blocking, HL7 MLLP client based upon :py:mod:`socket`.

    - `MLLPClient.__init__(self, host, port, encoding="utf-8")`: Initialize the MLLP client by connecting to the specified host and port. The `encoding` parameter (defaulting to UTF-8) is used for encoding unicode messages.

    - `MLLPClient.__enter__(self)`: Enter the runtime context for the `with` statement, returning the client instance.

    - `MLLPClient.__exit__(self, exc_type, exc_val, trackeback)`: Exit the runtime context for the `with` statement, ensuring the socket connection is closed.

    - `MLLPClient.close(self)`: Release the socket connection.

    - `MLLPClient.send_message(self, message)`: Wraps a byte string, unicode string, or :py:class:`hl7.Message` in an MLLP container and sends the message to the server. If the message is a byte string, it is assumed to be correctly encoded. Otherwise, it is encoded using the client’s encoding.

    - `MLLPClient.send(self, data)`: Low-level method to send raw data (already wrapped in an MLLP container) directly over the socket. Blocks until the server returns a response.

- `stdout(content)`: Writes content to standard output, handling both bytes and strings appropriately for the Python version.

- `stdin()`: Returns the standard input stream (`sys.stdin`).

- `stderr()`: Returns the standard error stream (`sys.stderr`).

- `read_stream(stream)`: Buffers the input stream and yields individual HL7 messages stripped of MLLP framing characters (`<SB>`, `<EB>`, `<CR>`). Handles both `<EB>` and `<FF>` as message separators.

- `read_loose(stream)`: Parses a loosely formatted HL7-like blob (e.g., with `\r\n` line endings) into valid HL7 messages. Assumes messages start with `"MSH|^~\&|"` and reconstructs them by removing MLLP control characters and normalizing line endings.

- `mllp_send()`: Command-line tool to send HL7 messages to an MLLP server. Supports reading from stdin or a file, with options for port, verbosity, and loose message parsing. Sends each message via an `MLLPClient` and optionally prints server responses.

`containers.py`:

- `Sequence`: Base class for sequences that support 1-based indexing via callable syntax.

    - `Sequence.__call__(self, index, value=_SENTINEL)`: Allows getting or setting items using HL7-compatible 1-based indices (e.g., `seq(1)` returns the first item). If a `value` is provided, it sets the item at the given index.

    - `Sequence._adjust_index(self, index)`: Converts a 1-based HL7 index to a 0-based Python list index. Subclasses may override this behavior.

- `Container`: Abstract root class for HL7 message parts. Inherits from `Sequence` and supports recursive container creation and string representation.

    - `Container.__init__(self, separator, sequence=[], esc="\\", separators="\r|~^&", factory=None)`: Initializes the container with a separator, optional sequence, escape character, field separators, and a factory for creating nested containers.

    - `Container.create_file(self, seq)`: Creates a new `hl7.File` instance compatible with this container.

    - `Container.create_batch(self, seq)`: Creates a new `hl7.Batch` instance compatible with this container.

    - `Container.create_message(self, seq)`: Creates a new `hl7.Message` instance compatible with this container.

    - `Container.create_segment(self, seq)`: Creates a new `hl7.Segment` instance compatible with this container.

    - `Container.create_field(self, seq)`: Creates a new `hl7.Field` instance compatible with this container.

    - `Container.create_repetition(self, seq)`: Creates a new `hl7.Repetition` instance compatible with this container.

    - `Container.create_component(self, seq)`: Creates a new `hl7.Component` instance compatible with this container.

    - `Container.__getitem__(self, item)`: Overrides list slicing to return a new instance of the same container subclass when sliced.

    - `Container.__str__(self)`: Returns a string representation by joining child elements with the container’s separator.

- `File`: Represents an HL7 file in batch protocol, containing a list of `Batch` instances. May include optional FHS (file header) and FTS (file trailer) segments.

    - `File.__init__(self, separator=None, sequence=[], esc="\\", separators="\r|~^&", factory=None)`: Initializes the file container using the segment separator (first character of `separators`).

    - `File.header`: Property to get or set the FHS segment. Raises `MalformedSegmentException` if assigned a non-FHS segment.

    - `File.trailer`: Property to get or set the FTS segment. Raises `MalformedSegmentException` if assigned a non-FTS segment.

    - `File.create_header(self)`: Creates a standard FHS segment compatible with this file.

    - `File.create_trailer(self)`: Creates a standard FTS segment compatible with this file.

    - `File.__str__(self)`: Returns the string representation of the file. If header and trailer are present, they are included; otherwise, only batches are joined. Raises `MalformedFileException` if only one of header or trailer is present.

- `Batch`: Represents an HL7 batch in batch protocol, containing a list of `Message` instances. May include optional BHS (batch header) and BTS (batch trailer) segments.

    - `Batch.__init__(self, separator=None, sequence=[], esc="\\", separators="\r|~^&", factory=None)`: Initializes the batch container using the segment separator.

    - `Batch.header`: Property to get or set the BHS segment. Raises `MalformedSegmentException` if assigned a non-BHS segment.

    - `Batch.trailer`: Property to get or set the BTS segment. Raises `MalformedSegmentException` if assigned a non-BTS segment.

    - `Batch.create_header(self)`: Creates a standard BHS segment compatible with this batch.

    - `Batch.create_trailer(self)`: Creates a standard BTS segment compatible with this batch.

    - `Batch.__str__(self)`: Returns the string representation of the batch. Includes BHS/BTS if both are present; raises `MalformedBatchException` if only one is present.

- `Message`: Represents an HL7 message, containing a list of `Segment` instances.

    - `Message.__init__(self, separator=None, sequence=[], esc="\\", separators="\r|~^&", factory=None)`: Initializes the message container using the segment separator.

    - `Message.__getitem__(self, key)`: Supports multiple access patterns:
        - Integer: returns segment at index.
        - 3-character string (e.g., `'PID'`): returns all segments with that ID via `segments()`.
        - Longer string or `Accessor`: delegates to `extract_field()`.

    - `Message.__setitem__(self, key, value)`: Supports assignment via:
        - Integer index: sets segment.
        - Accessor-style string (e.g., `"PID.2"`) or `Accessor` object: delegates to `assign_field()`.

    - `Message.segment(self, segment_id)`: Returns the first segment with the given ID (e.g., `'PID'`). Raises `KeyError` if none exist.

    - `Message.segments(self, segment_id)`: Returns a `Sequence` of all segments matching `segment_id`. Raises `KeyError` if none exist.

    - `Message.extract_field(self, segment, segment_num=1, field_num=1, repeat_num=1, component_num=1, subcomponent_num=1)`: Extracts a field value using hierarchical HL7 addressing (e.g., `PID.3.1.2`). Applies HL7 compatibility rules for incomplete or over-specified paths.

    - `Message.assign_field(self, value, segment, segment_num=1, field_num=None, repeat_num=None, component_num=None, subcomponent_num=None)`: Assigns a value to a field using hierarchical addressing. The target segment must already exist.

    - `Message.escape(self, field, app_map=None)`: Escapes special characters in a field according to HL7 rules (e.g., separators, non-ASCII characters). Uses message-level context (e.g., MSH-defined separators).

    - `Message.unescape(self, field, app_map=None)`: Unescapes HL7 escape sequences (e.g., `\F\`, `\X20\`) in a field, using application-defined mappings if provided.

    - `Message.create_ack(self, ack_code="AA", message_id=None, application=None, facility=None)`: Generates a standard HL7 ACK message in response to this message, per HL7 specification 2.9.2. Supports custom acknowledgment codes, message IDs, and application/facility names.

    - `Message.__str__(self)`: Returns the full HL7 message string, ending with a segment separator (`\r`), as required by the HL7 standard.

- `Segment`: Represents an HL7 segment (e.g., MSH, PID), containing a list of `Field` instances.

    - `Segment.__init__(self, separator=None, sequence=[], esc="\\", separators="\r|~^&", factory=None)`: Initializes using the field separator (`|`).

    - `Segment.extract_field(self, segment_num=1, field_num=1, repeat_num=1, component_num=1, subcomponent_num=1)`: Extracts a value from the segment using hierarchical field addressing. Handles optional fields and applies unescaping. Special handling for MSH.1 and MSH.2 (not unescaped).

    - `Segment.assign_field(self, value, field_num=None, repeat_num=None, component_num=None, subcomponent_num=None)`: Assigns a value into the segment’s field hierarchy, creating intermediate containers as needed.

    - `Segment._adjust_index(self, index)`: Overrides index adjustment to preserve 1-based access without offset (since segment name is at index 0, field 1 is at index 1).

    - `Segment.__str__(self)`: Returns the segment string. For MSH, FHS, and BHS segments, the first two fields are used to reconstruct the correct separator characters per HL7 spec.

- `Field`: Represents an HL7 field, containing strings or `Repetition` instances.

    - `Field.__init__(self, separator=None, sequence=[], esc="\\", separators="\r|~^&", factory=None)`: Initializes using the repetition separator (`~`).

- `Repetition`: Represents a repeating field value, containing strings or `Component` instances.

    - `Repetition.__init__(self, separator=None, sequence=[], esc="\\", separators="\r|~^&", factory=None)`: Initializes using the component separator (`^`).

- `Component`: Represents a composite HL7 component, containing subcomponent strings.

    - `Component.__init__(self, separator=None, sequence=[], esc="\\", separators="\r|~^&", factory=None)`: Initializes using the subcomponent separator (`&`).

- `Factory`: Factory class for creating container instances. Subclasses can override to use custom container types.

    - `Factory.create_file`: Class reference to `File`.

    - `Factory.create_batch`: Class reference to `Batch`.

    - `Factory.create_message`: Class reference to `Message`.

    - `Factory.create_segment`: Class reference to `Segment`.

    - `Factory.create_field`: Class reference to `Field`.

    - `Factory.create_repetition`: Class reference to `Repetition`.

    - `Factory.create_component`: Class reference to `Component`.

`datatypes.py`:

- `parse_datetime(value)`: Parse HL7 DTM string `value` into a `datetime.datetime` object.

    `value` is of the format YYYY[MM[DD[HH[MM[SS[.S[S[S[S]]]]]]]]][+/-HHMM] or a ValueError will be raised.

    :rtype: `datetime.datetime`

- `_UTCOffset`: A fixed-offset timezone class derived from `datetime.tzinfo`.

    - `_UTCOffset.__init__(self, minutes)`: Initialize a fixed-offset timezone.

        `minutes` is an offset from UTC, negative for west of UTC. The offset is stored as an integer to ensure compatibility with `datetime.timedelta` and proper formatting in `tzname`.

    - `_UTCOffset.__eq__(self, other)`: Compare two `_UTCOffset` instances for equality based on their minute offset.

    - `_UTCOffset.__hash__(self)`: Return a hash based on the minute offset, enabling use in sets and as dictionary keys.

    - `_UTCOffset.utcoffset(self, dt)`: Return the UTC offset as a `datetime.timedelta` based on the stored minutes.

    - `_UTCOffset.tzname(self, dt)`: Return the timezone name in the format `+HHMM` or `-HHMM`.

    - `_UTCOffset.dst(self, dt)`: Return a zero `datetime.timedelta`, indicating no daylight saving time adjustment.

`exceptions.py`:

- `HL7Exception`: Base exception class for all HL7-related errors.

- `MalformedSegmentException`: Raised when an HL7 segment is malformed or does not conform to expected structure.

- `MalformedBatchException`: Raised when an HL7 batch message (a collection of messages) is malformed.

- `MalformedFileException`: Raised when an HL7 file is malformed or cannot be parsed correctly.

- `ParseException`: Raised when a general parsing error occurs during HL7 message processing.

`__init__.py`:



`util.py`:

- `ishl7(line)`: Determines whether a `line` looks like an HL7 message.  
  This method only does a cursory check and does not fully validate the message.  
  :rtype: bool

- `isbatch(line)`: Determines if a `line` represents an HL7 batch message.  
  Batches are wrapped in BHS / BTS segments or contain more than one MSH segment (excluding file-wrapped messages starting with FHS).

- `isfile(line)`: Determines if a `line` represents an HL7 file.  
  Files are wrapped in FHS / FTS segments or may be a batch (as defined by `isbatch`).

- `split_file(hl7file)`: Splits a multi-message HL7 file into individual HL7 messages.  
  Does not validate messages. Discards file and batch control segments (FHS, FTS, BHS, BTS).  
  Returns a list of message strings, each ending with a carriage return (`\r`).

- `generate_message_control_id()`: Generate a unique 20-character HL7 message control ID.  
  Based on a UTC timestamp (16 characters, excluding the decade) and 4 random alphanumeric characters.  
  See: http://www.hl7resources.com/Public/index.html?a55433.htm

- `escape(container, field, app_map=None)`: Escapes special characters in an HL7 field according to HL7 escape sequence rules (Chapter 2, Section 2.10).  
  Replaces HL7 separators, escape character, carriage returns, and non-ASCII characters with HL7-encoded equivalents.  
  Supports application-defined escape mappings via `app_map`.  
  Returns an ASCII-encoded escaped string.

- `unescape(container, field, app_map=None)`: Unescapes HL7 escape sequences in a field according to HL7 rules (Chapter 2, Section 2.10).  
  Handles standard escape sequences (e.g., F, R, S, T, E, .br), hex-encoded bytes (Xnn), and application-defined mappings.  
  Partially supports rich text and repetition sequences (e.g., `.sp5`).  
  Logs warnings for unsupported features (e.g., inline character set switching with C/M).  
  Returns the unescaped string.

`parser.py`:

- `parse_hl7(line, encoding="utf-8", factory=Factory)`: Returns an instance of `hl7.Message`, `hl7.Batch`, or `hl7.File` that allows indexed access to the data elements, messages, or batches respectively.  
  A custom `hl7.Factory` subclass can be passed in to be used when constructing the message/batch/file and its components.  
  Accepts Unicode strings or byte strings (which are decoded using the specified `encoding`, defaulting to UTF-8).  
  :rtype: `hl7.Message` | `hl7.Batch` | `hl7.File`

- `parse(lines, encoding="utf-8", factory=Factory)`: Returns an instance of `hl7.Message` that allows indexed access to the data elements.  
  A custom `hl7.Factory` subclass can be passed in to be used when constructing the message and its components.  
  Accepts Unicode strings or byte strings (decoded using the specified `encoding`, defaulting to UTF-8).  
  :rtype: `hl7.Message`

- `_create_batch(batch, messages, encoding, factory)`: Creates and returns a `hl7.Batch` object from a BHS/BTS header/trailer (`batch`) and a list of raw message strings (`messages`).  
  Uses the provided `factory` and `encoding` to parse constituent messages and configure batch metadata.

- `parse_batch(lines, encoding="utf-8", factory=Factory)`: Returns an instance of `hl7.Batch` that allows indexed access to the contained messages.  
  A custom `hl7.Factory` subclass can be passed in for component construction.  
  Accepts Unicode or byte strings (decoded with `encoding`).  
  Parses BHS/BTS segments if present and groups MSH-starting segments into individual messages.  
  :rtype: `hl7.Batch`

- `_create_file(file, batches, encoding, factory)`: Creates and returns a `hl7.File` object from an optional FHS/FTS header/trailer (`file`) and a list of batch definitions (`batches`).  
  Each batch definition is a tuple of `[batch_header, message_list]`.  
  Uses the provided `factory` and `encoding` to construct nested objects and propagate separators/escape characters.

- `parse_file(lines, encoding="utf-8", factory=Factory)`: Returns an instance of `hl7.File` that allows indexed access to the contained batches.  
  A custom `hl7.Factory` subclass can be used for construction.  
  Accepts Unicode or byte strings (decoded with `encoding`).  
  Handles FHS/FTS file wrappers and nested BHS/BTS batches; messages outside batches are grouped into a default batch.  
  :rtype: `hl7.File`

- `_split(text, plan)`: Recursive function that splits the input `text` into a nested list structure according to the provided `_ParsePlan`.  
  Handles the special parsing logic for MSH, BHS, and FHS segments (which encode separator characters in their fields).  
  Returns a container object (e.g., Message, Segment, Field) as defined by the current level of the plan.

- `create_parse_plan(strmsg, factory=Factory)`: Creates a `_ParsePlan` object that defines how to parse an HL7 message based on its separator characters found in the first segment (MSH, BHS, or FHS).  
  Extracts field, component, repetition, escape, and sub-component separators, applying HL7 defaults when values are missing.

- `_ParsePlan`: Details on how to parse an HL7 message. Typically created via `create_parse_plan`.

    - `_ParsePlan.__init__(self, separator, separators, containers, esc, factory)`: Initialize a parse plan with the current separator, full separator string, list of container constructors, escape character, and factory.

    - `_ParsePlan.container(self, data)`: Return an instance of the appropriate container (e.g., Message, Segment) for the given `data`, using the current plan’s configuration.

    - `_ParsePlan.next(self)`: Generate the next level of the parsing plan by advancing to the next separator and container type. Returns `None` when no further parsing levels remain.

    - `_ParsePlan.applies(self, text)`: Return `True` if any of the current or child-level separators appear in `text`, indicating that further parsing is needed.

`mllp/__init__.py`:

`mllp/exceptions.py`:

- `InvalidBlockError`: An MLLP Block was received that violates MLLP protocol

`mllp/streams.py`:

- `open_hl7_connection(host=None, port=None, *, loop=None, limit=_DEFAULT_LIMIT, encoding=None, encoding_errors=None, **kwds)`:  
  A wrapper for `loop.create_connection()` returning a `(reader, writer)` pair.  
  The reader returned is a `hl7.mllp.HL7StreamReader` instance; the writer is a `hl7.mllp.HL7StreamWriter` instance.  
  The arguments are all the usual arguments to `create_connection()` except `protocol_factory`; most common are positional `host` and `port`, with various optional keyword arguments following.  
  Additional optional keyword arguments are `loop` (to set the event loop instance to use), `limit` (to set the buffer limit passed to the `HL7StreamReader`), `encoding` (to set the encoding on the `HL7StreamReader` and `HL7StreamWriter`) and `encoding_errors` (to set the encoding error handling mode).

- `start_hl7_server(client_connected_cb, host=None, port=None, *, loop=None, limit=_DEFAULT_LIMIT, encoding=None, encoding_errors=None, **kwds)`:  
  Start a socket server, call back for each client connected.  
  The first parameter, `client_connected_cb`, takes two parameters: `client_reader`, `client_writer`. `client_reader` is a `hl7.mllp.HL7StreamReader` object, while `client_writer` is a `hl7.mllp.HL7StreamWriter` object. This parameter can either be a plain callback function or a coroutine; if it is a coroutine, it will be automatically converted into a `Task`.  
  The rest of the arguments are all the usual arguments to `loop.create_server()` except `protocol_factory`; most common are positional `host` and `port`, with various optional keyword arguments following.  
  The return value is the same as `loop.create_server()`, i.e. a `Server` object which can be used to stop the service.

- `MLLPStreamReader`: A subclass of `asyncio.StreamReader` that reads MLLP-framed data blocks.

    - `MLLPStreamReader.__init__(self, limit=_DEFAULT_LIMIT, loop=None)`: Initialize the reader with the given buffer limit and event loop.

    - `MLLPStreamReader.readblock(self)`:  
      Read a chunk of data from the stream until the block termination separator (`b'\x1c\x0d'`) is found.  
      On success, the data and separator are removed from the internal buffer (consumed). Returned data excludes the separator at the end and the MLLP start block character (`b'\x0b'`) at the beginning.  
      The configured stream limit applies to the payload (excluding separators).  
      If EOF occurs before the full separator is found, an `IncompleteReadError` is raised.  
      If the limit is exceeded, a `ValueError` is raised.  
      If the block does not begin with the start block character (`<VT>`), an `InvalidBlockError` is raised.  
      Automatically resumes the stream if it was paused.

- `MLLPStreamWriter`: A subclass of `asyncio.StreamWriter` that writes MLLP-framed data blocks.

    - `MLLPStreamWriter.__init__(self, transport, protocol, reader, loop)`: Initialize the writer with transport, protocol, reader, and event loop.

    - `MLLPStreamWriter.writeblock(self, data)`:  
      Write a block of data to the stream, encapsulating it with `b'\x0b'` at the beginning and `b'\x1c\x0d'` at the end (standard MLLP framing).

- `HL7StreamProtocol`: A stream protocol that integrates HL7-specific reader and writer creation on connection.

    - `HL7StreamProtocol.__init__(self, stream_reader, client_connected_cb=None, loop=None, encoding=None, encoding_errors=None)`:  
      Initialize with a stream reader, optional client connection callback, event loop, and encoding settings.

    - `HL7StreamProtocol.connection_made(self, transport)`:  
      Called when a connection is established. Sets up the transport and creates an `HL7StreamWriter`.  
      If a `client_connected_cb` was provided, it is called with the reader and writer; if it returns a coroutine, it is scheduled as a task.

- `HL7StreamReader`: An `MLLPStreamReader` that decodes raw MLLP blocks into HL7 message objects.

    - `HL7StreamReader.__init__(self, limit=_DEFAULT_LIMIT, loop=None, encoding=None, encoding_errors=None)`:  
      Initialize with buffer limit, event loop, character encoding (default: `"ascii"`), and encoding error handling (default: `"strict"`).

    - `HL7StreamReader.encoding`: Property to get or set the character encoding used when decoding HL7 message bytes. Must be a string or `None`.

    - `HL7StreamReader.encoding_errors`: Property to get or set the error handling strategy for decoding (e.g., `"strict"`, `"ignore"`, `"replace"`). Must be a string or `None`.

    - `HL7StreamReader.readmessage(self)`:  
      Reads a full HL7 message from the stream by first reading an MLLP block via `readblock()`, then decoding and parsing it into an `hl7.Message` object using `hl7.parser.parse`.  
      Uses the configured `encoding` and `encoding_errors` for decoding.  
      May raise `InvalidBlockError` (for malformed MLLP framing) or `ValueError` (if block exceeds size limit).

- `HL7StreamWriter`: An `MLLPStreamWriter` that encodes and writes HL7 message objects as MLLP blocks.

    - `HL7StreamWriter.__init__(self, transport, protocol, reader, loop, encoding=None, encoding_errors=None)`:  
      Initialize with transport, protocol, reader, event loop, and encoding settings (defaults to ASCII with strict error handling).

    - `HL7StreamWriter.encoding`: Property to get or set the character encoding used when encoding HL7 messages to bytes. Defaults to `"ascii"`.

    - `HL7StreamWriter.encoding_errors`: Property to get or set the encoding error handling mode. Defaults to `"strict"`.

    - `HL7StreamWriter.writemessage(self, message)`:  
      Writes an `hl7.Message` object to the stream by converting it to a string, encoding it to bytes using the configured encoding and error handler, and sending it as an MLLP-framed block via `writeblock()`.