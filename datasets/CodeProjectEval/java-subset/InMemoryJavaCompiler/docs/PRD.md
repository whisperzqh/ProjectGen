# Product Requirements Document: InMemoryJavaCompiler

## Introduction

InMemoryJavaCompiler is a utility library that provides sample classes for compiling Java source code in memory.   The project was created after the author took huge effort to look for working examples on the internet and found nothing that worked, prompting them to create a very simple version.  

## Goals

The goal of this project is to provide a straightforward solution for in-memory Java compilation with minimal complexity. The library is designed to be easy to use - developers can compile Java classes dynamically by providing the fully qualified class name and source code as a string, without needing to write files to disk.   The project is distributed as a Maven artifact through Sonatype OSS Releases Repository for easy integration into other Java projects.  

## Features and Functionalities

The following features and functionalities are provided by the InMemoryJavaCompiler project:

### Core Compilation Capabilities
- Ability to compile Java source code from strings in memory without writing to disk  
- Ability to compile a single Java class from source code string  
- Ability to compile multiple Java classes together with interdependencies  
- Ability to add multiple source files incrementally before compilation  
- Ability to compile classes with inner classes  

### Compiler Configuration
- Ability to specify custom compiler options (e.g., '-Xlint:unchecked')  
- Ability to ignore non-critical compiler warnings  
- Ability to use a custom parent ClassLoader for compilation  
- Ability to retrieve the internal ClassLoader used by the compiler  

### Error Handling and Diagnostics
- Ability to collect and report detailed compilation errors with line numbers and messages  
- Ability to distinguish between errors, warnings, and notes during compilation  
- Ability to throw CompilationException with detailed diagnostic information on failure  

### Runtime Class Loading
- Ability to dynamically load compiled bytecode from memory without filesystem access  
- Ability to return compiled Class objects ready for instantiation and invocation  
- Ability to store and manage compiled bytecode in memory  

### Memory Management
- Ability to maintain source code as in-memory string representations  
- Ability to store compiled bytecode in ByteArrayOutputStream for efficient memory usage  
- Ability to manage multiple compilation units simultaneously  

### Integration Features
- Ability to use standard Java Compiler API under the hood  
- Ability to integrate with Maven/Gradle projects as a dependency  
- Ability to work with fully qualified class names and package structures  

## Technical Constraints

- The repository must use **Java as the primary programming language**  

- The repository must target **Java 8 (1.8) as the minimum version** for both source and compiled bytecode  

- The repository must use **Maven as the build and dependency management tool**  

- The repository must use **UTF-8 character encoding** for source files  

- The repository must be packaged as a **JAR library artifact**  

- The repository must require **JDK (not JRE) at runtime** to access the Java Compiler API  

- The repository must use **javax.tools.JavaCompiler API** for in-memory compilation via ToolProvider  

- The repository must use **SLF4J API** for logging functionality  

- The repository must use **JUnit 4** for unit testing  

- The repository must use **ForwardingJavaFileManager** from javax.tools to manage compiled code in memory  

## Requirements

### System Requirements

- **Java 1.8** (Java SE 8) - Minimum Java version required for compilation and runtime  
- **Maven** - Build and dependency management tool

### Dependencies

- `slf4j-api:1.7.5` - SLF4J API for logging abstraction  

### Test Dependencies

- `slf4j-jdk14:1.7.5` - SLF4J JDK14 binding for test logging  
- `junit:4.12` - Unit testing framework  

### Build Plugins

- `maven-compiler-plugin:3.2` - Maven compiler plugin  
- `cobertura-maven-plugin:2.7` - Code coverage analysis tool  
- `nexus-staging-maven-plugin:1.6.3` - Maven plugin for deploying to Nexus/OSS Sonatype  
- `maven-release-plugin:2.5.1` - Maven release management plugin  

### Release Profile Plugins

The following plugins are only active during the release profile:

- `maven-source-plugin:2.2.1` - Generates source JAR files  
- `maven-javadoc-plugin:2.9.1` - Generates Javadoc JAR files  
- `maven-gpg-plugin:1.5` - Signs artifacts with GPG for Maven Central deployment  

---

## Usage

### Maven Dependency

Add this dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>org.mdkt.compiler</groupId>
    <artifactId>InMemoryJavaCompiler</artifactId>
    <version>1.3.0</version>
