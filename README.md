### 🔹 What is a Bloom Filter?

A **Bloom Filter** is a **probabilistic data structure** used to test if an element **might be in a set**.

* It **can give false positives** (says item exists when it doesn’t).
* It **never gives false negatives** (if it says item is not present, it’s truly not there).
* It’s **memory efficient** compared to keeping all items in a list or set.

---

### 🔹 How does it work?

1. Create a **bit array** of size `m` (all 0’s initially).
2. When you **insert an item**:

   * Pass it through multiple **hash functions**.
   * Each hash gives an index in the bit array.
   * Set those bit positions to `1`.
3. To **check membership**:

   * Hash the item again.
   * If **all** those positions are `1`, item *might* exist.
   * If **any** of them is `0`, item *definitely does not exist*.

---

### 🔹 Implementation in Python (with 3 hash functions)

I’ll write the code and explain **every single line**:

```python
import hashlib   # we’ll use hashlib to create different hash functions

class BloomFilter:
    def __init__(self, size=100):
        # size = number of bits in the filter
        self.size = size
        # Initialize the bit array (all 0’s at the beginning)
        self.bit_array = [0] * size

    def _hashes(self, item):
        """
        Generate 3 different hash values for the item.
        Each hash must map the item to an index within [0, size-1].
        """
        # Convert item to string (in case it's not)
        item_str = str(item).encode('utf-8')

        # Hash function 1: MD5
        hash1 = int(hashlib.md5(item_str).hexdigest(), 16) % self.size

        # Hash function 2: SHA1
        hash2 = int(hashlib.sha1(item_str).hexdigest(), 16) % self.size

        # Hash function 3: SHA256
        hash3 = int(hashlib.sha256(item_str).hexdigest(), 16) % self.size

        # Return the three indices
        return [hash1, hash2, hash3]

    def add(self, item):
        """Add an item to the Bloom filter."""
        for hash_val in self._hashes(item):
            # Mark these positions as 1
            self.bit_array[hash_val] = 1

    def check(self, item):
        """Check if an item might be in the filter."""
        for hash_val in self._hashes(item):
            # If any of the positions is 0, the item is definitely not present
            if self.bit_array[hash_val] == 0:
                return False
        # Otherwise, the item might exist
        return True
```

---

### 🔹 Explanation line by line:

1. ```python
   import hashlib
   ```

   * We use `hashlib` because it provides multiple hashing algorithms (MD5, SHA1, SHA256).
   * Each gives a different hash → useful for simulating multiple hash functions.

2. ```python
   class BloomFilter:
   ```

   * Define a class to represent our Bloom Filter.

3. ```python
   def __init__(self, size=100):
   ```

   * Constructor, called when you create an object.
   * `size=100` means our bit array will have 100 slots (can be tuned for accuracy vs memory).

4. ```python
   self.bit_array = [0] * size
   ```

   * Creates a list of `0`s with length = `size`.
   * This is our bit array (ideally you’d use a true bitset for efficiency, but list works for learning).

5. ```python
   def _hashes(self, item):
   ```

   * Private helper method.
   * Takes an `item`, runs it through 3 hash functions, and returns 3 positions.

6. ```python
   item_str = str(item).encode('utf-8')
   ```

   * Convert item to a byte string → needed for hashing.

7. ```python
   hash1 = int(hashlib.md5(item_str).hexdigest(), 16) % self.size
   ```

   * Run MD5 hash, convert hex string → integer (`int(..., 16)` means base-16).
   * Take modulo `self.size` to ensure it fits within bit array index.

8. (Similarly for SHA1 and SHA256.)

9. ```python
   return [hash1, hash2, hash3]
   ```

   * Return all 3 indices.

10. ```python
    def add(self, item):
    ```

    * Add an item into the filter.

11. ```python
    for hash_val in self._hashes(item):
        self.bit_array[hash_val] = 1
    ```

    * For each index from hash functions → mark position as `1`.

