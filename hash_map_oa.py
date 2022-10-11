# Name: Andrew Olness
# OSU Email: olnessa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6-3-22
# Description: Hashmap implemented using open addressing with quadratic probing
#              for collision detection. Contains methods for manipulation of 
#              data such as add, remove, and get.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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
        Add key:value or update value if key is in the hashmap.
        """
        # resize before adding if needed.
        if self.table_load() >= .5:
            self.resize_table(self._capacity * 2)
        hash = self._hash_function(key)
        index = hash % self._capacity
        probe = 1
        # probe for empty bucket to add
        while self._buckets[index] is not None:
            # reach tombstone value
            if self._buckets[index].is_tombstone == True:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return
            # update existing key:value
            if self._buckets[index].key == key:
                self._buckets[index].value = value
                return
            index = (hash + probe**2) % self._capacity
            probe += 1
        # empty bucket, add key:value
        self._buckets[index] = HashEntry(key, value)
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the table load factor.
        """
        return float(self._size/self._capacity)

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets.
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the hashmap keeping all pre-existing
        key value pairs.
        """
        # non valid new capacity
        if new_capacity < 1 or new_capacity < self._size:
            return
        # new hash for storing key value pairs
        new_hash = HashMap(new_capacity, self._hash_function)
        for index in range(self._capacity):
            # add valid key:value
            if self._buckets[index] is not None and self._buckets[index].is_tombstone == False:
                new_hash.put(self._buckets[index].key, self._buckets[index].value)
        # set self to new data
        self._buckets = new_hash._buckets
        self._capacity = new_hash._capacity

    def get(self, key: str) -> object:
        """
        Returns the value associated with a key.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        probe = 1
        if self._buckets[index] is None:
            return None
        # probe for given key
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                # if key is tombstone
                if self._buckets[index].is_tombstone == True:
                    return None
                return self._buckets[index].value
            # continue probe
            index = (hash + probe**2) % self._capacity
            probe += 1
        return None
            
    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hashmap.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        probe = 1
        if self._buckets[index] is None:
            return False
        # probe for given key
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                # if key is tombstone
                if self._buckets[index].is_tombstone == True:
                    return False
                return True
            # continue probe
            index = (hash + probe**2) % self._capacity
            probe += 1
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the hashmap.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        probe = 1
        if self._buckets[index] is None:
            return
        # probe for key
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                # if key is already tombstone
                if self._buckets[index].is_tombstone == True:
                    return
                # set key to tombstone value
                self._buckets[index].is_tombstone = True
                self._size -= 1
                return
            # continue probe
            index = (hash + probe**2) % self._capacity
            probe += 1

    def clear(self) -> None:
        """
        Clears the contents of the hashmap.
        """
        new_arr = DynamicArray()
        for _ in range(self._capacity):
            new_arr.append(None)
        self._buckets = new_arr
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Returns a dynamic array that contains all the keys stored in the hashmap.
        """
        result = DynamicArray()
        for index in range(self._capacity):
            if self._buckets[index] is not None and self._buckets[index].is_tombstone == False:
                result.append(self._buckets[index].key)
        return result


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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
