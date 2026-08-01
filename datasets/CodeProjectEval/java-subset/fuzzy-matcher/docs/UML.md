``` mermaid
classDiagram
direction BT
class Builder {
  - double threshold
   double threshold
  + createDocument() Document
  + addElement(Element) Builder
  + Builder(String) 
}
class Builder~T~ {
  - double weight
  - T value
  - String variance
  - ElementType type
  - double threshold
  - MatchType matchType
  - Function~Element~T~, Stream~Token~~ tokenizerFunction
  - double neighborhoodRange
   MatchType matchType
   double threshold
   String variance
   T value
   double weight
   double neighborhoodRange
   ElementType type
   Function~Element~T~, Stream~Token~~ tokenizerFunction
   Function~T, T~ preProcessingFunction
  + createElement() Element
  + Builder() 
}
class Dictionary {
  + Map~String, String~ addressDictionary
  + Map~String, String~ nameDictionary
   Map~String, String~ addressDictionary
   Map~String, String~ nameDictionary
  - getDictionary(BufferedReader) Map~String, String~
  + Dictionary() 
}
class Document {
  - String key
  - Set~Element~ elements
  - double threshold
  - Boolean source
  - Set~Element~ preProcessedElement
   Stream~Element~ distinctElements
   double threshold
   Set~Element~ elements
   BiFunction~Match, List~Score~, Score~ scoringFunction
   double weight
   Stream~Element~ distinctNonEmptyElements
   Set~Element~ preProcessedElement
   Boolean source
   String key
  + equals(Object) boolean
  + hashCode() int
  + getChildCount(Matchable) long
  - distinctByKey(Function~T, ?~) Predicate~T~
  + getUnmatchedChildCount(Matchable) long
  + toString() String
  + getOrderedElements(Set~Element~) List~Element~
  + isSource() Boolean
  - Document(String, Set~Element~, double) 
}
class DocumentMatch {
  + matchDocuments(Stream~Document~) Stream~Match~Document~~
  - documentThresholdMatching(Document, Set~Match~Element~~) Stream~Match~Document~~
  + DocumentMatch() 
}
class Element~T~ {
  - MatchType matchType
  - double threshold
  - List~Token~ tokens
  - ElementClassification elementClassification
  - double neighborhoodRange
  - Function~Element~T~, Stream~Token~~ tokenizerFunction
  - T value
  - Document document
  - double weight
  - T preProcessedValue
  - Function~T, T~ preProcessFunction
   MatchType matchType
   double threshold
   Function~T, T~ preProcessFunction
   T value
   ElementClassification elementClassification
   double weight
   T preProcessedValue
   Function~Element~T~, Stream~Token~~ tokenizerFunction
   List~Token~ tokens
   Document document
   BiFunction~Match, List~Score~, Score~ scoringFunction
   SimpleEntry preprocessedValueWithType
   double neighborhoodRange
  + getScore(Integer, Element) double
  + toString() String
  + getUnmatchedChildCount(Matchable) long
  + equals(Object) boolean
  + hashCode() int
  + getChildCount(Matchable) long
  + Element(ElementType, String, T, double, double, double, Function~T, T~, Function~Element~T~, Stream~Token~~, MatchType) 
}
class ElementClassification {
  - String variance
  - ElementType elementType
   String variance
   ElementType elementType
  + equals(Object) boolean
  + hashCode() int
  + ElementClassification(ElementType, String) 
}
class ElementMatch {
  + matchElement(Element) Set~Match~Element~~
  - elementThresholdMatching(Token, Map~Element, Integer~, Set~Match~Element~~) void
  + ElementMatch() 
}
class ElementType {
<<enumeration>>
   MatchType matchType
   Function preProcessFunction
   Function tokenizerFunction
  + values() ElementType[]
  + valueOf(String) ElementType
  + ElementType() 
}
class Match~T~ {
  - T matchedWith
  - T data
  - Score score
   double weight
   double result
   T matchedWith
   Score score
   T data
  - getMaxDistinctScores(List~Score~) List~Score~
  + hashCode() int
  + toString() String
  + equals(Object) boolean
  + Match(T, T, List~Score~) 
  + Match(T, T, double) 
  + Match(T, T) 
}
class MatchException {
  + MatchException(Throwable) 
  + MatchException(String, Throwable) 
  + MatchException() 
  + MatchException(String) 
}
class MatchService {
  + applyMatch(List~Document~, List~Document~) Map~Document, List~Match~Document~~~
  + applyMatchByDocId(List~Document~) Map~String, List~Match~Document~~~
  - groupSimilar(Map~String, List~Match~Document~~~, String, Set~Match~Document~~) void
  + applyMatchByDocId(Document, List~Document~) Map~String, List~Match~Document~~~
  - containsMatch(Set~Match~Document~~, Match~Document~) boolean
  + applyMatch(Document, List~Document~) Map~Document, List~Match~Document~~~
  + applyMatchByGroups(List~Document~) Set~Set~Match~Document~~~
  + applyMatch(List~Document~) Map~Document, List~Match~Document~~~
  + applyMatchByDocId(List~Document~, List~Document~) Map~String, List~Match~Document~~~
  + MatchService() 
}
class MatchType {
<<enumeration>>
  + valueOf(String) MatchType
  + values() MatchType[]
  + MatchType() 
}
class Matchable {
<<Interface>>
   double weight
   BiFunction~Match, List~Score~, Score~ scoringFunction
  + getUnmatchedChildCount(Matchable) long
  + getChildCount(Matchable) long
}
class PreProcessFunction~T~ {
  + numericValue() Function~String, String~
  + none() Function
  + namePreprocessing() Function~String, String~
  + numberPreprocessing() Function
  + trim() Function~String, String~
  + removeSpecialChars() Function~String, String~
  + removeDomain() Function~String, String~
  + toLowerCase() Function~String, String~
  + usPhoneNormalization() Function~String, String~
  + removeTrailingNumber() Function~String, String~
  + nameNormalization() Function~String, String~
  + addressNormalization() Function~String, String~
  + addressPreprocessing() Function~String, String~
  + PreProcessFunction() 
}
class Repo {
  ~ put(Token, Element) void
  ~ get(Token) Set~Element~?
  ~ Repo(MatchType) 
}
class Score {
  - double result
  - Match match
   Match match
   double result
  + toString() String
  + Score(double, Match) 
}
class ScoringFunction {
<<Interface>>
   ScoringFunction exponentialWeightedAverageScore
   ScoringFunction simpleAverageScore
   ScoringFunction averageScore
   ScoringFunction weightedAverageScore
   ScoringFunction exponentialAverageScore
  + getUnmatchedChildScore(Match) double
  + getSumOfWeights(List~Score~) double
  + getNonPerfectMatchedElement(List~Score~) List~Score~
  + getExponentiallyIncreasedValue(double) double
  + getSumOfResult(List~Score~) double
  + getChildCount(Match) double
  + getSumOfWeightedResult(List~Score~) double
  + getPerfectMatchedElement(List~Score~) List~Score~
}
class Token~T~ {
  - T value
  - Element element
   Element element
   T value
  + equals(Object) boolean
  + hashCode() int
  + toString() String
  + Token(T, Element) 
}
class TokenRange {
  - getLower(Number, double, Double) Number
  - getHigher(Number, double, Double) Number
  ~ TokenRange(Token, double, Double) 
  ~ TokenRange(Token, double) 
}
class TokenRepo {
  + put(Token) void
  + get(Token) Set~Element~
  + TokenRepo() 
}
class TokenizerFunction {
  + chainTokenizers(Function~Element~String~, Stream~Token~String~~~[]) Function~Element~String~, Stream~Token~String~~~
  + wordTokenizer() Function~Element~String~, Stream~Token~String~~~
  + wordSoundexEncodeTokenizer() Function~Element~String~, Stream~Token~String~~~
  + getNGramTokens(int, Element) Stream~Token~String~~
  + decaGramTokenizer() Function~Element~String~, Stream~Token~String~~~
  + triGramTokenizer() Function~Element~String~, Stream~Token~String~~~
  + valueTokenizer() Function~Element, Stream~Token~~
  + TokenizerFunction() 
}
class Utils {
  + getNGrams(String, int) Stream~String~
  + getNormalizedString(String, Map~String, String~) String
  + isNumeric(String) boolean
  + Utils() 
}

Document  -->  Builder 
Element~T~  -->  Builder~T~ 
TokenRepo  -->  Repo 
TokenRepo  -->  TokenRange 
```