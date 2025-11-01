## Introduction

This document outlines the product requirements for `python-hl7`, a Python library for parsing Health Level 7 (HL7) version 2.x messages into Python objects. The project aims to provide a simple yet powerful solution for healthcare data interchange by converting pipe-delimited HL7 v2.x messages into easy-to-navigate Python data structures.

## Goals

The primary goal of python-hl7 is to simplify HL7 v2.x message parsing for Python developers working in healthcare IT. It aims to eliminate the complexity of manually parsing pipe-delimited healthcare messages by providing an intuitive API that supports both Python list-style indexing and HL7's 1-based indexing conventions. The library also includes MLLP (Minimal Lower Layer Protocol) support for transmitting HL7 messages over TCP/IP networks.

## Features and Functionalities

- **HL7 v2.x Message Parsing**: Parse pipe-delimited HL7 messages into hierarchical Python objects with support for all message components (segments, fields, repetitions, components, sub-components).

- **Hierarchical Data Structure**: Messages are parsed into a tree of `Container` subclasses (`Message`, `Segment`, `Field`, `Repetition`, `Component`) that extend Python's `list` type.

- **Dual Indexing Support**: Access message components using either 0-based Python list indexing or 1-based HL7 convention indexing via callable syntax.

- **Batch and File Support**: Parse HL7 batch messages (BHS/BTS) and file structures (FHS/FTS) in addition to single messages.

- **Symbolic Accessors**: Navigate message components using symbolic accessor names (e.g., `message['PID.F3.R1.C2']`).

- **MLLP Client (Synchronous)**: Send HL7 messages over TCP/IP using the `MLLPClient` class and `mllp_send` command-line tool. 

- **MLLP Server (Asynchronous)**: Receive HL7 messages using asyncio-based MLLP implementation with `open_hl7_connection()` and `start_hl7_server()` functions.

- **Datetime Parsing**: Convert HL7 DTM fields to Python `datetime` objects via `parse_datetime()` function.

- **ACK Generation**: Create HL7 acknowledgment messages from existing messages using `Message.create_ack()`.

- **Character Escaping**: Handle HL7 escape sequences with `Message.escape()` and `Message.unescape()` methods. 

- **Unicode Support**: Full Unicode support with configurable encoding for byte string parsing.

- **No External Dependencies**: Written in pure Python using only the standard library (no PyPI dependencies required at runtime).

- **Cross-Platform Compatibility**: Works on Python 3.9+ across all operating systems.

- **Extensible Factory Pattern**: Customize container subclasses created during parsing using the `Factory` class.

## Core Architecture

python-hl7 follows a hierarchical container architecture with these main components:

- **Parser Module** (`hl7.parser`): Entry point functions `parse()`, `parse_batch()`, `parse_file()`, and `parse_hl7()` that detect message type and dispatch to appropriate parsers.

- **Container Classes** (`hl7.containers`): Hierarchical data structures extending Python's `list`:
  - `File`: FHS/FTS wrapper containing batches
  - `Batch`: BHS/BTS wrapper containing messages
  - `Message`: Collection of segments with methods like `segment()`, `segments()`, `extract_field()`
  - `Segment`: Collection of fields
  - `Field`: Collection of repetitions
  - `Repetition`: Collection of components
  - `Component`: Collection of sub-components (primitive strings)

- **Accessor System** (`hl7.accessor`): Symbolic path-based navigation using dot notation (e.g., `PID.F3.R1.C2`).

- **MLLP Client** (`hl7.client`): Synchronous TCP/IP client for sending messages with MLLP framing.

- **MLLP Asyncio** (`hl7.mllp`): Asynchronous I/O support with `HL7StreamReader` and `HL7StreamWriter` classes.

- **Utility Functions** (`hl7.util`): Helper functions like `ishl7()`, `isbatch()`, `isfile()`, `split_file()`, `generate_message_control_id()`.

- **Factory Pattern** (`hl7.Factory`): Allows customization of container classes created during parsing. 

## Usage

