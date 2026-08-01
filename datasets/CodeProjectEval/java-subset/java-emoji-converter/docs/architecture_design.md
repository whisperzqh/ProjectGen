# Architecture Design

Below is a text-based representation of the file tree.
```bash
src
  ├── main
  │   ├── java
  │   │   └── com
  │   │       └── github
  │   │           └── binarywang
  │   │               └── java
  │   │                   └── emoji
  │   │                       ├── EmojiConverter.java
  │   │                       ├── EmojiReader.java
  │   │                       ├── model
  │   │                       │   └── Emoji4Unicode.java
  │   │                       └── util
  │   │                           └── EmojiUtils.java
  │   └── resources
  │       └── emoji4unicode.xml

```

`EmojiReader.java` :

- `EmojiReader`: A utility class responsible for reading and parsing emoji data from either a remote XML file or a local resource, and providing mappings from SoftBank emoji code points to standard Unicode representations.

  - `read(boolean onlyFromLocal)`: Reads and deserializes the emoji data into an `Emoji4Unicode` object. If `onlyFromLocal` is true, it loads exclusively from the embedded `/emoji4unicode.xml` resource; otherwise, it attempts to fetch from a remote URL first and falls back to the local file on failure.

  - `getSb2UnicodeMap()`: Constructs and returns a map that translates SoftBank emoji code point sequences (as `List<Integer>`) into their corresponding standard Unicode string representations. This map is lazily initialized and cached for subsequent calls.

`EmojiConverter.java` :

- `EmojiConverter`: A singleton utility class that converts emoji representations between SoftBank, Unicode, HTML decimal, and alias formats, using an internal `EmojiReader` to handle SoftBank-to-Unicode mapping and delegating to `EmojiParser` for standard conversions.

  - `getInstance()`: Returns the single shared instance of `EmojiConverter`, enforcing the singleton pattern.

  - `toAlias(String input)`: Converts a string containing Unicode or SoftBank emoji into a string where emojis are replaced with their corresponding short aliases (e.g., `:smile:`). If the input contains SoftBank emoji, it first converts them to Unicode before alias substitution.

  - `toHtml(String input)`: Converts a string containing Unicode or SoftBank emoji into a string where emojis are replaced with their HTML decimal numeric character references (e.g., `&#128512;`). SoftBank emoji are first normalized to Unicode if present.

  - `toUnicode(String input)`: Converts a string containing SoftBank emoji or alias representations (e.g., `:smile:`) into standard Unicode emoji characters. SoftBank sequences are mapped via an internal lookup table, and aliases are resolved using `EmojiParser`.

`Emoji4Unicode.java` :

- `Emoji4Unicode`: A data model class that represents the hierarchical structure of emoji definitions as parsed from an XML file (e.g., `emoji4unicode.xml`). It organizes emojis into categories, subcategories, and individual elements, each containing metadata such as vendor-specific codes (SoftBank, Google, etc.) and Unicode equivalents.

  - The instance attribute `categories` is a list of `Category` objects, representing top-level emoji groups (e.g., "People", "Nature").

  - `getCategories()`: Returns the list of top-level emoji categories.

  - `setCategories(List<Category> categories)`: Sets the list of top-level emoji categories.

  - `toSimpleString(Object obj)`: A static utility method that generates a clean, human-readable string representation of an object, omitting fields with `null` values. Used by inner classes for debugging or logging.

  - `Category`: A static nested class representing a top-level emoji category.

    - The instance attribute `name` holds the name of the category (e.g., "Smileys").
    - The instance attribute `subCategories` is a list of `SubCategory` objects under this category.
    - `getSubCategories()` and `setSubCategories(List<SubCategory>)`: Accessor and mutator for the subcategory list.
    - `getName()` and `setName(String name)`: Accessor and mutator for the category name.

  - `SubCategory`: A static nested class representing a subcategory within a category (e.g., "Face-smiling" under "Smileys").

    - The instance attribute `name` holds the subcategory name.
    - The instance attribute `elements` is a list of `Element` objects (individual emojis).
    - `getElements()` and `setElements(List<Element>)`: Accessor and mutator for the emoji element list.

  - `Element`: A static nested class representing a single emoji entry, containing mappings across multiple platforms and metadata.

    - The instance attribute `name` is the descriptive name of the emoji.
    - The instance attribute `softbank`, `google`, `docomo`, `kddi` store vendor-specific emoji identifiers.
    - The instance attribute `unicode` holds the standard Unicode representation of the emoji.
    - The instance attribute `text_fallback` and `text_repr` provide text alternatives for non-emoji-capable systems.
    - The instance attribute `ann` (annotations) and `desc` (descriptions) contain additional textual information.
    - Public getter and setter methods exist for all attributes (e.g., `getUnicode()`, `setSoftbank(String)`, etc.).

`EmojiUtils.java` :

- `EmojiUtils`: A utility class that provides static methods for detecting and working with SoftBank-specific emoji characters, based on a predefined set of code points.

  - `allSbEmojis()`: Returns a space-separated string containing all known SoftBank emoji characters.

  - `isSbEmoji(char c)`: Checks whether the given character is a SoftBank emoji by testing membership in the internal emoji character set.

  - `containsSbEmoji(String s)`: Scans the input string and returns `true` if it contains at least one SoftBank emoji character; otherwise, returns `false`.