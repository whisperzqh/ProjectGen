# PRD Document for xmnlp

## Introduction

xmnlp is an out-of-the-box, lightweight, open-source Chinese Natural Language Processing toolkit. It is designed as a comprehensive toolkit that provides essential Chinese NLP functionalities including word segmentation, part-of-speech tagging, named entity recognition, spell checking, sentiment analysis, text summarization, keyword extraction, pinyin conversion, and radical extraction. The toolkit leverages modern deep learning models, specifically using RoBERTa + CRF for lexical analysis tasks and ONNX runtime for efficient inference, making it suitable for production environments.

## Goals

The primary goals of xmnlp are to provide an accessible and practical solution for Chinese natural language processing tasks. The toolkit is designed to be "out-of-the-box" , meaning it requires minimal setup and configuration for users to start processing Chinese text immediately. It aims to support multiple operating systems including Linux, Windows, and macOS, with compatibility for Python versions 3.6, 3.7, and 3.8. The project's goal is to create a simple and easy-to-use Chinese NLP tool through community contributions, as stated in the contribution section. Additionally, xmnlp provides both fast processing modes (using reverse maximum matching) and deep learning modes (using neural models) to balance between speed and accuracy depending on users' needs.

## Features and Functionalities

The following features and functionalities are available in the xmnlp project:

### Chinese Lexical Analysis
- Ability to perform Chinese word segmentation using reverse maximum matching with RoBERTa + CRF for new word identification  
- Ability to perform fast word segmentation based on reverse maximum matching without new word identification  
- Ability to perform deep word segmentation using RoBERTa + CRF model (simplified Chinese only)  
- Ability to perform part-of-speech (POS) tagging with multiple speed/accuracy options  
- Ability to perform fast POS tagging based on reverse maximum matching  
- Ability to perform deep POS tagging using RoBERTa + CRF model  
- Ability to customize segmentation and tagging with user-defined dictionaries  
- Ability to use dictionaries compatible with jieba format  
- Ability to toggle new word detection on/off for performance optimization  

### Named Entity Recognition
- Ability to recognize TIME (time) entities in text  
- Ability to recognize LOCATION (location) entities in text  
- Ability to recognize PERSON (person) entities in text  
- Ability to recognize JOB (occupation) entities in text  
- Ability to recognize ORGANIZATION (organization) entities in text  
- Ability to return entity positions (start and end indices) in text  

### Text Summarization & Keyword Extraction
- Ability to extract keywords from text using TextRank algorithm  
- Ability to specify the number of keywords to extract  
- Ability to filter stopwords during keyword extraction  
- Ability to specify allowed POS tags for keyword extraction  
- Ability to return keywords with their corresponding weights  
- Ability to extract key phrases (sentences) from text using TextRank algorithm  
- Ability to specify the number of key phrases to extract  

### Sentiment Analysis
- Ability to perform sentiment analysis trained on e-commerce review data  
- Ability to return both negative and positive sentiment probabilities  
- Ability to analyze sentiment using RoBERTa fine-tuned model  

### Text to Pinyin Conversion
- Ability to convert Chinese text to pinyin using Trie structure  
- Ability to return pinyin as a list of syllables  

### Chinese Character Radical Extraction
- Ability to extract Chinese character radicals (偏旁部首) using HashMap  
- Ability to return radicals as a list  

### Spell Checking & Text Correction
- Ability to detect spelling errors in Chinese text using Detector + Corrector approach  
- Ability to return error positions and error words  
- Ability to provide correction suggestions for detected errors  
- Ability to specify the number of correction suggestions to return  
- Ability to return suggestion weights for ranking corrections  

### Sentence Vector & Similarity Computation
- Ability to transform sentences into vector representations  
- Ability to calculate similarity between two texts or vectors  
- Ability to find most similar documents from a list given a query  
- Ability to select genre-specific models (通用/金融/国际) for different domains  
- Ability to configure maximum input text length  
- Ability to return top-k most similar documents  

### Parallel Processing
- Ability to process texts in parallel using custom callback functions  
- Ability to configure the number of parallel jobs  
- Ability to use parallel processing with any xmnlp function  

### Model Configuration & Deployment
- Ability to configure model paths using environment variables  
- Ability to configure model paths programmatically  
- Ability to use ONNX runtime for efficient model inference  
- Ability to run on multiple operating systems (Linux, Windows, Mac)  