```python
>>> message = 'MSH|^~\&|GHH LAB|ELAB-3|GHH OE|BLDG4|200202150930||ORU^R01|CNTRL-3456|P|2.4\r'
>>> message += 'PID|||555-44-4444||EVERYWOMAN^EVE^E^^^^L|JONES|196203520|F|||153 FERNWOOD DR.^^STATESVILLE^OH^35292||(206)3345232|(206)752-121||||AC555444444||67-A4335^OH^20030520\r'
>>> message += 'OBR|1|845439^GHH OE|1045813^GHH LAB|1554-5^GLUCOSE|||200202150730||||||||555-55-5555^PRIMARY^PATRICIA P^^^^MD^^LEVEL SEVEN HEALTHCARE, INC.|||||||||F||||||444-44-4444^HIPPOCRATES^HOWARD H^^^^MD\r'
>>> message += 'OBX|1|SN|1554-5^GLUCOSE^POST 12H CFST:MCNC:PT:SER/PLAS:QN||^182|mg/dl|70_105|H|||F\r'
```

Call the `hl7.parse` function with the string message:

```python
>>> import hl7
>>> h = hl7.parse(message)
```

We can get a `hl7.Message` object, wrapping a series of `hl7.Segment` objects:

```python
>>> type(h)
<class 'hl7.containers.Message'>
```

We can always get the HL7 message back:

```python
>>> str(h) == message
True
```

Interestingly, `hl7.Message` can be accessed as a list:

```python
>>> isinstance(h, list)
True
```

There were 4 segments (MSH, PID, OBR, OBX):

```python
>>> len(h)
4
```

We can extract the `hl7.Segment` from the `hl7.Message` instance:

```python
>>> h[3]
[['OBX'], ['1'], ['SN'], [[['1554-5'], ['GLUCOSE'], ['POST 12H CFST:MCNC:PT:SER/PLAS:QN']]], [''], [[[''], ['182']]], ['mg/dl'], ['70_105'], ['H'], [''], [''], ['F']]
>>> h[3] is h(4)
True
```

Note that since the first element of the segment is the segment name, segments are effectively 1-based in Python as well (because the HL7 spec does not count the segment name as part of the segment itself):

```python
>>> h[3][0]
['OBX']
>>> h[3][1]
['1']
>>> h[3][2]
['SN']
>>> h(4)(2)
['SN']
```

We can easily reconstitute this segment as HL7, using the appropriate separators:

```python
>>> str(h[3])
'OBX|1|SN|1554-5^GLUCOSE^POST 12H CFST:MCNC:PT:SER/PLAS:QN||^182|mg/dl|70_105|H|||F'
```

We can extract individual elements of the message:

```python
>>> h[3][3][0][1][0]
'GLUCOSE'
>>> h[3][3][0][1][0] is h(4)(3)(1)(2)(1)
True
>>> h[3][5][0][1][0]
'182'
>>> h[3][5][0][1][0] is h(4)(5)(1)(2)(1)
True
```

We can look up segments by the segment identifier, either via `hl7.Message.segments` or via the traditional dictionary syntax:

```python
>>> h.segments('OBX')[0][3][0][1][0]
'GLUCOSE'
>>> h['OBX'][0][3][0][1][0]
'GLUCOSE'
>>> h['OBX'][0][3][0][1][0] is h['OBX'](1)(3)(1)(2)(1)
True
```

Since many types of segments only have a single instance in a message (e.g., PID or MSH), `hl7.Message.segment` provides a convenience wrapper around `hl7.Message.segments` that returns the first matching `hl7.Segment`:

```python
>>> h.segment('PID')[3][0]
'555-44-4444'
>>> h.segment('PID')[3][0] is h.segment('PID')(3)(1)
True
```

The result of parsing contains up to 5 levels. The last level is a non-container type.

```python
>>> type(h)
<class 'hl7.containers.Message'>

>>> type(h[3])
<class 'hl7.containers.Segment'>

>>> type(h[3][3])
<class 'hl7.containers.Field'>

>>> type(h[3][3][0])
<class 'hl7.containers.Repetition'>

>>> type(h[3][3][0][1])
<class 'hl7.containers.Component'>

>>> type(h[3][3][0][1][0])
<class 'str'>
```

The parser only generates the levels which are present in the message.

```python
>>> type(h[3][1])
<class 'hl7.containers.Field'>

>>> type(h[3][1][0])
<class 'str'>
```

## Requirements

### Dependencies
- Python 3.9 or higher
- No external runtime dependencies (pure Python standard library)

## Design and User Interface

As a backend library, python-hl7 does not have a GUI. The interface is through Python classes and functions following Pythonic design principles. The API is designed to be intuitive by supporting both Python's 0-based list indexing and HL7's 1-based indexing conventions, allowing developers to choose the style that best fits their needs. The library emphasizes simplicity and ease of use while maintaining full compatibility with the HL7 v2.x specification.