# Architecture Design

Below is a text-based representation of the file tree.
```bash
└── src
    ├── main
    │   └── java
    │       └── org
    │           └── json
    │               ├── CDL.java
    │               ├── Cookie.java
    │               ├── CookieList.java
    │               ├── HTTP.java
    │               ├── HTTPTokener.java
    │               ├── JSONArray.java
    │               ├── JSONException.java
    │               ├── JSONML.java
    │               ├── JSONMLParserConfiguration.java
    │               ├── JSONObject.java
    │               ├── JSONParserConfiguration.java
    │               ├── JSONPointer.java
    │               ├── JSONPointerException.java
    │               ├── JSONPropertyIgnore.java
    │               ├── JSONPropertyName.java
    │               ├── JSONString.java
    │               ├── JSONStringer.java
    │               ├── JSONTokener.java
    │               ├── JSONWriter.java
    │               ├── ParserConfiguration.java
    │               ├── Property.java
    │               ├── StringBuilderWriter.java
    │               ├── XML.java
    │               ├── XMLParserConfiguration.java
    │               ├── XMLTokener.java
    │               └── XMLXsiTypeConverter.java
```

---

## API Documentation

`CDL.java`:

- `CDL`: Utility class for converting comma-delimited text (CSV) to JSONArray and vice versa.

  - `CDL() -> CDL` (Deprecated): Default constructor, utility class should not be instantiated.

  - `getValue(x: JSONTokener, delimiter: char) -> String` (Private): Extracts the next value from a tokenized CSV line, handling quoted values and empty fields.

  - `rowToJSONArray(x: JSONTokener) -> JSONArray`: Converts a single row of comma-delimited values into a JSONArray of strings.

  - `rowToJSONArray(x: JSONTokener, delimiter: char) -> JSONArray`: Converts a row with custom delimiter into JSONArray.

  - `rowToJSONObject(names: JSONArray, x: JSONTokener) -> JSONObject`: Converts a row into JSONObject using provided column names from a parallel JSONArray.

  - `rowToJSONObject(names: JSONArray, x: JSONTokener, delimiter: char) -> JSONObject`: Converts a row with custom delimiter into JSONObject using column names.

  - `rowToString(ja: JSONArray) -> String`: Converts a JSONArray into a comma-delimited string row, quoting values that contain special characters.

  - `rowToString(ja: JSONArray, delimiter: char) -> String`: Converts JSONArray to delimited string with custom delimiter.

  - `toJSONArray(string: String) -> JSONArray`: Converts entire CSV text to JSONArray of JSONObjects, using first row as column names.

  - `toJSONArray(string: String, delimiter: char) -> JSONArray`: Converts CSV with custom delimiter to JSONArray of JSONObjects.

  - `toJSONArray(x: JSONTokener) -> JSONArray`: Converts tokenized CSV to JSONArray of JSONObjects.

  - `toJSONArray(x: JSONTokener, delimiter: char) -> JSONArray`: Converts tokenized CSV with custom delimiter to JSONArray.

  - `toJSONArray(names: JSONArray, string: String) -> JSONArray`: Converts CSV using provided column names instead of first row.

  - `toJSONArray(names: JSONArray, string: String, delimiter: char) -> JSONArray`: Converts CSV with custom delimiter using provided column names.

  - `toJSONArray(names: JSONArray, x: JSONTokener) -> JSONArray`: Converts tokenized CSV using provided column names.

  - `toJSONArray(names: JSONArray, x: JSONTokener, delimiter: char) -> JSONArray`: Converts tokenized CSV with custom delimiter and provided names.

  - `toString(ja: JSONArray) -> String`: Converts JSONArray of JSONObjects into CSV text format.

  - `toString(ja: JSONArray, delimiter: char) -> String`: Converts JSONArray to CSV with custom delimiter.

  - `toString(ja: JSONArray, names: JSONArray) -> String`: Converts JSONArray to CSV using specific column names.

  - `toString(ja: JSONArray, names: JSONArray, delimiter: char) -> String`: Converts JSONArray to CSV with custom delimiter and column names.

---

`Cookie.java`:

- `Cookie`: Utility class for converting between web browser cookie strings and JSONObject representations.

  - `Cookie() -> Cookie` (Deprecated): Default constructor, utility class should not be instantiated.

  - `escape(string: String) -> String`: URL-encodes cookie values, escaping special characters (+, %, =, ;) and control characters to %hh format.

  - `toJSONObject(string: String) -> JSONObject`: Parses cookie specification string into JSONObject with "name", "value" and attribute properties.

  - `toString(jo: JSONObject) -> String`: Converts JSONObject containing cookie data into standard cookie specification string format.

  - `unescape(string: String) -> String`: Decodes URL-encoded cookie string, converting %hh sequences and + to original characters.

---

`CookieList.java`:

- `CookieList`: Utility class for converting between cookie list strings and JSONObject representations.

  - `CookieList() -> CookieList` (Deprecated): Default constructor, utility class should not be instantiated.

  - `toJSONObject(string: String) -> JSONObject`: Parses cookie list string (name=value pairs separated by semicolons) into JSONObject.

  - `toString(jo: JSONObject) -> String`: Converts JSONObject into cookie list string with semicolon-separated name=value pairs.

---

`HTTP.java`:

- `HTTP`: Utility class for converting between HTTP headers and JSONObject representations.

  - `HTTP() -> HTTP`: Default constructor for HTTP utility class.

  - `toJSONObject(string: String) -> JSONObject`: Parses HTTP request or response header string into JSONObject containing method/status and fields.

  - `toString(jo: JSONObject) -> String`: Converts JSONObject into properly formatted HTTP header string with CRLF line endings.

---

`HTTPTokener.java`:

- `HTTPTokener`: Specialized tokenizer extending JSONTokener for parsing HTTP header text.

  - `HTTPTokener(string: String) -> HTTPTokener`: Constructs HTTPTokener from HTTP header string source.

  - `nextToken() -> String`: Extracts next token from HTTP header, handling quoted strings and whitespace-delimited tokens.

---

`JSONArray.java`:

- `JSONArray`: Ordered sequence of JSON values, supporting get/put operations by index with type conversion methods. Implements Iterable<Object>.

  - `JSONArray() -> JSONArray`: Constructs empty JSONArray with default configuration.

  - `JSONArray(x: JSONTokener) -> JSONArray`: Parses JSONArray from JSONTokener using default configuration.

  - `JSONArray(x: JSONTokener, jsonParserConfiguration: JSONParserConfiguration) -> JSONArray`: Parses JSONArray from tokenizer with custom parser configuration for strict mode and nesting limits.

  - `checkForSyntaxError(x: JSONTokener, jsonParserConfiguration: JSONParserConfiguration, isInitial: boolean) -> boolean` (Private): Validates JSON syntax for commas and closing brackets according to strict mode rules.

  - `JSONArray(source: String) -> JSONArray`: Parses JSON array from string with default configuration.

  - `JSONArray(source: String, jsonParserConfiguration: JSONParserConfiguration) -> JSONArray`: Parses JSON array string with custom parser configuration.

  - `JSONArray(collection: Collection<?>) -> JSONArray`: Constructs JSONArray from Java Collection with default configuration.

  - `JSONArray(collection: Collection<?>, jsonParserConfiguration: JSONParserConfiguration) -> JSONArray`: Constructs from Collection with custom parser configuration.

  - `JSONArray(collection: Collection<?>, recursionDepth: int, jsonParserConfiguration: JSONParserConfiguration) -> JSONArray`: Internal constructor handling recursive object creation with depth limit enforcement.

  - `JSONArray(iter: Iterable<?>) -> JSONArray`: Shallow copy constructor from any Iterable collection.

  - `JSONArray(array: JSONArray) -> JSONArray`: Shallow copy constructor from another JSONArray.

  - `JSONArray(array: Object) -> JSONArray`: Constructs from Java primitive or object array, validating array type.

  - `JSONArray(initialCapacity: int) -> JSONArray`: Constructs empty JSONArray with specified initial capacity.

  - `iterator() -> Iterator<Object>`: Returns iterator over array elements for foreach loops.

  - `get(index: int) -> Object`: Retrieves object at index, throwing exception if not found.

  - `getBoolean(index: int) -> boolean`: Gets boolean value at index, converting string "true"/"false" if necessary.

  - `getDouble(index: int) -> double`: Gets numeric value as double, parsing strings if needed.

  - `getFloat(index: int) -> float`: Gets numeric value as float, parsing strings if needed.

  - `getNumber(index: int) -> Number`: Gets value as Number object, converting strings if possible.

  - `getEnum(clazz: Class<E>, index: int) -> E`: Gets enum value at index, converting from string name if necessary.

  - `getBigDecimal(index: int) -> BigDecimal`: Gets value as BigDecimal, using double constructor for floating-point values.

  - `getBigInteger(index: int) -> BigInteger`: Gets value as BigInteger, throwing exception if conversion fails.

  - `getInt(index: int) -> int`: Gets integer value at index, parsing strings if needed.

  - `getJSONArray(index: int) -> JSONArray`: Gets nested JSONArray at index, throwing exception if wrong type.

  - `getJSONObject(index: int) -> JSONObject`: Gets nested JSONObject at index, throwing exception if wrong type.

  - `getLong(index: int) -> long`: Gets long integer value at index, parsing strings if needed.

  - `getString(index: int) -> String`: Gets String value at index, throwing exception if null or wrong type.

  - `isNull(index: int) -> boolean`: Checks if value at index is JSON null or missing.

  - `join(separator: String) -> String`: Concatenates array elements into string with separator between each element.

  - `length() -> int`: Returns number of elements including nulls.

  - `clear() -> void`: Removes all elements from the array.

  - `opt(index: int) -> Object`: Gets optional value at index, returning null if out of bounds or missing.

  - `optBoolean(index: int) -> boolean`: Gets boolean at index with false as default if missing or unconvertible.

  - `optBoolean(index: int, defaultValue: boolean) -> boolean`: Gets boolean with custom default value.

  - `optBooleanObject(index: int) -> Boolean`: Gets Boolean object with false default if missing.

  - `optBooleanObject(index: int, defaultValue: Boolean) -> Boolean`: Gets Boolean object with custom default.

  - `optDouble(index: int) -> double`: Gets double with NaN default if missing or unconvertible.

  - `optDouble(index: int, defaultValue: double) -> double`: Gets double with custom default value.

  - `optDoubleObject(index: int) -> Double`: Gets Double object with NaN default if missing.

  - `optDoubleObject(index: int, defaultValue: Double) -> Double`: Gets Double object with custom default.

  - `optFloat(index: int) -> float`: Gets float with NaN default if missing or unconvertible.

  - `optFloat(index: int, defaultValue: float) -> float`: Gets float with custom default value.

  - `optFloatObject(index: int) -> Float`: Gets Float object with NaN default if missing.

  - `optFloatObject(index: int, defaultValue: Float) -> Float`: Gets Float object with custom default.

  - `optInt(index: int) -> int`: Gets int with zero default if missing or unconvertible.

  - `optInt(index: int, defaultValue: int) -> int`: Gets int with custom default value.

  - `optIntegerObject(index: int) -> Integer`: Gets Integer object with zero default if missing.

  - `optIntegerObject(index: int, defaultValue: Integer) -> Integer`: Gets Integer object with custom default.

  - `optEnum(clazz: Class<E>, index: int) -> E`: Gets enum with null default if missing or invalid.

  - `optEnum(clazz: Class<E>, index: int, defaultValue: E) -> E`: Gets enum with custom default value.

  - `optBigInteger(index: int, defaultValue: BigInteger) -> BigInteger`: Gets BigInteger with custom default if unconvertible.

  - `optBigDecimal(index: int, defaultValue: BigDecimal) -> BigDecimal`: Gets BigDecimal with custom default if unconvertible.

  - `optJSONArray(index: int) -> JSONArray`: Gets optional nested JSONArray, returning null if missing or wrong type.

  - `optJSONArray(index: int, defaultValue: JSONArray) -> JSONArray`: Gets JSONArray with custom default.

  - `optJSONObject(index: int) -> JSONObject`: Gets optional nested JSONObject, returning null if missing or wrong type.

  - `optJSONObject(index: int, defaultValue: JSONObject) -> JSONObject`: Gets JSONObject with custom default.

  - `optLong(index: int) -> long`: Gets long with zero default if missing or unconvertible.

  - `optLong(index: int, defaultValue: long) -> long`: Gets long with custom default value.

  - `optLongObject(index: int) -> Long`: Gets Long object with zero default if missing.

  - `optLongObject(index: int, defaultValue: Long) -> Long`: Gets Long object with custom default.

  - `optNumber(index: int) -> Number`: Gets Number with null default if missing or unconvertible.

  - `optNumber(index: int, defaultValue: Number) -> Number`: Gets Number with custom default.

  - `optString(index: int) -> String`: Gets String with empty string default if missing.

  - `optString(index: int, defaultValue: String) -> String`: Gets String with custom default.

  - `put(value: boolean) -> JSONArray`: Appends boolean value to end of array.

  - `put(value: Collection<?>) -> JSONArray`: Appends Collection as nested array to end.

  - `put(value: double) -> JSONArray`: Appends double value, validating it's finite.

  - `put(value: float) -> JSONArray`: Appends float value, validating it's finite.

  - `put(value: int) -> JSONArray`: Appends int value to end of array.

  - `put(value: long) -> JSONArray`: Appends long value to end of array.

  - `put(value: Map<?, ?>) -> JSONArray`: Appends Map as nested JSONObject to end.

  - `put(value: Object) -> JSONArray`: Appends arbitrary object, wrapping complex types appropriately.

  - `put(index: int, value: boolean) -> JSONArray`: Sets boolean value at specific index, expanding array if needed.

  - `put(index: int, value: Collection<?>) -> JSONArray`: Sets Collection as nested array at index.

  - `put(index: int, value: double) -> JSONArray`: Sets double value at index, validating finite.

  - `put(index: int, value: float) -> JSONArray`: Sets float value at index, validating finite.

  - `put(index: int, value: int) -> JSONArray`: Sets int value at specific index.

  - `put(index: int, value: long) -> JSONArray`: Sets long value at specific index.

  - `put(index: int, value: Map<?, ?>) -> JSONArray`: Sets Map as JSONObject at index.

  - `put(index: int, value: Object) -> JSONArray`: Sets arbitrary object at index, wrapping if needed.

  - `putAll(collection: Collection<?>) -> JSONArray`: Appends all elements from Collection to end.

  - `putAll(iter: Iterable<?>) -> JSONArray`: Appends all elements from Iterable to end.

  - `putAll(array: JSONArray) -> JSONArray`: Appends all elements from another JSONArray.

  - `putAll(array: Object) -> JSONArray`: Appends all elements from Java array.

  - `addAll(collection: Collection<?>, wrap: boolean) -> void` (Private): Internal method to add collection elements with optional wrapping.

  - `addAll(collection: Collection<?>, wrap: boolean, recursionDepth: int, jsonParserConfiguration: JSONParserConfiguration) -> void` (Private): Adds collection with recursion depth tracking.

  - `addAll(iter: Iterable<?>, wrap: boolean) -> void` (Private): Adds iterable elements with optional wrapping.

  - `addAll(array: Object, wrap: boolean, recursionDepth: int) -> void` (Private): Adds Java array elements with recursion tracking.

  - `query(jsonPointer: String) -> Object`: Evaluates RFC 6901 JSON Pointer string on this array.

  - `query(jsonPointer: JSONPointer) -> Object`: Evaluates JSONPointer object on this array.

  - `optQuery(jsonPointer: String) -> Object`: Optional JSON Pointer query returning null on error instead of exception.

  - `optQuery(jsonPointer: JSONPointer) -> Object`: Optional query with JSONPointer object.

  - `remove(index: int) -> Object`: Removes and returns element at index, or null if out of bounds.

  - `similar(other: Object) -> boolean`: Deep comparison checking structural similarity with another JSONArray.

  - `toJSONObject(names: JSONArray) -> JSONObject`: Creates JSONObject using this array's values and provided keys.

  - `toString() -> String`: Converts to compact JSON string representation.

  - `toString(indentFactor: int) -> String`: Converts to pretty-printed JSON string with specified indentation.

  - `write(writer: Writer) -> Writer`: Writes compact JSON to Writer without newlines.

  - `write(writer: Writer, indentFactor: int, indent: int) -> Writer`: Writes formatted JSON with indentation control.

  - `toList() -> List<Object>`: Converts to Java List, recursively converting nested structures.

  - `isEmpty() -> boolean`: Checks if array contains no elements.

  - `addAll(collection: Collection<?>) -> void`: Adds all elements from Collection without wrapping.

  - `addAll(index: int, collection: Collection<?>) -> void`: Inserts collection elements at specific index.

  - `wrongValueFormatException(idx: int, valueType: String, value: Object, cause: Throwable) -> JSONException` (Static): Creates formatted exception for type conversion failures.