## Technical Constraints

### Programming Language and Version
- The repository must use **Python 3.6, 3.7, or 3.8** as the primary programming language  

### Core Dependencies
- The repository must use **tokenizers** library for BERT WordPiece tokenization  

- The repository must use **scikit-learn** for machine learning utilities (KDTree for similarity search)  

- The repository must use **numpy** for array operations and numerical processing  

- The repository must use **onnxruntime version 1.9.0** specifically for ONNX model inference  

### Model Architecture and Inference
- All neural network models must use **ONNX format** for model serialization  

- All model inference must run on **CPU only** (using CPUExecutionProvider), with no GPU/CUDA dependency  

- Lexical analysis (word segmentation, POS tagging, NER) must use **RoBERTa + CRF** architecture  

### Operating System Support
- The repository must support **Linux, Windows, and macOS** operating systems  

### Model Distribution and Configuration
- Model weights must be **distributed separately** from the PyPI package and downloaded by users  

- Users must configure the model path using either the **XMNLP_MODEL environment variable** or the **set_model() function**  

### Architecture Patterns
- All model modules must implement **thread-safe lazy loading** with singleton pattern using threading.Lock  

### Language Support
- Deep learning models (deep_seg, deep_tag) must support **simplified Chinese only**, not traditional Chinese  

- All file operations must use **UTF-8 encoding**  

### Sequence Length Constraints
- Lexical analysis models must handle a **maximum sequence length of 512 tokens**  

- Sentiment analysis models must use a **maximum sequence length of 150 tokens**  

- Spell checker must raise ValueError when text exceeds **512 tokens**  

### Data Structures and Algorithms
- Pinyin conversion must use **Trie (prefix tree)** data structure for character-to-pinyin mapping  

- Radical extraction must use **HashMap** data structure  

- Keyword and keyphrase extraction must use **TextRank algorithm**  

## Requirements

### Dependencies

- `tokenizers` - Fast tokenization library for NLP models
- `scikit-learn` - Machine learning library for Python
- `numpy` - Fundamental package for numerical computing
- `onnxruntime==1.9.0` - ONNX Runtime inference engine  

### Development Dependencies

- `pytest` - Testing framework
- `pytest-cov` - Test coverage plugin for pytest
- `flake8` - Python code linter and style checker
- `langml` - Language modeling library  

## Usage

### Installation

Install the latest version of xmnlp:
```bash
pip install -U xmnlp
```

For users in China (with mirror):
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U xmnlp
```  

### Model Setup

After installation, download the model weights and configure the model path.

**Method 1: Environment Variable (Recommended)**
```bash
export XMNLP_MODEL=/path/to/xmnlp-models
```

**Method 2: In Python Code**
```python
import xmnlp
xmnlp.set_model('/path/to/xmnlp-models')
```  

### Basic Usage Examples

**Chinese Word Segmentation:**
```python
import xmnlp
text = """xmnlp 是一款开箱即用的轻量级中文自然语言处理工具🔧。"""
print(xmnlp.seg(text))
# ['xmnlp', '是', '一款', '开箱', '即用', '的', '轻量级', '中文', '自然语言', '处理', '工具', '🔧', '。']
```  

**Part-of-Speech Tagging:**
```python
import xmnlp
text = """xmnlp 是一款开箱即用的轻量级中文自然语言处理工具🔧。"""
print(xmnlp.tag(text))
# [('xmnlp', 'eng'), ('是', 'v'), ('一款', 'm'), ...]
```  

**Named Entity Recognition:**
```python
import xmnlp
text = "现任美国总统是拜登。"
print(xmnlp.ner(text))
# [('美国', 'LOCATION', 2, 4), ('总统', 'JOB', 4, 6), ('拜登', 'PERSON', 7, 9)]
```  

### Advanced Usage Examples

**Keyword Extraction:**
```python
import xmnlp
text = """自然语言处理: 是人工智能和语言学领域的分支学科。..."""
print(xmnlp.keyword(text))
```  

**Sentiment Analysis:**
```python
import xmnlp
text = "这本书真不错，下次还要买"
print(xmnlp.sentiment(text))
# (0.02727833203971386, 0.9727216958999634)
```  

**Text to Pinyin Conversion:**
```python
import xmnlp
text = "自然语言处理"
print(xmnlp.pinyin(text))
# ['Zi', 'ran', 'yu', 'yan', 'chu', 'li']
```  

**Spell Checking:**
```python
import xmnlp
text = "不能适应体育专业选拔人材的要求"
print(xmnlp.checker(text))
# {(11, '材'): [('才', 1.585...), ('材', 1.000...), ...]}
```  

**Sentence Vector and Similarity:**
```python
from xmnlp.sv import SentenceVector

