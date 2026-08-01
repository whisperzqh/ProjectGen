## UML Class Diagram

```mermaid
classDiagram
  class ClassicAdapter {
    action : NoneType
    category : DeprecationWarning
    extra_stacklevel : int
    reason : str
    version : str
    get_deprecated_msg(wrapped, instance)
  }
  class SphinxAdapter {
    directive
    line_length : int
    get_deprecated_msg(wrapped, instance)
  }
  SphinxAdapter --|> ClassicAdapter
```

## UML Package Diagram

```mermaid
classDiagram
  class deprecated {
  }
  class classic {
  }
  class sphinx {
  }
  deprecated --> classic
  sphinx --> classic

```
