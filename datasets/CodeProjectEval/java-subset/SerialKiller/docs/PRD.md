# Project Requirements Document: SerialKiller

## Introduction

SerialKiller is a look-ahead Java deserialization library designed to protect applications from untrusted input during object deserialization.  When Java serialization is used to exchange information between clients and servers, attackers can replace legitimate serialized streams with malicious data.  The library works by inspecting Java classes during naming resolution and allows a combination of blacklisting and whitelisting to secure applications. 

## Goals

The primary goal of SerialKiller is to provide an easy-to-use drop-in replacement for `java.io.ObjectInputStream` that can detect and block malicious deserialization payloads.  The library aims to protect applications by default against known attacks through pre-configured blacklist patterns,  while also allowing developers to define application-specific whitelists for maximum security.  Additionally, the library provides a profiling mode to help developers enumerate classes deserialized by their applications without blocking deserialization. 

## Features and Functionalities

### Deserialization Protection

- Provides a drop-in replacement for `java.io.ObjectInputStream` via the `SerialKiller` class 
- Supports blacklist-based filtering using Java regex patterns to block known malicious classes 
- Supports whitelist-based filtering using Java regex patterns to allow only trusted classes 
- Throws `InvalidClassException` when a class is blocked by blacklist or not matched by whitelist 
- Includes pre-configured blacklist patterns for known ysoserial gadgets and payloads 

### Configuration Management

- Supports XML-based configuration files for defining blacklist and whitelist patterns 
- Provides hot-reload capability with configurable refresh delay to update rules without application restart 
- Allows configuration of refresh delay in milliseconds via the `<refresh>` element 
- Supports regex-based pattern matching for both blacklist and whitelist rules 
- Maintains configuration cache per config file path using `ConcurrentHashMap` 

### Profiling and Logging

- Provides profiling mode to enumerate deserialized classes without blocking them 
- Logs blacklist matches in profiling mode using INFO level 
- Logs blocked classes in blocking mode using ERROR level 
- Integrates with Apache Commons Logging for log output 
- Supports Java logging configuration via `java.util.logging.config.file` system property 

### Build and Dependency Management

- Uses Maven as the build system with `pom.xml` configuration 
- Packages as a standard JAR library artifact 
- Produces a fat JAR with dependencies using Maven Assembly Plugin 
- Supports unit testing via JUnit 4 

## Technical Constraints

- The project must use Java 8 as the minimum runtime version 
- The project must use Java 8 as the source and target compilation version 
- The project must use Maven as the build system 
- The project requires UTF-8 source encoding 
- *Implied*: The project must have access to XML configuration files at runtime for blacklist/whitelist rules, as the SerialKiller constructor requires a config file path 

## Requirements

### Dependencies

- `commons-collections:commons-collections:3.2.2` - Apache Commons Collections library used by the project 
- `commons-configuration:commons-configuration:1.10` - XML configuration file parsing and hot-reload functionality 
- `commons-lang:commons-lang:2.6` - Apache Commons Lang utilities 
- `commons-logging:commons-logging:1.2` - Logging facade for the library 

### Development Dependencies

- `junit:junit:4.12` - Unit testing framework (JUnit 4) 

## Usage

### Build and Test

Build with Maven (Standard - not explicitly documented):
```bash
mvn clean package
```

Run tests with Maven (Standard - not explicitly documented):
```bash
mvn test
```

### Library Integration

Maven:
```xml
<dependency>
  <groupId>org.nibblesec</groupId>
  <artifactId>serialkiller</artifactId>
  <version>0.5</version>
</dependency>
``` 

Gradle:
```gradle
dependencies {
  implementation "org.nibblesec:serialkiller:0.5"
}
```

Minimal Java example:
```java
import org.nibblesec.tools.SerialKiller;
import java.io.ObjectInputStream;

public class Demo {
  public static void main(String[] args) throws Exception {
    // Replace ObjectInputStream with SerialKiller
    ObjectInputStream ois = new SerialKiller(inputStream, "/etc/serialkiller.conf");
    Object obj = ois.readObject();
  }
}
``` 

## Command Line Configuration Arguments

SerialKiller is a library, not a command-line application, and therefore does not provide CLI arguments. Configuration is performed through XML configuration files passed to the `SerialKiller` constructor. 

Logging can be configured via the standard Java logging system property: `-Djava.util.logging.config.file=<path>`. 

## Terms/Concepts Explanation

**Look-ahead Deserialization**: A security technique that inspects and validates Java classes during the deserialization naming resolution phase, before objects are fully instantiated.  SerialKiller overrides `resolveClass()` to implement this pattern. 

**Blacklist/Whitelist**: Security filtering approaches where blacklist defines known malicious class patterns to block, and whitelist defines trusted class patterns to allow.  SerialKiller enforces both sequentially during deserialization. 

**Profiling Mode**: A non-blocking mode that logs all deserialized classes without throwing exceptions, used to enumerate application class usage for whitelist development.  Controlled by the `<profiling>` configuration element. 

**ysoserial Gadgets**: Known Java deserialization exploit payloads from the ysoserial tool that abuse existing Java library classes (e.g., Commons Collections, Spring) to achieve remote code execution.  SerialKiller's default configuration includes patterns for these gadgets. 

**Hot-reload**: The ability to update SerialKiller's configuration file and have changes automatically detected and applied without restarting the application.  Implemented using Commons Configuration's `FileChangedReloadingStrategy`. 

**InvalidClassException**: The Java exception thrown by SerialKiller when a class is blocked by blacklist or not matched by whitelist during deserialization.  Applications should catch this exception to handle blocked deserializations gracefully. 

**ObjectInputStream**: The standard Java class for deserializing objects from a stream.  SerialKiller extends this class to intercept class resolution. 
