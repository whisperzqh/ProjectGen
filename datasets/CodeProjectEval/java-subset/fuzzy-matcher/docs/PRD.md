# Product Requirements Document: fuzzy-matcher

## Introduction

Fuzzy-matcher is a Java-based library designed to match and group "similar" elements within a collection of documents . The library can operate on any domain object and determine the probability that two or more objects are similar by analyzing data at the character level . It addresses use cases such as detecting duplicate contacts, preventing duplicate data entry, and categorizing records with similar names, addresses, or other attributes .

## Goals

The primary goal of the fuzzy-matcher library is to enable computers to recognize similarity in data the way humans do—by looking beyond exact string equality to identify records that are semantically similar despite minor variances in spelling, abbreviations, or formatting . The library supports three main use cases: de-duplication of existing data where it finds duplicates within a given list of documents; checking for duplicates when inserting a single new document against an existing list; and checking for duplicates when bulk inserting multiple new documents against an existing list .

## Features and Functionalities

### Build and Dependency Management
- Supports building the project using Maven with reproducible dependency management 
- Provides test execution via standard Maven tasks 
- Packages the library as a distributable JAR artifact for Maven Central 
- Includes JaCoCo code coverage enforcement with a minimum 90% instruction coverage requirement 

### Core Matching API
- Provides a `MatchService` entry point with multiple methods for applying fuzzy matching across different scenarios 
- Supports de-duplication by matching documents within a single list 
- Supports bulk duplicate detection by matching new documents against an existing list 
- Supports single document duplicate checking against an existing list 
- Allows result aggregation by Document object or by Document ID 
- Provides grouping of transitive matches where if A matches B and B matches C, all are grouped together 

### Element Types and Configuration
- Provides predefined element types including NAME, TEXT, ADDRESS, EMAIL, PHONE, NUMBER, DATE, and AGE 
- Supports configurable thresholds at both document level (default 0.5) and element level (default 0.3) 
- Allows element-level weight configuration to prioritize certain fields in document scoring 
- Supports element variance to differentiate multiple elements of the same type within a document 
- Allows override of preprocessing functions, tokenizer functions, and match types at the element level 

### Tokenization and Preprocessing
- Applies automatic preprocessing including trim and lowercase conversion for string values 
- Supports word tokenization for TEXT elements breaking values by spaces 
- Supports Soundex encoding tokenization for NAME and ADDRESS elements to handle phonetic similarity 
- Supports N-Gram tokenization (tri-gram for EMAIL, deca-gram for PHONE) for partial string matching 
- Supports value tokenization for numeric and date elements where the value itself is the token 
- Provides specialized preprocessing for different element types including special character removal, domain removal for emails, and numeric normalization 

### Match Types and Scoring
- Supports EQUALITY match type using exact token matching for most element types 
- Supports NEAREST_NEIGHBORS match type for NUMBER, DATE, and AGE elements to find values within a neighborhood range 
- Provides configurable neighborhood range (default 0.9) for NEAREST_NEIGHBORS matching 
- Uses exponential weighted average scoring for document-level matches 
- Returns match results with probability scores between 0.0 and 1.0 indicating similarity 

### Performance Characteristics
- Achieves linear O(N) performance for EQUALITY match types 
- Achieves O(N logN) performance for NEAREST_NEIGHBORS match types 

## Technical Constraints

- The repository uses Java as the primary programming language 
- The repository requires Java 11 as specified in the pom.xml properties 
- The repository uses Maven as the build system 
- The Maven compiler plugin is configured to use Java 11 as the release version 
- The repository enforces UTF-8 source encoding 

## Requirements

### Runtime Dependencies

- `org.apache.commons:commons-lang3:3.18.0` - Common utility functions and string operations 
- `org.apache.commons:commons-text:1.10.0` - Text processing utilities including Soundex encoding 
- `org.apache.commons:commons-collections4:4.4` - Collection utilities for set operations 
- `org.slf4j:slf4j-api:1.7.32` - Logging facade for Java applications 
- `org.slf4j:slf4j-simple:1.7.32` - Simple SLF4J logging implementation 
- `commons-codec:commons-codec:1.15` - Encoding and decoding utilities 
- `org.apache.lucene:lucene-core:8.10.0` - Core Lucene library for text indexing and search 
- `org.apache.lucene:lucene-analyzers-common:8.10.0` - Common text analyzers for Lucene 

