# HashMap Implementations in Python

## Project Overview

This project involves the implementation of two HashMap classes in Python, each utilizing a different collision resolution technique: Chaining and Open Addressing. Both implementations are optimized to ensure that the average case performance of all operations is O(1). The project is structured with comprehensive methods for managing the hash maps and handling collisions effectively.

## Implementations

### Chaining HashMap

The Chaining HashMap implementation uses a DynamicArray to store the hash table and LinkedLists to handle collisions. Each entry in the hash table points to a linked list of key/value pairs, ensuring that collisions are resolved through chaining. The following methods are implemented:

- **put(key, value)**: Inserts a key/value pair into the hash map. If the key already exists, its value is updated.
- **resize_table(new_capacity)**: Resizes the hash table to the given capacity and rehashes all key/value pairs.
- **table_load()**: Returns the current load factor of the hash table.
- **empty_buckets()**: Returns the number of empty buckets in the hash table.
- **get(key)**: Retrieves the value associated with the given key. Returns `None` if the key is not found.
- **contains_key(key)**: Checks if the given key is in the hash map.
- **remove(key)**: Removes the key/value pair associated with the given key.
- **get_keys_and_values()**: Returns a list of all key/value pairs in the hash map.
- **clear()**: Clears the hash map.
- **find_mode()**: Finds the key(s) with the highest frequency in the hash map.

#### Implementation Details

1. **Data Structures**: Uses a DynamicArray to store the hash table and LinkedList objects to store chains of key/value pairs.
2. **Collision Resolution**: Implements chaining, storing collisions in linked list nodes.
3. **Performance**: Ensures average case performance of all operations is O(1).

### Open Addressing HashMap

The Open Addressing HashMap implementation uses a DynamicArray for the hash table and employs quadratic probing for collision resolution. The following methods are implemented:

- **put(key, value)**: Inserts a key/value pair into the hash map. If the key already exists, its value is updated.
- **resize_table(new_capacity)**: Resizes the hash table to the given capacity and rehashes all key/value pairs.
- **table_load()**: Returns the current load factor of the hash table.
- **empty_buckets()**: Returns the number of empty buckets in the hash table.
- **get(key)**: Retrieves the value associated with the given key. Returns `None` if the key is not found.
- **contains_key(key)**: Checks if the given key is in the hash map.
- **remove(key)**: Removes the key/value pair associated with the given key.
- **get_keys_and_values()**: Returns a list of all key/value pairs in the hash map.
- **clear()**: Clears the hash map.
- **__iter__()**, **__next__()**: Iterates over the key/value pairs in the hash map.
- **find_mode()**: Finds the key(s) with the highest frequency in the hash map.

#### Implementation Details

1. **Data Structures**: Uses a DynamicArray to store the hash table.
2. **Collision Resolution**: Implements Open Addressing with Quadratic Probing.
3. **Performance**: Ensures average case performance of all operations is O(1).

## Usage

### Dependencies

The project uses two pre-written classes, `DynamicArray` and `LinkedList`, provided in the `a6_include.py` file. These classes are utilized to manage the underlying data structures of the hash maps.

### Testing

Two pre-written hash functions are provided for testing the implementations. Ensure to test the hash map implementations with both hash functions to verify their correctness and performance.