---

`JSONException.java`:

- `JSONException`: Runtime exception thrown by JSON.org classes when parsing or processing errors occur.

  - `JSONException(message: String) -> JSONException`: Constructs exception with descriptive error message.

  - `JSONException(message: String, cause: Throwable) -> JSONException`: Constructs exception with message and underlying cause.

  - `JSONException(cause: Throwable) -> JSONException`: Constructs exception wrapping another throwable as cause.

---

`JSONML.java`:

- `JSONML`: Utility class for converting between XML and JSON using the JsonML transform format.

  - `JSONML() -> JSONML` (Deprecated): Default constructor, utility class should not be instantiated.

  - `parse(x: XMLTokener, arrayForm: boolean, ja: JSONArray, keepStrings: boolean, currentNestingDepth: int) -> Object` (Private): Internal parser converting XML to JSONArray or JSONObject with string preservation option.

  - `parse(x: XMLTokener, arrayForm: boolean, ja: JSONArray, config: JSONMLParserConfiguration, currentNestingDepth: int) -> Object` (Private): Enhanced parser using configuration object for parsing behavior control.

  - `toJSONArray(string: String) -> JSONArray`: Converts XML string to JSONArray using JsonML array form representation.

  - `toJSONArray(string: String, keepStrings: boolean) -> JSONArray`: Converts XML to JSONArray, optionally preserving all values as strings without type conversion.

  - `toJSONArray(string: String, config: JSONMLParserConfiguration) -> JSONArray`: Converts XML to JSONArray using custom parser configuration.

  - `toJSONArray(x: XMLTokener, config: JSONMLParserConfiguration) -> JSONArray`: Converts XML from tokenizer to JSONArray with configuration.

  - `toJSONArray(x: XMLTokener, keepStrings: boolean) -> JSONArray`: Converts tokenized XML to JSONArray with string preservation option.

  - `toJSONArray(x: XMLTokener) -> JSONArray`: Converts tokenized XML to JSONArray with default configuration.

  - `toJSONObject(string: String) -> JSONObject`: Converts XML string to JSONObject using JsonML object form with tagName properties.

  - `toJSONObject(string: String, keepStrings: boolean) -> JSONObject`: Converts XML to JSONObject with optional string preservation.

  - `toJSONObject(string: String, config: JSONMLParserConfiguration) -> JSONObject`: Converts XML to JSONObject using custom configuration.

  - `toJSONObject(x: XMLTokener, config: JSONMLParserConfiguration) -> JSONObject`: Converts tokenized XML to JSONObject with configuration.

  - `toJSONObject(x: XMLTokener, keepStrings: boolean) -> JSONObject`: Converts tokenized XML to JSONObject with string preservation.

  - `toJSONObject(x: XMLTokener) -> JSONObject`: Converts tokenized XML to JSONObject with default settings.

  - `toString(ja: JSONArray) -> String`: Converts JSONArray in JsonML format back to XML string.

  - `toString(jo: JSONObject) -> String`: Converts JSONObject in JsonML format back to XML string.

