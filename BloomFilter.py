import hashlib

class BloomFilter:
    def __init__(self, size=100):
        #size = number of bits in the filter 
        self.size = size 
        # initially the bit array
        self.bit_arrays = [[0] * self.size for _ in range(3)]
    
    def _hashes(self, item):
        '''Generate 3 different hash values for the 
        item. Each hash must map the item to an index
        within [0, size-1]'''

        # convert item to string (in case it is not)
        item_str = str(item).encode('utf-8')

        # Hash function 2: md5
        hash1 = int(hashlib.md5(item_str).hexdigest(), 16) % self.size

        # Hash funciton 2: SHA1
        hash2 = int(hashlib.sha1(item_str).hexdigest(), 16) % self.size 

        # Hash function 3: SHA256
        hash3 = int(hashlib.sha256(item_str).hexdigest(), 16) % self.size

        return [hash1, hash2, hash3]

    def add(self, item):
        """Check if an item might be in the filter"""
        for index, hash_val in enumerate(self._hashes(item)):
            self.bit_arrays[index][hash_val] = 1

    def check(self, item):
        """Check if an item might be in the filter."""
        for index, hash_val in enumerate(self._hashes(item)):
            if self.bit_arrays[index][hash_val] == 0:
                return False 
        # The item might exist
        return True            


bf = BloomFilter(size=50)

# Add some items
bf.add("google")
bf.add("openai")

print(bf.check("google"))   # True (definitely added)
print(bf.check("openai"))   # True (definitely added)
print(bf.check("microsoft")) # False (definitely not added)
