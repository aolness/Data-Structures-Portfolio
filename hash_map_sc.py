# Name: Andrew Olness
# OSU Email: olnessa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/3/2022
# Description: Hashmap class utilizing chaining for collision resolution. Chaining is
#              accomplished by a DynamicArray. Contains methods for manipulation of 
#              data such as add, remove, and get.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
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
        Add a key:value pair to the hash map. If the key already exists,
        update the value to the new value.
        """
        index = (self._hash_function(key) % self._capacity)
        # if key not in hashmap, add key:value
        if self._buckets[index].contains(key) is None:
            self._buckets[index].insert(key, value)
            self._size += 1
        # if key in hashmap, update value
        else:
            self._buckets[index].contains(key).value = value

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets.
        """
        # counter for number of not empty buckets
        size = 0
        for bucket in range(self._capacity):
            if self._buckets[bucket].length() > 0:
                size += 1
        return self._capacity - size

    def table_load(self) -> float:
        """
        Returns the current load factor.
        """
        return float(self._size/self._capacity)

    def clear(self) -> None:
        """
        Clears the hash map.
        """
        # set each bucket to empty linked list
        for index in range(self._capacity):
            self._buckets[index] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map by creating a new dynamic array with new size,
        copies all old key:values to new array.
        """
        if new_capacity < 1:
            return
        else:
            # create new dynamic array with empty linked lists
            new_arr = DynamicArray()
            for _ in range(new_capacity):
                new_arr.append(LinkedList())
            # copy original values into new dynamic array
            for bucket in range(self._capacity):
                for node in self._buckets[bucket]:
                    index = (self._hash_function(node.key) % new_capacity)
                    new_arr[index].insert(node.key, node.value)
            # set hashmap to new data
            self._buckets = new_arr
            self._capacity = new_capacity

    def get(self, key: str) -> object:
        """
        returns the value associated with the given key.
        """
        # find key
        index = (self._hash_function(key) % self._capacity)
        result = self._buckets[index].contains(key)
        # if key in hashmap
        if result != None:
            return result.value
        # key not in hashmap
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the key is in the hash map.
        """
        if self._size == 0:
            return False
        # find key in hashmap
        index = (self._hash_function(key) % self._capacity)
        result = self._buckets[index].contains(key)
        # if key in hashmap
        if result != None:
            return True
        # key not in hashmap
        return False

    def remove(self, key: str) -> None:
        """
        Removes the key and its value from the tree.
        """
        index = (self._hash_function(key) % self._capacity)
        if self._buckets[index].remove(key):
            self._size -= 1
        
    def get_keys(self) -> DynamicArray:
        """
        Get all keys in the Hashmap and return them in a dynamic array.
        """
        result = DynamicArray()
        for bucket in range(self._capacity):
            for node in self._buckets[bucket]:
                result.append(node.key)
        return result


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the most frequent value(s) and the frequency of occurence.
    Returns a tuple of the dynamic array and the freq.
    """
    mode = DynamicArray()
    freq = 0
    # new hashmap to track values and their freq
    map = HashMap(da.length() // 3, hash_function_1)
    for index in range(da.length()):
        # if value in hashmap, +1 to the freq
        if map.contains_key(da[index]):
            node = map.get(da[index]) + 1
            map.put(da[index], node) 
        # if value not in hashmap, add value and freq of 1
        else:
            map.put(da[index], 1)
    # cycle through the keys in the hashmap
    keys = map.get_keys()
    for index in range(keys.length()):
        # freq value
        node = map.get(keys[index])
        # if current key freq greater than highest freq
        if node > freq:
            # new array and add new high values
            mode = DynamicArray()
            mode.append(keys[index])
            freq = node
        # if current key freq equal to high freq
        elif node == freq:
            mode.append(keys[index])
    return (mode, freq)




# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
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
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

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

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
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
    m = HashMap(75, hash_function_2)
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
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    # map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        # map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