---

`JSONMLParserConfiguration.java`:

- `JSONMLParserConfiguration`: Immutable configuration object for XML to JSONML parser, extending ParserConfiguration.

  - `JSONMLParserConfiguration() -> JSONMLParserConfiguration`: Creates default configuration with type conversion enabled.

  - `JSONMLParserConfiguration(keepStrings: boolean, maxNestingDepth: int) -> JSONMLParserConfiguration` (Protected): Internal constructor for creating configured instances.

  - `clone() -> JSONMLParserConfiguration` (Protected): Creates deep copy of configuration for immutable modifications.

  - `withKeepStrings(newVal: boolean) -> JSONMLParserConfiguration`: Returns new configuration with keepStrings setting modified.

  - `withMaxNestingDepth(maxNestingDepth: int) -> JSONMLParserConfiguration`: Returns new configuration with modified nesting depth limit.

---

`JSONObject.java`:

- `JSONObject`: Unordered collection of name-value pairs representing JSON objects with comprehensive type-safe accessor methods.

  - `JSONObject() -> JSONObject`: Constructs empty JSONObject with default configuration.

  - `JSONObject(jo: JSONObject, names: String...) -> JSONObject`: Creates JSONObject subset containing only specified keys from source.

  - `JSONObject(x: JSONTokener) -> JSONObject`: Parses JSONObject from tokenizer with default configuration.

  - `JSONObject(x: JSONTokener, jsonParserConfiguration: JSONParserConfiguration) -> JSONObject`: Parses from tokenizer with custom parser configuration for strict mode and duplicate key handling.

  - `JSONObject(m: Map<?, ?>) -> JSONObject`: Constructs from Java Map, recursively converting nested structures.

  - `JSONObject(m: Map<?, ?>, jsonParserConfiguration: JSONParserConfiguration) -> JSONObject`: Constructs from Map with custom configuration.

  - `JSONObject(bean: Object) -> JSONObject`: Constructs from Java bean using reflection to extract public getters.

  - `JSONObject(bean: Object, jsonParserConfiguration: JSONParserConfiguration) -> JSONObject`: Constructs from bean with custom configuration.

  - `JSONObject(object: Object, names: String[]) -> JSONObject`: Constructs from object fields specified by name array.

  - `JSONObject(source: String) -> JSONObject`: Parses JSON object from string with default configuration.

  - `JSONObject(source: String, jsonParserConfiguration: JSONParserConfiguration) -> JSONObject`: Parses from string with custom configuration.

  - `JSONObject(baseName: String, locale: Locale) -> JSONObject`: Constructs from ResourceBundle for internationalization.

  - `JSONObject(recursionDepth: int, jsonParserConfiguration: JSONParserConfiguration) -> JSONObject` (Protected): Internal constructor with recursion tracking for nested object creation.

  - `accumulate(key: String, value: Object) -> JSONObject`: Appends value to existing key, creating array if key already exists with value.

  - `append(key: String, value: Object) -> JSONObject`: Appends value to JSONArray under key, creating array if necessary.

  - `clear() -> void`: Removes all key-value pairs from the object.

  - `get(key: String) -> Object`: Retrieves value for key, throwing exception if key doesn't exist.

  - `getEnum(clazz: Class<E>, key: String) -> E`: Gets enum value for key, converting from string if necessary.

  - `getBoolean(key: String) -> boolean`: Gets boolean value, converting string "true"/"false" if needed.

  - `getBigInteger(key: String) -> BigInteger`: Gets value as BigInteger, throwing exception if conversion fails.

  - `getBigDecimal(key: String) -> BigDecimal`: Gets value as BigDecimal, using double constructor for floats.

  - `getDouble(key: String) -> double`: Gets numeric value as double, parsing strings if possible.

  - `getFloat(key: String) -> float`: Gets numeric value as float, parsing strings if possible.

  - `getNumber(key: String) -> Number`: Gets value as Number object, converting strings if needed.

  - `getInt(key: String) -> int`: Gets integer value, parsing strings if necessary.

  - `getJSONArray(key: String) -> JSONArray`: Gets nested JSONArray value, throwing exception if wrong type.

  - `getJSONObject(key: String) -> JSONObject`: Gets nested JSONObject value, throwing exception if wrong type.

  - `getLong(key: String) -> long`: Gets long integer value, parsing strings if needed.

  - `getString(key: String) -> String`: Gets String value, throwing exception if null or missing.

  - `getMapType() -> Class<? extends Map>`: Returns runtime class of underlying Map implementation.

  - `has(key: String) -> boolean`: Checks if key exists in object regardless of value.

  - `increment(key: String) -> JSONObject`: Increments numeric value by 1, initializing to 1 if missing or creating array if non-numeric.

  - `isNull(key: String) -> boolean`: Checks if key's value is JSON null or key is missing.

  - `isEmpty() -> boolean`: Checks if object contains no key-value pairs.

  - `iterator() -> Iterator<String>`: Returns iterator over key names.

  - `keySet() -> Set<String>`: Returns set view of all keys.

  - `length() -> int`: Returns number of key-value pairs.

  - `names() -> JSONArray`: Returns JSONArray containing all key names, or null if empty.

  - `opt(key: String) -> Object`: Gets optional value, returning null if key doesn't exist.

  - `optEnum(clazz: Class<E>, key: String) -> E`: Gets enum with null default if missing or invalid.

  - `optEnum(clazz: Class<E>, key: String, defaultValue: E) -> E`: Gets enum with custom default value.

  - `optBoolean(key: String) -> boolean`: Gets boolean with false default if missing or unconvertible.

  - `optBoolean(key: String, defaultValue: boolean) -> boolean`: Gets boolean with custom default.

  - `optBooleanObject(key: String) -> Boolean`: Gets Boolean object with false default.

  - `optBooleanObject(key: String, defaultValue: Boolean) -> Boolean`: Gets Boolean object with custom default.

  - `optBigDecimal(key: String, defaultValue: BigDecimal) -> BigDecimal`: Gets BigDecimal with custom default if unconvertible.

  - `optBigInteger(key: String, defaultValue: BigInteger) -> BigInteger`: Gets BigInteger with custom default if unconvertible.

  - `optDouble(key: String) -> double`: Gets double with NaN default if missing or unconvertible.

  - `optDouble(key: String, defaultValue: double) -> double`: Gets double with custom default.

  - `optDoubleObject(key: String) -> Double`: Gets Double object with NaN default.

  - `optDoubleObject(key: String, defaultValue: Double) -> Double`: Gets Double object with custom default.

  - `optFloat(key: String) -> float`: Gets float with NaN default if missing or unconvertible.

  - `optFloat(key: String, defaultValue: float) -> float`: Gets float with custom default.

  - `optFloatObject(key: String) -> Float`: Gets Float object with NaN default.

  - `optFloatObject(key: String, defaultValue: Float) -> Float`: Gets Float object with custom default.

  - `optInt(key: String) -> int`: Gets int with zero default if missing or unconvertible.

  - `optInt(key: String, defaultValue: int) -> int`: Gets int with custom default.

  - `optIntegerObject(key: String) -> Integer`: Gets Integer object with zero default.

  - `optIntegerObject(key: String, defaultValue: Integer) -> Integer`: Gets Integer object with custom default.

  - `optJSONArray(key: String) -> JSONArray`: Gets optional JSONArray, returning null if missing or wrong type.

  - `optJSONArray(key: String, defaultValue: JSONArray) -> JSONArray`: Gets JSONArray with custom default.

  - `optJSONObject(key: String) -> JSONObject`: Gets optional JSONObject, returning null if missing or wrong type.

  - `optJSONObject(key: String, defaultValue: JSONObject) -> JSONObject`: Gets JSONObject with custom default.

  - `optLong(key: String) -> long`: Gets long with zero default if missing or unconvertible.

  - `optLong(key: String, defaultValue: long) -> long`: Gets long with custom default.

  - `optLongObject(key: String) -> Long`: Gets Long object with zero default.

  - `optLongObject(key: String, defaultValue: Long) -> Long`: Gets Long object with custom default.

  - `optNumber(key: String) -> Number`: Gets Number with null default if missing or unconvertible.

  - `optNumber(key: String, defaultValue: Number) -> Number`: Gets Number with custom default.

  - `optString(key: String) -> String`: Gets String with empty string default if missing.

  - `optString(key: String, defaultValue: String) -> String`: Gets String with custom default.

  - `put(key: String, value: boolean) -> JSONObject`: Sets boolean value for key, replacing existing value.

  - `put(key: String, value: Collection<?>) -> JSONObject`: Sets Collection as nested JSONArray for key.

  - `put(key: String, value: double) -> JSONObject`: Sets double value, validating it's finite.

  - `put(key: String, value: float) -> JSONObject`: Sets float value, validating it's finite.

  - `put(key: String, value: int) -> JSONObject`: Sets int value for key.

  - `put(key: String, value: long) -> JSONObject`: Sets long value for key.

  - `put(key: String, value: Map<?, ?>) -> JSONObject`: Sets Map as nested JSONObject for key.

  - `put(key: String, value: Object) -> JSONObject`: Sets arbitrary object value, wrapping complex types appropriately.

  - `putOnce(key: String, value: Object) -> JSONObject`: Sets value only if key doesn't already exist, throwing exception on duplicate.

  - `putOpt(key: String, value: Object) -> JSONObject`: Sets value only if both key and value are non-null, otherwise no-op.

  - `query(jsonPointer: String) -> Object`: Evaluates RFC 6901 JSON Pointer string to retrieve nested value.

  - `query(jsonPointer: JSONPointer) -> Object`: Evaluates JSONPointer object to retrieve nested value.

  - `optQuery(jsonPointer: String) -> Object`: Optional pointer query returning null on error instead of exception.

  - `optQuery(jsonPointer: JSONPointer) -> Object`: Optional query with JSONPointer object.

  - `remove(key: String) -> Object`: Removes key and returns its value, or null if key doesn't exist.

  - `similar(other: Object) -> boolean`: Deep comparison checking structural similarity with another JSONObject.

  - `toJSONArray(names: JSONArray) -> JSONArray`: Creates JSONArray using specified keys as indices for values.

  - `toMap() -> Map<String, Object>`: Converts to Java Map, recursively converting nested JSON structures.

  - `toString() -> String`: Converts to compact JSON string representation without whitespace.

  - `toString(indentFactor: int) -> String`: Converts to pretty-printed JSON string with specified indentation.

  - `write(writer: Writer) -> Writer`: Writes compact JSON to Writer.

  - `write(writer: Writer, indentFactor: int, indent: int) -> Writer`: Writes formatted JSON with indentation control.

  - `toBean(clazz: Class<T>) -> T`: Deserializes JSONObject to instance of specified Java class using reflection.

  - `doubleToString(d: double) -> String` (Static): Converts double to JSON-compatible string, handling special values.

  - `getNames(jo: JSONObject) -> String[]` (Static): Extracts sorted array of all keys from JSONObject.

  - `getNames(object: Object) -> String[]` (Static): Extracts public field names from object using reflection.

  - `numberToString(number: Number) -> String` (Static): Converts Number to JSON string, validating finite values.

  - `quote(string: String) -> String` (Static): Wraps string in quotes and escapes special characters for JSON.

  - `quote(string: String, w: Writer) -> Writer` (Static): Quotes string directly to Writer for efficient serialization.

  - `stringToValue(string: String) -> Object` (Static): Attempts to convert string to appropriate type (boolean, number, or string).

  - `stringToNumber(val: String) -> Number` (Static): Parses string to most appropriate Number type (Integer, Long, Double, or BigInteger).

  - `testValidity(o: Object) -> void` (Static): Validates object is suitable for JSON, checking for infinite/NaN numbers.

  - `valueToString(value: Object) -> String` (Static): Converts arbitrary value to JSON string representation.

  - `wrap(object: Object) -> Object` (Static): Wraps Java object in appropriate JSON type (JSONObject, JSONArray, or primitive).

  - `wrap(object: Object, objectsRecord: Set<Object>) -> Object` (Static): Internal wrap with cycle detection using object record set.

  - `objectToBigDecimal(val: Object, defaultValue: BigDecimal) -> BigDecimal` (Static): Converts value to BigDecimal with fallback default.

  - `objectToBigInteger(val: Object, defaultValue: BigInteger) -> BigInteger` (Static): Converts value to BigInteger with fallback default.

  - `toBean(clazz: Class<T>, jo: JSONObject) -> T` (Static): Static deserialization method creating bean from JSONObject.

  - `wrongValueFormatException(key: String, valueType: String, cause: Throwable) -> JSONException` (Static): Creates formatted exception for type conversion failures.

  - `wrongValueFormatException(key: String, valueType: String, value: Object, cause: Throwable) -> JSONException` (Static): Creates exception with actual value included in message.

  - `recursivelyDefinedObjectException(key: String) -> JSONException` (Static): Creates exception for circular reference detection.

