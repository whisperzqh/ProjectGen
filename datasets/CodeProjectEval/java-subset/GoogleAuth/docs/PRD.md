# Product Requirements Document: GoogleAuth

## Introduction

GoogleAuth is a Java server library that implements the Time-based One-time Password (TOTP) algorithm specified in RFC 6238.  The implementation borrows from Google Authenticator and provides server-side code for creating TOTP shared secrets, generating TOTP passwords, and verifying TOTP passwords.  The library is designed for developers who want to add TOTP multi-factor authentication to Java applications, supporting both hardware token devices and software-based authenticator applications like Google Authenticator. 

## Goals

The primary goal of this project is to provide a comprehensive server-side implementation of the TOTP standard for Java applications, enabling multi-factor authentication with minimal integration effort.  The library aims to be compatible with standard TOTP client applications, particularly Google Authenticator, while offering flexibility through configurable parameters such as code length, time window size, hash functions, and secret key representations.  Additionally, the project provides convenience features including QR code generation for easy credential provisioning and extensible credential storage through a repository interface pattern. 

## Features and Functionalities

### Build and Dependency Management
- Supports Maven as the build system with Maven wrapper scripts included 
- Provides reproducible builds with enforced Maven version (3.0.5 minimum) 
- Packages as a JAR library artifact for distribution 
- Supports release profile with GPG signing, source/javadoc attachment, and Nexus staging 

### TOTP Credential Generation
- Generates new secret keys with configurable bit length (default 160 bits, minimum 128 bits) 
- Creates verification codes at time zero for initial setup validation 
- Generates scratch codes (default 5) as emergency backup codes 
- Supports Base32 and Base64 encoding for secret key representation 

### TOTP Password Verification
- Validates TOTP passwords against secret keys using RFC 6238 algorithm 
- Supports configurable time window tolerance (default 3 windows) to handle clock skew 
- Provides time-specific validation for testing or replaying past codes 
- Validates codes with configurable digit length (6-8 digits) 

### TOTP Password Generation
- Generates current TOTP passwords for testing or client simulation 
- Supports time-specific password generation for any given timestamp 
- Allows password generation by username when credential repository is configured 

### QR Code and URI Generation
- Generates QR code URLs for easy provisioning into authenticator apps 
- Creates otpauth TOTP URIs with issuer and account name formatting 
- Encodes algorithm, digits, and period parameters in otpauth URI 

### Credential Repository Integration
- Provides ICredentialRepository interface for pluggable storage implementations 
- Supports Java ServiceLoader API for automatic repository discovery 
- Allows direct credential repository injection via setter method 
- Enables username-based credential operations when repository is configured 

### Cryptographic Configuration
- Supports multiple HMAC hash functions: HmacSHA1 (default), HmacSHA256, HmacSHA512 
- Allows custom SecureRandom algorithm and provider via system properties or constructor parameters 
- Uses ReseedingSecureRandom for enhanced security (Implied: based on class usage in constructors) 
- Provides builder pattern for comprehensive configuration customization 

### Documentation and Testing
- Includes full JavaDoc documentation for all public APIs 
- Provides JUnit test suite as example code 
- Offers PDF manual generated from Texinfo sources 

## Technical Constraints

- The project uses Java as the primary programming language 
- The minimum Java version required to build and use the library is Java 7 
- The project targets Java 8 for compilation (source and target compatibility) 
- Maven is required as the build system (minimum version 3.0.5) 
- The project uses Maven wrapper scripts (`mvnw`, `mvnw.cmd`) for consistent builds  (Implied: wrapper files present in repository root)
- UTF-8 source encoding is enforced 

## Requirements

### Dependencies

- `commons-codec:commons-codec` version 1.17.1 - Base32 and Base64 encoding/decoding for secret keys 
- `org.apache.httpcomponents:httpclient` version 4.5.14 - HTTP client for URI building in QR code generation 

### Development Dependencies

