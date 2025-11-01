## UML Class Diagram

```mermaid
classDiagram
  class GenericTranslator {
    css_to_xpath(css: str, prefix: str) str
  }
  class HTMLTranslator {
    css_to_xpath(css: str, prefix: str) str
  }
  class TranslatorMixin {
    xpath_attr_functional_pseudo_element(xpath: OriginalXPathExpr, function: FunctionalPseudoElement) XPathExpr
    xpath_element(selector: Element) XPathExpr
    xpath_pseudo_element(xpath: OriginalXPathExpr, pseudo_element: PseudoElement) OriginalXPathExpr
    xpath_text_simple_pseudo_element(xpath: OriginalXPathExpr) XPathExpr
  }
  class TranslatorProtocol {
    css_to_xpath(css: str, prefix: str)* str
    xpath_element(selector: Element)* OriginalXPathExpr
  }
  class XPathExpr {
    attribute : str | None
    textnode : bool
    from_xpath(xpath: OriginalXPathExpr, textnode: bool, attribute: str | None) Self
    join(combiner: str, other: OriginalXPathExpr) Self
  }
  class CTGroupValue {
  }
  class CannotDropElementWithoutParent {
  }
  class CannotRemoveElementWithoutParent {
  }
  class CannotRemoveElementWithoutRoot {
  }
  class SafeXMLParser {
  }
  class Selector {
    attrib : dict[str, str]
    extract
    namespaces : dict
    root : Any, NoneType, object
    selectorlist_cls
    type : str
    css(query: str) SelectorList[Self]
    drop() None
    get() Any
    getall() list[str]
    jmespath(query: str) SelectorList[Self]
    re(regex: str | Pattern[str], replace_entities: bool) list[str]
    re_first(regex: str | Pattern[str], default: None, replace_entities: bool)* str | None
    register_namespace(prefix: str, uri: str) None
    remove_namespaces() None
    xpath(query: str, namespaces: Mapping[str, str] | None) SelectorList[Self]
  }
  class SelectorList {
    attrib : Mapping[str, str]
    extract
    extract_first
    css(query: str) SelectorList[_SelectorType]
    drop() None
    get(default: None)* str | None
    getall() list[str]
    jmespath(query: str) SelectorList[_SelectorType]
    re(regex: str | Pattern[str], replace_entities: bool) list[str]
    re_first(regex: str | Pattern[str], default: None, replace_entities: bool)* str | None
    xpath(xpath: str, namespaces: Mapping[str, str] | None) SelectorList[_SelectorType]
  }
  GenericTranslator --|> TranslatorMixin
  HTMLTranslator --|> TranslatorMixin
  CannotDropElementWithoutParent --|> CannotRemoveElementWithoutParent
  Selector --> SelectorList : selectorlist_cls
```

## UML Package Diagram

```mermaid
classDiagram
  class parsel {
  }
  class csstranslator {
  }
  class selector {
  }
  class utils {
  }
  class xpathfuncs {
  }
  parsel --> parsel
  parsel --> csstranslator
  parsel --> selector
  parsel --> xpathfuncs
  selector --> csstranslator
  selector --> utils
```