---

`JSONParserConfiguration.java`:

- `JSONParserConfiguration`: Immutable configuration for JSON parser controlling duplicate key handling, null values, and strict mode.

  - `JSONParserConfiguration() -> JSONParserConfiguration`: Creates default configuration with lenient mode and no native nulls.

  - `withMaxNestingDepth(maxNestingDepth: int) -> JSONParserConfiguration`: Returns new configuration with modified maximum nesting depth limit.

  - `withDuplicateKeyException() -> JSONParserConfiguration`: Returns configuration that throws exceptions on duplicate keys in JSON objects.

  - `withNativeNull() -> JSONParserConfiguration`: Returns configuration that preserves null values instead of converting to JSONObject.NULL.

  - `withStrictMode() -> JSONParserConfiguration`: Returns configuration enabling strict JSON parsing according to RFC specifications.

  - `withStrictMode(strictMode: boolean) -> JSONParserConfiguration`: Returns configuration with strict mode explicitly set.

  - `isThrowDuplicateKeyException() -> boolean`: Returns whether parser throws exceptions on encountering duplicate keys.

  - `isNativeNull() -> boolean`: Returns whether parser preserves native Java null instead of using JSONObject.NULL.

  - `isStrictMode() -> boolean`: Returns whether strict parsing mode is enabled for JSON syntax validation.

