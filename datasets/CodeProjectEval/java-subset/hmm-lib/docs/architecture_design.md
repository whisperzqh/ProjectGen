# Architecture Design

Below is a text-based representation of the file tree. 
```bash
src
    ├── main
    │   └── java
    │       └── com
    │           └── bmw
    │               └── hmm
    │                   ├── ForwardBackwardAlgorithm.java
    │                   ├── SequenceState.java
    │                   ├── Transition.java
    │                   ├── Utils.java
    │                   └── ViterbiAlgorithm.java
```

`ForwardBackwardAlgorithm.java`:

- `ForwardBackwardAlgorithm`: Computes the forward-backward algorithm (smoothing) to determine the probability of each state candidate at each time step given the entire observation sequence.

  - `startWithInitialStateProbabilities(initialStates: Collection<S>, initialProbabilities: Map<S, Double>) -> void`: Initializes the computation with explicit initial state probabilities.
  
  - `startWithInitialObservation(observation: O, candidates: Collection<S>, emissionProbabilities: Map<S, Double>) -> void`: Initializes the computation starting with the first observation and its emission probabilities.
  
  - `nextStep(observation: O, candidates: Collection<S>, emissionProbabilities: Map<S, Double>, transitionProbabilities: Map<Transition<S>, Double>) -> void`: Processes the next time step, updating forward probabilities based on new observations and transitions.
  
  - `computeSmoothingProbabilities() -> List<Map<S, Double>>`: Computes and returns the smoothing probabilities for all candidates across all time steps.
  
  - `forwardProbability(t: int, candidate: S) -> double`: Returns the forward probability of a specific candidate at a specific time step `t`.
  
  - `currentForwardProbability(candidate: S) -> double`: Returns the forward probability of a candidate at the most recent time step.
  
  - `observationLogProbability() -> double`: Returns the log probability of the entire observation sequence observed so far.
  
  - `computeSmoothingProbabilities(outBackwardProbabilities: List<Map<S, Double>>) -> List<Map<S, Double>>`: Internal method (package-private) that computes smoothing probabilities and optionally populates backward probabilities.
  
  - `computeSmoothingProbabilitiesVector(candidates: Collection<S>, forwardProbabilities: Map<S, Double>, backwardProbabilities: Map<S, Double>) -> Map<S, Double>`: Private helper to combine forward and backward probabilities for a single step.
  
  - `computeUnscaledBackwardProbability(candidate: S, nextBackwardProbabilities: Map<S, Double>, nextStep: Step) -> double`: Private helper to compute the unscaled backward probability for a candidate.
  
  - `sumsToOne(probabilities: Collection<Double>) -> boolean`: Private helper to verify that a collection of probabilities sums to approximately 1.0.
  
  - `initializeStateProbabilities(observation: O, candidates: Collection<S>, initialProbabilities: Map<S, Double>) -> void`: Private helper to set up the initial step of the algorithm.

  - `computeForwardProbability(curState: S, prevForwardProbabilities: Map<S, Double>, emissionProbabilities: Map<S, Double>, transitionProbabilities: Map<Transition<S>, Double>) -> double`: Returns the non-normalized forward probability of the specified state.

  - `transitionProbability(prevState: S, curState: S, transitionProbabilities: Map<Transition<S>, Double>) -> double`: Returns zero probability for non-existing transitions.

  - `normalizeForwardProbabilities(forwardProbabilities: Map<S, Double>, sum: double) -> void`: Normalizes the forward probabilities.

- `ForwardBackwardAlgorithm.Step`: Private inner class representing the internal state of the algorithm at a specific time step.

  - `Constructor(candidates: Collection<S>, emissionProbabilities: Map<S, Double>, transitionProbabilities: Map<Transition<S>, Double>, forwardProbabilities: Map<S, Double>, scalingDivisor: double) -> Step`: Stores the data for a single time step.

`SequenceState.java`:

- `SequenceState`: Represents a state in the most likely sequence, carrying additional context like the observation, transition descriptor, and smoothing probability.

  - `Constructor(state: S, observation: O, transitionDescriptor: D, smoothingProbability: Double) -> SequenceState`: Initializes the sequence state with its components.

`Transition.java`:

- `Transition`: Represents a directed transition between two state candidates (`fromCandidate` to `toCandidate`).

  - `Constructor(fromCandidate: S, toCandidate: S) -> Transition`: Creates a new transition object.
  
  - `hashCode() -> int`: Computes the hash code based on the source and target candidates.
  
  - `equals(obj: Object) -> boolean`: Checks equality based on the source and target candidates.
  
  - `toString() -> String`: Returns a string representation of the transition.

