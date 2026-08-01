# Product Requirements Document: jetbrick-template-2x

## Introduction

jetbrick-template is a next-generation Java template engine designed for high performance and extensibility.  It serves as a replacement for JSP pages or other template engines like Velocity, suitable for dynamic HTML page generation or code generation.  The template syntax uses directives similar to Velocity while keeping expressions consistent with Java, making it easy to learn and use.  The project is organized as a multi-module Maven build with a core template engine and multiple web framework integration modules. 

## Goals

The primary goals of jetbrick-template are to provide high performance and high extensibility for template processing.  The engine aims to support both strong-typed and weak-typed variable declaration modes,  enable template hot-reloading for development efficiency,  and provide rich extensibility through custom methods, functions, tags, and macros.  The project also integrates with multiple popular Java web frameworks including Spring MVC, JFinal, Jodd, Struts, and Nutz,  demonstrating a goal of broad ecosystem compatibility.

## Features and Functionalities

### Build and Dependency Management
- Supports building the project using Maven with a multi-module structure 
- Supports running unit tests via `mvn test` with JUnit 4 
- Packages the core library and integration modules as JAR artifacts 
- Uses ANTLR4 Maven plugin to generate parser code from grammar definitions during build 

### Template Engine Core
- Provides template creation via `JetEngine.create()` factory methods with configurable initialization 
- Supports loading templates from classpath or file system through pluggable ResourceLoader implementations 
- Renders templates to output streams or writers with context variable binding 
- Enables template hot-reloading based on file modification timestamps when configured 
- Supports creating uncached templates from string source code via `createTemplate()` method (Implied: method exists in JetEngine interface)

### Template Syntax and Directives
- Supports Velocity-like directives including `#define`, `#for`, `#if/#elseif/#else`, `#set`, `#break`, `#continue`, `#stop`, and `#return` 
- Provides `#macro` directive for defining reusable template fragments 
- Supports custom `#tag` invocations for user-defined template components 
- Implements layout inheritance through built-in layout tags 
- Allows variable type declarations with `#define` directive 

### Type System and Expression Evaluation
- Supports both strict mode (requiring explicit type declarations) and weak mode (dynamic typing) 
- Provides Java-compatible expression syntax for variable access and method calls 
- Supports static method and field access in template expressions 
- Handles varargs method invocation and method overloading resolution 
- Provides safe-call operator support to prevent null pointer exceptions 

### Extension System
- Allows registration of extension methods via `@JetAnnotations.Methods` annotation 
- Supports extension functions registration via `@JetAnnotations.Functions` annotation 
- Enables custom tag registration through `@JetAnnotations.Tags` annotation 
- Provides automatic package scanning for extension discovery 
- Includes built-in extension methods, functions, and tags in runtime package 

### Configuration and Customization
- Supports configuration via properties files (default: `classpath:/jetbrick-template.properties`) 
- Allows programmatic configuration through Properties object 
- Provides configurable input/output encoding settings 
- Supports customizable template file suffix (default: `.jetx`) 
- Enables whitespace trimming configuration for directives and leading spaces 

### Security
- Implements security manager interface for controlling access to classes, methods, fields, and constructors 
- Supports configurable security manager implementation 
- Provides access control exception handling for restricted operations 

### Web Framework Integration
- Provides servlet-based web integration module with request/response context support 
- Includes Spring MVC integration with ViewResolver implementation 
- Supports Spring Boot auto-configuration for easy integration 
- Offers integration modules for JFinal, Jodd, Struts, and Nutz frameworks 

### Parsing and Code Generation
- Uses ANTLR4 for lexical analysis and syntax parsing 
- Generates Abstract Syntax Tree (AST) from template source (Implied: AstBuilder and AstCodeVisitor classes handle AST generation)
- Implements visitor pattern for AST traversal and code generation 

## Technical Constraints

- The project uses Java as the primary programming language 
- The project requires JDK 6.0+ for runtime compatibility (Implied: README badge indicates JDK v6.0+) 
- The project uses Maven as the build system 
- The project uses ANTLR4 version 4.10.1 for parser generation 
- The project requires Servlet API 3.0.1+ for web integration modules 
- The project inherits build configuration from parent POM `com.github.subchen:maven-parent:3.0.0` 
- The project uses SLF4J 1.7.7 for logging abstraction 
- The build requires `--add-opens java.base/java.lang=ALL-UNNAMED` JVM argument for testing 

## Requirements

### Core Dependencies

- `com.github.subchen:jetbrick-commons:2.1.9` - Common utility library for jetbrick projects 
- `org.antlr:antlr4-runtime:4.10.1` - ANTLR4 runtime for executing generated parsers 
- `org.slf4j:slf4j-api:1.7.7` - Logging facade for Java applications 

