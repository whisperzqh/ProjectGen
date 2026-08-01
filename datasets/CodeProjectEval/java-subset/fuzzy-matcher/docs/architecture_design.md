# Architecture Design

Below is a text-based representation of the file tree. 
```bash
src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── intuit
    │   │           └── fuzzymatcher
    │   │               ├── component
    │   │               │   ├── Dictionary.java
    │   │               │   ├── DocumentMatch.java
    │   │               │   ├── ElementMatch.java
    │   │               │   ├── MatchService.java
    │   │               │   └── TokenRepo.java
    │   │               ├── domain
    │   │               │   ├── Document.java
    │   │               │   ├── ElementClassification.java
    │   │               │   ├── Element.java
    │   │               │   ├── ElementType.java
    │   │               │   ├── Matchable.java
    │   │               │   ├── Match.java
    │   │               │   ├── MatchType.java
    │   │               │   ├── Score.java
    │   │               │   └── Token.java
    │   │               ├── exception
    │   │               │   └── MatchException.java
    │   │               ├── function
    │   │               │   ├── PreProcessFunction.java
    │   │               │   ├── ScoringFunction.java
    │   │               │   └── TokenizerFunction.java
    │   │               └── util
    │   │                   └── Utils.java
```

`Dictionary.java`:

- `Dictionary`: Used for pre-processing, caching pre-defined normalization and replacements for common characters found in names and addresses.

  - `getAddressDictionary() -> Map<String, String>`: Loads and returns the address dictionary from the classpath resource `address-dictionary.txt`.
  
  - `getNameDictionary() -> Map<String, String>`: Loads and returns the name dictionary from the classpath resource `name-dictionary.txt`.
  
  - `getDictionary(br: BufferedReader) -> Map<String, String>`: Parses the input stream and builds a dictionary map, converting keys to lowercase and splitting by colon.

`DocumentMatch.java`:

- `DocumentMatch`: Orchestrates the matching process by performing element-level matching and aggregating results back to document matches.

  - `Constructor() -> DocumentMatch`: Initializes the `DocumentMatch` instance and creates an internal `ElementMatch` component.
  
  - `matchDocuments(documents: Stream<Document>) -> Stream<Match<Document>>`: Executes matching for a stream of documents, aggregating element matches into document matches.
  
  - `documentThresholdMatching(document: Document, matchingElements: Set<Match<Element>>) -> Stream<Match<Document>>`: Groups element matches by target document, calculates scores, and returns valid document matches exceeding the threshold.

`ElementMatch.java`:

- `ElementMatch`: Handles matching at the element level using a token repository.

  - `Constructor() -> ElementMatch`: Initializes the `ElementMatch` instance and creates an internal `TokenRepo`.
  
  - `matchElement(element: Element) -> Set<Match<Element>>`: Matches a single element by breaking it into tokens and querying the repository, returning a set of element matches.
  
  - `elementThresholdMatching(token: Token, elementTokenScore: Map<Element, Integer>, matchingElements: Set<Match<Element>>) -> void`: Retrieves potential matches for a token, aggregates scores for elements, and adds valid matches to the result set if they exceed the threshold.

`MatchService.java`:

- `MatchService`: The primary entry point for fuzzy matching, offering various methods to match lists of documents for de-duplication or bulk checks.

  - `applyMatch(documents: List<Document>) -> Map<Document, List<Match<Document>>>`: Performs de-duplication on a list of documents, grouping matches by the source document.
  
  - `applyMatch(documents: List<Document>, matchWith: List<Document>) -> Map<Document, List<Match<Document>>>`: Checks a list of new documents against an existing list, grouping matches by the new documents.
  
  - `applyMatch(document: Document, matchWith: List<Document>) -> Map<Document, List<Match<Document>>>`: Checks a single new document against an existing list of documents.
  
  - `applyMatchByDocId(document: Document, matchWith: List<Document>) -> Map<String, List<Match<Document>>>`: Checks a single document against a list and aggregates results by document ID.
  
  - `applyMatchByDocId(documents: List<Document>) -> Map<String, List<Match<Document>>>`: Performs de-duplication on a list and aggregates results by document ID.
  
  - `applyMatchByDocId(documents: List<Document>, matchWith: List<Document>) -> Map<String, List<Match<Document>>>`: Checks new documents against existing ones and aggregates results by document ID.
  
  - `applyMatchByGroups(documents: List<Document>) -> Set<Set<Match<Document>>>`: Performs de-duplication and groups transitive matches together (e.g., if A matches B and B matches C, all are grouped).
  
  - `groupSimilar(matchMap: Map<String, List<Match<Document>>>, key: String, matchGroups: Set<Match<Document>>) -> void`: Recursively traverses matches to form transitive groups of matched documents.
  
  - `containsMatch(matchGroups: Set<Match<Document>>, match: Match<Document>) -> boolean`: Checks if a specific match relationship already exists within the collected groups.

