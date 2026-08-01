# Architecture Design

Below is a text-based representation of the file tree. 
```bash
├── parsel
│   ├── csstranslator.py
│   ├── __init__.py
│   ├── py.typed
│   ├── selector.py
│   ├── utils.py
│   └── xpathfuncs.py
```

`csstranslator.py` :

- `XPathExpr`: A subclass of `cssselect.xpath.XPathExpr` that extends XPath expressions to support pseudo-elements like `::text` and `::attr(ATTR_NAME)` by tracking whether the expression targets a text node or a specific attribute.

  - `from_xpath(cls, xpath, textnode=False, attribute=None)`: Class method to create a new `XPathExpr` instance from an existing `OriginalXPathExpr`, optionally marking it to select text nodes or a specific attribute.

  - `__str__(self)`: Overrides the string representation to append `/text()` when `textnode=True` or `/@{attribute}` when `attribute` is set, producing a valid XPath string that reflects pseudo-element semantics.

  - `join(self, combiner, other, *args, **kwargs)`: Joins this expression with another `XPathExpr`, inheriting the `textnode` and `attribute` properties from the `other` expression. Raises a `ValueError` if `other` is not an instance of `XPathExpr`.

- `TranslatorProtocol`: A typing protocol defining the interface expected from a CSS-to-XPath translator, specifically requiring `xpath_element` and `css_to_xpath` methods.

- `TranslatorMixin`: A mixin class that adds support for CSS pseudo-elements (`::text` and `::attr(...)`) to any translator that implements `TranslatorProtocol`.

  - `xpath_element(self, selector)`: Overrides the base `xpath_element` to wrap the result in `XPathExpr`, enabling pseudo-element handling.

  - `xpath_pseudo_element(self, xpath, pseudo_element)`: Dispatches handling of pseudo-elements to specialized methods based on the pseudo-element’s name and type (simple or functional).

  - `xpath_attr_functional_pseudo_element(self, xpath, function)`: Handles the `::attr(ATTR_NAME)` pseudo-element by extracting the attribute name (as a string or identifier) and returning an `XPathExpr` configured to select that attribute.

  - `xpath_text_simple_pseudo_element(self, xpath)`: Handles the `::text` pseudo-element by returning an `XPathExpr` configured to select text nodes.

- `GenericTranslator`: A CSS-to-XPath translator for generic XML documents, combining `TranslatorMixin` with `cssselect.GenericTranslator`. Adds LRU caching to `css_to_xpath` for performance.

  - `css_to_xpath(self, css, prefix="descendant-or-self::")`: Converts a CSS selector to an XPath expression, with results cached using `functools.lru_cache`.

- `HTMLTranslator`: A CSS-to-XPath translator optimized for HTML documents, combining `TranslatorMixin` with `cssselect.HTMLTranslator`. Adds LRU caching to `css_to_xpath`.

  - `css_to_xpath(self, css, prefix="descendant-or-self::")`: Converts an HTML-targeted CSS selector to an XPath expression, with results cached using `functools.lru_cache`.

- `css2xpath(query)`: A convenience function that uses a shared `HTMLTranslator` instance to convert a CSS selector string into its equivalent XPath expression.

`__init__.py`:

`selector.py` :

- `CannotRemoveElementWithoutRoot`: Exception raised when attempting to drop a pseudo-element or text node that has no associated root element (e.g., from `::text`).

- `CannotRemoveElementWithoutParent`: Base exception for operations that require a parent element but find none.

- `CannotDropElementWithoutParent`: Subclass of `CannotRemoveElementWithoutParent`, raised when trying to drop a root-level element that has no parent.

- `SafeXMLParser`: A subclass of `lxml.etree.XMLParser` that disables external entity resolution by default (`resolve_entities=False`) to prevent XXE attacks.

- `_xml_or_html(type_)`: Helper function that returns `"xml"` if the input `type_` is `"xml"`, otherwise returns `"html"`.

