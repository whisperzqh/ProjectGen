# PRD Document for bplustree

## Introduction

The purpose of this project is to develop a disk-based B+ tree data structure implementation in C that provides persistent storage and efficient retrieval of key-value pairs. The repository offers a complete B+ tree library designed for applications requiring scalable, disk-persistent indexed data storage, capable of handling millions or billions of entries. This tool is designed for developers and systems programmers who need a reliable, high-performance indexing structure with persistent storage capabilities.

## Goals

The objective of this project is to provide a robust, disk-based B+ tree implementation with efficient search, insertion, and deletion operations, memory caching to reduce disk I/O, and free block management for disk space optimization. The library should handle persistent storage across program restarts, support range queries, and maintain B+ tree properties through automatic node splitting and merging.

## Features and Functionalities

The following features and functionalities are expected in the project:

### Core Operations
- Ability to insert key-value pairs into the tree with automatic node splitting when nodes become full
- Ability to search for values by key with O(log n) time complexity using binary search within nodes 
- Ability to delete key-value pairs with automatic node merging and borrowing when nodes become too empty
- Ability to perform range queries to retrieve sequences of values within a key range

### Persistence and Storage
- Ability to store B+ tree nodes persistently on disk in a binary file format
- Ability to maintain metadata in a separate boot file including root offset, block size, file size, and free blocks list
- Ability to configure block size (must be power of 2) that determines maximum entries per node
- Ability to track and reuse deleted blocks through a free block list to prevent disk fragmentation

### Memory Management
- Ability to cache frequently accessed nodes in memory using a fixed-size cache array (MIN_CACHE_NUM = 5)
- Ability to borrow and return cache slots dynamically via `cache_refer()` and `cache_defer()` functions
- Ability to flush modified nodes back to disk to ensure data persistence

### Tree Structure Management
- Ability to maintain both leaf nodes (storing key-value pairs) and non-leaf nodes (storing key-child pointer pairs)
- Ability to automatically split nodes when they exceed capacity during insertion 
- Ability to automatically merge or borrow from sibling nodes when nodes become too sparse during deletion
- Ability to maintain linked list structure between leaf nodes for efficient range queries

## Technical Constraints

- The repository should use C as the primary programming language
- The repository should implement a classic disk-based B+ tree design with configurable block sizes
- The repository should use binary file I/O for persistent storage
- Block sizes must be powers of 2 and large enough to accommodate at least one node structure

## Requirements

### Core Data Structures

The implementation uses several key data structures defined in `lib/bplustree.h`:

- `bplus_tree` - Main tree structure containing cache array, file descriptor, root offset, and free blocks list
- `bplus_node` - Node structure with self/parent/prev/next offsets, type indicator, and children count
- `free_block` - Structure for tracking deleted blocks available for reuse
- `list_head` - Doubly-linked list structure for managing free blocks

### API Functions

The library provides the following public API (defined in `lib/bplustree.h`):

- `bplus_tree_init(filename, block_size)` - Initialize a B+ tree from file or create new one 
- `bplus_tree_deinit(tree)` - Clean up tree resources and save metadata to boot file
- `bplus_tree_get(tree, key)` - Retrieve value associated with key
- `bplus_tree_put(tree, key, data)` - Insert or delete key-value pair (data = 0 for deletion)
- `bplus_tree_get_range(tree, key1, key2)` - Retrieve values within key range
## Installation
```
pip install bplustree
```

## Usage

### Basic Operations

Initialize a B+ tree:
```c
struct bplus_tree *tree = bplus_tree_init("mydata.db", 4096);
```

Insert key-value pairs:
```c
bplus_tree_put(tree, 42, 12345);
```

Search for a value:
```c
long value = bplus_tree_get(tree, 42);
```

Delete a key:
```c
bplus_tree_put(tree, 42, 0);  // data = 0 indicates deletion
```

Clean up:
```c
bplus_tree_deinit(tree);
```

### Demo Application

The repository includes a demo application in `tests/bplustree_demo.c` that provides an interactive command-line interface :

- `i` - Insert keys (e.g., `i 1 4-7 9`)
- `r` - Remove keys (e.g., `r 1-100`)
- `s` - Search by key (e.g., `s 41-60`)
- `d` - Dump tree structure
- `q` - Quit

## Terms/Concepts Explanation

**B+ Tree**: A self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time. Unlike B-trees, all values are stored in leaf nodes, with internal nodes only storing keys for navigation.

**Block Size**: The size of each node in bytes when stored on disk. Must be a power of 2 and determines the maximum number of entries per node through the formula: `(block_size - sizeof(node)) / (sizeof(key_t) + sizeof(data_type))`.

**Node Splitting**: When a node becomes full during insertion, it is split into two nodes at approximately half capacity, with changes propagated upward potentially creating a new root.

**Node Merging**: When a node becomes too sparse during deletion, it either borrows entries from siblings or merges with them, with changes propagated upward potentially reducing tree height.

**Free Block Management**: A mechanism to track deleted node locations on disk for reuse, preventing disk space fragmentation by maintaining a linked list of available offsets.

**Cache System**: A fixed-size array of pre-allocated node buffers that reduces disk I/O by keeping frequently accessed nodes in memory.

**Boot File**: A metadata file (`.boot` extension) that stores the root node offset, block size, file size, and free blocks list to enable tree reconstruction across program restarts.