`TokenRepo.java`:

- `TokenRepo`: Serves as a repository to store and retrieve tokens, indexed by element classification and match type.

  - `Constructor() -> TokenRepo`: Initializes the `TokenRepo` with a concurrent hash map for storage.
  
  - `put(token: Token) -> void`: Adds a token to the appropriate internal repository based on its element classification.
  
  - `get(token: Token) -> Set<Element>`: Retrieves a set of elements that match the given token from the repository.

`Document.java`:

- `Document`: Represents a data record containing a collection of elements, serving as the primary object for matching.

  - `Constructor(key: String, elements: Set<Element>, threshold: double) -> Document`: Private constructor used by the Builder to create a document.
  
  - `getKey() -> String`: Returns the unique identifier of the document.
  
  - `getElements() -> Set<Element>`: Returns the set of elements associated with the document.
  
  - `getPreProcessedElement() -> Set<Element>`: Returns a set of distinct, non-empty elements after pre-processing.
  
  - `getThreshold() -> double`: Returns the match threshold for the document.
  
  - `getDistinctElements() -> Stream<Element>`: Returns a stream of elements distinct by their pre-processed value and type.
  
  - `getDistinctNonEmptyElements() -> Stream<Element>`: Returns a stream of distinct elements that are not null or empty.
  
  - `distinctByKey(keyExtractor: Function<? super T, ?>) -> Predicate<T>`: Returns a predicate to filter stream elements by a specific key.
  
  - `getChildCount(other: Matchable) -> long`: Calculates the size of the union of element classifications between this document and another.
  
  - `getUnmatchedChildCount(other: Matchable) -> long`: Calculates the number of element classifications that differ between this document and another.
  
  - `getScoringFunction() -> BiFunction<Match, List<Score>, Score>`: Returns the default scoring function (Exponential Weighted Average) for the document.
  
  - `getWeight() -> double`: Returns the weight of the document (default 1.0).
  
  - `isSource() -> Boolean`: Returns whether this document is a source document in the matching process.
  
  - `setSource(source: Boolean) -> void`: Sets the source flag for the document.
  
  - `toString() -> String`: Returns a string representation of the document's elements.
  
  - `getOrderedElements(elements: Set<Element>) -> List<Element>`: Returns elements sorted by their classification type.
  
  - `equals(o: Object) -> boolean`: Checks equality based on the document key.
  
  - `hashCode() -> int`: Returns the hash code derived from the document key.

- `Document.Builder`: Builder class for creating Document instances.

  - `Constructor(key: String) -> Builder`: Initializes the builder with a document key.

  - `setThreshold(threshold: double) -> Builder`: Sets the match threshold (default 0.5).

  - `addElement(element: Element) -> Builder`: Adds an element to the document.

  - `createDocument() -> Document`: Builds and returns the Document instance.

`ElementClassification.java`:

- `ElementClassification`: Defines the classification of an element using its type and a variance string.

  - `Constructor(elementType: ElementType, variance: String) -> ElementClassification`: Initializes the classification with a type and variance.
  
  - `getElementType() -> ElementType`: Returns the element type.
  
  - `getVariance() -> String`: Returns the variance identifier.
  
  - `equals(o: Object) -> boolean`: Checks equality based on element type and variance.
  
  - `hashCode() -> int`: Returns the hash code derived from element type and variance.

