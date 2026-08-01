# Product Requirements Document: hmm-lib

## Introduction and Goals

**Introduction**

hmm-lib is a Java library that implements Hidden Markov Models (HMM) for time-inhomogeneous Markov processes. Unlike many other HMM implementations, this library allows for different states and different transition matrices at each time step.  The library was initially developed by BMW Car IT GmbH and BMW AG for HMM-based map matching, specifically following the approach described in the Newson & Krumm paper on Hidden Markov map matching through noise and sparseness.  It is now used by Graphhopper's map matching project and is designed to be applicable to other domains beyond map matching. 

**Goals**

The primary goal of hmm-lib is to provide efficient implementations of two core HMM algorithms: the Viterbi algorithm for computing the most likely sequence of states, and the forward-backward algorithm for computing smoothing probabilities of all state candidates given the entire observation sequence.  A key design goal is memory efficiency—the library reduces memory footprint from O(t*n²) to O(t*n) or even O(t) in many applications by leveraging Java's garbage collection to manage back pointers that converge to a single path.  The API is designed for iterative calling with flexibility for users to compute transition and observation probabilities on-the-fly, and to support transition descriptors (e.g., routes between road positions) without requiring the caller to store all possible transitions. 

## Features and Functionalities

The following features and functionalities are provided by the project:

### Hidden Markov Model Algorithms
- Provides Viterbi algorithm implementation for computing the most likely sequence of states in time-inhomogeneous Markov processes 
- Provides forward-backward algorithm (smoothing) for computing the probability of each state candidate at each time step given the entire observation sequence 
- Supports logarithmic probabilities as input to prevent arithmetic underflows for small probability values 
- Allows optional computation of smoothing probabilities for states in the most likely sequence using the forward-backward algorithm 

### Time-Inhomogeneous Markov Process Support
- Supports different sets of state candidates at each time step 
- Supports different transition matrices between consecutive time steps 
- Allows zero transition probabilities for missing transitions without requiring explicit specification 

### Flexible API Design
- Allows iterative processing with separate methods for initialization and subsequent time steps 
- Supports starting with either initial state probabilities or with an initial observation 
- Provides HMM break detection when all states have zero probability 

### Transition Descriptor Support
- Stores optional transition descriptors (e.g., routes between map positions) alongside state transitions 
- Retrieves transition descriptors in the final most likely sequence without requiring caller to store all possible transitions 
- Reduces memory requirements from O(t*n²) to O(t*n) by storing only one transition descriptor per back pointer 

### Memory Optimization
- Exploits back pointer convergence to enable garbage collection of unreachable states 
- Achieves O(t) memory footprint when back pointers converge after a constant number of steps 
- Uses chained back pointers with plain Java references to allow automatic memory reclamation 

### Debugging and Introspection
- Supports optional message history storage for debugging intermediate forward messages 
- Provides methods to query forward probabilities at any time step 
- Computes observation log probability for the entire sequence 

### Build and Dependency Management
- Provides Maven-based build system with standard lifecycle 
- Packages as a JAR library for integration into other projects 
- Distributes releases and snapshots via GitHub-hosted Maven repositories 
- Supports unit testing with JUnit 4 

## Technical Constraints

- The repository uses Java as the primary programming language 
- The repository targets Java 7 (source and target version 1.7) as specified in the Maven compiler plugin configuration 
- The repository uses Maven as the build system 
- The repository has no runtime dependencies beyond the Java standard library (excluding test dependencies) 
- UTF-8 encoding is required for source and reporting 

## Requirements

### Runtime Dependencies

The library has no runtime dependencies beyond the Java standard library. 

### Development Dependencies

- `junit:junit:4.13.1` - Unit testing framework (JUnit 4) 

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

This project is a library intended to be used as a dependency in other Java projects. 

Maven:
```xml
<dependency>
  <groupId>com.bmw.hmm</groupId>
  <artifactId>hmm-lib</artifactId>
  <version>1.1.0-SNAPSHOT</version>
</dependency>
``` 

For snapshots, add the snapshot repository:
```xml
<repositories>
  <repository>
    <id>hmm-lib-snapshots</id>
    <url>https://raw.github.com/bmwcarit/hmm-lib/mvn-snapshots/</url>
    <snapshots>
      <enabled>true</enabled>
      <updatePolicy>always</updatePolicy>
    </snapshots>
  </repository>
</repositories>
``` 

Minimal Java example using the Viterbi algorithm:
```java
import com.bmw.hmm.ViterbiAlgorithm;
import com.bmw.hmm.SequenceState;
import java.util.*;

public class Demo {
  public static void main(String[] args) {
    ViterbiAlgorithm<State, Observation, TransitionDescriptor> viterbi = 
        new ViterbiAlgorithm<>();
    
    // Start with initial observation
    viterbi.startWithInitialObservation(observation, candidates, emissionLogProbs);
    
    // Process subsequent time steps
    viterbi.nextStep(nextObservation, nextCandidates, 
        emissionLogProbs, transitionLogProbs, transitionDescriptors);
    
    // Retrieve most likely sequence
    List<SequenceState<State, Observation, TransitionDescriptor>> sequence = 
        viterbi.computeMostLikelySequence();
  }
}
```

## Command Line Configuration Arguments

This project is a library and does not provide a command line interface or configuration arguments. It is designed to be integrated into other Java applications programmatically. 

## Terms/Concepts Explanation

**Hidden Markov Model (HMM)**: A statistical model where the system state is not directly observable (hidden) but can be inferred from observations; in hmm-lib, this is implemented for time-inhomogeneous processes where states and transition probabilities can vary at each time step. 

**Viterbi Algorithm**: An algorithm that computes the most likely sequence of hidden states given a sequence of observations; hmm-lib's implementation supports iterative processing and optional smoothing probability computation. 

**Forward-Backward Algorithm**: Also known as smoothing, this algorithm computes the probability of each state candidate at each time step given the entire observation sequence, as opposed to just the observations up to that point. 

**Time-Inhomogeneous Markov Process**: A Markov process where the set of states and state transition probabilities are not fixed for all time steps; this is the key differentiator of hmm-lib from many other HMM implementations. 

**Emission Probability**: The probability of observing a particular observation given a hidden state; in hmm-lib, these are provided as logarithmic probabilities to prevent arithmetic underflows. 

**Transition Probability**: The probability of transitioning from one state to another between consecutive time steps; hmm-lib assumes zero probability for missing transitions. 

**Back Pointer**: A reference from a state in the current time step to the most likely previous state; hmm-lib chains back pointers using Java references to enable garbage collection of unreachable paths. 

**Transition Descriptor**: An optional object that describes transitions between states (e.g., the route between two road positions in map matching); hmm-lib stores these efficiently alongside back pointers. 

**HMM Break**: A situation where all state candidates have zero probability, indicating that no valid sequence can be constructed; hmm-lib detects and handles this condition. 

**Smoothing Probability**: The probability of a state given all observations (past and future), as opposed to just past observations; computed by the forward-backward algorithm and optionally included in the Viterbi result. 

**Map Matching**: The primary application domain for which hmm-lib was initially developed; the process of matching GPS positions to road positions on a map using HMM techniques. 

**Logarithmic Probability**: Probabilities expressed in logarithmic form to prevent arithmetic underflow when dealing with very small probability values; hmm-lib expects logarithmic probabilities as input. 
