# Product Requirements Document: JSON-java

## Introduction and Goals

**Introduction**

JSON-java (package `org.json`) is a reference implementation that demonstrates how to parse JSON documents into Java objects and how to generate new JSON documents from Java classes. The library implements JSON encoders and decoders in Java and can convert between JSON and other data formats including XML, HTTP headers, Cookies, and CDL (comma-delimited lists). This is a lightweight, language-independent data interchange format implementation published as a Maven artifact (`org.json:json`) and distributed under the Public Domain license.

**Goals**

The project has explicitly stated goals including: reliable and consistent results, adherence to the JSON specification, ease of building/using/including in other projects, no external dependencies, fast execution and low memory footprint, maintaining backward compatibility, and designed and tested to use on Java versions 1.6 through 25. The library aims to provide a reference implementation for the Java community while the ecosystem standardizes on a JSON solution.

## Features and Functionalities

### Build and Dependency Management
- Supports building the project using both Maven and Gradle with no external runtime dependencies
- Provides standard test execution via `mvn clean test` or `gradlew clean build test`
- Packages the library as an OSGi-compatible bundle artifact (via `maven-bundle-plugin`)[10](#0-9) 
- Supports Java module system (JPMS) with automatic module-info injection for Java 9+
- Provides optional strict mode testing via Maven profile (`test-strict-mode`) or Gradle task (`testWithStrictMode`)
- Generates source and JavaDoc JARs for distribution
- Includes JaCoCo test coverage reporting

### JSON Parsing and Generation
- Parses JSON text from `String`, `Reader`, or `InputStream` into `JSONObject` or `JSONArray`[16](#0-15) 
- Supports lenient parsing by default: accepts unquoted keys, unquoted values, unescaped literals, and extra commas
- Provides strict mode parsing option that enforces adherence to JSON specification
- Serializes JSON objects to compliant JSON text strings via `toString()` methods
- Supports `JSONTokener` for breaking text into individual tokens from `String`, `Reader`, or `InputStream`

### Data Manipulation and Access
- Provides `get()` methods that return values or throw exceptions if not found
- Provides `opt()` methods that return default values instead of throwing exceptions
- Supports typed `get` and `opt` methods with automatic type checking and coercion
- Allows adding or replacing values via `put()` methods
- Supports conversion between `JSONObject` and `JSONArray` using key arrays

### Parser Configuration
- Allows configuring maximum nesting depth (default 512) to prevent stack overflow
- Supports configurable behavior for duplicate keys (throw exception or overwrite)
- Provides configuration for handling Java null values during map conversion (convert to JSONObject.NULL or ignore)
- Supports strict mode to enforce valid JSON syntax and disallow garbage characters

### Format Conversion
- Converts between JSON and XML formats via `XML.toJSONObject()` and `XML.toString()`
- Converts between JSON and JSONML (JSON Markup Language)
- Converts between JSON and HTTP headers via `HTTP` class
- Converts between JSON and cookies/cookie lists via `Cookie` and `CookieList` classes
- Converts between JSON and comma-delimited lists (CDL) via `CDL` class
- Converts between JSON and Java Properties objects via `Property` class

### Java Bean Integration
- Supports Java Bean serialization to JSON using reflection on getter methods
- Provides `@JSONPropertyIgnore` annotation to exclude specific properties from serialization
- Provides `@JSONPropertyName` annotation to override property names in JSON output
- Supports `JSONString` interface for custom object serialization

### JSON Building Utilities
- Provides `JSONStringer` for convenient building of JSON strings
- Provides `JSONWriter` for building JSON text through a Writer
- Supports JSON Pointer (RFC 6901) for referencing specific values in JSON documents

### Type Support
- Fully supports `Integer`, `Long`, and `Double` Java types
- Provides partial support for `BigInteger` and `BigDecimal` via get(), opt(), and put() methods
- Handles numbers out of range for Double or Long by parsing them as strings
- Supports `JSONObject.NULL` to represent JSON null (distinct from Java null)

## Technical Constraints

- The repository uses Java as the primary programming language
- The repository targets Java 8 (source and target compatibility 1.8)[45](#0-44) 
- The repository supports Java versions 1.6 through 25 for testing and deployment
- The repository uses both Maven and Gradle as build systems
- The repository has no external runtime dependencies
- The repository uses UTF-8 source encoding[49](#0-48) 
- The repository generates OSGi-compatible bundle artifacts[10](#0-9) 
- The repository supports Java Platform Module System (JPMS) for Java 9+
- (Implied) The library adheres to ECMA-404 and RFC 8259 JSON specifications

## Requirements

### Runtime Dependencies

This library has no external runtime dependencies.

### Development Dependencies

- `junit:junit:4.13.2` - Unit testing framework (JUnit 4)
- `com.jayway.jsonpath:json-path:2.9.0` - JSON Path evaluation library for testing
- `org.mockito:mockito-core:4.2.0` - Mocking framework for unit tests

### Build Tool Dependencies

- `org.apache.felix:maven-bundle-plugin:5.1.9` - Creates OSGi-compatible bundle manifests
- `org.moditect:moditect-maven-plugin:1.0.0.Final` - Adds module-info for Java 9+ compatibility

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

Build with Gradle:
```bash
gradlew clean build test
```

Run tests with Gradle:
```bash
gradlew test
```

Optional strict mode testing with Gradle:
```bash
gradlew testWithStrictMode
```

Optional strict mode testing with Maven:
```bash
mvn test -P test-strict-mode
```

Build from command line (without build tools):
```bash
# Build class files
javac org/json/*.java

# Create JAR file
jar cf json-java.jar org/json/*.class
```

### Library Integration

Maven:
```xml
<dependency>
  <groupId>org.json</groupId>
  <artifactId>json</artifactId>
  <version>20251224</version>
</dependency>
```

Gradle:
```gradle
dependencies {
  implementation 'org.json:json:20251224'
}
```

Minimal Java example - Parse JSON string to JSONObject:
```java
import org.json.JSONObject;

public class Test {
    public static void main(String args[]){
       JSONObject jo = new JSONObject("{ \"abc\" : \"def\" }");
       System.out.println(jo);
    }
}
```

Compile and run with the library:
```bash
# Windows
javac -cp .;json-java.jar Test.java
java -cp .;json-java.jar Test

# Unix/Linux/macOS
javac -cp .:json-java.jar Test.java
java -cp .:json-java.jar Test
```

## Command Line Configuration Arguments

This project is a library and does not provide a command-line interface or accept command-line configuration arguments. It is designed to be integrated into other Java applications as a dependency for JSON parsing and generation functionality.

## Terms/Concepts Explanation

**JSONObject**: An unordered collection of name/value pairs representing a JSON object, providing methods for parsing JSON text, manipulating contents via get/opt/put methods, and serializing back to JSON-compliant strings.

**JSONArray**: A vector-like object representing a JSON array, capable of parsing JSON text and providing methods for manipulating its contents and producing JSON-compliant array serialization.

**JSONTokener**: A tokenizer that breaks JSON text into a sequence of individual tokens, constructable from String, Reader, or InputStream, and capable of parsing simple JSON values.

**JSONException**: The standard exception type thrown by this package when JSON parsing or manipulation errors occur.

**JSONObject.NULL**: A special singleton value representing JSON null (distinct from Java's null), which is equivalent to JavaScript's null value.

**JSON Pointer (RFC 6901)**: A standardized syntax for identifying a specific value within a JSON document, supported via the JSONPointer class in both string and URI fragment representations.

**Strict Mode**: A parser configuration option that enforces strict adherence to JSON syntax, disallowing garbage characters, unquoted strings, and single-quoted strings that are normally accepted in lenient mode.

**@JSONPropertyIgnore**: An annotation for Java Bean getter methods that forces specific properties to be excluded from the resulting JSONObject during serialization.

**@JSONPropertyName**: An annotation for Java Bean getter methods that overrides the default getter-to-key-name logic, allowing custom property names in the serialized JSON output.

**CDL (Comma-Delimited List)**: A conversion format supported by the library that allows transforming between JSON structures and comma-delimited text representations.

**OSGi Bundle**: A packaging format for modular Java applications; this library is packaged as an OSGi-compatible bundle with proper manifest entries for use in OSGi containers.[66](#0-65) 

**Reference Implementation**: This library serves as a reference implementation demonstrating how to implement JSON parsing and generation in Java, intended as an example until the Java community standardizes on a single JSON library.[6](#0-5) 
