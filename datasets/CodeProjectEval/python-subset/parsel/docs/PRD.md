## Introduction

This document outlines the product requirements for `Parsel`, a BSD-licensed Python library designed to extract data from HTML, JSON, and XML documents. The project aims to provide a powerful yet simple data extraction solution for web scraping and data parsing applications.

## Goals

The primary goal of Parsel is to offer a unified interface for data extraction across multiple document formats (HTML, XML, JSON) using industry-standard query languages. It aims to simplify web scraping workflows by providing a consistent API that supports CSS selectors, XPath expressions, and JMESPath queries.

## Features and Functionalities

- **Multi-Format Support**: Extract data from HTML, XML, and JSON documents using a unified interface.

- **Multiple Query Languages**: 
  - CSS and XPath expressions for HTML and XML documents
  - JMESPath expressions for JSON documents
  - Regular expressions for pattern matching

- **Selector Chaining**: Support for nested selector operations, allowing users to refine selections progressively.

- **Flexible Data Extraction**: Multiple extraction methods including `.get()`, `.getall()`, `.re()`, and `.re_first()` for different use cases. 

- **Attribute Access**: Direct access to element attributes via the `.attrib` property. 

- **XML Namespace Support**: Built-in support for XML namespaces with registration and removal capabilities. 

- **EXSLT Extensions**: Pre-registered EXSLT namespaces for regular expressions and set manipulation in XPath. 

- **Custom XPath Functions**: Extended XPath functionality including the `has-class()` function for HTML class matching. 

- **CSS Pseudo-Elements**: Non-standard pseudo-elements `::text` and `::attr(name)` for selecting text nodes and attributes. 

## Core Architecture

Parsel follows a selector-based architecture with these main components:

- **Selector Class**: Main entry point that wraps input data and provides query methods (`.xpath()`, `.css()`, `.jmespath()`). 

- **SelectorList Class**: A list subclass that holds multiple Selector objects and provides batch operations. 

- **Query Translation Layer**: Converts CSS selectors to XPath expressions internally for unified processing. 

- **lxml Integration**: Built on top of lxml for HTML/XML parsing, providing speed and accuracy. 

## Usage

```python
>>> from parsel import Selector
>>> text = """
... <html>
...     <body>
...         <h1>Hello, Parsel!</h1>
...         <ul>
...             <li><a href="http://example.com">Link 1</a></li>
...             <li><a href="http://scrapy.org">Link 2</a></li>
...         </ul>
...         <script type="application/json">{"a": ["b", "c"]}</script>
...     </body>
... </html>"""
>>> selector = Selector(text=text)
>>> selector.css("h1::text").get()
'Hello, Parsel!'
>>> selector.xpath("//h1/text()").re(r"\w+")
['Hello', 'Parsel']
>>> for li in selector.css("ul > li"):
...     print(li.xpath(".//@href").get())
...
http://example.com
http://scrapy.org
>>> selector.css("script::text").jmespath("a").get()
'b'
>>> selector.css("script::text").jmespath("a").getall()
['b', 'c']
```

### 1. Basic Usage

#### HTML/XML Parsing

```python
from parsel import Selector

html_text = "<html><body><h1>Hello, Parsel!</h1></body></html>"
selector = Selector(text=html_text)

# Using CSS
selector.css('h1')                     # [<Selector ...>]
selector.css('h1::text').get()         # 'Hello, Parsel!'

# Using XPath
selector.xpath('//h1')                 # [<Selector ...>]
selector.xpath('//h1/text()').get()    # 'Hello, Parsel!'
```

#### JSON Parsing

```python
json_text = '{"title":"Hello, Parsel!"}'
selector = Selector(text=json_text)

selector.jmespath('title').get()       # 'Hello, Parsel!'
selector.jmespath('title').getall()    # ['Hello, Parsel!']
```

### 2. Extracting Data

- `.get()` / `.extract_first()`: Returns the **first match** or `None`.
- `.getall()` / `.extract()`: Returns a **list of all matches**.

```python
selector.xpath('//title/text()').get()      # 'Example website'
selector.xpath('//title/text()').getall()   # ['Example website']
```

### 3. CSS Selector Extensions (Parsel-specific)

Standard CSS cannot select text nodes or attributes, so Parsel adds:

- `::text` — selects text content
- `::attr(name)` — selects attribute value

```python
selector.css('a::attr(href)').getall()   # list of href values
selector.css('title::text').get()        # text inside <title>
```

### 4. Working with Attributes

Multiple ways to extract attributes:

```python
# XPath
selector.xpath('//a/@href').getall()

# CSS with ::attr()
selector.css('a::attr(href)').getall()

# Using .attrib property
[a.attrib['href'] for a in selector.css('a')]
selector.css('base').attrib['href']  # for single element
```

### 5. Nesting Selectors

Selection methods return `SelectorList`, which supports chaining:

```python
links = selector.xpath('//a[contains(@href, "image")]')
for link in links:
    url = link.xpath('@href').get()
    img = link.xpath('img/@src').get()
```

### 6. Regular Expressions

- `.re(pattern)`: returns list of strings matching regex.
- `.re_first(pattern)`: returns first match.

```python
selector.xpath('//a/text()').re(r'Name:\s*(.*)')
# ['My image 1 ', 'My image 2 ', ...]
```

### 7. Removing Elements

Use `.drop()` to **destructively remove** elements (e.g., ads):

```python
selector.xpath('//div[@class="ad"]').drop()
```

## Requirements

### Dependencies
- Python 3.x
- lxml library for HTML/XML parsing 
- cssselect library for CSS selector support 

All dependencies:
```bash
cssselect>=1.2.0
jmespath
lxml
packaging
w3lib>=1.19.0
```

## Design and User Interface

As a backend library, Parsel does not have a GUI. The interface is through Python classes and methods following Pythonic design principles. The API is designed to be intuitive and chainable, allowing for progressive refinement of data extraction queries. The library emphasizes simplicity while providing powerful extraction capabilities for web scraping applications.

