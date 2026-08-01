# Project Requirements Document: Password4j

## Introduction and Goals

Password4j is a Java cryptographic library designed for encrypting and verifying passwords using various Key Derivation Functions (KDFs) and Cryptographic Hash Functions (CHFs).  The library emphasizes user-friendliness and supports industry-standard algorithms including Argon2, bcrypt, scrypt, balloon hashing, and PBKDF2, while also providing comprehensive salt and pepper management capabilities.  Password4j is compatible with Java 8 or higher and Android API 21+, making it portable across different platforms. 

The primary goal is to provide a portable, highly customizable cryptographic solution where algorithms can be configured either programmatically or through a property file in the classpath.  The library aims to optimize security by delivering a benchmarking tool (SystemChecker) that helps developers determine optimal parameters for their specific environment based on system performance and desired computational time constraints.  According to the project description, all implementations follow cryptographic standards and have been optimized specifically for JVM performance. 

## Features and Functionalities

### Password Hashing
- Supports hashing passwords with multiple KDF algorithms: PBKDF2 (since 1.0.0), bcrypt (since 1.0.0), scrypt (since 1.0.0), Argon2 (since 1.5.0), and Balloon Hashing (since 1.8.0) 
- Supports legacy cryptographic hash functions including MD Family, SHA1 Family, SHA2 Family, and SHA3 Family (since 1.4.0) 
- Provides builder pattern API through `HashBuilder` for fluent password hashing configuration 
- Allows hashing with both CharSequence and byte array inputs 

### Password Verification
- Provides hash verification functionality through `HashChecker` to validate plain text passwords against hashes 
- Supports verification with salt and pepper parameters 
- Allows verification using Hash objects that encapsulate the hashing function and parameters 

### Cryptographic Salt and Pepper Management
- Provides automatic salt generation through `SaltGenerator` with configurable length 
- Supports manual salt specification for custom salt values 
- Allows shared pepper configuration via properties file and programmatic pepper addition 
- Supports SecureRandom.getInstanceStrong() for cryptographically strong random generation when configured 

### Hash Migration and Updating
- Provides functionality to migrate from unsecure algorithms (MD5, SHA-256) to stronger algorithms 
- Supports hash updating when configurations become obsolete, allowing migration between different CHF algorithms 

### Configuration Management
- Allows configuration through `psw4j.properties` file placed in classpath with algorithm-specific parameters 
- Supports custom configuration path via system property `-Dpsw4j.configuration` 
- Reads configuration parameters including iterations, memory, parallelism, and algorithm variants through `PropertyReader` 

### Performance Benchmarking
- Provides `SystemChecker` class for environment-specific performance benchmarking 
- Supports finding optimal parameters for bcrypt based on maximum desired milliseconds 
- Supports finding optimal parameters for Argon2 with configurable memory, parallelism, output length, and type 
- Supports finding optimal parameters for PBKDF2 with algorithm variant and length specification 
- Supports finding optimal work factor and resources for scrypt 
- Performs warmup rounds before benchmarking to ensure JVM optimization 

### Build and Dependency Management
- Uses Maven as the build system with standard lifecycle phases 
- Includes JaCoCo plugin for code coverage reporting during test phase 
- Provides animal-sniffer-maven-plugin to verify Android API Level 21 compatibility 
- Includes release profile with GPG signing, source/javadoc generation, and Maven Central publishing configuration 

### Logging
- Uses SLF4J API as logging facade for framework-independent logging 
- Logs configuration warnings when properties are missing and default values are used 

### Algorithm Support Detection
- Provides methods to check if PBKDF2 variants are supported by the current JVM's security providers 
- Provides methods to check if message digest algorithms are supported by the current JVM 

## Technical Constraints

- The project must use Java as the primary programming language 
- The project must target Java 8 as both source and target compatibility level 
- The project must use Maven as the build system 
- The project must maintain compatibility with Android API Level 21 (Android 5.0) or higher, enforced by animal-sniffer-maven-plugin 
- The project must use UTF-8 encoding for source files and reports 
- Implied: The project requires JVM security providers to support specific cryptographic algorithms; PBKDF2 and SHA3 availability depends on the Security Services provided by the JVM 

## Requirements

### Dependencies

- `org.slf4j:slf4j-api:2.0.12` - Logging facade for Java applications 

### Development Dependencies