query = '我想买手机'
docs = ['我想买苹果手机', '我喜欢吃苹果']

sv = SentenceVector(genre='通用')
print('similarity:', sv.similarity(query, docs[0]))
print('most similar doc:', sv.most_similar(query, docs))
```  

**Custom Dictionary for Segmentation:**
```python
from xmnlp.lexical.tokenization import Tokenization

# Initialize tokenizer with custom dictionary
tokenizer = Tokenization(user_dict_path, detect_new_word=True)

# Segmentation
tokenizer.seg(texts)
# POS tagging
tokenizer.tag(texts)
```  

**Parallel Processing:**
```python
from functools import partial
import xmnlp
from xmnlp.utils import parallel_handler

seg_parallel = partial(parallel_handler, xmnlp.seg)
print(seg_parallel(texts))
``` 

## Terms/Concepts Explanation

**Chinese Word Segmentation**: The process of dividing Chinese text into individual words, as Chinese text doesn't use spaces between words. xmnlp implements this using reverse maximum matching combined with a RoBERTa + CRF model for new word identification.  

**Part-of-Speech (POS) Tagging**: The task of assigning grammatical categories (noun, verb, adjective, etc.) to each word in a text. xmnlp provides POS tagging capabilities through both fast dictionary-based and deep learning-based approaches.  

**Named Entity Recognition (NER)**: A technique to identify and classify named entities in text into predefined categories such as TIME, LOCATION, PERSON, JOB, and ORGANIZATION.  

**RoBERTa + CRF**: A neural network architecture combining RoBERTa (a robustly optimized BERT pretraining approach) with Conditional Random Fields (CRF) for sequence labeling tasks. This model is fine-tuned for Chinese lexical analysis including segmentation, POS tagging, and NER.  

**ONNX (Open Neural Network Exchange)**: A cross-platform format for representing machine learning models. xmnlp uses ONNX Runtime for efficient model inference across all its neural network-based features.  

**BIO Tagging Scheme**: A sequence labeling format where B (Begin) marks the start of an entity, I (Inside) marks continuation, and O (Outside) marks non-entity tokens. This scheme is used internally to decode named entities from model predictions.

**Reverse Maximum Matching**: A dictionary-based word segmentation algorithm that processes text from right to left, matching the longest possible words from a vocabulary. Used in `fast_seg` and `fast_tag` functions for high-speed tokenization without deep learning.  

**TextRank Algorithm**: A graph-based ranking algorithm adapted from PageRank for text analysis. Used in xmnlp for both keyword extraction (word-level) and keyphrase extraction (sentence-level) through iterative importance scoring.  

**BM25 (Best Matching 25)**: A probabilistic ranking algorithm used to calculate similarity between documents based on term frequency and inverse document frequency. In xmnlp, BM25 powers the sentence similarity calculation in TextRank-based keyphrase extraction.  

**Trie Data Structure**: A tree-based data structure for efficient prefix matching and retrieval. Used in the pinyin conversion module to map Chinese characters to their phonetic representations.  

**Spell Checking (Detector + Corrector)**: A two-stage approach where a Detector model identifies potentially incorrect characters, and a Corrector model suggests replacements based on phonetic similarity and context.  

**Sentiment Analysis**: Classification of text into positive or negative sentiment categories. xmnlp's sentiment model is trained on e-commerce review data and returns probability scores for both negative and positive sentiment.  

**Sentence Vector/Embeddings**: Dense numerical representations of sentences that capture semantic meaning. xmnlp provides sentence embeddings for similarity calculation and supports different domains including general, finance, and international.  

**Custom Dictionary**: User-provided vocabulary files that allow xmnlp to recognize domain-specific terms. Supports formats compatible with both xmnlp and jieba segmentation libraries.  

**Radical**: The semantic or phonetic component of a Chinese character used for dictionary organization. xmnlp provides extraction of character radicals using a HashMap-based lookup.  