### Test Dependencies

- `junit:junit:4.13.2` - Unit testing framework (JUnit 4) 
- `org.mockito:mockito-core:5.21.0` - Mocking framework for unit tests 
- `com.opencsv:opencsv:5.11.1` - CSV parsing library for test data 
- `org.apache.commons:commons-math3:3.6.1` - Mathematical utilities for tests 

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

Maven :
```xml
<dependency>
    <groupId>com.intuit.fuzzymatcher</groupId>
    <artifactId>fuzzy-matcher</artifactId>
    <version>1.2.1</version>
</dependency>
```

Minimal Java example :
```java
import com.intuit.fuzzymatcher.component.MatchService;
import com.intuit.fuzzymatcher.domain.Document;
import com.intuit.fuzzymatcher.domain.Element;
import com.intuit.fuzzymatcher.domain.Match;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import static com.intuit.fuzzymatcher.domain.ElementType.NAME;
import static com.intuit.fuzzymatcher.domain.ElementType.ADDRESS;

public class Demo {
    public static void main(String[] args) {
        String[][] input = {
            {"1", "Steven Wilson", "45th Avenue 5th st."},
            {"2", "John Doe", "546 freeman ave"},
            {"3", "Stephen Wilkson", "45th Ave 5th Street"}
        };
        
        List<Document> documentList = Arrays.asList(input).stream().map(contact -> {
            return new Document.Builder(contact[0])
                    .addElement(new Element.Builder<String>().setValue(contact[1]).setType(NAME).createElement())
                    .addElement(new Element.Builder<String>().setValue(contact[2]).setType(ADDRESS).createElement())
                    .createDocument();
        }).collect(Collectors.toList());
        
        MatchService matchService = new MatchService();
        Map<String, List<Match<Document>>> result = matchService.applyMatchByDocId(documentList);
        
        result.entrySet().forEach(entry -> {
            entry.getValue().forEach(match -> {
                System.out.println("Data: " + match.getData() + 
                    " Matched With: " + match.getMatchedWith() + 
                    " Score: " + match.getScore().getResult());
            });
        });
    }
}
```

## Command Line Configuration Arguments

This project is a library and does not provide a command-line interface. It is designed to be integrated into other Java applications programmatically .

## Terms/Concepts Explanation

**Document**: The primary object for matching, representing a record with a unique key and a set of elements to match against . Documents are compared to find similar records based on their constituent elements.

**Element**: A configurable field within a document representing a specific attribute (like name, address, or email) that participates in matching . Elements can be configured with type, weight, threshold, and custom processing functions.

**ElementType**: A predefined enumeration (NAME, TEXT, ADDRESS, EMAIL, PHONE, NUMBER, DATE, AGE) that determines default preprocessing, tokenization, and match type behavior .

**Token**: The atomic unit created by breaking down an element value through tokenization . Tokens are compared to determine similarity between elements.

**Tokenization**: The process of breaking down element values into smaller units (tokens) for comparison, using strategies like word splitting, N-grams, or Soundex encoding .

**MatchType**: An enumeration defining the strategy for comparing tokens—EQUALITY for exact matches or NEAREST_NEIGHBORS for proximity-based matching .

**Soundex**: A phonetic encoding algorithm that converts words to a standardized code based on how they sound, allowing "Steven" and "Stephen" to match despite different spelling .

**N-Gram**: A tokenization technique that breaks text into overlapping sequences of N characters (e.g., tri-grams are 3-character sequences), useful for matching partial strings like emails .

**Threshold**: A configurable score value (0.0 - 1.0) that determines when elements or documents are considered a match . Elements default to 0.3 threshold and documents to 0.5.

**Weight**: A multiplier applied to an element to increase or decrease its influence on the overall document score . Default weight is 1.0, with higher values making that element more significant.

**Preprocessing**: The initial data cleaning stage that applies transformations like trimming, lowercasing, removing special characters, or normalizing values before tokenization .

**NeighborhoodRange**: A parameter specific to NEAREST_NEIGHBORS matching that defines how close numeric or date values must be to be considered a match, with values between 0.0 and 1.0 (default 0.9) .