- `create_root_node(text, parser_cls, base_url=None, huge_tree=True, body=b"", encoding="utf-8")`: Creates an lxml root node from either a string (`text`) or raw bytes (`body`) using the specified parser class. Supports the `huge_tree` option for parsing very large documents if supported by the lxml version.

- `SelectorList`: A subclass of Python’s built-in `list` that wraps a list of `Selector` objects and provides convenience methods for batch operations.

  - `__getitem__(self, pos)`: Returns a `Selector` for an index or a new `SelectorList` for a slice.

  - `__getstate__(self)`: Prevents pickling of `SelectorList` instances.

  - `jmespath(self, query, **kwargs)`: Applies a JMESPath query to each selector in the list and returns a flattened `SelectorList` of results.

  - `xpath(self, xpath, namespaces=None, **kwargs)`: Applies an XPath query to each selector and returns a flattened `SelectorList` of results.

  - `css(self, query)`: Applies a CSS selector to each element and returns a flattened `SelectorList` of results by internally converting CSS to XPath.

  - `re(self, regex, replace_entities=True)`: Applies a regex to the string representation of each selector and returns a flattened list of matches.

  - `re_first(self, regex, default=None, replace_entities=True)`: Returns the first match of the regex across all selectors, or `default` if no match is found.

  - `getall(self)`: Returns a list of string representations (via `.get()`) for all selectors in the list.

  - `extract(self)`: Alias for `getall`.

  - `get(self, default=None)`: Returns the string representation of the first selector, or `default` if the list is empty.

  - `extract_first(self)`: Alias for `get`.

  - `attrib`: Property that returns the attributes dictionary of the first selector’s underlying element, or an empty dict if the list is empty.

  - `drop(self)`: Calls `.drop()` on each selector to remove its matched node from its parent.

- `_get_root_from_text(text, *, type_, **lxml_kwargs)`: Internal helper to create an lxml root from a text string using the parser associated with the given type (`html` or `xml`).

- `_get_root_and_type_from_bytes(body, encoding, *, input_type, **lxml_kwargs)`: Determines document type (`json`, `html`, or `xml`) from raw bytes and constructs the appropriate root object.

- `_get_root_and_type_from_text(text, *, input_type, **lxml_kwargs)`: Determines document type from a string and constructs the appropriate root (JSON object or lxml element).

- `_get_root_type(root, *, input_type)`: Infers the selector type (`json`, `html`, `xml`) based on the provided `root` object and optional `input_type`.

- `_is_valid_json(text)`: Returns `True` if the input can be parsed as valid JSON.

- `_load_json_or_none(text)`: Attempts to parse input as JSON; returns `None` on failure.