`Element.java`:

- `Element`: Represents a specific data field (like name or address) within a document, containing logic for pre-processing, tokenization, and matching.

  - `Constructor(type: ElementType, variance: String, value: T, weight: double, threshold: double, neighborhoodRange: double, preProcessFunction: Function<T, T>, tokenizerFunction: Function<Element<T>, Stream<Token>>, matchType: MatchType) -> Element`: Initializes the element with all configuration parameters.
  
  - `getElementClassification() -> ElementClassification`: Returns the classification object for this element.
  
  - `getValue() -> T`: Returns the raw value of the element.
  
  - `getWeight() -> double`: Returns the weight used in scoring.
  
  - `getThreshold() -> double`: Returns the threshold for element matching.
  
  - `getNeighborhoodRange() -> double`: Returns the range used for nearest neighbor matching.
  
  - `getDocument() -> Document`: Returns the parent document of this element.
  
  - `setDocument(document: Document) -> void`: Sets the parent document.
  
  - `setPreProcessedValue(preProcessedValue: T) -> void`: Manually sets the pre-processed value.
  
  - `getPreProcessFunction() -> Function<T, T>`: Returns the function used for pre-processing.
  
  - `getPreProcessedValue() -> T`: returns the cached pre-processed value, calculating it if necessary.
  
  - `getPreprocessedValueWithType() -> AbstractMap.SimpleEntry`: Returns a map entry containing the classification and pre-processed value.
  
  - `getTokenizerFunction() -> Function<Element<T>, Stream<Token>>`: Returns the function used for tokenization.
  
  - `getMatchType() -> MatchType`: Returns the match type strategy (e.g., Equality, Nearest Neighbors).
  
  - `getTokens() -> List<Token>`: Generates and returns the list of tokens for this element.
  
  - `getScore(matchingCount: Integer, other: Element) -> double`: Calculates the match score based on matching token count and child count.
  
  - `getChildCount(other: Matchable) -> long`: Returns the maximum token count between this element and another.
  
  - `getUnmatchedChildCount(other: Matchable) -> long`: Returns the count of empty or null tokens between this and another element.
  
  - `getScoringFunction() -> BiFunction<Match, List<Score>, Score>`: Returns null as elements typically don't aggregate further child scores in this context.
  
  - `toString() -> String`: Returns a string representation of the element's value.
  
  - `equals(o: Object) -> boolean`: Checks equality based on value, classification, and document.
  
  - `hashCode() -> int`: Returns the hash code derived from value, classification, and document.

- `Element.Builder`: Builder class for creating Element instances.

  - `setType(type: ElementType) -> Builder`: Sets the element type.

  - `setVariance(variance: String) -> Builder`: Sets the variance string.

  - `setValue(value: T) -> Builder`: Sets the element value.

  - `setWeight(weight: double) -> Builder`: Sets the weight (default 1.0).

  - `setThreshold(threshold: double) -> Builder`: Sets the match threshold (default 0.3).

  - `setNeighborhoodRange(neighborhoodRange: double) -> Builder`: Sets the neighborhood range (default 0.9).

  - `setPreProcessingFunction(preProcessingFunction: Function<T, T>) -> Builder`: Sets a custom pre-processing function.

  - `setTokenizerFunction(tokenizerFunction: Function<Element<T>, Stream<Token>>) -> Builder`: Sets a custom tokenizer function.

  - `setMatchType(matchType: MatchType) -> Builder`: Sets the match type (EQUALITY/NEAREST_NEIGHBORS).

  - `createElement() -> Element`: Builds and returns the Element instance.

`ElementType.java`:

- `ElementType`: Enum defining standard types of elements (NAME, TEXT, ADDRESS, etc.) and their default behaviors.

  - `getPreProcessFunction() -> Function`: Returns the default pre-processing function for the enum constant.
  
  - `getTokenizerFunction() -> Function`: Returns the default tokenization function for the enum constant.
  
  - `getMatchType() -> MatchType`: Returns the default match type for the enum constant.

`Matchable.java`:

- `Matchable`: Interface implemented by objects that can be matched and scored (Document, Element).

  - `getChildCount(other: Matchable) -> long`: Returns the count of child components used for scoring normalization.
  
  - `getScoringFunction() -> BiFunction<Match, List<Score>, Score>`: Returns the function used to aggregate scores.
  
  - `getWeight() -> double`: Returns the importance weight of the object.
  
  - `getUnmatchedChildCount(other: Matchable) -> long`: Returns the count of unmatched children for penalty calculation.

`Match.java`:

- `Match`: Represents a match result between two objects (Documents or Elements), holding the data, the match target, and the score.

  - `Constructor(t: T, matchedWith: T) -> Match`: Creates a match container for two objects.
  
  - `Constructor(t: T, matchedWith: T, childScores: List<Score>) -> Match`: Creates a match and calculates score based on child scores.
  
  - `Constructor(t: T, matchedWith: T, result: double) -> Match`: Creates a match with a specific result score.
  
  - `getData() -> T`: Returns the source object of the match.
  
  - `getMatchedWith() -> T`: Returns the target object matched against.
  
  - `getResult() -> double`: Returns the numerical score of the match.
  
  - `getScore() -> Score`: Returns the Score object.
  
  - `setScore(childScores: List<Score>) -> void`: Calculates and sets the score using the object's scoring function and child scores.
  
  - `getMaxDistinctScores(scoreList: List<Score>) -> List<Score>`: Filters child scores to keep only the highest score per distinct data item.
  
  - `getWeight() -> double`: Returns the weight of the source data.
  
  - `toString() -> String`: Returns a string summary of the match.
  
  - `equals(o: Object) -> boolean`: Checks equality based on the two matched objects.
  
  - `hashCode() -> int`: Returns hash code derived from the two matched objects.

`MatchType.java`:

- `MatchType`: Enum defining the strategy for matching (EQUALITY, NEAREST_NEIGHBORS).

`Score.java`:

- `Score`: Holds the numerical result of a match and a reference to the match itself.

  - `Constructor(result: double, match: Match) -> Score`: Initializes the score with a value and match reference.
  
  - `getResult() -> double`: Returns the numerical score value.
  
  - `getMatch() -> Match`: Returns the associated match object.
  
  - `toString() -> String`: Returns a string representation of the score.

`Token.java`:

- `Token`: Represents a discrete unit extracted from an Element, used for efficient indexing and matching.

  - `Constructor(value: T, element: Element) -> Token`: Creates a token with a value and reference to its parent element.
  
  - `getValue() -> T`: Returns the token value.
  
  - `getElement() -> Element`: Returns the parent element.
  
  - `toString() -> String`: Returns a string representation of the token value.
  
  - `equals(o: Object) -> boolean`: Checks equality based on value and parent element.
  
  - `hashCode() -> int`: Returns hash code derived from value and parent element.

`MatchException.java`:

- `MatchException`: Custom runtime exception for errors occurring during the matching process.

  - `Constructor() -> MatchException`: Creates an exception with no details.
  
  - `Constructor(message: String) -> MatchException`: Creates an exception with a message.
  
  - `Constructor(t: Throwable) -> MatchException`: Creates an exception wrapping a cause.
  
  - `Constructor(message: String, t: Throwable) -> MatchException`: Creates an exception with message and cause.

`PreProcessFunction.java`:

- `PreProcessFunction`: Provides a collection of static functions for string pre-processing (trimming, cleaning, normalizing).

  - `trim() -> Function<String, String>`: Returns a function that trims whitespace.
  
  - `toLowerCase() -> Function<String, String>`: Returns a function that converts text to lowercase.
  
  - `numericValue() -> Function<String, String>`: Returns a function that strips non-numeric characters.
  
  - `removeSpecialChars() -> Function<String, String>`: Returns a function that removes non-alphanumeric characters.
  
  - `removeDomain() -> Function<String, String>`: Returns a function that removes the email domain (after @).
  
  - `addressPreprocessing() -> Function<String, String>`: Chains special character removal and address normalization.
  
  - `namePreprocessing() -> Function<String, String>`: Chains trailing number removal, special char removal, and name normalization.
  
  - `addressNormalization() -> Function<String, String>`: Normalizes common address abbreviations (e.g., "st." to "street") using a dictionary.
  
  - `removeTrailingNumber() -> Function<String, String>`: Removes trailing digits from a string.
  
  - `nameNormalization() -> Function<String, String>`: Removes common name prefixes/suffixes using a dictionary.
  
  - `usPhoneNormalization() -> Function<String, String>`: Standardizes US phone numbers by adding a prefix if needed.
  
  - `numberPreprocessing() -> Function`: Extracts numeric sequences including decimals from a string.
  
  - `none() -> Function`: Returns an identity function which does nothing.