</dependency>
```  

### Basic Usage

**Note:** Make sure you use JDK (not JRE) in your runtime environment.  

Compile a single Java class from source code:

```java
StringBuilder sourceCode = new StringBuilder();
sourceCode.append("package org.mdkt;\n");
sourceCode.append("public class HelloClass {\n");
sourceCode.append("   public String hello() { return \"hello\"; }");
sourceCode.append("}");

Class<?> helloClass = InMemoryJavaCompiler.newInstance()
    .compile("org.mdkt.HelloClass", sourceCode.toString());
```  

### Advanced Usage Examples

**Compile multiple classes at once:**

```java
String cls1 = "public class A{ public B b() { return new B(); }}";
String cls2 = "public class B{ public String toString() { return \"B!\"; }}";

Map<String, Class<?>> compiled = InMemoryJavaCompiler.newInstance()
    .addSource("A", cls1)
    .addSource("B", cls2)
    .compileAll();

Class<?> aClass = compiled.get("A");
Class<?> bClass = compiled.get("B");
```  

**Ignore compilation warnings:**

```java
Class<?> helloClass = InMemoryJavaCompiler.newInstance()
    .ignoreWarnings()
    .compile("org.mdkt.HelloClass", sourceCode.toString());
```  

**Use custom compiler options:**

```java
InMemoryJavaCompiler.newInstance()
    .useOptions("-Xlint:unchecked")
    .compile("org.mdkt.HelloClass", sourceCode.toString());
```  

**Use custom parent ClassLoader:**

```java
ClassLoader parentClassLoader = // your custom class loader
InMemoryJavaCompiler.newInstance()
    .useParentClassLoader(parentClassLoader)
    .compile("org.mdkt.HelloClass", sourceCode.toString());
```  

**Compile classes with inner classes:**

```java
StringBuffer sourceCode = new StringBuffer();
sourceCode.append("package org.mdkt;\n");
sourceCode.append("public class HelloClass {\n");
sourceCode.append("   private static class InnerHelloWorld { int inner; }\n");
sourceCode.append("   public String hello() { return \"hello\"; }");
sourceCode.append("}");

Class<?> helloClass = InMemoryJavaCompiler.newInstance()
    .compile("org.mdkt.HelloClass", sourceCode.toString());
```  

## Terms/Concepts Explanation

**In-Memory Compilation**: The process of compiling Java source code directly in memory without writing intermediate files to disk, allowing dynamic compilation and loading of classes at runtime.  

**JavaCompiler (javax.tools.JavaCompiler)**: The JDK's standard compiler API provided by `ToolProvider.getSystemJavaCompiler()` that enables programmatic access to the Java compiler. Note: Requires a JDK (not just JRE) at runtime.   

**SourceCode**: A custom implementation of `SimpleJavaFileObject` that represents Java source code as a string in memory, providing the compiler with access to source content without requiring physical `.java` files.  

**CompiledCode**: A custom implementation of `SimpleJavaFileObject` that captures compiled bytecode into a `ByteArrayOutputStream`, storing the resulting `.class` file content in memory rather than on disk.  

**DynamicClassLoader**: A custom `ClassLoader` that extends the standard Java ClassLoader to load classes directly from in-memory bytecode stored in `CompiledCode` objects, bypassing the need for `.class` files on the filesystem.  

**ExtendedStandardJavaFileManager**: A custom file manager that extends `ForwardingJavaFileManager` to intercept output operations and redirect compiled class files into memory (`CompiledCode` objects) instead of writing them to disk.  

**DiagnosticCollector**: A standard Java compiler component that collects compilation diagnostics (errors, warnings, notes) during the compilation process, allowing the library to report detailed compilation issues to users.  

**Bytecode**: The binary representation of compiled Java classes (`.class` file content) stored as byte arrays in memory, which can be loaded by the `DynamicClassLoader` to create executable `Class<?>` objects.  

**CompilationException**: A custom runtime exception thrown when source code compilation fails due to errors or warnings (unless warnings are ignored), providing detailed diagnostic information about compilation problems.  

**Compiler Options**: Command-line style options (e.g., `-Xlint:unchecked`) that can be passed to the Java compiler to control compilation behavior such as warning levels and language features.  

**Fluent API Pattern**: The design pattern used throughout the library where methods return `this` (the `InMemoryJavaCompiler` instance), enabling method chaining for configuration and compilation operations.  