- `Selector`: A unified interface for selecting data from HTML, XML, or JSON using XPath, CSS, or JMESPath.

  - `__init__(self, text=None, type=None, body=b"", encoding="utf-8", namespaces=None, root=_NOT_SET, base_url=None, _expr=None, huge_tree=True)`: Initializes a selector from `text`, `body`, or an existing `root`. Automatically detects type (`html`, `xml`, `json`, or `text`) unless explicitly provided.

  - `__getstate__(self)`: Prevents pickling of `Selector` instances.

  - `_get_root(self, text="", base_url=None, huge_tree=True, type_=None, body=b"", encoding="utf-8")`: Internal method to reconstruct an lxml root node with given parameters.

  - `jmespath(self, query, **kwargs)`: Executes a JMESPath query on JSON data (either stored in `self.root` or extracted from HTML/XML text content) and returns a `SelectorList` of results wrapped as new `Selector` objects.

  - `xpath(self, query, namespaces=None, **kwargs)`: Executes an XPath query on HTML/XML documents and returns a `SelectorList` of matching nodes as `Selector` instances. Supports XPath variables and custom namespaces.

  - `css(self, query)`: Converts a CSS selector to XPath using the appropriate translator (`HTMLTranslator` or `GenericTranslator`) and delegates to `.xpath()`.

  - `_css2xpath(self, query)`: Internal method that translates a CSS selector string into an XPath string using the type-appropriate CSS translator.

  - `re(self, regex, replace_entities=True)`: Applies a regular expression to the string representation of the selected content and returns all matches as a list of strings.

  - `re_first(self, regex, default=None, replace_entities=True)`: Returns the first match from `re()`, or `default` if no match exists.

  - `get(self)`: Serializes the selected node(s) to a string. For HTML/XML, uses `lxml.etree.tostring`; for JSON/text, returns the raw value.

  - `extract(self)`: Alias for `get`.

  - `getall(self)`: Returns a single-element list containing the result of `get()`.

  - `register_namespace(self, prefix, uri)`: Registers a namespace prefix for use in XPath queries.

  - `remove_namespaces(self)`: Strips all namespaces from the underlying XML/HTML document to simplify XPath queries. No-op for JSON selectors.

  - `drop(self)`: Removes the selected element from its parent in the tree. Uses `drop_tree()` for HTML or `parent.remove()` for XML. Raises exceptions if the element cannot be dropped (e.g., pseudo-elements or root nodes).

  - `attrib`: Property that returns a copy of the underlying element’s attributes as a dictionary. Returns an empty dict for JSON selectors.

  - `__bool__(self)`: Returns `True` if `get()` yields non-empty content.

  - `__str__(self)`: Returns the string representation of the selected content.

  - `__repr__(self)`: Returns a concise representation showing the query and a shortened preview of the selected data.

`util.py` :

- `flatten(x)`: Returns a single, flat list containing all elements from the input iterable and any nested sub-iterables (recursively flattened). Strings and bytes are treated as atomic and not iterated into.

- `iflatten(x)`: Generator version of `flatten`; yields elements from the input iterable and its nested sub-iterables recursively, without creating an intermediate list.

- `_is_listlike(x)`: Internal helper function that returns `True` if `x` is iterable but not a string or bytes object. Used by `flatten` and `iflatten` to determine whether an item should be recursively expanded.

- `extract_regex(regex, text, replace_entities=True)`: Extracts substrings from `text` using the provided regular expression, following these rules:
  - If the regex defines a named group called `"extract"`, only the content of that group is returned.
  - If the regex contains multiple numbered capturing groups, all matched groups are returned (flattened into a single list).
  - If the regex has no groups, the entire match is returned for each match.
  By default, HTML character entities (e.g., `&nbsp;`) are replaced with their corresponding characters, except for `<` and `&amp;`. Set `replace_entities=False` to disable this behavior.

- `shorten(text, width, suffix="...")`: Truncates the input `text` to fit within the specified `width`, appending the given `suffix` if truncation occurs. Handles edge cases such as when `width` is smaller than the suffix length. Raises `ValueError` if `width` is negative.

`xpathfuncs.py` :

- `set_xpathfunc(fname, func)`: Registers or unregisters a custom XPath extension function in the default (empty) namespace for use with lxml XPath expressions.

  - If `func` is a callable, it is registered under the name `fname` and can be invoked in XPath expressions as `fname(...)`. The function receives a context object (providing access to the current node and evaluation state) followed by any arguments passed from the XPath expression.
  - If `func` is `None`, any existing function registered under `fname` is removed.
  - This leverages lxml’s `FunctionNamespace` mechanism; see [lxml’s XPath extension documentation](https://lxml.de/extensions.html#xpath-extension-functions) for details.

- `setup()`: Initializes the XPath extension environment by registering the `has-class` function via `set_xpathfunc`. Intended to be called once at module or application startup to make the function available globally in XPath queries.

- `has_class(context, *classes)`: An XPath extension function that checks whether an HTML element’s `class` attribute contains all of the specified CSS class names.
