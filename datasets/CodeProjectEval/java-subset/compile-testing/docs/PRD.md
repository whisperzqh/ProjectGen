# Product Requirements Document: compile-testing

## Introduction and Goals

**Introduction**

compile-testing is a Java testing library that allows developers to compile Java source code within unit tests and make assertions about the compilation results.[2](#0-1)  The library provides a fluent API for configuring compilation tasks, including annotation processors, compiler options, and source files, and integrates with Google Truth for making rich assertions about diagnostics, generated files, and compilation success or failure.

**Goals**

The primary goal of the project is to enable easy testing of annotation processors without forking `javac` or creating separate integration test projects. The library aims to provide comprehensive assertion capabilities for compilation results, including verifying successful/failed compilations, checking diagnostics (errors, warnings, notes) with precise file and line location information, and validating generated source files by comparing their abstract syntax trees (AST).

## Features and Functionalities

### Compilation and Compilation Configuration

- Supports compiling Java source files programmatically using the system `javac` compiler or a custom `JavaCompiler` instance
- Allows configuration of annotation processors to be applied during compilation
- Supports passing custom compiler options to `javac`
- Allows specification of custom compilation classpath and annotation processor path
- Provides in-memory file management for compilation inputs and outputs without filesystem I/O

### Source File Creation and Manipulation

- Provides utilities for creating `JavaFileObject` instances from strings, lines of code, or classpath resources
- Supports reading Java source files from JAR resources and classpath resources
- Allows parsing Java source code into compilation unit trees without full compilation

### Compilation Result Assertions

- Provides fluent Truth-based assertions for compilation success/failure status
- Supports asserting the exact count of errors, warnings, and notes reported during compilation
- Allows searching for diagnostics containing specific message fragments or matching regex patterns
- Enables precise diagnostic location assertions (file, line number, column number)

### Generated File Verification

- Supports asserting that specific files were generated during compilation at expected locations
- Provides AST-based equivalence checking for generated source files
- Allows content-based assertions on generated files (byte-for-byte or string comparison)
- Supports partial AST matching to verify that expected patterns exist in generated code

### AST Analysis and Tree Differencing

- Provides detailed tree differencing that identifies syntactic differences between two compilation units
- Supports finding specific subtrees by kind and identifier within parsed syntax trees
- Offers breadcrumb-style descriptions of tree paths for debugging and error reporting
- Provides utilities for extracting top-level type names from compilation units

### JUnit Integration

- Provides a JUnit 4 Rule (`CompilationRule`) that makes `Elements` and `Types` instances available during test execution via an internal annotation processor

## Technical Constraints

- The repository uses Java as the primary programming language
- The target JDK version is Java 8 (source and target level 1.8)
- The repository uses Maven as the build system with a minimum Maven version requirement of 3.5.0
- Compilation outputs are stored entirely in memory, not written to disk
- The library requires access to the Java compiler API (`javax.tools` package) for programmatic compilation
- For Java 9+, the library requires specific `--add-exports` flags to access internal compiler packages
- Implied: The library depends on tools.jar (JDK 8) or jdk.compiler module (JDK 9+) for accessing compiler internals (based on Maven profiles for tools.jar/classes.jar)

## Requirements

### Dependencies

- `junit:junit:4.13.2` - JUnit 4 testing framework for test execution and the CompilationRule
- `com.google.truth:truth:1.4.5` - Google Truth assertion framework for fluent test assertions
- `com.google.guava:guava:33.5.0-jre` - Google Core Libraries for Java for immutable collections and utilities
- `com.google.errorprone:error_prone_annotations:2.45.0` (provided scope) - Error Prone annotations for static analysis
- `com.google.auto.value:auto-value-annotations:1.11.1` - AutoValue annotations for generating value classes
- `com.google.auto:auto-common:1.2.2` - AutoCommon utilities for annotation processing
- `org.jspecify:jspecify:1.0.0` - JSpecify nullness annotations

### Development Dependencies

- `com.google.auto.value:auto-value:1.11.1` - Annotation processor for generating AutoValue implementations (configured in annotation processor path)

## Usage

### Build and Test

Standard build commands (Maven-based project):

Build with Maven:
```bash
mvn clean package
```

Run tests with Maven:
```bash
mvn test
```

### Library Integration

This is a library project. Maven coordinates:

Maven:
```xml
<dependency>
  <groupId>com.google.testing.compile</groupId>
  <artifactId>compile-testing</artifactId>
  <version>HEAD-SNAPSHOT</version>
</dependency>
```

Gradle:
```gradle
dependencies {
  testImplementation 'com.google.testing.compile:compile-testing:HEAD-SNAPSHOT'
}
```

Minimal Java usage example (based on package documentation):

```java
import static com.google.testing.compile.CompilationSubject.assertThat;
import static com.google.testing.compile.Compiler.javac;
import com.google.testing.compile.Compilation;
import com.google.testing.compile.JavaFileObjects;

public class AnnotationProcessorTest {
  public void testProcessor() {
    Compilation compilation = javac()
        .withProcessors(new MyAnnotationProcessor())
        .compile(JavaFileObjects.forSourceString("HelloWorld", 
                 "final class HelloWorld {}"));
    assertThat(compilation).succeeded();
  }
}
```

## Command Line Configuration Arguments

This library does not provide a command-line interface. It is designed to be used programmatically within Java unit tests. Configuration is done through the fluent Java API provided by the `Compiler` class, which allows setting compiler options, annotation processors, classpaths, and other compilation parameters.

## Terms/Concepts Explanation

**Compiler**: An object that configures and executes Java compilation tasks programmatically, wrapping the system `javac` or a custom `JavaCompiler` instance with specified processors, options, and classpaths.

**Compilation**: An immutable value object representing the results of a compilation attempt, including the status (success/failure), all diagnostics reported, source files compiled, and generated output files.

**CompilationSubject**: A Google Truth `Subject` implementation that provides fluent assertion methods for verifying compilation results, such as checking success/failure, diagnostic counts and messages, and generated file properties.

**JavaFileObject**: The standard Java API representation of a source or class file, used throughout the library to represent compilation inputs and outputs; this library provides utilities to create them from strings, resources, or in-memory storage.

**Annotation Processor**: A Java compiler plugin (implementing `javax.annotation.processing.Processor`) that processes annotations at compile-time and can generate new source files or report diagnostics; testing these is the primary use case for this library.

**Diagnostic**: A compiler message (error, warning, mandatory warning, or note) reported during compilation, which includes the message text, severity kind, source file, and optional line/column position.

**AST (Abstract Syntax Tree)**: The tree representation of Java source code structure created by the parser; this library provides utilities for comparing ASTs to verify that generated code matches expected structure rather than exact text.

**InMemoryJavaFileManager**: A custom `JavaFileManager` implementation that stores all compilation outputs (class files, generated sources) in memory rather than writing to disk, enabling fast, isolated test execution.

**TreeDiffer**: A utility that performs deep structural comparison of two Java syntax trees (ASTs) and reports specific differences, used to verify that generated code matches expected patterns or golden files.

**CompilationRule**: A JUnit 4 `TestRule` that compiles a dummy source file with a special annotation processor, making `Elements` and `Types` utility instances available during test execution for advanced type system queries.

**Google Truth**: An assertion framework that this library integrates with, providing fluent "subject" APIs (like `CompilationSubject`, `JavaFileObjectSubject`) for making readable, chainable test assertions.