---

`JSONPointer.java`:

- `JSONPointer`: RFC 6901 implementation for navigating and querying JSON documents using pointer syntax.

  - `JSONPointer(pointer: String) -> JSONPointer`: Constructs JSONPointer from RFC 6901 pointer string (e.g., "/foo/bar/0").

  - `JSONPointer(refTokens: List<String>) -> JSONPointer`: Constructs from pre-parsed list of reference tokens.

  - `queryFrom(document: Object) -> Object`: Evaluates pointer against document, returning referenced value or throwing exception if not found.

  - `toString() -> String`: Returns pointer string in standard RFC 6901 format.

  - `toURIFragment() -> String`: Returns pointer as URI fragment with # prefix for use in URLs.

  - `builder() -> Builder` (Static): Creates new Builder instance for constructing JSONPointer programmatically.

- `JSONPointer.Builder`: Fluent builder for constructing JSONPointer paths programmatically.

  - `Builder() -> Builder`: Creates empty builder for constructing pointer path.

  - `append(token: String) -> Builder`: Appends string reference token to pointer path.

  - `append(arrayIndex: int) -> Builder`: Appends array index reference token to pointer path.

  - `build() -> JSONPointer`: Constructs immutable JSONPointer from accumulated tokens.

---

`JSONPointerException.java`:

- `JSONPointerException`: Exception thrown when JSONPointer operations fail, extending JSONException.

  - `JSONPointerException(message: String) -> JSONPointerException`: Constructs exception with descriptive error message.

  - `JSONPointerException(message: String, cause: Throwable) -> JSONPointerException`: Constructs exception with message and underlying cause.

---

`JSONPropertyIgnore.java`:

- `@JSONPropertyIgnore`: Annotation to mark bean getter methods that should be excluded from JSON serialization.

  - **Target**: ElementType.METHOD

  - **Retention**: RetentionPolicy.RUNTIME

---

`JSONPropertyName.java`:

- `@JSONPropertyName`: Annotation to override the JSON property name for bean getter methods during serialization.

  - **Target**: ElementType.METHOD

  - **Retention**: RetentionPolicy.RUNTIME

  - `value() -> String`: Returns the custom JSON property name to use instead of derived name.

---

`JSONString.java`:

- `JSONString`: Interface for objects that can provide their own JSON string representation.

  - `toJSONString() -> String`: Returns valid JSON string representation of implementing object.

---

`JSONStringer.java`:

- `JSONStringer`: Convenience class for quickly producing JSON text, extending JSONWriter with internal StringWriter.

  - `JSONStringer() -> JSONStringer`: Creates fresh JSONStringer ready to produce JSON output.

  - `toString() -> String`: Returns accumulated JSON text as string.

---

`JSONTokener.java`:

- `JSONTokener`: Tokenizer for parsing JSON text, tracking position and providing syntax error reporting.

  - `JSONTokener(reader: Reader) -> JSONTokener`: Constructs from Reader with default configuration.

  - `JSONTokener(reader: Reader, jsonParserConfiguration: JSONParserConfiguration) -> JSONTokener`: Constructs from Reader with custom parser configuration.

  - `JSONTokener(inputStream: InputStream) -> JSONTokener`: Constructs from InputStream using UTF-8 encoding.

  - `JSONTokener(inputStream: InputStream, jsonParserConfiguration: JSONParserConfiguration) -> JSONTokener`: Constructs from InputStream with custom configuration.

  - `JSONTokener(s: String) -> JSONTokener`: Constructs from String source with default configuration.

  - `JSONTokener(s: String, jsonParserConfiguration: JSONParserConfiguration) -> JSONTokener`: Constructs from String with custom configuration.

  - `back() -> void`: Steps back one character in the input stream for re-reading.

  - `end() -> boolean`: Checks if tokenizer has reached end of input.

  - `more() -> boolean`: Checks if more characters are available to read.

  - `next() -> char`: Reads and returns next character, returning 0 at end of input.

  - `next(c: char) -> char`: Reads next character and throws exception if it doesn't match expected character.

  - `next(n: int) -> String`: Reads next n characters as string, stopping at end if fewer available.

  - `nextClean() -> char`: Reads next non-whitespace character, skipping whitespace and comments.

  - `nextString(quote: char) -> String`: Reads quoted string up to closing quote, handling escape sequences.

  - `nextTo(delimiter: char) -> String`: Reads characters until delimiter is found, not consuming delimiter.

  - `nextTo(delimiters: String) -> String`: Reads until any delimiter character is found.

  - `nextValue() -> Object`: Parses and returns next JSON value (object, array, string, number, boolean, or null).

  - `skipTo(to: char) -> char`: Skips characters until specified character is found and consumes it.

  - `syntaxError(message: String) -> JSONException`: Creates JSONException with message including current position information.

  - `syntaxError(message: String, causedBy: Throwable) -> JSONException`: Creates exception with cause for chained error reporting.

  - `toString() -> String`: Returns descriptive string showing current position in input.

  - `close() -> void`: Closes underlying Reader, releasing resources.

  - `getJsonParserConfiguration() -> JSONParserConfiguration`: Returns current parser configuration.

  - `setConfiguration(jsonParserConfiguration: JSONParserConfiguration) -> void` (Deprecated): Sets parser configuration, deprecated in favor of constructor parameter.

  - `dehexchar(c: char) -> int` (Static): Converts hex character (0-9, A-F, a-f) to integer value, returning -1 if invalid.