- `junit:junit:4.13.2` - Unit testing framework (JUnit 4) 
- `org.slf4j:slf4j-simple:2.0.12` - Simple SLF4J logging implementation for tests 

### Build Tool Requirements

- Maven 3.x or higher (implied from pom.xml version 4.0.0 modelVersion) 
- JDK 8 or higher for compilation 

## Usage

### Build and Test

Build with Maven (standard, not explicitly documented):
```bash
mvn clean package
```

Run tests with Maven (standard, not explicitly documented):
```bash
mvn test
```

### Library Integration

Password4j is a library designed to be integrated into applications. 

Maven:
```xml
<dependency>
    <groupId>com.password4j</groupId>
    <artifactId>password4j</artifactId>
    <version>1.8.3</version>
</dependency>
``` 

Minimal Java example for hashing:
```java
import com.password4j.Password;
import com.password4j.Hash;

public class Demo {
  public static void main(String[] args) {
    // Hash a password
    Hash hash = Password.hash("myPassword").withScrypt();
    
    // Verify a password
    boolean verified = Password.check("myPassword", hash.getResult()).withScrypt();
  }
}
``` 

### Configuration

Place a `psw4j.properties` file in your classpath to configure algorithm parameters, or specify a custom path:
```bash
java -Dpsw4j.configuration=/my/path/to/some.properties ...
``` 

### Performance Tuning

Use `SystemChecker` class programmatically to find optimal parameters for your environment:
```java
import com.password4j.SystemChecker;
import com.password4j.BenchmarkResult;
import com.password4j.BcryptFunction;

// Find optimal bcrypt rounds for max 500ms hashing time
BenchmarkResult<BcryptFunction> result = SystemChecker.benchmarkBcrypt(500);
``` 

## Command Line Configuration Arguments

Password4j does not provide a command-line interface. It is a library designed to be integrated into applications and used programmatically. 

However, the library supports the following system property for runtime configuration:

- `-Dpsw4j.configuration=<PATH>` - Specifies a custom path to the properties configuration file (default: `psw4j.properties` in classpath) 

## Terms/Concepts Explanation

**Key Derivation Function (KDF)**: A cryptographic algorithm that derives one or more secret keys from a secret value (password) using a pseudorandom function; Password4j supports Argon2, bcrypt, scrypt, PBKDF2, and balloon hashing. 

**Cryptographic Hash Function (CHF)**: A mathematical algorithm that maps data of arbitrary size to a fixed-size hash value with properties including determinism, collision resistance, and one-way computation; Password4j supports legacy CHFs like MD, SHA1, SHA2, and SHA3 families for migration purposes. 

**Salt**: A unique, randomly generated byte sequence added to each password during hashing to prevent rainbow table attacks; Password4j generates salts automatically via `SaltGenerator` or accepts custom salts. 

**Pepper**: A secret value shared between all stored passwords (unlike salt which is unique per password) that is concatenated with the password before hashing and not stored in the database; configured via `psw4j.properties` or programmatically. 

**Hash**: An immutable object containing the result of a cryptographic hashing operation along with metadata including the salt, pepper, and the `HashingFunction` used to generate it; used for password verification. 

**HashBuilder**: A builder pattern class that provides a fluent API for configuring password hashing operations including salt, pepper, and algorithm selection before executing the hash. 

**HashChecker**: A builder pattern class used to verify if a plain text password matches a given hash, supporting the same configuration options as `HashBuilder` for salt and pepper. 

**SystemChecker**: A benchmarking utility that determines optimal algorithm parameters for the target environment by measuring hash computation time and finding the best configuration within a specified maximum duration. 

**PropertyReader**: An internal class that loads and parses the `psw4j.properties` configuration file from classpath or custom path, providing default values when properties are not specified. 

**Argon2**: A memory-hard KDF that won the Password Hashing Competition in 2015; Password4j supports variants Argon2i, Argon2d, and Argon2id with configurable memory, iterations, parallelism, and output length. 

**bcrypt**: A KDF based on the Blowfish cipher that uses a logarithmic cost parameter (rounds) to control computational difficulty; Password4j supports bcrypt with configurable rounds and minor version. 

**scrypt**: A memory-hard KDF designed to make large-scale hardware attacks costly by requiring significant amounts of memory; Password4j supports scrypt with configurable work factor (N), resources (r), and parallelization (p) parameters. 
