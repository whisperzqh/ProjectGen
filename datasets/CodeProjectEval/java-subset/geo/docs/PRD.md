# Product Requirements Document: Geo

## Introduction

Geo is a Java utility library that provides geohashing capabilities for geographic coordinate encoding and manipulation。 The library enables efficient storage, indexing, and querying of geographic data through geohash encoding, which converts latitude and longitude coordinates into compact string representations.

Geohashing is particularly valuable for database systems that need to perform bounding box queries efficiently, especially in scenarios where databases have limitations on inequality conditions across multiple variables.

## Goals

The primary goals of this project are:

1. **Efficient Geographic Querying**: Enable fast bounding box searches in databases by converting multi-dimensional geographic queries into single-variable range queries using geohashes.

2. **High Performance**: Achieve approximately 3 million `encodeHash` operations per second on standard hardware.

3. **Thread Safety**: Provide a completely thread-safe API with no mutable types exposed.

4. **Database Compatibility**: Support databases with scalability constraints, such as Google App Engine Datastore, which limits inequality conditions to one variable per query.

5. **Comprehensive Test Coverage**: Maintain 100% unit test coverage to ensure reliability.

## Features and Functionalities

### Core Geohashing Operations

1. **Encoding**: Convert latitude and longitude coordinates to geohash strings of arbitrary length.

2. **Decoding**: Extract latitude and longitude from geohash strings.

3. **Adjacent Hash Calculation**: Find adjacent geohashes in any direction, with special handling for borders including poles.

4. **Neighbor Discovery**: Calculate all 8 adjacent hashes surrounding a given hash.

### Bounding Box Operations

1. **Hash Length Calculation**: Determine optimal hash length to enclose a bounding box.

2. **Coverage Calculation**: Generate a set of geohashes that cover a bounding box with a specified maximum number of hashes (default: 12).

3. **Dimensional Calculations**: Calculate height and width of geohashes in degrees.

### Base32 Encoding

The library provides encoding and decoding of long values from geohashes for efficient storage.

## Core Architecture

### Module Structure

**geo**: Core geohashing library with no external runtime dependencies

### Key Components

1. **GeoHash Class**: The central utility class providing static methods for all geohashing operations.

2. **LatLong Class**: Immutable representation of WGS84 coordinates.

3. **Base32 Class**: Handles conversion between geohash strings and long integer representations.

4. **Direction and Parity**: Support classes for adjacent hash calculations.

### Design Principles

- **Immutability**: All exposed types are immutable for thread safety.
- **Static Utility Pattern**: Core operations provided through static methods
- **Lookup Tables**: Pre-computed maps for neighbor and border calculations for performance optimization.

## Usage

### Maven Dependency

`pom.xml`:

```xml
<dependency>
    <groupId>com.github.davidmoten</groupId>
    <artifactId>geo</artifactId>
    <version>VERSION_HERE</version>
</dependency>
```

### Basic Operations

The library provides a simple API for encoding, decoding, and manipulating geohashes.

### Bounding Box Query Strategy

For optimal database querying with bounding boxes:

1. Store geohashes of various lengths as indexed fields alongside latitude/longitude positions.
2. Calculate a set of geohashes that cover the bounding box using `coverBoundingBox`. 
3. Perform queries using time range and geohash equality conditions.
4. Filter results to include only those within the actual bounding box.

### Hash Length Optimization

The optimal hash length depends on specific use cases and metrics like CPU usage, data transfer, and database load. The library allows explicit control through `coverBoundingBoxMaxHashes`.

## Requirements

### Runtime Requirements

- **Java Version**: Java 8 or higher
- **Encoding**: UTF-8

### Dependencies

The core `geo` module has **zero runtime dependencies**, making it lightweight and easy to integrate.

**Test Dependencies Only:**
- JUnit Jupiter 5.13.4
- Guava 33.5.0-jre
- H2 Database 2.2.224
- Commons IO 2.21.0
- JMH (Java Microbenchmark Harness) 1.37 for performance testing


### Build Tools

- Maven 3.x
- Compiler target: Java 8 or higher

### Licensing

The project is licensed under Apache License 2.0.

