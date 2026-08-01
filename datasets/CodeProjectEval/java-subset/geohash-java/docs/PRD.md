# Product Requirements Document: geohash-java

## Introduction and Goals

**Introduction**: geohash-java is a pure Java implementation of the Geohash spatial indexing system.  The library encodes geographic coordinates (latitude/longitude) into short alphanumeric strings and provides decoding capabilities.  The implementation supports both character-based precision (compatible with the geohash.org reference implementation) and full 64-bit precision encoding. 

**Goals**: The primary goal is to provide a robust geospatial hashing library that enables efficient spatial queries and proximity searches.  The library aims to support bounding box queries that can span the 180 meridian,  enable neighbor hash calculations for adjacency searches,  and provide geodetic calculations using Vincenty's formula for accurate distance computations.  The library is distributed via Maven Central for easy integration into Java projects. 

## Features and Functionalities

### Geohash Encoding and Decoding
- Supports encoding geographic coordinates to geohashes with character precision (1-12 characters, multiples of 5 bits) 
- Supports encoding with bit precision up to 64 bits for maximum accuracy 
- Provides decoding from base32-encoded geohash strings to geographic coordinates 
- Supports binary string encoding and decoding for geohashes 
- Allows conversion between long value representation and geohash objects 

### Spatial Queries and Bounding Boxes
- Provides bounding box queries to find geohashes covering a specific area 
- Supports circle queries for radius-based searches around a center point 
- Supports bounding boxes that cross the 180 meridian 
- Allows checking if a point or geohash falls within a query area 
- Provides bounding box expansion to include additional points or boxes 
- Supports intersection detection between bounding boxes 
- Enables iteration through all geohashes within a bounding box 
- Supports random sampling of geohashes within a bounding box without replacement 
- Provides WKT (Well-Known Text) output format for query areas 

### Neighbor and Adjacency Operations
- Calculates adjacent geohashes in all 8 directions (N, NE, E, SE, S, SW, W, NW) 
- Provides individual directional neighbor methods (northern, southern, eastern, western) 
- Supports sequential navigation through geohashes using next() and prev() methods 
- Allows calculation of steps between two geohashes with the same precision 

### Geodetic Calculations
- Implements Vincenty's formula for accurate geodetic calculations on the WGS84 ellipsoid 
- Supports moving a point in a specified direction by a given distance in meters 

### Data Validation and Serialization
- Validates latitude values within ±90 degrees and longitude values within ±180 degrees 
- Provides Serializable implementations for GeoHash, WGS84Point, and BoundingBox classes 
- Implements proper equals(), hashCode(), and compareTo() methods for geohash comparisons 

### Build and Dependency Management
- Supports building with Apache Maven using standard targets (clean, compile, test, package) 
- Provides Maven artifact deployment to Maven Central repository 
- Includes source and javadoc JAR generation for library distribution 

## Technical Constraints

- The repository uses Java as the primary programming language 
- The target JDK version is Java 1.7 (source and target compatibility) 
- The repository uses Apache Maven as the build system 
- The project packages as a JAR library artifact 
- The project requires UTF-8 source and reporting encoding 

## Requirements

### Dependencies

This project has no runtime dependencies - it is a pure Java implementation with no external library requirements beyond the Java standard library.

### Development Dependencies

- `junit:junit:4.13.1` - Unit testing framework (JUnit 4) 

## Usage

### Build and Test

Build with Maven:
```bash
mvn clean package
```

Run tests with Maven:
```bash
mvn test
```

Compile sources:
```bash
mvn compile
```

These commands are documented in the README. 

### Library Integration

This is a library project. Maven coordinates are available: 

Maven:
```xml
<dependency>
  <groupId>ch.hsr</groupId>
  <artifactId>geohash</artifactId>
  <version>1.5.0</version>
</dependency>
```

Gradle:
```gradle
dependencies {
  implementation 'ch.hsr:geohash:1.5.0'
}
```

Minimal Java example:
```java
import ch.hsr.geohash.GeoHash;
import ch.hsr.geohash.WGS84Point;

public class Demo {
  public static void main(String[] args) {
    // Encode a location
    GeoHash hash = GeoHash.withCharacterPrecision(47.5, 8.5, 5);
    System.out.println("Geohash: " + hash.toBase32());
    
    // Decode a geohash
    GeoHash decoded = GeoHash.fromGeohashString("u0qj5");
    WGS84Point point = decoded.getOriginatingPoint();
    System.out.println("Lat: " + point.getLatitude() + ", Lon: " + point.getLongitude());
  }
}
```

The library is distributed via Maven Central. 

## Command Line Configuration Arguments

This project does not provide a command-line interface. It is a library intended to be integrated into other Java applications. No main entry point or CLI argument parsing is present in the codebase.

## Terms/Concepts Explanation

**Geohash**: A hierarchical spatial indexing system that encodes geographic coordinates (latitude/longitude) into a short alphanumeric string; neighboring locations share common prefixes, making it useful for proximity searches and spatial queries. 

**WGS84Point**: A class representing a point on Earth's surface using the WGS84 coordinate system, encapsulating latitude and longitude values with validation to ensure they fall within valid ranges (±90° for latitude, ±180° for longitude). 

**BoundingBox**: A rectangular geographic area defined by north/south latitude bounds and east/west longitude bounds; this implementation supports bounding boxes that cross the 180° meridian. 

**Base32 Encoding**: The standard text representation of geohashes using 32 characters (0-9, b-z excluding a, i, l, o); each character represents 5 bits of the binary geohash, making it compatible with the geohash.org reference implementation. 

**Bit Precision**: The number of significant bits used in a geohash representation, ranging from 1 to 64 bits; higher precision provides smaller bounding boxes and more accurate location representation. 

**Character Precision**: The number of base32 characters used to represent a geohash (1-12 characters); each character adds 5 bits of precision, and the precision directly correlates to the spatial accuracy (e.g., 5 characters ≈ 2.4 km error). 

**Adjacent Hashes**: The 8 neighboring geohash cells surrounding a given geohash (N, NE, E, SE, S, SW, W, NW); used for proximity searches and expanding search areas around a point. 

**Vincenty's Formula**: A geodetic algorithm for calculating distances and bearings on an ellipsoid (WGS84) with high accuracy; used in this library to move points along the Earth's surface by a specified bearing and distance. 

**180 Meridian**: The line of longitude at ±180° where the International Date Line is located; bounding boxes in this library can span across this meridian for queries in the Pacific region. 

**Significant Bits**: The number of meaningful bits in a geohash's binary representation; determines the precision and size of the geohash's bounding box. 

**Circle Query**: A spatial query that finds all geohashes within a specified radius (in meters) from a center point; internally approximates the circle with a bounding box for efficient computation. 

**TwoGeoHashBoundingBox**: A bounding box defined by two corner geohashes (southwest and northeast) rather than explicit latitude/longitude coordinates; useful for geohash-based spatial queries. 

**WKT (Well-Known Text)**: A text markup language for representing vector geometry objects; this library can output bounding boxes in WKT format for integration with GIS systems. 