---

`JSONWriter.java`:

- `JSONWriter`: Produces properly formatted JSON text, maintaining state to ensure valid structure.

  - `JSONWriter(w: Writer) -> JSONWriter`: Constructs JSONWriter that outputs to specified Writer.

  - `array() -> JSONWriter`: Begins new JSON array, expecting subsequent values or end.

  - `endArray() -> JSONWriter`: Closes current JSON array with closing bracket.

  - `object() -> JSONWriter`: Begins new JSON object, expecting key-value pairs.

  - `endObject() -> JSONWriter`: Closes current JSON object with closing brace.

  - `key(string: String) -> JSONWriter`: Writes object key, expecting value to follow.

  - `value(value: boolean) -> JSONWriter`: Writes boolean value (true or false).

  - `value(value: double) -> JSONWriter`: Writes double value, validating it's finite.

  - `value(value: long) -> JSONWriter`: Writes long integer value.

  - `value(value: Object) -> JSONWriter`: Writes arbitrary object value, handling nulls and complex types.

---

`ParserConfiguration.java`:

- `ParserConfiguration`: Base immutable configuration class for JSON and XML parsers with common settings.

  - `ParserConfiguration() -> ParserConfiguration`: Creates default configuration with type conversion enabled and standard nesting limits.

  - `ParserConfiguration(keepStrings: boolean, maxNestingDepth: int) -> ParserConfiguration` (Protected): Internal constructor for subclass configuration initialization.

  - `isKeepStrings() -> boolean`: Returns whether parser preserves all values as strings without type conversion.

  - `withKeepStrings(newVal: boolean) -> T` (Protected): Returns new configuration with modified keepStrings setting.

  - `getMaxNestingDepth() -> int`: Returns maximum allowed nesting depth for nested objects/arrays.

  - `withMaxNestingDepth(maxNestingDepth: int) -> T` (Protected): Returns new configuration with modified nesting depth limit.

  - `clone() -> T` (Protected): Creates deep copy of configuration for immutable modification pattern.

---

`Property.java`:

- `Property`: Utility class for converting between java.util.Properties and JSONObject representations.

  - `Property() -> Property` (Deprecated): Default constructor, utility class should not be instantiated.

  - `toJSONObject(properties: Properties) -> JSONObject` (Static): Converts Properties object to JSONObject with string values.

  - `toProperties(jo: JSONObject) -> Properties` (Static): Converts JSONObject back to Properties, converting values to strings.

---

`StringBuilderWriter.java`:

- `StringBuilderWriter`: High-performance Writer implementation using StringBuilder instead of synchronized StringBuffer.

  - `StringBuilderWriter() -> StringBuilderWriter`: Creates writer with default initial capacity.

  - `StringBuilderWriter(capacity: int) -> StringBuilderWriter`: Creates writer with specified initial StringBuilder capacity.

  - `write(value: int) -> void`: Writes single character to builder.

  - `write(value: char[]) -> void`: Writes entire character array to builder.

  - `write(value: String) -> void`: Writes entire string to builder.

  - `write(value: String, offset: int, length: int) -> void`: Writes substring to builder from offset with specified length.

  - `append(value: CharSequence) -> StringBuilderWriter`: Appends CharSequence, implementing Appendable interface.

  - `append(value: CharSequence, start: int, end: int) -> StringBuilderWriter`: Appends CharSequence subsequence.

  - `append(value: char) -> StringBuilderWriter`: Appends single character.

  - `toString() -> String`: Returns accumulated string content from builder.

  - `flush() -> void`: No-op flush since no buffering beyond StringBuilder occurs.

  - `close() -> void`: No-op close, writer remains usable after closing.

---

`XML.java`:

- `XML`: Utility class for bidirectional conversion between XML and JSON (JSONObject or JSONArray).

  - `XML() -> XML`: Default constructor for XML utility class.

  - `escape(string: String) -> String` (Static): Escapes XML special characters (<, >, &, ', ") with entity references.

  - `unescape(string: String) -> String` (Static): Converts XML entity references (&lt;, &gt;, &amp;, etc.) back to characters.

  - `noSpace(string: String) -> void` (Static): Validates string contains no whitespace, throwing exception if found.

  - `stringToValue(string: String) -> Object` (Static): Converts string to appropriate type (boolean, number, or string).

  - `stringToValue(string: String, typeConverter: XMLXsiTypeConverter<?>) -> Object` (Static): Converts string using custom type converter.

  - `toJSONObject(reader: Reader) -> JSONObject` (Static): Parses XML from Reader into JSONObject with default configuration.

  - `toJSONObject(reader: Reader, config: XMLParserConfiguration) -> JSONObject` (Static): Parses XML from Reader with custom configuration.

  - `toJSONObject(reader: Reader, keepStrings: boolean) -> JSONObject` (Static): Parses XML preserving all values as strings if requested.

  - `toJSONObject(reader: Reader, replacementChar: Character) -> JSONObject` (Static): Parses XML replacing certain characters during conversion.

  - `toJSONObject(string: String) -> JSONObject` (Static): Parses XML string into JSONObject with default configuration.

  - `toJSONObject(string: String, keepStrings: boolean) -> JSONObject` (Static): Parses XML string with optional string preservation.

  - `toJSONObject(string: String, replacementChar: Character) -> JSONObject` (Static): Parses XML string with character replacement.

  - `toJSONObject(string: String, config: XMLParserConfiguration) -> JSONObject` (Static): Parses XML string using custom parser configuration.

  - `toString(object: Object) -> String` (Static): Converts JSONObject or JSONArray to XML string with default settings.

  - `toString(object: Object, tagName: String) -> String` (Static): Converts to XML with specified root tag name.

  - `toString(object: Object, config: XMLParserConfiguration) -> String` (Static): Converts to XML using custom configuration for formatting.

  - `toString(object: Object, tagName: String, config: XMLParserConfiguration) -> String` (Static): Converts to XML with tag name and configuration.

  - `toJSONArray(string: String) -> JSONArray` (Static): Parses XML string to JSONArray for array-like XML structures.

  - `toJSONArray(string: String, keepStrings: boolean) -> JSONArray` (Static): Parses XML to JSONArray with string preservation option.

  - `toJSONArray(string: String, config: XMLParserConfiguration) -> JSONArray` (Static): Parses XML to JSONArray with custom configuration.

---

`XMLParserConfiguration.java`:

- `XMLParserConfiguration`: Immutable configuration for XML to JSON parser controlling type conversion, CDATA handling, and formatting.

  - `XMLParserConfiguration() -> XMLParserConfiguration`: Creates default configuration with type conversion and standard CDATA handling.

  - `XMLParserConfiguration(keepStrings: boolean, cDataTagName: String, convertNilAttributeToNull: boolean) -> XMLParserConfiguration` (Protected): Internal constructor for basic configuration.

  - `XMLParserConfiguration(keepStrings: boolean, cDataTagName: String, convertNilAttributeToNull: boolean, xsiTypeMap: Map<String, XMLXsiTypeConverter<?>>, forceList: Set<String>) -> XMLParserConfiguration` (Protected): Extended constructor with type conversion and force list settings.

  - `XMLParserConfiguration(keepStrings: boolean, cDataTagName: String, convertNilAttributeToNull: boolean, xsiTypeMap: Map<String, XMLXsiTypeConverter<?>>, forceList: Set<String>, maxNestingDepth: int) -> XMLParserConfiguration` (Protected): Full constructor with nesting depth control.

  - `XMLParserConfiguration(keepStrings: boolean, cDataTagName: String, convertNilAttributeToNull: boolean, xsiTypeMap: Map<String, XMLXsiTypeConverter<?>>, forceList: Set<String>, maxNestingDepth: int, closeEmptyTag: boolean, trimWhitespace: boolean) -> XMLParserConfiguration` (Protected): Complete constructor with all configuration options.

  - `clone() -> XMLParserConfiguration` (Protected): Creates deep copy of configuration for safe modification.

  - `withKeepStrings(newVal: boolean) -> XMLParserConfiguration`: Returns new configuration with keepStrings setting modified.

  - `withKeepNumberAsString(newVal: boolean) -> XMLParserConfiguration`: Returns configuration that preserves numbers as strings.

  - `withKeepBooleanAsString(newVal: boolean) -> XMLParserConfiguration`: Returns configuration that preserves booleans as strings.

  - `withcDataTagName(newCDataTagName: String) -> XMLParserConfiguration`: Returns configuration with custom CDATA tag name.

  - `withConvertNilAttributeToNull(newVal: boolean) -> XMLParserConfiguration`: Returns configuration that converts xsi:nil to null values.

  - `withXsiTypeMap(xsiTypeMap: Map<String, XMLXsiTypeConverter<?>>) -> XMLParserConfiguration`: Returns configuration with custom type converter map.

  - `withForceList(forceList: Set<String>) -> XMLParserConfiguration`: Returns configuration forcing specified tags to always be arrays.

  - `withMaxNestingDepth(maxNestingDepth: int) -> XMLParserConfiguration`: Returns configuration with modified nesting depth limit.

  - `withCloseEmptyTag(closeEmptyTag: boolean) -> XMLParserConfiguration`: Returns configuration controlling empty tag output format (self-closing vs paired tags).

  - `withTrimWhitespace(trimWhitespace: boolean) -> XMLParserConfiguration`: Returns configuration controlling text node whitespace trimming.

  - `getcDataTagName() -> String`: Returns tag name used for CDATA sections in JSON output.

  - `isKeepNumberAsString() -> boolean`: Returns whether numbers are preserved as strings.

  - `isKeepBooleanAsString() -> boolean`: Returns whether booleans are preserved as strings.

  - `isConvertNilAttributeToNull() -> boolean`: Returns whether xsi:nil attributes are converted to null.

  - `getXsiTypeMap() -> Map<String, XMLXsiTypeConverter<?>>`: Returns map of custom type converters for xsi:type attributes.

  - `getForceList() -> Set<String>`: Returns set of tag names that should always be represented as arrays.

  - `isCloseEmptyTag() -> boolean`: Returns whether empty tags use self-closing format.

  - `isTrimWhitespace() -> boolean`: Returns whether whitespace in text nodes is trimmed.

---

`XMLTokener.java`:

- `XMLTokener`: Specialized tokenizer extending JSONTokener for parsing XML documents with entity resolution.

  - `XMLTokener(reader: Reader) -> XMLTokener`: Constructs from Reader for streaming XML parsing.

  - `XMLTokener(s: String) -> XMLTokener`: Constructs from String containing XML text.

  - `XMLTokener(reader: Reader, config: XMLParserConfiguration) -> XMLTokener`: Constructs from Reader with custom parser configuration.

  - `nextCDATA() -> String`: Reads CDATA section content until ]]> closing delimiter.

  - `nextContent() -> Object`: Reads next XML content token (text, entity reference, or structural character).

  - `nextEntity(ampersand: char) -> Object`: Resolves entity reference starting with & to character or throws exception if unknown.

  - `nextMeta() -> Object`: Reads next meta-token within tags (attributes, values, structural characters).

  - `nextToken() -> Object`: Reads next XML token handling quotes, tags, and text content.

  - `skipPast(to: String) -> boolean`: Skips characters until specified string is found and consumed.

  - `unescapeEntity(e: String) -> String` (Static): Converts entity name to corresponding character string.

---

`XMLXsiTypeConverter.java`:

- `XMLXsiTypeConverter<T>`: Interface for custom conversion of XML xsi:type attribute values to Java types.

  - `convert(value: String) -> T`: Converts string value from XML to target type T based on xsi:type attribute.

---
