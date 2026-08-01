# Architecture Design

Below is a text-based representation of the file tree.

``` bash
├── xmnlp
│   ├── base_model.py
│   ├── checker
│   │   ├── checker.py
│   │   └── __init__.py
│   ├── config
│   │   ├── __init__.py
│   │   └── path.py
│   ├── dict.big.txt
│   ├── __init__.py
│   ├── lexical
│   │   ├── __init__.py
│   │   ├── lexical_model.py
│   │   └── tokenization.py
│   ├── module.py
│   ├── pinyin
│   │   ├── __init__.py
│   │   ├── pinyin.pickle
│   │   └── pinyin.py
│   ├── radical
│   │   ├── __init__.py
│   │   ├── radical.pickle
│   │   └── radical.py
│   ├── sentiment
│   │   ├── __init__.py
│   │   └── sentiment_model.py
│   ├── stopword.txt
│   ├── summary
│   │   ├── __init__.py
│   │   └── textrank.py
│   ├── sv
│   │   ├── __init__.py
│   │   └── model.py
│   ├── trainer.py
│   └── utils
│       ├── bm25.py
│       ├── __init__.py
│       └── trie.py
```

`__init__.py` :

- `set_model(dirname: str)`: Sets the directory path for model files used by xmnlp. This function updates the global `MODEL_DIR` configuration variable to point to the specified directory.

- `set_stopword(fpath: str)`: Loads custom stopwords from a file and merges them with the system’s default stopwords. The file should contain one stopword per line. This function updates the global `SYS_STOPWORDS` configuration set.

- `keyword(text: str, k: int = 10, stopword: bool = True, allowPOS: Optional[List[str]] = None) -> List[Tuple[str, float]]`: Extracts top-k keywords from the input text based on statistical and linguistic features.  

- `keyphrase(text: str, k: int = 10, stopword: bool = False) -> List[str]`: Extracts top-k keyphrases (typically noun phrases or salient multi-word expressions) from the input Chinese text.  

`base_model.py` :

- `BaseModel(model_path: str)`: An abstract base class for machine learning models that loads an ONNX model from the specified file path using ONNX Runtime with CPU execution.

  - The instance attribute `sess` holds the ONNX Runtime inference session used for model predictions.

  - `predict()`: An abstract method that must be implemented by any subclass. It is intended to perform inference using the loaded ONNX model and return prediction results.

`module.py` :

- `filelist(self, fpath)`: A generator that yields file paths. If the input `fpath` is a directory, it recursively walks through the directory and yields the full path of each file; if it's a file, it simply yields the file path itself.

- `save(self, fname, iszip=True)`: Serializes and saves the object's attributes to a file. By default, it compresses the output using bzip2. Attributes listed in `__notsave__` are excluded from saving, unless `__onlysave__` is defined—in which case only attributes in `__onlysave__` are saved. Sets are converted to lists for serialization, and objects with a `__dict__` attribute are saved by their internal dictionary.

- `load(self, fname, iszip=True)`: Loads and restores the object's state from a saved file. It attempts to read a bzip2-compressed file first; if that fails (e.g., due to an `IOError`), it falls back to reading an uncompressed file. During loading, lists are converted back to sets if the target attribute was originally a set, and objects with a `__dict__` are restored by updating their internal dictionary.

`module.py`:

- `Module`: A base class providing serialization/deserialization utilities and file operations for other components in the project.

  - `filelist(fpath)`: Generator method that yields file paths. If the input path is a directory, it recursively walks through all files in the directory. If the input path is a file, it yields the single file path.

  - `save(fname, iszip=True)`: Serializes and saves the object's attributes to a file. Can save in either compressed (bz2) or uncompressed pickle format. Allows control over which attributes to save using `__onlysave__` and `__notsave__` lists.

  - `load(fname, iszip=True)`: Loads and deserializes object attributes from a file. Supports both compressed (bz2) and uncompressed pickle formats. Restores the object's state by updating its `__dict__` with saved values.

`trainer.py`:

- `Trainer()`: A base trainer class with no implemented functionality, serving as a parent class for specific model trainers.

- `PinyinTrainer()`: A subclass of `Trainer` that provides functionality for training pinyin models.

  - `pinyin(srcfile, outfile)`: Trains a pinyin model using the provided corpus file (`srcfile`) and saves the trained model to the specified output file (`outfile`). This method initializes a `Pinyin` instance, trains it on the corpus, and persists the model.

