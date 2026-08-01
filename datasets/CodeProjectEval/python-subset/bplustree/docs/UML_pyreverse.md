## UML Class Diagram
```mermaid
classDiagram
  class Entry {
    dump()* bytes
    load(data: bytes)*
  }
  class Record {
    key : NoneType
    length
    overflow_page : NoneType, Optional[int]
    value : NoneType, Optional[bytes]
    dump() bytes
    load(data: bytes)
  }
  class Reference {
    after : NoneType
    before : NoneType
    key : NoneType
    length
    dump() bytes
    load(data: bytes)
  }
  class FakeCache {
    clear()*
    get(k)*
  }
  class FileMemory {
    last_page : int
    next_available_page
    read_transaction
    write_transaction
    close()
    get_metadata() tuple
    get_node(page: int)
    get_page(page: int) bytes
    perform_checkpoint(reopen_wal)
    set_metadata(root_node_page: int, tree_conf: TreeConf)
    set_node(node: Node)
    set_page(page: int, data: bytes)
  }
  class FrameType {
    name
  }
  class ReachedEndOfFile {
  }
  class ReadTransaction {
  }
  class WAL {
    FRAME_HEADER_LENGTH : int
    filename
    needs_recovery : bool
    checkpoint()
    commit()
    get_page(page: int) Optional[bytes]
    rollback()
    set_page(page: int, page_data: bytes)
  }
  class WriteTransaction {
  }
  class InternalNode {
    entries : list
    max_children
    min_children
  }
  class LeafNode {
    entries : list
    max_children
    min_children
  }
  class LonelyRootNode {
    max_children
    min_children : int
    parent
    convert_to_leaf()
  }
  class Node {
    biggest_entry
    biggest_key
    can_add_entry
    can_delete_entry
    entries : list
    max_children : int
    min_children : int
    next_page : NoneType, Optional[int]
    num_children
    page : Optional[int]
    parent : str
    smallest_entry
    smallest_key
    dump() bytearray
    from_page_data(tree_conf: TreeConf, data: bytes, page: int) 'Node'
    get_entry(key) Entry
    insert_entry(entry: Entry)
    insert_entry_at_the_end(entry: Entry)
    load(data: bytes)
    pop_smallest() Entry
    remove_entry(key)
    split_entries() list
  }
  class RecordNode {
    num_children
  }
  class ReferenceNode {
    num_children
    insert_entry(entry: 'Reference')
  }
  class RootNode {
    max_children
    min_children : int
    parent
    convert_to_internal()
  }
  class DatetimeUTCSerializer {
    deserialize(data: bytes) datetime
    serialize(obj: datetime, key_size: int) bytes
  }
  class IntSerializer {
    deserialize(data: bytes) int
    serialize(obj: int, key_size: int) bytes
  }
  class Serializer {
    deserialize(data: bytes)* object
    serialize(obj: object, key_size: int)* bytes
  }
  class StrSerializer {
    deserialize(data: bytes) str
    serialize(obj: str, key_size: int) bytes
  }
  class UUIDSerializer {
    deserialize(data: bytes) UUID
    serialize(obj: UUID, key_size: int) bytes
  }
  class BPlusTree {
    InternalNode : partial
    LeafNode : partial
    LonelyRootNode : partial
    Record : partial
    Reference : partial
    RootNode : partial
    keys
    batch_insert(iterable: Iterable)
    checkpoint()
    close()
    get(key, default) bytes
    insert(key, value: bytes, replace)
    items(slice_: Optional[slice]) Iterator[tuple]
    values(slice_: Optional[slice]) Iterator[bytes]
  }
  Record --|> Entry
  Reference --|> Entry
  InternalNode --|> ReferenceNode
  LeafNode --|> RecordNode
  LonelyRootNode --|> RecordNode
  RecordNode --|> Node
  ReferenceNode --|> Node
  RootNode --|> ReferenceNode
  DatetimeUTCSerializer --|> Serializer
  IntSerializer --|> Serializer
  StrSerializer --|> Serializer
  UUIDSerializer --|> Serializer
```

## UML Package Diagram
```mermaid
classDiagram
  class bplustree {
  }
  class const {
  }
  class entry {
  }
  class memory {
  }
  class node {
  }
  class serializer {
  }
  class tree {
  }
  class utils {
  }
  bplustree --> const
  bplustree --> serializer
  bplustree --> tree
  entry --> const
  memory --> const
  memory --> node
  node --> const
  node --> entry
  serializer --> const
  tree --> const
  tree --> entry
  tree --> memory
  tree --> node
  tree --> serializer
```