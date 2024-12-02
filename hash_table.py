from typing import Any, List, Tuple, Optional

class HashTable:
    # HashTable class to store key-value pairs
    def __init__(self, size: int = 40):
        # Setup with size and t table to store key-value pairs
        self.size = size
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(size)]

    # Hash function to calculate the index of the key
    def _hash(self, key: Any) -> int:
        if isinstance(key, list):
            # Convert list to string representation
            key = str(key)  
        return hash(key) % self.size

    # Search for a key in the HashTable
    def search(self, key: Any) -> Optional[Any]:
        # Calculate the index of the key
        index = self._hash(key)
        for k, v in self.table[index]:
            if key == k:
                return v
        return None

    # Insert a key-value pair into the HashTable
    def insert(self, key: Any, value: Any):
        index = self._hash(key)
        # If the key exists, update the value
        for i, (k, v) in enumerate(self.table[index]):
            if key == k:
                self.table[index][i] = (key, value)
                return
        # If the key doesn't exist, append the key-value pair
        self.table[index].append((key, value))

    # Calculate the hash index for a given input
    def calculate_hash_index(self, input):
        pre_mod_hash = 0
        input = str(input)
        # sum up the ASCII or Decimal value of the input
        for c in input:
            pre_mod_hash += ord(c)
        # Return the caculated hash index
        return pre_mod_hash % self.size
    
    # Add a Key-Value pair to the Hash_Table
    def add(self, key, val):
        # Calculate the hash value for the key(/value pair) to add
        hash_index = self.calculate_hash_index(key)
        value = (key, val)
        # If the key doesn't exist in the table yet, add it
        if not self.table[hash_index]:
            self.table[hash_index].append(value)
        else:
            for i, (k, v) in enumerate(self.table[hash_index]):
                # If the key is the same, overwrite the value
                if k == key:
                    self.table[hash_index][i] = value
                    return
            # If the key is not the same, append it to the list
            self.table[hash_index].append(value)

    # Get the value of a key from the Hash_Table
    def get(self, key: Any) -> Optional[Any]:
        return self.search(key)

    # Set item in the Hash_Table
    def __setitem__(self, key: Any, value: Any):
        self.insert(key, value)

    # Get item from the Hash_Table
    def __getitem__(self, key: Any) -> Optional[Any]:
        result = self.search(key)
        if result is None:
            raise KeyError(f"Key {key} not found in HashTable")
        return result

    # Check if a key is in the Hash_Table
    def __contains__(self, key: Any) -> bool:
        return self.search(key) is not None

    # Get the keys from the Hash_Table
    def keys(self) -> List[Any]:
        # Create a list to store the keys
        keys_list = []
        # Iterate through the table and append the keys
        for bucket in self.table:
            for k, _ in bucket:
                # Append the key to the list
                keys_list.append(k)
        # Return the list of keys
        return keys_list

    # Lists of items for the Hash_Table
    def items(self) -> List[Tuple[Any, Any]]:
        items_list = []
        # Iterate through the table and append the key-value pairs
        for bucket in self.table:
            for k, v in bucket:
                items_list.append((k, v))
        # Return the list of key-value pairs
        return items_list
    
    # Remove a key from the Hash_Table
    def remove(self, key: Any):
        # Calculate the index of the key
        index = self._hash(key)
        # Iterate through the bucket and remove the key-value pair
        for i, (k, v) in enumerate(self.table[index]):
            if key == k:
                del self.table[index][i]
                return
        # If the key is not found, raise
        raise KeyError(f"Key {key} not found in HashTable")