- `RadicalTrainer()`: A subclass of `Trainer` that provides functionality for training radical (Chinese character component) models.

  - `radical(srcfile, outfile)`: Trains a radical model using the given corpus file (`srcfile`) and saves the resulting model to `outfile`. It creates a `Radical` instance, trains it on the input data, and serializes the model.

- `SysTrainer()`: A subclass of `Trainer` that orchestrates the training of all supported models in the system.

  - `all()`: A convenience method that trains all supported models (currently pinyin and radical) using their default corpus and model paths defined in the global configuration (`xmnlp.config.path`). It sequentially invokes the individual trainers and logs the overall progress.

`checker/__init.py__` :

- `load_checker(reload: bool = False)`: Lazily loads the spell checker model into memory. Ensures thread-safe initialization using a lock. If the model directory is not configured, raises a `ValueError`. If `reload` is `True` or the checker hasn't been loaded yet, it instantiates a new `CheckerDecoder` from the model path.

- `spellcheck(text: str, suggest: bool = True, k: int = 5, max_k: int = 200)`: Performs spell checking on the input text.  If `suggest` is `True`, returns a dictionary mapping each detected error (represented as a tuple of `(position, incorrect_token)`) to a list of up to `k` suggested corrections with their scores (as `(suggestion, score)` tuples), limited by `max_k` total candidates considered internally.  If `suggest` is `False`, returns a list of detected errors as `(position, incorrect_token)` tuples.  Internally calls `load_checker()` to ensure the model is loaded before prediction.

`checker/checker.py` :

- `DetectorModel(BaseModel)`: A model wrapper class for the detector ONNX model that predicts token-level error probabilities.

  - `predict(token_ids: np.ndarray, segment_ids: np.ndarray) -> np.ndarray`: Runs inference on the detector model using input token and segment IDs, returning sigmoid probabilities indicating whether each token is likely incorrect.

- `CorrectorModel(BaseModel)`: A model wrapper class for the corrector ONNX model that predicts token-level correction candidates.

  - `predict(token_ids: np.ndarray, segment_ids: np.ndarray) -> np.ndarray`: Runs inference on the corrector model using input token and segment IDs, returning logits over the vocabulary for masked token prediction.

- `CheckerDecoder`: A spell checker decoder that combines detection and correction models with a BERT WordPiece tokenizer to identify and suggest corrections for misspelled tokens.

  - `__init__(self, model_dir)`: Initializes the detector, corrector, and tokenizer from the specified model directory and determines the [MASK] token ID from the vocabulary.

  - `predict(self, text, suggest=False, k=5, max_k=200)`: Performs spell checking on the input text. If `suggest=False`, returns positions and tokens of detected errors. If `suggest=True`, also generates up to `k` correction suggestions per error token, ranked by a combined score of model probability and pinyin similarity.

`lexical/__init__.py` :

- `load_lexical(reload: bool = False)`: Lazily loads the lexical model from the configured model directory. Ensures thread-safe initialization using a lock. If `reload` is True or the model hasn't been loaded yet, it instantiates the `Lexical` model from the path `os.path.join(config.MODEL_DIR, 'lexical')`. Raises a `ValueError` if `config.MODEL_DIR` is not set.

- `deep_seg(doc: str)`: Performs fine-grained word segmentation on the input text using the deep lexical model. Returns a list of segmented words.

- `deep_tag(doc: str)`: Performs part-of-speech tagging on the input text using the deep lexical model. Returns a list of tuples, each containing a word and its corresponding POS tag. Standardizes model-specific tags to human-readable labels using `TAG_MAP`.

- `ner(doc: str)`: Performs named entity recognition on the input text. Supports both rule-based entities (EMAIL, URL, BOOK) and model-predicted entities (ORGANIZATION, TIME, JOB, PERSON, LOCATION). Returns a list of tuples in the format `(entity_text, entity_type, start_index, end_index)`, sorted by occurrence position in the text.

`lexical/lexical_model.py` :

- `LexicalModel(model_path: str)`: A model wrapper that loads an ONNX lexical model and provides a prediction interface.

  - `predict(token_ids: np.ndarray, segment_ids: np.ndarray) -> np.ndarray`: Runs inference using the ONNX lexical model, taking token and segment IDs as input and returning model logits for sequence labeling.