12. ```python
    def check(self, item):
    ```

    * Check if an item might be in the filter.

13. ```python
    if self.bit_array[hash_val] == 0:
        return False
    ```

    * If **any bit is 0**, item definitely wasn’t added.

14. ```python
    return True
    ```

    * Otherwise, all positions are 1 → item might exist.

---

### 🔹 Usage Example:

```python
bf = BloomFilter(size=50)

# Add some items
bf.add("google")
bf.add("openai")

print(bf.check("google"))   # True (definitely added)
print(bf.check("openai"))   # True (definitely added)
print(bf.check("microsoft")) # False (definitely not added)
```

⚠️ But if you add enough items, **false positives** can appear:

```python
print(bf.check("random_word"))  # Might print True, even if not added
```

---

✅ That’s a **basic working Bloom Filter** with 3 hash functions.

## 🔹 Time Complexity

### Bloom Filter

* **Insert (`add`)**:

  * Compute `k` hash functions (here `k = 3`).
  * Update `k` positions in the bit array.
  * ✅ Complexity = **O(k)** → since `k` is constant, this is effectively **O(1)**.

* **Membership Check (`check`)**:

  * Compute `k` hash functions.
  * Check `k` positions in the bit array.
  * ✅ Complexity = **O(k)** = **O(1)**.

👉 Both add and lookup are constant time, independent of how many items you insert.

---

### Hash Set (e.g., Python `set`, Redis `SET`)

* **Insert**: Average **O(1)** (hashing + collision handling).
* **Lookup**: Average **O(1)**.
* Worst-case (with bad hashing/collisions): **O(n)**.
* ✅ Still extremely fast in practice.

---

## 🔹 Space Complexity

This is where Bloom filters win.

### Bloom Filter

* Needs only a **bit array of size `m`**.
* For **n items** and **false positive probability p**, the optimal size is:

$$
m \approx - \frac{n \cdot \ln(p)}{(\ln 2)^2}
$$

and the optimal number of hash functions:

$$
k \approx \frac{m}{n} \ln 2
$$

* Example:

  * Insert 1 million items (`n = 10^6`).
  * Want 1% false positive rate (`p = 0.01`).
  * Then `m ≈ 9.6 million bits ≈ 1.2 MB`.
  * A plain hash set would need \~24 MB just to store the strings (ignoring overhead).

👉 Bloom filter is **10–20x more memory efficient**.

---

### Hash Set / Redis `SET`

* Stores actual elements (not just bits).

* Memory = proportional to `O(n * size_of_element)`.

* For strings, overhead is huge (pointers, object metadata, etc).

* Example: 1 million unique strings (\~10 bytes each).

  * Needs at least 10 MB + internal overhead.
  * In Redis, this could balloon to **dozens of MBs**.

---

## 🔹 Trade-offs

| Feature               | Bloom Filter                                   | Hash Set / Redis |
| --------------------- | ---------------------------------------------- | ---------------- |
| **Insert**            | O(1)                                           | O(1)             |
| **Lookup**            | O(1)                                           | O(1)             |
| **Space usage**       | Very small                                     | Large            |
| **False positives**   | ✅ Yes                                          | ❌ No             |
| **False negatives**   | ❌ No                                           | ❌ No             |
| **Can delete items?** | Hard (needs extra tricks like counting filter) | ✅ Easy           |

---

## 🔹 When to use Bloom Filter instead of Redis Set?

* **Great choice** if:

  * You only need to check *membership* (is this element present or not).
  * False positives are acceptable (e.g., web cache, spam detection, duplicate URL check).
  * Memory is limited, and dataset is huge.

* **Not suitable** if:

  * You need exact results (like financial transactions).
  * You need to delete elements frequently.
  * You need to store actual items, not just presence information.

---

✅ In short:

* Bloom filter → **O(1) time, O(m) space (very small)**, but **allows false positives**.
* Redis set → **O(1) time, O(n) space (much larger)**, but **exact, no errors**.
