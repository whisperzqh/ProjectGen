```mermaid
classDiagram
direction BT
class Builder {
  + build() JSONPointer
  + append(String) Builder
  + append(int) Builder
  + Builder() 
}
class CDL {
  + toString(JSONArray, JSONArray, char) String
  - getValue(JSONTokener, char) String?
  + toJSONArray(JSONArray, JSONTokener) JSONArray
  + rowToJSONArray(JSONTokener, char) JSONArray?
  + rowToJSONObject(JSONArray, JSONTokener, char) JSONObject?
  + toJSONArray(String, char) JSONArray
  + toString(JSONArray, char) String?
  + rowToJSONObject(JSONArray, JSONTokener) JSONObject
  + toJSONArray(JSONArray, String) JSONArray
  + toString(JSONArray, JSONArray) String
  + rowToString(JSONArray, char) String
  + toJSONArray(String) JSONArray
  + toJSONArray(JSONArray, JSONTokener, char) JSONArray
  + toString(JSONArray) String
  + toJSONArray(JSONTokener) JSONArray
  + rowToString(JSONArray) String
  + toJSONArray(JSONTokener, char) JSONArray
  + toJSONArray(JSONArray, String, char) JSONArray
  + rowToJSONArray(JSONTokener) JSONArray
  + CDL() 
}
class Cookie {
  + toString(JSONObject) String
  + unescape(String) String
  + toJSONObject(String) JSONObject
  + escape(String) String
  + Cookie() 
}
class CookieList {
  + toJSONObject(String) JSONObject
  + toString(JSONObject) String
  + CookieList() 
}
class HTTP {
  + toJSONObject(String) JSONObject
  + toString(JSONObject) String
  + HTTP() 
}
class HTTPTokener {
  + nextToken() String
  + HTTPTokener(String) 
}
class JSONArray {
   boolean empty
  + put(int, Map~?, ?~) JSONArray
  + isNull(int) boolean
  + put(float) JSONArray
  + put(long) JSONArray
  + optJSONArray(int, JSONArray) JSONArray
  + optInt(int) int
  + put(int, double) JSONArray
  + optFloatObject(int) Float
  + optEnum(Class~E~, int, E) E
  + optBooleanObject(int, Boolean) Boolean
  + getJSONArray(int) JSONArray
  - checkForSyntaxError(JSONTokener, JSONParserConfiguration, boolean) boolean
  + optJSONArray(int) JSONArray
  - isSimilar(Object, Object) boolean
  + optDouble(int, double) double
  + optEnum(Class~E~, int) E
  + optLong(int) long
  + optLongObject(int) Long
  + putAll(Collection~?~) JSONArray
  + put(Object) JSONArray
  + optString(int, String) String
  + put(int, int) JSONArray
  + similar(Object) boolean
  + optDoubleObject(int) Double
  + optBooleanObject(int) Boolean
  + query(String) Object
  + optDoubleObject(int, Double) Double
  + toString(int) String
  - addAll(Collection~?~, boolean, int, JSONParserConfiguration) void
  + toList() List~Object~
  + put(boolean) JSONArray
  + optDouble(int) double
  + getFloat(int) float
  + optFloat(int) float
  - addAll(Object, boolean, int, JSONParserConfiguration) void
  + getEnum(Class~E~, int) E
  + put(double) JSONArray
  - addAll(Object, boolean) void
  + optLong(int, long) long
  + opt(int) Object
  + optFloat(int, float) float
  + optNumber(int) Number
  + putAll(Object) JSONArray
  + put(int, float) JSONArray
  + get(int) Object
  + getBigInteger(int) BigInteger
  + putAll(JSONArray) JSONArray
  + put(int, long) JSONArray
  - wrongValueFormatException(int, String, Object, Throwable) JSONException
  + getNumber(int) Number
  + optQuery(JSONPointer) Object
  + remove(int) Object
  + put(Map~?, ?~) JSONArray
  + getInt(int) int
  + put(int, Object) JSONArray
  + getJSONObject(int) JSONObject
  + length() int
  + optFloatObject(int, Float) Float
  + optJSONObject(int, JSONObject) JSONObject
  + getBigDecimal(int) BigDecimal
  + getLong(int) long
  + getDouble(int) double
  + optNumber(int, Number) Number
  + query(JSONPointer) Object
  - addAll(Object, boolean, int) void
  + optBoolean(int, boolean) boolean
  + optBigInteger(int, BigInteger) BigInteger
  + put(int, boolean) JSONArray
  + put(int, Collection~?~) JSONArray
  - addAll(Iterable~?~, boolean) void
  + join(String) String
  + optQuery(String) Object
  + toJSONObject(JSONArray) JSONObject
  + clear() void
  + getBoolean(int) boolean
  + optJSONObject(int) JSONObject
  + optIntegerObject(int, Integer) Integer
  + write(Writer, int, int) Writer
  + write(Writer) Writer
  + putAll(Iterable~?~) JSONArray
  + getString(int) String
  + optString(int) String
  + optBigDecimal(int, BigDecimal) BigDecimal
  + optInt(int, int) int
  + optLongObject(int, Long) Long
  + iterator() Iterator~Object~
  + optBoolean(int) boolean
  + toString() String
  + put(Collection~?~) JSONArray
  + put(int, Map~?, ?~, JSONParserConfiguration) JSONArray
  + optIntegerObject(int) Integer
  + put(int) JSONArray
  - writeArrayAttempt(Writer, int, int, int) void
  + JSONArray(Collection~?~) 
  + JSONArray(JSONArray) 
  ~ JSONArray(Collection~?~, int, JSONParserConfiguration) 
  + JSONArray(Object) 
  + JSONArray(JSONTokener) 
  + JSONArray(String, JSONParserConfiguration) 
  + JSONArray(int) 
  + JSONArray(JSONTokener, JSONParserConfiguration) 
  + JSONArray(Collection~?~, JSONParserConfiguration) 
  + JSONArray(String) 
  + JSONArray() 
  + JSONArray(Iterable~?~) 
}
class JSONException {
  + JSONException(String, Throwable) 
  + JSONException(Throwable) 
  + JSONException(String) 
}
class JSONML {
  - parse(XMLTokener, boolean, JSONArray, JSONMLParserConfiguration, int) Object
  + toJSONObject(XMLTokener) JSONObject
  - parse(XMLTokener, boolean, JSONArray, boolean, int) Object
  + toJSONObject(String, JSONMLParserConfiguration) JSONObject
  + toJSONObject(String, boolean) JSONObject
  + toJSONArray(String) JSONArray
  + toJSONArray(String, boolean) JSONArray
  + toJSONObject(String) JSONObject
  + toJSONArray(XMLTokener, JSONMLParserConfiguration) JSONArray
  + toString(JSONObject) String
  + toString(JSONArray) String
  + toJSONArray(XMLTokener, boolean) JSONArray
  + toJSONObject(XMLTokener, boolean) JSONObject
  + toJSONArray(String, JSONMLParserConfiguration) JSONArray
  + toJSONObject(XMLTokener, JSONMLParserConfiguration) JSONObject
  + toJSONArray(XMLTokener) JSONArray
  + JSONML() 
}
class JSONMLParserConfiguration {
  + withKeepStrings(boolean) JSONMLParserConfiguration
  + withMaxNestingDepth(int) JSONMLParserConfiguration
  # clone() JSONMLParserConfiguration
  # JSONMLParserConfiguration(boolean, int) 
  + JSONMLParserConfiguration() 
}
class JSONObject {
   Class~Map~ mapType
   boolean empty
  + optEnum(Class~E~, String, E) E
  + put(String, Map~?, ?~) JSONObject
  + put(String, int) JSONObject
  + fromJson(Class~T~) T
  + getNames(JSONObject) String[]?
  - getNumber(String, char) Number
  + getJSONArray(String) JSONArray
  + optLongObject(String) Long
  + query(String) Object
  - writeAsHex(Writer, char) void
  + optDouble(String) double
  + put(String, double) JSONObject
  + toString(int) String
  + optBigInteger(String, BigInteger) BigInteger
  - convertValue(Object, Type) Object
  - parseEndOfKeyValuePair(JSONTokener, JSONParserConfiguration, boolean) boolean
  - checkKeyForStrictMode(JSONTokener, JSONParserConfiguration, Object) void
  + optJSONArray(String) JSONArray
  + quote(String) String
  + put(String, Object) JSONObject
  + getBigDecimal(String) BigDecimal
  + optJSONObject(String, JSONObject) JSONObject
  - annotationValueNotEmpty(JSONPropertyName) boolean
  # entrySet() Set~Entry~String, Object~~
  + remove(String) Object
  - stringToEnum(Class~?~, String) E
  + write(Writer, int, int) Writer
  + get(String) Object
  + has(String) boolean
  + similar(Object) boolean
  + optNumber(String, Number) Number
  + numberToString(Number) String
  - checkObjectType(Object, Object) boolean
  + getJSONObject(String) JSONObject
  + putOpt(String, Object) JSONObject
  + optNumber(String) Number
  - processJsonStringToWriteValue(Writer, Object) void
  + optQuery(JSONPointer) Object
  - processNumberToWriteValue(Writer, Number) void
  - wrongValueFormatException(String, String, Object, Throwable) JSONException
  + optInt(String, int) int
  - populateMap(Object, JSONParserConfiguration) void
  + optJSONObject(String) JSONObject
  + fromJson(String, Class~T~) T
  + doubleToString(double) String
  + testValidity(Object) void
  + put(String, float) JSONObject
  + put(String, long) JSONObject
  + length() int
  + optString(String) String
  - getCollection(Class~?~) Collection
  - parseJSONObject(JSONTokener, JSONParserConfiguration, boolean) boolean
  + optBooleanObject(String, Boolean) Boolean
  ~ objectToBigDecimal(Object, BigDecimal) BigDecimal
  + optJSONArray(String, JSONArray) JSONArray
  - getAnnotationDepth(Method, Class~Annotation~) int
  - recursivelyDefinedObjectException(String) JSONException
  + optIntegerObject(String, Integer) Integer
  + increment(String) JSONObject
  + wrap(Object) Object
  + optBooleanObject(String) Boolean
  + optFloatObject(String, Float) Float
  - getMapTypes(Type) Type[]
  - getMethods(Class~?~) Method[]
  - getRawType(Type) Class~?~
  + optFloatObject(String) Float
  + optLong(String, long) long
  + valueToString(Object) String
  - isRecordStyleAccessor(String, Method) boolean
  + getBoolean(String) boolean
  + getNames(Object) String[]
  + clear() void
  - fromJsonArray(JSONArray, Class~?~, Type) Collection~T~
  + optFloat(String) float
  - getAnnotation(Method, Class~A~) A
  ~ objectToBigDecimal(Object, BigDecimal, boolean) BigDecimal
  + toString() String
  + keys() Iterator~String~
  + optBoolean(String, boolean) boolean
  ~ writeValue(Writer, Object, int, int) Writer
  - getElementType(Type) Type
  + getInt(String) int
  - getKeyNameFromMethod(Method, boolean) String?
  - writeContent(Writer, int, int, boolean) void
  ~ objectToBigInteger(Object, BigInteger) BigInteger
  + optDouble(String, double) double
  + names() JSONArray
  - checkSimilarEntries(Object) boolean
  + write(Writer) Writer
  - convertToMap(JSONObject, Type, Type, Class~?~) Map~?, ?~
  + getLong(String) long
  ~ indent(Writer, int) void
  + putOnce(String, Object) JSONObject
  + quote(String, Writer) Writer
  # isDecimalNotation(String) boolean
  + optFloat(String, float) float
  - numberIsFinite(Number) boolean
  + optIntegerObject(String) Integer
  ~ isNumberSimilar(Number, Number) boolean
  + toJSONArray(JSONArray) JSONArray
  + optQuery(String) Object
  - isValidMethodName(String) boolean
  + getFloat(String) float
  + toMap() Map~String, Object~
  + accumulate(String, Object) JSONObject
  - closeClosable(Object) void
  + getBigInteger(String) BigInteger
  + optBigDecimal(String, BigDecimal) BigDecimal
  + optLong(String) long
  + optLongObject(String, Long) Long
  - populateMap(Object, Set~Object~, JSONParserConfiguration) void
  + put(String, Collection~?~) JSONObject
  + put(String, boolean) JSONObject
  - isRecordType(Class~?~) boolean
  + optString(String, String) String
  + query(JSONPointer) Object
  - wrap(Object, Set~Object~, int, JSONParserConfiguration) Object?
  + stringToValue(String) Object
  - wrap(Object, Set~Object~) Object
  + getString(String) String
  + keySet() Set~String~
  + opt(String) Object
  + optDoubleObject(String, Double) Double
  + optDoubleObject(String) Double
  ~ wrap(Object, int, JSONParserConfiguration) Object
  - checkForInvalidNumberFormat(String, char) void
  + optEnum(Class~E~, String) E
  # stringToNumber(String) Number
  + optInt(String) int
  + getEnum(Class~E~, String) E
  + isNull(String) boolean
  + getDouble(String) double
  + append(String, Object) JSONObject
  - isValidMethod(Method) boolean
  + optBoolean(String) boolean
  - processMethod(Object, Set~Object~, JSONParserConfiguration, Method, String) void
  - attemptWriteValue(Writer, int, int, Entry~String, ?~, String) void
  + getNumber(String) Number
  + JSONObject(Object, String[]) 
  + JSONObject(String, Locale) 
  - JSONObject(Object, Set~Object~) 
  + JSONObject(String, JSONParserConfiguration) 
  + JSONObject(JSONTokener, JSONParserConfiguration) 
  + JSONObject(Object, JSONParserConfiguration) 
  # JSONObject(int) 
  + JSONObject() 
  + JSONObject(JSONObject, String[]) 
  + JSONObject(Map~?, ?~, JSONParserConfiguration) 
  + JSONObject(String) 
  + JSONObject(Object) 
  + JSONObject(JSONTokener) 
  + JSONObject(Map~?, ?~) 
  - JSONObject(Map~?, ?~, int, JSONParserConfiguration) 
}
class JSONParserConfiguration {
  - boolean strictMode
  - boolean overwriteDuplicateKey
  - boolean useNativeNulls
   boolean overwriteDuplicateKey
   boolean strictMode
   boolean useNativeNulls
  + withOverwriteDuplicateKey(boolean) JSONParserConfiguration
  + withStrictMode() JSONParserConfiguration
  + withStrictMode(boolean) JSONParserConfiguration
  # clone() JSONParserConfiguration
  + withMaxNestingDepth(int) JSONParserConfiguration
  + withUseNativeNulls(boolean) JSONParserConfiguration
  + JSONParserConfiguration() 
}
class JSONPointer {
  + builder() Builder
  + toString() String
  - readByIndexToken(Object, String) Object
  + toURIFragment() String
  + queryFrom(Object) Object
  - unescape(String) String
  - escape(String) String
  + JSONPointer(String) 
  + JSONPointer(List~String~) 
}
class JSONPointerException {
  + JSONPointerException(String) 
  + JSONPointerException(String, Throwable) 
}
class JSONPropertyIgnore
class JSONPropertyName {
  + value() String
}
class JSONString {
<<Interface>>
  + toJSONString() String
}
class JSONStringer {
  + toString() String
  + JSONStringer() 
}
class JSONTokener {
  - char previous
  - JSONParserConfiguration jsonParserConfiguration
   char previous
   JSONParserConfiguration jsonParserConfiguration
  - decrementIndexes() void
  + nextClean() char
  + syntaxError(String) JSONException
  + nextTo(String) String
  + nextString(char) String
  + next(int) String
  - incrementIndexes(int) void
  + close() void
  + next(char) char
  + syntaxError(String, Throwable) JSONException
  ~ nextSimpleValue(char) Object
  + nextTo(char) String
  + dehexchar(char) int
  + nextValue() Object
  + skipTo(char) char
  + back() void
  + next() char
  + end() boolean
  + toString() String
  + more() boolean
  + JSONTokener(String) 
  + JSONTokener(String, JSONParserConfiguration) 
  + JSONTokener(InputStream, JSONParserConfiguration) 
  + JSONTokener(InputStream) 
  + JSONTokener(Reader) 
  + JSONTokener(Reader, JSONParserConfiguration) 
}
class JSONWriter {
  + valueToString(Object) String
  - append(String) JSONWriter
  + key(String) JSONWriter
  - end(char, char) JSONWriter
  + value(long) JSONWriter
  + value(boolean) JSONWriter
  - pop(char) void
  + value(Object) JSONWriter
  + array() JSONWriter
  - push(JSONObject) void
  + endArray() JSONWriter
  + value(double) JSONWriter
  + endObject() JSONWriter
  + object() JSONWriter
  + JSONWriter(Appendable) 
}
class Null {
  + hashCode() int
  + toString() String
  + equals(Object) boolean
  + Null() 
}
class ParserConfiguration {
  # int maxNestingDepth
  # boolean keepStrings
   int maxNestingDepth
   boolean keepStrings
  # clone() ParserConfiguration
  + withMaxNestingDepth(int) T
  + withKeepStrings(boolean) T
  # ParserConfiguration(boolean, int) 
  + ParserConfiguration() 
}
class Property {
  + toJSONObject(Properties) JSONObject
  + toProperties(JSONObject) Properties
  + Property() 
}
class StringBuilderWriter {
  + write(char[], int, int) void
  + write(String, int, int) void
  + append(CharSequence, int, int) StringBuilderWriter
  + write(String) void
  + append(CharSequence) StringBuilderWriter
  + append(char) StringBuilderWriter
  + flush() void
  + toString() String
  + close() void
  + write(int) void
  + StringBuilderWriter(int) 
  + StringBuilderWriter() 
}
class XML {
  - isDecimalNotation(String) boolean
  - stringToNumber(String) Number
  + noSpace(String) void
  + toJSONObject(Reader, boolean) JSONObject
  + stringToValue(String) Object
  + toString(Object) String
  + stringToValue(String, XMLXsiTypeConverter~?~) Object
  + toJSONObject(String, boolean, boolean) JSONObject
  + toString(Object, String, XMLParserConfiguration) String
  + toString(Object, String, int) String
  - indent(int) String
  + toJSONObject(Reader, XMLParserConfiguration) JSONObject
  + toString(Object, String) String
  - codePointIterator(String) Iterable~Integer~
  - parse(XMLTokener, JSONObject, String, XMLParserConfiguration, int) boolean
  - isStringAllWhiteSpace(String) boolean
  - toString(Object, String, XMLParserConfiguration, int, int) String
  + toJSONObject(String) JSONObject
  - mustEscape(int) boolean
  + escape(String) String
  + toString(Object, String, XMLParserConfiguration, int) String
  + toJSONObject(String, boolean) JSONObject
  + toString(Object, int) String
  + toJSONObject(Reader, boolean, boolean) JSONObject
  + unescape(String) String
  + toJSONObject(Reader) JSONObject
  + toJSONObject(String, XMLParserConfiguration) JSONObject
  - removeEmpty(JSONObject, XMLParserConfiguration) void
  + XML() 
}
class XMLParserConfiguration {
  - boolean keepBooleanAsString
  - Set~String~ forceList
  - boolean keepNumberAsString
  - boolean convertNilAttributeToNull
  - String cDataTagName
  - Map~String, XMLXsiTypeConverter~?~~ xsiTypeMap
  - boolean closeEmptyTag
   Set~String~ forceList
   boolean keepNumberAsString
   Map~String, XMLXsiTypeConverter~?~~ xsiTypeMap
   String cDataTagName
   boolean convertNilAttributeToNull
   boolean closeEmptyTag
   boolean keepBooleanAsString
  + withcDataTagName(String) XMLParserConfiguration
  + withKeepStrings(boolean) XMLParserConfiguration
  + withConvertNilAttributeToNull(boolean) XMLParserConfiguration
  + withXsiTypeMap(Map~String, XMLXsiTypeConverter~?~~) XMLParserConfiguration
  + withShouldTrimWhitespace(boolean) XMLParserConfiguration
  + withForceList(Set~String~) XMLParserConfiguration
  # clone() XMLParserConfiguration
  + withKeepBooleanAsString(boolean) XMLParserConfiguration
  + shouldTrimWhiteSpace() boolean
  + withKeepNumberAsString(boolean) XMLParserConfiguration
  + withMaxNestingDepth(int) XMLParserConfiguration
  + withCloseEmptyTag(boolean) XMLParserConfiguration
  - XMLParserConfiguration(boolean, String, boolean, Map~String, XMLXsiTypeConverter~?~~, Set~String~, int, boolean, boolean, boolean) 
  + XMLParserConfiguration(boolean, String) 
  + XMLParserConfiguration(boolean) 
  + XMLParserConfiguration(boolean, String, boolean) 
  + XMLParserConfiguration() 
  + XMLParserConfiguration(String) 
}
class XMLTokener {
  + nextToken() Object
  + nextContent() Object
  + nextEntity(char) Object
  + nextMeta() Object
  + nextCDATA() String
  + skipPast(String) void
  ~ unescapeEntity(String) String
  + XMLTokener(String) 
  + XMLTokener(Reader) 
  + XMLTokener(Reader, XMLParserConfiguration) 
}
class XMLXsiTypeConverter~T~ {
<<Interface>>
  + convert(String) T
}

JSONPointer  -->  Builder 
JSONObject  -->  Null 

```