- `Lexical(model_dir: Optional[str] = None)`: A lexical analysis module for Chinese named entity recognition, using a BERT-based tokenizer and an ONNX-backed sequence labeling model.

  - `predict_one(text: str, base_position: int = 0) -> List[Tuple[str, str, int, int]]`: Performs named entity recognition on a single input text segment (up to 512 tokens), returning detected entities along with their types and character-level start/end positions adjusted by base_position.

  - `bio_decode(labels: List[str]) -> List[Tuple[int, int, str]]`: Decodes a sequence of BIO-formatted labels into contiguous entity spans, each represented by start index, end index, and entity type.

  - `transform(data: List[Tuple[str, str, int, int]], with_position: bool) -> List[Union[Tuple[str, str], Tuple[str, str, int, int]]]`: Formats the prediction results based on the with_position flag—includes character positions if True, otherwise returns only the word and its label.

  - `predict(text: str, with_position: bool = False) -> List[Union[Tuple[str, str], Tuple[str, str, int, int]]]`: Predicts named entities in the input text. If the text exceeds the maximum length (512 tokens), it splits the text into sentence-like segments, processes each segment, and merges the results while preserving global character positions.

`lexical/tokenization.py` :

- `Tokenization(user_vocab_path: Optional[str] = None, detect_new_word: bool = True)`: A class for Chinese word segmentation that supports user-defined dictionaries and optional detection of out-of-vocabulary (new) words using a deep learning-based tagger.

  - `seg(doc: str) -> List[str]`: Segments the input document into a list of word tokens by internally calling the `tag` method and extracting only the word strings.
  
  - `tag(doc: str) -> List[Tuple[str, str]]`: Performs word segmentation and part-of-speech tagging on the input document. It uses a maximum-matching algorithm with a backward scan, merges consecutive English letters and digits into single tokens labeled as 'eng', and optionally applies a deep learning-based new word detection step for sequences of single-character tokens.
  
  - `load_vocab(fpaths: List[str]) -> Tuple[dict, int]`: Loads vocabulary files (system and optional user-defined) into a dictionary mapping words to their part-of-speech tags and returns the maximum word length found, used to constrain segmentation window size.

`pinyin/__init__.py` :

- `loader()`: A thread-safe lazy-loading utility function that initializes the global Pinyin model instance only once, loading it from the configured model path when first needed.

- `translate(text: str) -> List[str]`: Converts Chinese characters in the input text to their corresponding pinyin representations, preserving non-Chinese segments (such as English words or punctuation) as-is. Returns a flat list of pinyin syllables and original non-Chinese tokens.

`pinyin.py` :

- `Pinyin()`: A class that provides Chinese character to pinyin conversion using a trie-based dictionary model trained from external data files.

  - `train(fpath)`: Trains the pinyin model by loading mapping data from text files in the specified path, where each line contains a Chinese word followed by its pinyin pronunciations; builds an internal trie structure for efficient lookup.
  
  - `translate(text) -> List[str]`: Converts a string of Chinese characters into a flat list of corresponding pinyin syllables using the trained trie model; returns pinyin tokens in sequence matching the input text.
  
  - The instance attribute `trie` is a Trie object that stores the mapping from Chinese character sequences to their pinyin pronunciations.

`radical/__init__.py` :

- `loader()`: A thread-safe lazy-loading utility function that initializes the global Radical model instance only once, loading it from the configured model path when first needed.

- `radical(text: str) -> List[str]`: Returns a list of radical components corresponding to each Chinese character in the input text. If the input is empty, returns None. Uses a preloaded Radical model to look up the radical for each character.

`radical/radical.py` :

- `Radical()`: A class that maps Chinese characters to their corresponding radicals using a dictionary-based lookup model trained from external data files.

  - `train(fpath)`: Trains the radical model by reading CSV-formatted files from the specified path, where each line contains a Chinese character and its radical separated by a comma; populates the internal dictionary for lookup.
  
  - `radical(char) -> str`: Returns the radical of the given Chinese character by looking it up in the internal dictionary; returns None if the character is not found.
  
  - The instance attribute `dictionary` is a dict that stores mappings from Chinese characters (str) to their radicals (str).

`sentiment/__init__.py` :

