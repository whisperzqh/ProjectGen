# Architecture Design

Below is a text-based representation of the file tree. 
```bash
src
│   ├── main
│   │   └── java
│   │       └── org
│   │           └── nibblesec
│   │               └── tools
│   │                   ├── package-info.java
│   │                   └── SerialKiller.java
```

`SerialKiller.java`:

- `SerialKiller`: Facade class extending `ObjectInputStream` that enforces a blacklist/whitelist policy during Java deserialization to prevent security vulnerabilities.

  - `Constructor(inputStream: InputStream, configFile: String) -> SerialKiller`: Initializes the `SerialKiller` stream with a source input stream and a path to the configuration file.
  
  - `resolveClass(serialInput: ObjectStreamClass) -> Class<?>`: Overrides the default class resolution to inspect the class name against configured blacklists and whitelists before loading. Returns the resolved class if safe.

- `SerialKiller.Configuration`: Internal static helper class to manage loading and reloading of the XML configuration file (package-private).

  - `Constructor(configPath: String) -> Configuration`: Loads the XML configuration from the specified path and sets up a reloading strategy.
  
  - `init(config: XMLConfiguration) -> void`: Private method to parse blacklist and whitelist regular expressions from the configuration object.
  
  - `reloadIfNeeded() -> void`: Checks if the configuration file has changed and reloads it if necessary.
  
  - `blacklist() -> Iterable<Pattern>`: Returns the iterable collection of compiled blacklist patterns.
  
  - `whitelist() -> Iterable<Pattern>`: Returns the iterable collection of compiled whitelist patterns.
  
  - `isProfiling() -> boolean`: Returns true if the application is in profiling mode (logging only), false if in blocking mode.

- `SerialKiller.PatternList`: Internal static helper class wrapping an array of compiled Regex patterns, implementing `Iterable` for easy iteration (package-private).

  - `Constructor(regExps: String...) -> PatternList`: Compiles an array of regex strings into valid `Pattern` objects.
  
  - `iterator() -> Iterator<Pattern>`: Returns an iterator over the compiled patterns.
  
  - `toString() -> String`: Returns a string representation of the internal pattern array.