`ScoringFunction.java`:

- `ScoringFunction`: Interface and factory for functions that aggregate child scores into a total match score.

  - `getAverageScore() -> ScoringFunction`: Returns a strategy that calculates the simple average of child scores, penalizing missing children.
  
  - `getSimpleAverageScore() -> ScoringFunction`: Returns a strategy that calculates the simple average based on existing child scores only.
  
  - `getWeightedAverageScore() -> ScoringFunction`: Returns a strategy that calculates a weighted average of child scores.
  
  - `getExponentialAverageScore() -> ScoringFunction`: Returns a strategy that applies an exponential boost if multiple high-quality matches exist.
  
  - `getExponentialWeightedAverageScore() -> ScoringFunction`: Default strategy combining weighted average with exponential boosting for high-quality matches.
  
  - `getSumOfWeightedResult(childScoreList: List<Score>) -> double`: Helper to calculate sum of score * weight.
  
  - `getSumOfResult(childScoreList: List<Score>) -> double`: Helper to calculate sum of raw scores.
  
  - `getSumOfWeights(childScoreList: List<Score>) -> double`: Helper to calculate sum of weights.
  
  - `getExponentiallyIncreasedValue(value: double) -> double`: Applies an exponent (1.5) to a value.
  
  - `getNonPerfectMatchedElement(childScoreList: List<Score>) -> List<Score>`: Filters scores below the perfection threshold.
  
  - `getPerfectMatchedElement(childScoreList: List<Score>) -> List<Score>`: Filters scores meeting or exceeding the perfection threshold.
  
  - `getChildCount(match: Match) -> double`: Helper to retrieve child count from the match object.
  
  - `getUnmatchedChildScore(match: Match) -> double`: Helper to calculate score penalty for unmatched children.

`TokenizerFunction.java`:

- `TokenizerFunction`: Provides static factory methods for creating different tokenization strategies.

  - `valueTokenizer() -> Function<Element, Stream<Token>>`: Tokenizes the entire value as a single token.
  
  - `wordTokenizer() -> Function<Element<String>, Stream<Token<String>>>`: Splits the string value by whitespace into word tokens.
  
  - `wordSoundexEncodeTokenizer() -> Function<Element<String>, Stream<Token<String>>>`: Splits words and encodes them using Soundex logic for phonetic matching.
  
  - `triGramTokenizer() -> Function<Element<String>, Stream<Token<String>>>`: Generates 3-character n-grams from the value.
  
  - `decaGramTokenizer() -> Function<Element<String>, Stream<Token<String>>>`: Generates 10-character n-grams from the value.
  
  - `getNGramTokens(size: int, element: Element) -> Stream<Token<String>>`: Helper to generate n-grams of a specific size.
  
  - `chainTokenizers(tokenizers: Function<Element<String>, Stream<Token<String>>>[]) -> Function<Element<String>, Stream<Token<String>>>`: Combines multiple tokenizers into one stream.

`Utils.java`:

- `Utils`: General utility methods for string manipulation and N-Gram generation.

  - `getNGrams(value: String, size: int) -> Stream<String>`: Generates a stream of N-Grams using Lucene's tokenizer.
  
  - `getNormalizedString(str: String, dict: Map<String, String>) -> String`: Replaces words in a string based on a provided dictionary map.
  
  - `isNumeric(str: String) -> boolean`: Checks if a string contains any numeric characters.
