## UML Class Diagram

```mermaid
classDiagram
    class Selector {
        +root: Any
        +type: str
        +namespaces: dict
        -_expr: str
        -_huge_tree: bool
        -_text: str
        +__init__(text, type, body, encoding, namespaces, root, base_url, _expr, huge_tree)
        +xpath(query, namespaces, **kwargs) SelectorList
        +css(query) SelectorList
        +jmespath(query, **kwargs) SelectorList
        +get() str
        +getall() list
        +re(regex, replace_entities) list
        +re_first(regex, default, replace_entities) str
        +register_namespace(prefix, uri)
        +remove_namespaces()
        +drop()
        +attrib: dict
    }
    
    class SelectorList {
        +xpath(query, namespaces, **kwargs) SelectorList
        +css(query) SelectorList
        +jmespath(query, **kwargs) SelectorList
        +get(default) str
        +getall() list
        +re(regex, replace_entities) list
        +re_first(regex, default, replace_entities) str
        +attrib: dict
        +drop()
    }
    
    class XPathFunctions {
        <<module>>
        +set_xpathfunc(fname, func)
        +has_class(context, *classes) bool
        +setup()
    }
    
    list <|-- SelectorList
    Selector --> SelectorList : returns
    SelectorList --> Selector : contains
    Selector ..> XPathFunctions : uses
    Selector ..> lxml_etree : uses
    Selector ..> jmespath : uses
```

## UML Package Diagram

```mermaid
graph TD
    A["parsel package"] --> B["parsel.selector"]
    A --> C["parsel.xpathfuncs"]
    
    B --> D["lxml.etree"]
    B --> E["jmespath"]
    B --> F["w3lib.html"]
    
    C --> D
    C --> F
    
    G["External Dependencies"] -.-> D
    G -.-> E
    G -.-> F
```

## UML Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Selector
    participant Parser as "lxml/jmespath"
    participant SelectorList
    
    User->>Selector: __init__(text, type)
    Selector->>Parser: parse document
    Parser-->>Selector: root element/data
    
    User->>Selector: xpath()/css()/jmespath()
    Selector->>Parser: evaluate query
    Parser-->>Selector: matching nodes
    Selector->>SelectorList: create with Selector objects
    SelectorList-->>User: return SelectorList
    
    User->>SelectorList: xpath()/css() (chaining)
    loop for each Selector in list
        SelectorList->>Selector: apply query
        Selector->>Parser: evaluate query
        Parser-->>Selector: results
    end
    SelectorList->>SelectorList: combine results
    SelectorList-->>User: return new SelectorList
    
    User->>SelectorList: get()/getall()
    SelectorList->>Selector: extract data
    Selector-->>SelectorList: text/data
    SelectorList-->>User: return string/list
```
