import random
import sys
import time


###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

# Hash function.
#
# |key|: string
# Return value: a hash value


def calculate_hash(key):
    assert type(key) == str
    # Note: This is not a good hash function. Do you see why?
    # B進法を用いてハッシュ値を計算
    # 今回は100進法を用いた
    hash = 0
    B = 100
    K = len(key)
    for i in range(K):
        hash += ord(key[i])*(B**(K-(i+1)))
    return hash


# n以下の素数(2を含む)を生成する
# エラトステネスのふるいを利用
# 計算量：N log logN

def make_prime_number(n):
    Deleted = [False] * (n+1)
    LIMIT = int(n ** 0.5)
    for i in range(2, LIMIT+1):
        if Deleted[i] == False:
            for j in range(i*2, n+1, i):
                Deleted[j] = True
    answer = []
    for num in range(2, n+1):
        if Deleted[num] == False:
            answer.append(num)
    if len(answer) != 0:
        return answer[len(answer)-1]
    else:
        return n

# An item object that represents one key - value pair in the hash table


class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    # |time_item|: itemの順番を管理する. cashe.pyで必要
    def __init__(self, key, value, next, time_item=None):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next
        self.time_item = time_item


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
    def __init__(self, n):
        self.bucket_size = n
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # 再ハッシュ
    def rehash(self):
        if self.item_count > self.bucket_size * 0.7 or self.item_count < self.bucket_size * 0.3:
            prev_bucket_size = self.bucket_size
            prev_buckets = self.buckets

            self.bucket_size = self.calculate_bucket_size()
            self.buckets = [None] * self.bucket_size
            self.item_count = 0
            for i in range(prev_bucket_size):
                bucket_index = i
                item = prev_buckets[bucket_index]
                while item:
                    self.rehash_item(item)
                    item = item.next
            return True

        else:
            return False

    # それぞれのitemのハッシュ値を再計算する
    def rehash_item(self, item):
        key = item.key
        value = item.value
        time_item = item.time_item
        bucket_index = calculate_hash(key) % self.bucket_size
        new_item = Item(key, value, self.buckets[bucket_index], time_item)
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        return True

    # ハッシュテーブルのサイズを計算する
    def calculate_bucket_size(self):
        if self.item_count > self.bucket_size * 0.7:
            self.bucket_size = self.bucket_size*2
        elif self.item_count < self.bucket_size * 0.3:
            self.bucket_size = int(self.bucket_size // 2)
        return make_prime_number(self.bucket_size+1)

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.

    def put(self, key, value, time_item=None):
        assert type(key) == str
        self.check_size()  # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index], time_item)
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        self.rehash()
        return True

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        self.check_size()  # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    def return_item(self, key):
        assert type(key) == str
        self.check_size()  # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item)
            item = item.next
        return (None)

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str
        self.check_size()
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        if item != None:
            # 最も新しい要素(1番後ろの要素)を消す場合
            if item.key == key:
                self.buckets[bucket_index] = item.next
                self.item_count -= 1
                self.rehash()
                return True
            # それ以外の要素を削除する場合
            prev = item
            item = item.next
            while item:
                if item.key == key:
                    next = item.next
                    prev.next = next
                    self.item_count -= 1
                    self.rehash()
                    return True
                prev = item
                item = item.next
            return False
        else:
            return False

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable(97)

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable(97)

    # 出力ファイルを新規作成
    path = "result.txt"
    with open(path, mode="w") as f:
        pass

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

        with open(path, mode="a") as f:
            f.write("%d %.6f" % ((iteration+1)*10000, end-begin))
            f.write("\n")

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()