- `load_sentiment(reload: bool = False)`: A thread-safe utility function that lazily loads the global sentiment analysis model from the configured model directory; supports reloading the model if `reload=True`.

- `sentiment(doc: str) -> Tuple[float, float]`: Performs sentiment classification on the input document and returns a tuple containing the probabilities of negative and positive sentiment, respectively.

`sentiment/sentiment_model.py` :

- `SentimentModel(model_path: str)`: A wrapper class for an ONNX-based sentiment classification model that inherits from `BaseModel` and provides a prediction interface using token and segment IDs.

  - `predict(token_ids: np.ndarray, segment_ids: np.ndarray) -> np.ndarray`: Runs inference on the ONNX sentiment model using input token and segment IDs, returning the softmax probabilities for sentiment classes.

- `Sentiment(model_dir: str)`: A high-level sentiment analysis class that integrates a BERT-style tokenizer and an ONNX runtime model to classify input text into negative and positive sentiment probabilities.

  - `predict(text: str) -> Tuple[float, float]`: Tokenizes the input text using a BERT WordPiece tokenizer, prepares model inputs, and returns a tuple of predicted probabilities for negative and positive sentiment, respectively.
  
  - The instance attribute `sentiment_model` is a `SentimentModel` object that wraps the ONNX runtime session for inference.
  
  - The instance attribute `tokenizer` is a `BertWordPieceTokenizer` configured with the model’s vocabulary and truncation to a maximum length of 150 tokens.

`summary/__init__.py` :

- `keyword(text: str, k: int = 10, stopword: Optional[List[str]] = None, allowPOS: Optional[List[str]] = None) -> List[Tuple[str, float]]`: Extracts top-k keywords from the input text using a TextRank-based algorithm. Filters tokens by user-provided stopwords and allowed part-of-speech tags, then returns keywords with their importance weights.

- `keyphrase(text: str, k: int = 10, stopword: Optional[List[str]] = None) -> List[str]`: Extracts top-k key sentences (keyphrases) from the input text using a sentence-level TextRank algorithm. Splits text into sentences, removes stopwords, and returns the most representative sentences as strings.

`summary/textrank.py` :

- `KeywordTextRank(words, window=5, alpha=0.85, iters=300)`: A class that implements the TextRank algorithm for keyword extraction from a list of words, using a co-occurrence graph within a sliding window.

  - The instance attribute `words` stores the input list of words.
  - The instance attribute `vertex` is a set of unique words used as graph nodes.
  - The instance attribute `edge` maps each word to its neighboring words within the window.
  - The instance attribute `PR` holds the final PageRank scores for each word after convergence.
  
  - `build_edge()`: Constructs the co-occurrence edges between words based on a sliding window around each word.
  
  - `build_matrix()`: Builds a normalized adjacency matrix from the co-occurrence graph for use in PageRank computation.
  
  - `calc_pr()`: Computes PageRank scores iteratively using the transition matrix and damping factor.
  
  - `topk(k)`: Returns the top-k keywords ranked by their PageRank scores in descending order.

- `TextRank(docs, alpha=0.85, min_diff=1e-2, iters=500)`: A class that implements the TextRank algorithm for document ranking (e.g., extractive summarization), where document similarity is computed using BM25.

  - The instance attribute `docs` stores the input list of documents (typically sentences or paragraphs).
  - The instance attribute `bm25` is a BM25 model trained on the input documents for similarity scoring.
  - The instance attribute `vertex` holds the PageRank score for each document after convergence.
  
  - `build()`: Precomputes pairwise BM25 similarity scores between all documents and initializes necessary structures for ranking.
  
  - `calc_pr()`: Iteratively updates document PageRank scores based on BM25-weighted transitions until convergence or maximum iterations.
  
  - `topk(k)`: Returns the indices of the top-k highest-ranked documents according to their PageRank scores.

`sv/model.py` :

- `SentenceVectorModel(model_path: str)`: A wrapper class for an ONNX-based sentence embedding model that computes sentence vectors from token and segment IDs.

  - `predict(token_ids: np.ndarray, segment_ids: np.ndarray) -> np.ndarray`: Runs inference on the ONNX model using input token and segment IDs, returning the corresponding sentence embedding vector.