`Utils.java`:

- `Utils`: Package-private utility class containing helper methods for arithmetic and collection sizing.

  - `initialHashMapCapacity(maxElements: int) -> int`: Calculates the optimal initial capacity for a HashMap to avoid resizing.
  
  - `logToNonLogProbabilities(logProbabilities: Map<S, Double>) -> Map<S, Double>`: Converts a map of log probabilities to linear probabilities.
  
  - `probabilityInRange(probability: double, delta: double) -> boolean`: Checks if a probability value is within the valid range [0, 1] considering a delta tolerance.

`ViterbiAlgorithm.java`:

- `ViterbiAlgorithm`: Implements the Viterbi algorithm for time-inhomogeneous Markov processes to find the most likely sequence of states.

  - `Constructor() -> ViterbiAlgorithm`: Creates a new instance of the Viterbi algorithm.
  
  - `setKeepMessageHistory(keepMessageHistory: boolean) -> ViterbiAlgorithm<S, O, D>`: Configures whether to store intermediate forward messages for debugging.
  
  - `setComputeSmoothingProbabilities(computeSmoothingProbabilities: boolean) -> ViterbiAlgorithm<S, O, D>`: Configures whether to also compute smoothing probabilities using the forward-backward algorithm.
  
  - `processingStarted() -> boolean`: Checks if the algorithm has processed any data (initialization called).
  
  - `startWithInitialStateProbabilities(initialStates: Collection<S>, initialLogProbabilities: Map<S, Double>) -> void`: Starts the algorithm with explicit initial state log probabilities.
  
  - `startWithInitialObservation(observation: O, candidates: Collection<S>, emissionLogProbabilities: Map<S, Double>) -> void`: Starts the algorithm with an initial observation and its emission log probabilities.
  
  - `nextStep(observation: O, candidates: Collection<S>, emissionLogProbabilities: Map<S, Double>, transitionLogProbabilities: Map<Transition<S>, Double>, transitionDescriptors: Map<Transition<S>, D>) -> void`: Processes the next time step with optional transition descriptors.
  
  - `nextStep(observation: O, candidates: Collection<S>, emissionLogProbabilities: Map<S, Double>, transitionLogProbabilities: Map<Transition<S>, Double>) -> void`: Overload of `nextStep` without transition descriptors.
  
  - `computeMostLikelySequence() -> List<SequenceState<S, O, D>>`: Computes and returns the globally most likely sequence of states.
  
  - `isBroken() -> boolean`: Returns true if a break occurred (all state probabilities became zero).
  
  - `isComputeSmoothingProbabilities() -> boolean`: Returns the current configuration for smoothing probabilities computation.
  
  - `isKeepMessageHistory() -> boolean`: Returns the current configuration for message history storage.
  
  - `messageHistory() -> List<Map<S, Double>>`: Returns the list of intermediate messages if history was kept.
  
  - `messageHistoryString() -> String`: Returns a string representation of the message history for debugging.
  
  - `hmmBreak(message: Map<S, Double>) -> boolean`: Private helper to check if an HMM break occurred (all log probabilities are negative infinity).
  
  - `initializeStateProbabilities(observation: O, candidates: Collection<S>, initialLogProbabilities: Map<S, Double>) -> void`: Private helper to initialize internal state structures.
  
  - `forwardStep(observation: O, prevCandidates: Collection<S>, curCandidates: Collection<S>, message: Map<S, Double>, emissionLogProbabilities: Map<S, Double>, transitionLogProbabilities: Map<Transition<S>, Double>, transitionDescriptors: Map<Transition<S>, D>) -> ForwardStepResult<S, O, D>`: Private helper to perform the forward step calculation.
  
  - `transitionLogProbability(prevState: S, curState: S, transitionLogProbabilities: Map<Transition<S>, Double>) -> double`: Private helper to retrieve transition log probability safely.
  
  - `mostLikelyState() -> S`: Private helper to find the state with the highest probability in the current message.
  
  - `retrieveMostLikelySequence() -> List<SequenceState<S, O, D>>`: Private helper to reconstruct the path using back pointers.

- `ViterbiAlgorithm.ExtendedState`: Private static inner class storing state, back pointer to previous state, observation, and transition descriptor.

  - `Constructor(state: S, backPointer: ExtendedState<S, O, D>, observation: O, transitionDescriptor: D) -> ExtendedState`: Initializes the extended state node.

- `ViterbiAlgorithm.ForwardStepResult`: Private static inner class holding the results of a single forward step (new message and extended states).

  - `Constructor(numberStates: int) -> ForwardStepResult`: Initializes containers with expected capacity.
