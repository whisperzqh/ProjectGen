## UML Class Diagram

```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        +InferenceSession session
        +__init__(model_path)
        +predict()* 
    }
    
    class Module {
        +save(fpath)
        +load(fpath)$
    }
    
    class Tokenization {
        -Trie vocab
        -bool detect_new_word
        +seg(text) List~str~
        +tag(text) List~Tuple~
    }
    
    class LexicalModel {
        -BertWordPieceTokenizer tokenizer
        +predict(text)
        -decode_bio(labels, tokens)
    }
    
    class Lexical {
        -LexicalModel model
        +seg(text) List~str~
        +tag(text) List~Tuple~
        +ner(text) List~Tuple~
    }
    
    class SentimentModel {
        -BertWordPieceTokenizer tokenizer
        +predict(text)
    }
    
    class DetectorModel {
        -BertWordPieceTokenizer tokenizer
        +predict(text)
    }
    
    class CorrectorModel {
        -BertWordPieceTokenizer tokenizer
        +predict(text)
    }
    
    class CheckerDecoder {
        -DetectorModel detector
        -CorrectorModel corrector
        -Pinyin pinyin
        +spellcheck(text, suggest, k)
    }
    
    class SentenceVectorModel {
        -BertWordPieceTokenizer tokenizer
        +predict(text)
    }
    
    class SentenceVector {
        -SentenceVectorModel model
        -str genre
        +transform(text) ndarray
        +similarity(x, y) float
        +most_similar(query, docs, k) List~Tuple~
    }
    
    class Pinyin {
        -Trie trie
        +train()
        +translate(text) List~str~
    }
    
    class Radical {
        -dict data
        +train()
        +radical(text) List~str~
    }
    
    class KeywordTextRank {
        +extract(text, k, stopword, allowPOS) List~Tuple~
    }
    
    class TextRank {
        +extract(text, k, stopword) List~str~
    }
    
    class Trie {
        -dict root
        +add(key, value)
        +get(key)
    }
    
    class BM25 {
        +similarity(query, doc) float
    }
    
    BaseModel <|-- LexicalModel
    BaseModel <|-- SentimentModel
    BaseModel <|-- DetectorModel
    BaseModel <|-- CorrectorModel
    BaseModel <|-- SentenceVectorModel
    Module <|-- Pinyin
    Module <|-- Radical
    
    Lexical --> LexicalModel
    Tokenization --> Lexical
    CheckerDecoder --> DetectorModel
    CheckerDecoder --> CorrectorModel
    CheckerDecoder --> Pinyin
    SentenceVector --> SentenceVectorModel
    Pinyin --> Trie
    TextRank --> BM25
```
## UML Package Diagram

```mermaid
graph TB
    Main["xmnlp (Main Package)"]
    
    Config["xmnlp.config"]
    Lexical["xmnlp.lexical"]
    Sentiment["xmnlp.sentiment"]
    Checker["xmnlp.checker"]
    Summary["xmnlp.summary"]
    Pinyin["xmnlp.pinyin"]
    Radical["xmnlp.radical"]
    SV["xmnlp.sv"]
    Utils["xmnlp.utils"]
    
    Main --> Config
    Main --> Lexical
    Main --> Sentiment
    Main --> Checker
    Main --> Summary
    Main --> Pinyin
    Main --> Radical
    Main --> SV
    Main --> Utils
    
    Lexical --> Config
    Lexical --> Utils
    Sentiment --> Config
    Checker --> Config
    Checker --> Pinyin
    Summary --> Lexical
    Summary --> Utils
    Pinyin --> Config
    Pinyin --> Utils
    Radical --> Config
    SV --> Config
    
    subgraph "Core Modules"
        Lexical
        Sentiment
        Checker
    end
    
    subgraph "Utility Modules"
        Summary
        Pinyin
        Radical
        SV
    end
    
    subgraph "Infrastructure"
        Config
        Utils
    end
``` 