- `junit:junit` version 4.13.2 - Unit testing framework (JUnit 4) 

## Usage

### Build and Test

Build with Maven (standard commands):
```bash
./mvnw clean package
```

Run tests with Maven:
```bash
./mvnw test
```

### Library Integration

Maven:
```xml
<dependency>
  <groupId>com.warrenstrange</groupId>
  <artifactId>googleauth</artifactId>
  <version>1.4.0</version>
</dependency>
```

Gradle:
```gradle
compile 'com.warrenstrange:googleauth:1.4.0'
``` 

### Basic Usage Examples

Creating credentials for a new user:
```java
GoogleAuthenticator gAuth = new GoogleAuthenticator();
final GoogleAuthenticatorKey key = gAuth.createCredentials();
``` 

The secret key can be retrieved with:
```java
key.getKey()
``` 

Verifying a TOTP password:
```java
GoogleAuthenticator gAuth = new GoogleAuthenticator();
boolean isCodeValid = gAuth.authorize(secretKey, password);
``` 

Generating a TOTP password for testing:
```java
GoogleAuthenticator gAuth = new GoogleAuthenticator();
int code = gAuth.getTotpPassword(secretKey);
``` 

Creating credentials with credential repository:
```java
GoogleAuthenticator gAuth = new GoogleAuthenticator();
final GoogleAuthenticatorKey key = gAuth.createCredentials("Bob");
``` 

Authorizing a user with credential repository:
```java
GoogleAuthenticator gAuth = new GoogleAuthenticator();
boolean isCodeValid = gAuth.authorizeUser("Bob", code);
``` 

## Command Line Configuration Arguments

This project is a library and does not provide a command-line interface. However, it supports runtime configuration through Java system properties for the random number generator:

- `com.warrenstrange.googleauth.rng.algorithm` - Specifies the SecureRandom algorithm to use 
- `com.warrenstrange.googleauth.rng.algorithmProvider` - Specifies the SecureRandom provider to use 

These properties are read during GoogleAuthenticator instantiation when no explicit algorithm is provided. 

## Terms/Concepts Explanation

**TOTP (Time-based One-time Password)**: An algorithm specified in RFC 6238 that generates a one-time password based on the current time and a shared secret key; this library implements TOTP for server-side validation compatible with Google Authenticator. 

**Secret Key**: A cryptographically random Base32 or Base64-encoded value shared between the server and the authenticator device; the library generates 160-bit secrets by default that must be securely stored and provisioned to the user's device. 

**Verification Code**: A 6-8 digit integer generated by the TOTP algorithm that changes every 30 seconds (default); used to verify user identity during authentication. 

**Scratch Codes**: Emergency backup codes (typically 5) generated alongside the secret key; these are one-time use codes that allow users to authenticate if they lose access to their token device. 

**Window Size**: The number of time steps checked during validation to account for clock skew between server and client; the default value of 3 means the library checks the current time window plus/minus one window. 

**Time Step**: The duration in milliseconds for which a TOTP code remains valid; the default is 30,000 milliseconds (30 seconds) as specified by RFC 6238. 

**HMAC (Hash-based Message Authentication Code)**: A cryptographic hash function used in the TOTP algorithm; this library supports HmacSHA1 (default), HmacSHA256, and HmacSHA512. 

**Base32/Base64**: Encoding schemes for representing the binary secret key as text; Base32 is the default and preferred format for Google Authenticator compatibility. 

**QR Code**: A two-dimensional barcode that encodes the otpauth URI containing the secret key and configuration; users scan this with Google Authenticator to configure their device. 

**ICredentialRepository**: A service interface for storing and retrieving user credentials; implementations can be discovered via Java ServiceLoader or injected directly to enable username-based API methods. 

**RFC 6238**: The Internet Engineering Task Force specification that defines the TOTP algorithm; this library implements this standard to ensure compatibility with standard authenticator applications. 
