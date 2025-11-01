## UML Class Diagram

```mermaid
classDiagram
  class BaseModel {
    sess
    predict()*
  }
  class CheckerDecoder {
    corrector
    detector
    mask_id
    tokenizer
    predict(text, suggest, k, max_k)
  }
  class CorrectorModel {
    predict(token_ids: np.ndarray, segment_ids: np.ndarray) np.ndarray
  }
  class DetectorModel {
    predict(token_ids: np.ndarray, segment_ids: np.ndarray) np.ndarray
  }
  class Lexical {
    id2label
    lexical_model
    tokenizer
    bio_decode(labels: List[str]) List[Tuple[int, int, str]]
    predict(text: str, with_position: bool) List[Union[Tuple[str, str], Tuple[str, str, int, int]]]
    predict_one(text: str, base_position: int) List[Tuple[str, str, int, int]]
    transform(data: List[Tuple[str, str, int, int]], with_position: bool) List[Union[Tuple[str, str], Tuple[str, str, int, int]]]
  }
  class LexicalModel {
    predict(token_ids: np.ndarray, segment_ids: np.ndarray) np.ndarray
  }
  class Tokenization {
    max_word_length : int
    new_word_kernel
    word2tag : dict
    load_vocab(fpaths: List[str]) dict
    seg(doc: str) List[str]
    tag(doc: str) List[Tuple[str, str]]
  }
  class Module {
    filelist(fpath)
    load(fname, iszip)
    save(fname, iszip)
  }
  class Pinyin {
    trie
    train(fpath)
    translate(text)
  }
  class Radical {
    dictionary : dict
    radical(char)
    train(fpath)
  }
  class Sentiment {
    sentiment_model
    tokenizer
    predict(text: str) Tuple[float, float]
  }
  class SentimentModel {
    predict(token_ids: np.ndarray, segment_ids: np.ndarray) np.ndarray
  }
  class KeywordTextRank {
    PR : ndarray
    d : float
    edge : dict
    idx_dict : dict
    iters : int
    matrix : ndarray
    vertex : set
    window : int
    word_idx : dict
    words
    build_edge()
    build_matrix()
    calc_pr()
    topk(k)
  }
  class TextRank {
    N
    bm25
    d : float
    docs
    iters : int
    min_diff : float
    vertex : list
    weight : list
    weight_sum : list
    build()
    calc_pr()
    topk(k)
  }
  class SentenceVector {
    genre : str
    sv_model
    tokenizer
    most_similar(query: str, docs: List[str], k: int) List[Tuple[str, float]]
    similarity(x: Union[str, np.ndarray], y: Union[str, np.ndarray]) float
    transform(text: str) np.ndarray
  }
  class SentenceVectorModel {
    predict(token_ids: np.ndarray, segment_ids: np.ndarray) np.ndarray
  }
  class PinyinTrainer {
    pinyin(srcfile, outfile)
  }
  class RadicalTrainer {
    radical(srcfile, outfile)
  }
  class SysTrainer {
    all()
  }
  class Trainer {
  }
  class BM25 {
    N
    avgdl
    b : float
    df : dict
    docs
    idf : dict
    k1 : float
    tf : list
    build()
    get_sims(doc)
    sim(doc, idx)
  }
  class Trie {
    root : dict
    add(key, val)
    find(sent, start)
    get(sent)
  }
  CorrectorModel --|> BaseModel
  DetectorModel --|> BaseModel
  LexicalModel --|> BaseModel
  Pinyin --|> Module
  Radical --|> Module
  SentimentModel --|> BaseModel
  SentenceVectorModel --|> BaseModel
  PinyinTrainer --|> Trainer
  RadicalTrainer --|> Trainer
  SysTrainer --|> Trainer
  CorrectorModel --* CheckerDecoder : corrector
  DetectorModel --* CheckerDecoder : detector
  LexicalModel --* Lexical : lexical_model
  SentimentModel --* Sentiment : sentiment_model
  SentenceVectorModel --* SentenceVector : sv_model
  BM25 --* TextRank : bm25
  Trie --* Pinyin : trie

```
## UML Package Diagram

```mermaid
classDiagram
  class xmnlp {
  }
  class base_model {
  }
  class checker {
  }
  class checker {
  }
  class config {
  }
  class path {
  }
  class lexical {
  }
  class lexical_model {
  }
  class tokenization {
  }
  class module {
  }
  class pinyin {
  }
  class pinyin {
  }
  class radical {
  }
  class radical {
  }
  class sentiment {
  }
  class sentiment_model {
  }
  class summary {
  }
  class textrank {
  }
  class sv {
  }
  class model {
  }
  class trainer {
  }
  class utils {
  }
  class bm25 {
  }
  class trie {
  }
  xmnlp --> xmnlp
  xmnlp --> checker
  xmnlp --> config
  xmnlp --> lexical
  xmnlp --> pinyin
  xmnlp --> radical
  xmnlp --> sentiment
  xmnlp --> summary
  xmnlp --> utils
  checker --> xmnlp
  checker --> checker
  checker --> config
  checker --> xmnlp
  checker --> base_model
  checker --> utils
  config --> config
  config --> path
  config --> utils
  lexical --> xmnlp
  lexical --> config
  lexical --> lexical_model
  lexical --> tokenization
  lexical_model --> base_model
  lexical_model --> utils
  tokenization --> path
  tokenization --> lexical
  pinyin --> config
  pinyin --> path
  pinyin --> pinyin
  pinyin --> module
  pinyin --> trie
  radical --> config
  radical --> path
  radical --> radical
  radical --> module
  sentiment --> xmnlp
  sentiment --> config
  sentiment --> sentiment_model
  sentiment_model --> base_model
  summary --> lexical
  summary --> textrank
  summary --> utils
  textrank --> bm25
  sv --> model
  model --> xmnlp
  model --> base_model
  model --> config
  trainer --> config
  trainer --> path
  trainer --> pinyin
  trainer --> radical

```

