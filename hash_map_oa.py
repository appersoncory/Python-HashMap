# Name: Cory Apperson
# OSU Email: appersoc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/06/2024
# Description: Implements an open addressing hash map with quadratic probing for collision resolution. Supports dynamic
# resizing to maintain efficient operations as the map grows.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Insert or update the given key with the specified value in the hash map using quadratic probing.
        If the table load exceeds 0.5 before insertion, the table is resized to twice its current capacity.
        This method handles collisions using quadratic probing and reuses empty slots marked by tombstones.
        """
        # If the load factor is too high, double the table capacity to maintain efficient operations
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Calculate the bucket index for the key using the hash function and modulus with current capacity
        index = self._hash_function(key) % self._capacity
        initial_index = index
        probe = 0

        first_tombstone_index = None

        while True:
            current_entry = self._buckets.get_at_index(index)

            if current_entry is None:
                # If a tombstone was found earlier, use that slot instead
                if first_tombstone_index is not None:
                    index = first_tombstone_index
                self._buckets.set_at_index(index, HashEntry(key, value))
                self._size += 1
                return

            elif current_entry.is_tombstone:
                if first_tombstone_index is None:
                    first_tombstone_index = index

            elif current_entry.key == key:
                # Update existing entry
                if current_entry.is_tombstone:
                    self._size += 1  # Correcting the size if we're reviving a tombstone
                current_entry.value = value
                current_entry.is_tombstone = False  # Ensure this is marked as active
                return

            # Quadratic probing
            probe += 1
            index = (initial_index + probe ** 2) % self._capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table to a new capacity that is a prime number, rehashing all existing non-tombstone entries.
        """
        # Verify the new capacity is greater than the current size and is a prime number
        if new_capacity < self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new dynamic array with the new capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)

        # Temporary save old buckets and reset size to re-add entries accurately
        old_buckets = self._buckets
        old_size = self._size
        self._buckets = new_buckets
        self._capacity = new_capacity
        self._size = 0  # Reset size to accurately count when re-adding items

        # Rehash all items that are not tombstones
        for i in range(old_buckets.length()):
            entry = old_buckets.get_at_index(i)
            if entry and not entry.is_tombstone:
                self.put(entry.key, entry.value)

        # Debug check to confirm size matches expected after resizing
        if self._size != old_size:
            print(f"Error: Expected size {old_size}, but got {self._size}")

    def table_load(self) -> float:
        """
        Return the current load factor of the hash table.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_count = 0
        for i in range(self._capacity):
            if self._buckets[i] is None:
                empty_count += 1
        return empty_count

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key, or None if the key is not found.
        """
        index = self._hash_function(key) % self._capacity
        probe = 0

        while True:
            # Calculate the index with quadratic probing
            current_index = (index + probe ** 2) % self._capacity
            current_entry = self._buckets[current_index]

            # If the slot is empty, the key is not present
            if current_entry is None:
                return None

            # If the slot is not a tombstone and the keys match, return the value
            if not current_entry.is_tombstone and current_entry.key == key:
                return current_entry.value

            # Update the probe number and continue
            probe += 1

            # If we've looped back to the start, the key is not in the hash table
            if probe > self._capacity:
                return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the hash map contains the specified key, False otherwise.
        """
        index = self._hash_function(key) % self._capacity
        probe = 0

        while True:
            # Calculate the index with quadratic probing
            current_index = (index + probe ** 2) % self._capacity
            current_entry = self._buckets[current_index]

            # If the slot is empty, the key is not present
            if current_entry is None:
                return False

            # If the slot is not a tombstone and the keys match, the key is present
            if not current_entry.is_tombstone and current_entry.key == key:
                return True

            # Update the probe number and continue
            probe += 1

            # If we've looped back to the start, the key is not in the hash table
            if probe > self._capacity:
                return False

    def remove(self, key: str) -> None:
        """
        Removes the specified key and its associated value from the hash map.
        If the key is not found, the method does nothing.
        """
        index = self._hash_function(key) % self._capacity
        probe = 0

        while True:
            # Calculate the current index with quadratic probing
            current_index = (index + probe ** 2) % self._capacity
            current_entry = self._buckets[current_index]

            # If an empty slot is reached without finding the key, stop the search
            if current_entry is None:
                return

            # Check if the current entry matches the key
            if current_entry is not None and not current_entry.is_tombstone:
                if current_entry.key == key:
                    # Mark this entry as a tombstone
                    current_entry.is_tombstone = True
                    self._size -= 1
                    return

            # Increment probe number and continue
            probe += 1

            # To avoid an infinite loop in a full table, we stop if we've cycled back to the start
            if probe > self._capacity:
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing tuples of (key, value) for all entries
        in the hash map that are not tombstones and not None.
        """
        result = DynamicArray()
        for i in range(self._capacity):
            entry = self._buckets[i]
            if entry is not None and not entry.is_tombstone:
                result.append((entry.key, entry.value))
        return result

    def clear(self) -> None:
        """
        Clears all key/value pairs in the hash map without changing the hash table's capacity.
        """
        # Loop over the entire hash table and set each slot to None
        for i in range(self._capacity):
            self._buckets[i] = None

        # Reset the size counter to zero since the hash map is now empty
        self._size = 0

    def __iter__(self):
        """
        Initializes the iterator by setting the current index to 0 and preparing to iterate
        over hash map entries.
        """
        self._current_index = 0
        return self

    def __next__(self):
        """
        Returns the next active hash entry in the hash map. Skips over
        tombstone and None entries.
        """
        while self._current_index < self._capacity:
            entry = self._buckets[self._current_index]
            self._current_index += 1
            if entry is not None and not entry.is_tombstone:
                return entry
        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