### Web Integration Dependencies

- `javax.servlet:javax.servlet-api:3.0.1` - Servlet API for web integration (provided scope) 
- `org.springframework:spring-webmvc:4.2.4.RELEASE` - Spring MVC framework for Spring integration 
- `org.springframework.boot:spring-boot-starter-web:1.3.1.RELEASE` - Spring Boot web starter (provided scope) 

### Build-time Dependencies

- `org.antlr:antlr4-maven-plugin:4.10.1` - Maven plugin for generating parser from ANTLR grammar 

### Development Dependencies

- `junit:junit:4.11` - Unit testing framework (JUnit 4) 
- `org.slf4j:slf4j-simple:1.7.7` - Simple SLF4J logging implementation for tests 

## Usage

### Build and Test

Build the entire project with Maven (Standard - Maven multi-module project):
```bash
mvn clean package
```

Run tests with Maven:
```bash
mvn test
```

Build only the core template module:
```bash
cd jetbrick-template
mvn clean package
```

### Library Integration

The project is published to Maven Central. 

Maven dependency for core template engine:
```xml
<dependency>
    <groupId>com.github.subchen</groupId>
    <artifactId>jetbrick-template</artifactId>
    <version>2.2.0</version>
</dependency>
``` 

Gradle dependency:
```gradle
dependencies {
    implementation "com.github.subchen:jetbrick-template:2.2.0"
}
```

### Basic Java Usage Example 

Create a template engine and render a template:
```java
import jetbrick.template.JetEngine;
import jetbrick.template.JetTemplate;
import java.util.Map;
import java.util.HashMap;
import java.io.StringWriter;

public class TemplateExample {
    public void render() {
        // Create a default JetEngine
        JetEngine engine = JetEngine.create();
        
        // Get a template from classpath
        JetTemplate template = engine.getTemplate("/users.jetx");
        
        // Create context
        Map<String, Object> context = new HashMap<>();
        context.put("users", usersList);
        
        // Render template
        StringWriter writer = new StringWriter();
        template.render(context, writer);
        
        System.out.println(writer.toString());
    }
}
```

## Command Line Configuration Arguments

This project is a library and does not provide a command-line interface. Configuration is performed programmatically via the `JetEngine.create()` methods or through a properties file. 

Runtime configuration can be provided via:
- Default properties file at `classpath:/jetbrick-template.properties` 
- Custom properties file path passed to `JetEngine.create(String configLocation)` 
- Properties object passed to `JetEngine.create(Properties config)` 

## Terms/Concepts Explanation

**JetEngine**: The main entry point for the template engine, responsible for loading configuration, managing resource loaders, and creating template instances.  Created via factory methods like `JetEngine.create()`.

**JetTemplate**: Represents a compiled template that can be rendered with a context map to produce output.  Obtained from JetEngine via `getTemplate()` or `createTemplate()` methods.

**ResourceLoader**: Interface for loading template source files from various locations (classpath, file system, etc.).  Controls template hot-reloading behavior through the `isReloadable()` method.

**Extension Methods/Functions**: Static methods marked with `@JetAnnotations.Methods` or `@JetAnnotations.Functions` that can be called from templates.  Methods are invoked on objects, while functions are standalone.

**Custom Tags**: User-defined template components marked with `@JetAnnotations.Tags` and invoked via `#tag` directive.  Enable reusable template logic with custom syntax.

**Macro**: A reusable template fragment defined with `#macro` directive that can accept parameters and be called from other templates.  Similar to functions but defined in template syntax rather than Java.

**Strict Mode**: A type-checking mode that requires all template variables to be explicitly declared with types before use.  Enabled via `jetx.syntax.strict=true` configuration.

**ANTLR4**: A parser generator used to parse template syntax.  The engine uses ANTLR grammar files (`JetTemplateLexer.g4`, `JetTemplateParser.g4`) to generate lexer and parser classes.

**AST (Abstract Syntax Tree)**: Internal representation of parsed template structure used for rendering. Generated by AstBuilder from ANTLR parse trees and traversed during template execution (Implied: AstBuilder, AstCodeVisitor, and AstNode classes exist in parser package).

**Security Manager**: Interface for controlling template access to Java classes, methods, fields, and constructors.  Throws `AccessControlException` when access is denied.

**Safe-call Operator**: A feature that prevents null pointer exceptions during template evaluation when accessing properties or methods on potentially null objects.  Configured via `jetx.syntax.safecall` property.

**Layout**: A template inheritance mechanism implemented through built-in layout tags that allows child templates to override blocks defined in parent layouts.