- `SentenceVector(model_dir: Optional[str] = None, genre: str = '通用', max_length: int = 512)`: A high-level interface for generating and comparing sentence embeddings using a pre-trained ONNX model, supporting domain-specific embeddings (e.g., general, finance, international).

  - The instance attribute `genre` specifies the domain type used as a prefix during encoding (one of ['通用', '金融', '国际']).
  - The instance attribute `sv_model` is the underlying ONNX model instance for embedding computation.
  - The instance attribute `tokenizer` is a BERT WordPiece tokenizer configured with truncation and vocabulary from the model directory.
  
  - `transform(text: str) -> np.ndarray`: Encodes the input text into a fixed-dimensional sentence embedding vector by prepending the genre tag and tokenizing with BERT-style formatting.
  
  - `similarity(x: Union[str, np.ndarray], y: Union[str, np.ndarray]) -> float`: Computes the cosine similarity between two sentences (or their precomputed embeddings).
  
  - `most_similar(query: str, docs: List[str], k: int = 1, **kwargs) -> List[Tuple[str, float]]`: Finds the top-k most similar documents to a query sentence using KDTree for efficient nearest neighbor search; returns a list of (document, distance) tuples (note: distance is Euclidean, not similarity).

`utils/__init__.py` :

- `split_text(doc: str) -> List[str]`: Splits a multi-line document into individual sentences using line breaks and common Chinese sentence delimiters (e.g., ，。？！；), stripping whitespace and skipping empty segments.

- `filelist(path: str) -> Generator[str, None, None]`: Recursively yields file paths from a given directory (or returns the path itself if it's a file), traversing all subdirectories.

- `load_stopword(fpath: str) -> List[str]`: Loads stopwords from one or more files (supporting directories) into a list, reading each line as a stopword while ignoring empty lines.

- `rematch(offsets)`: Reconstructs character-level token-to-original-text mappings from BERT tokenizer offsets by converting each [start, end) offset pair into a list of character indices.

- `topK(matrix, K, axis=1)`: Efficiently computes the top-K values and their indices along a specified axis of a NumPy array using argpartition and argsort for partial sorting.

- `parallel_handler(callback: Callable, texts: List[str], n_jobs: int = 2, **kwargs) -> Generator[List[Any], None, None]`: Applies a callback function to a list of texts in parallel using a thread pool, optionally passing additional keyword arguments via functools.partial; yields results in order.

`utils/bm25.py` :

- `BM25(docs, k1=1.5, b=0.75)`: A class that implements the BM25 (Best Match 25) ranking function for computing relevance scores between a query document and a corpus of documents.

  - The instance attribute `N` is the total number of documents in the corpus.
  - The instance attribute `avgdl` is the average document length in the corpus.
  - The instance attribute `docs` stores the original list of tokenized documents.
  - The instance attribute `tf` is a list of term frequency dictionaries, one per document.
  - The instance attribute `df` maps each term to its document frequency (number of documents containing the term).
  - The instance attribute `idf` maps each term to its inverse document frequency score computed using BM25’s IDF formula.
  - The instance attributes `k1` and `b` are BM25 tuning parameters controlling term frequency saturation and document length normalization, respectively.
  
  - `build()`: Precomputes term frequencies (TF), document frequencies (DF), and inverse document frequencies (IDF) for all terms in the corpus.
  
  - `sim(doc, idx) -> float`: Computes the BM25 similarity score between a query document (list of terms) and the document at index `idx` in the corpus.
  
  - `get_sims(doc) -> List[float]`: Returns a list of BM25 similarity scores between the query document and every document in the corpus.

`utils/trie.py` :

- `Trie()`: A prefix tree (Trie) data structure that supports efficient string prefix matching and value retrieval, with logic to handle ambiguous matches by selecting the most frequent associated value.

  - The instance attribute `root` is a nested dictionary representing the root of the Trie.
  
  - `add(key, val)`: Inserts a key (sequence of characters) into the Trie and associates it with a given value `val`.
  
  - `find(sent, start=0) -> Optional[Tuple[str, Any]]`: Searches the Trie for the longest match starting at position `start` in the input string `sent`; returns a tuple of (matched substring, associated value). If no exact terminal match is found, it attempts to resolve ambiguity by selecting the most frequent pinyin-like value among immediate children.
  
  - `get(sent) -> List[Any]`: Tokenizes the input string `sent` by greedily matching longest prefixes in the Trie and returns a list of associated values for all matched segments.
