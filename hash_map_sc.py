# A hash map implementation using separate chaining for collision resolution, allowing efficient key-value
# mappings even under high load factors.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Adds a new key-value pair to the hash map, updating the value if the key already exists.
        Resizes the hash map if the load factor would exceed 1.0.
        """
        # Check if resizing is necessary
        if self.table_load() >= 1.0:
            self.resize_table(2 * self._capacity)

        # Determine bucket index and get the corresponding bucket
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(index)

        # Search for the key in the bucket
        for node in bucket:
            if node.key == key:
                node.value = value  # Update existing key
                return

        # Key not found, insert new key-value pair
        bucket.insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map to a new capacity if greater than the current and a prime number,
        rehashing all existing entries into the new bucket array.
        """
        # Check the new capacity for validity
        if new_capacity < 1:
            return

        # Ensure the new capacity is prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new hash map with the adjusted capacity
        new_map = HashMap(new_capacity, self._hash_function)
        if new_capacity == 2:
            new_map._capacity = 2  # Handle the edge case directly

        # Rehash all entries
        for i in range(self._capacity):
            current_bucket = self._buckets.get_at_index(i)
            for node in current_bucket:
                new_map.put(node.key, node.value)

        # Update the current hash map with new settings
        self._buckets = new_map._buckets
        self._size = new_map._size
        self._capacity = new_map._capacity

    def table_load(self) -> float:
        """
        Calculate and return the load factor of the hash map.
        """
        # Return the ratio of size to capacity
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Count and return the number of empty buckets in the hash map.
        """
        # Initialize counter for empty buckets
        empty = 0
        # Iterate over all buckets
        for i in range(self._buckets.length()):
            # Check if the bucket's list head is None
            if self._buckets[i]._head is None:
                # Increment the empty bucket count
                empty += 1
        return empty

    def get(self, key: str):
        """
        Retrieve the value associated with the given key in the hash map.
        """
        # Compute bucket index
        index = self._hash_function(key) % self._capacity
        # Search for the key in the bucket
        node = self._buckets[index].contains(key)
        if node:
            # Return the value if key is found
            return node.value
            # Return None if key is not found
        return None

    def contains_key(self, key: str) -> bool:
        """
        Check if the hash map contains the given key.
        """
        # Utilize get method to check key presence
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Remove the key-value pair associated with the given key from the hash map.
        """
        # Compute bucket index
        index = self._hash_function(key) % self._capacity
        # Attempt to remove the key
        if self._buckets[index].remove(key):
            # Decrement the size if removal was successful
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Retrieve all key-value pairs stored in the hash map.
        """
        # Initialize the result array
        result = DynamicArray()
        # Iterate over all buckets
        for i in range(self._buckets.length()):
            # Start with the head of the linked list
            current = self._buckets[i]._head
            while current:  # Traverse the linked list
                # Append the (key, value) tuple
                result.append((current.key, current.value))
                current = current.next
        return result

    def clear(self) -> None:
        """
        Clear all contents of the hash map.
        """
        # Iterate over all buckets
        for i in range(self._capacity):
            # Reset each bucket to a new empty LinkedList
            self._buckets[i] = LinkedList()
            # Reset the size of the hash map to zero
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Find the mode(s) of the values in a DynamicArray and their corresponding frequency.
    """
    # Initialize a hash map to store the frequency of each element
    frequency_map = HashMap()

    # Populate the frequency map with counts for each element
    for i in range(da.length()):
        element = da.get_at_index(i)
        # Retrieve current frequency or set to zero if key not present
        current_count = frequency_map.get(element) or 0
        frequency_map.put(element, current_count + 1)

    # Determine the maximum frequency and collect the elements with that frequency
    max_frequency = 0
    mode_elements = DynamicArray()

    # Re-iterate to find the maximum frequency
    for i in range(da.length()):
        element = da.get_at_index(i)
        frequency = frequency_map.get(element)
        if frequency > max_frequency:
            max_frequency = frequency
            mode_elements = DynamicArray()  # Reset mode elements
            mode_elements.append(element)
        elif frequency == max_frequency:
            # Check if element is already in mode_elements to avoid duplicates
            if not in_dynamic_array(mode_elements, element):
                mode_elements.append(element)

    return (mode_elements, max_frequency)

def in_dynamic_array(dyn_array: DynamicArray, item: object) -> bool:
    """
    Helper function to check if an item is in the dynamic array,
    since DynamicArray does not support 'contains' method.
    """
    for i in range(dyn_array.length()):
        if dyn_array.get_at_index(i) == item:
            return True
    return False

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
