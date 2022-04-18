
class BTreeNode:
    """
    B-Tree node data structure.
    """
    def __init__(self, keys, children):
        """
        Generates a b-tree node containing the given keys
        and children.
        Note: This procedure assumes that, if provided,
        keys and children have the proper structure.
        """
        self.keys = keys 
        self.children = children

        """
        return the chldren of node
        """ 
    def get_children(self):
        return self.children
    
    def is_leaf(self):
        """
        Checks whether self is a leaf.
        """
        return len(self.children)==0

    def num_keys(self):
        """
        Returns the number of key stored in self.
        """
        return len(self.keys)

    def get_keys(self):
        return self.keys

    
    def search_key(self, key):
        """
        Returns the index of the key preceding key in self.
        If all keys in self are smaller than key, then the
        returned index equals the number of keys in self.
        """
        left = 0 
        right = self.num_keys()
        while right > left:
            mid = (left + right)//2
            if self.keys[mid] >= key:
                right = mid
            else:
                left = mid + 1
        return left

    def contains_key(self, key, index):
        """
        Checks whether index is the index of key in self.
        """
        return index < self.num_keys() and self.keys[index] == key
    
    def insert_key(self, key):
        """
        Inserts key in self.
        """
        index = self.search_key(key) # First Search the key
        self.keys.insert(index, key) # and then insert the key
        
    
    def deep_min(self):
        """
        Returns the smallest key in self's sub-tree.
        """
        node = self
        while not node.is_leaf():
            node = node.children[0]
        return node.keys[0] if node.keys else None
    
    def deep_max(self):
        """
        Returns the largest key in self's sub-tree.
        """
        node = self
        while not node.is_leaf():
            node = node.children[-1]
        return node.keys[-1] if node.keys else None
    
    def locate_successor(self, key):
        """
        Returns the index of the key potentially
        succeeding key in self. If no successor 
        exists, then the number of keys in self is
        returned.
        """
        index = 0
        while index < self.num_keys() and self.keys[index] <= key:
            index += 1
        return index

    def locate_predecessor(self, key):
        """
        Returns the index of the key potentially
        preceding key in self. If no predecessor
        exists, then the number of keys in self -1 is returned.
        """
        index = self.search_key(key)
        return index-1

    def predecessor(self, key):
        """
        Returns the key preceding key in self.
        If no predecessor exists, then  None is
        returned.
        """
        index = self.locate_predecessor(key)
        return self.keys[index] if index >= 0 else None

    def deep_predecessor(self, index):
        """
        Returns the key, in self's sub-tree, that
        precedes the index-th key in self.
        Note: Assumes that self is not a leaf.
        """
        return self.children[index].deep_max()

    def successor(self, key):
        """
        Returns the key succeeding key in self.
        If no successor exists, then  None is
        returned.
        """
        index = self.locate_successor(key)
        self.keys[index] if index < self.num_keys() else None


    def deep_successor(self, index):
        """
        Returns the key, in self's sub-tree, that
        succeeds the index-th key in self.
        Note: Assumes that self is not a leaf.
        """
        return self.children[index+1].deep_min()
    
    def split_child(self, index):
        """
        Splits self's index-th child.
        Splitting divides that child into three parts:
            - The median key.
            - A new left node containing:
                    - The keys located at the left of the median key
                    - The left children of those keys together with
                      the left child of the median key.
            - A new right node containing:
                    - The keys located at the right of the median key in child
                    - the right child of the median key together with the
                      right children of the rest of those keys
        Then makes those nodes the left and right children of the median key
        and inserts the median key into self.
        """
        child = self.children[index] # Splits self's index-th child
        median = (child.num_keys())//2 # We divied the number of key to get the median 
        median_key = child.keys[median] # the median key
        left  = BTreeNode(child.keys[:median], child.children[:median + 1]) # the lift node of the median
        right = BTreeNode(child.keys[median + 1:], child.children[median + 1:]) # the right node of the median
        self.keys.insert(index, median_key) # the inserstion of the median
        self.children[index:index+1] = [left, right] # insert the left and the right child of the median

    def merge_children(self, index):
        """
        Merges self's index-th keyi and its left
        and right children into a single node.
        """
        median_key = self.keys[index] 
        left, right = self.children[index : index+2]

        left.keys.append(median_key) # add the hey in the end of the node
        left.keys.extend(right.keys) # Add the keys in the end of the node

        if not right.is_leaf():
            left.children.extend(right.children)

        del self.keys[index]
        del self.children[index+1]

        merged = left

        if self.num_keys() == 0:
            self.keys = left.keys
            self.children = left.children
            merged = self

        return merged    
    def delete_key(self, key):
        """
        Deletes key from self.
        """
        index = self.search_key(key) # Search for the key in the Tree
        if self.contains_key(key, index): # If the index contains the key 
            del self.keys[index] # Delete the index key

    def transfer_key_clockwise(self, index):
        """
        Let child be self's index-th child and let sibling be child's left sibling.
        This method transfers the largest key of sibling to self, replacing its
        index-th key. Then the replaced key and the rightmost child of sibling are
        transferred to child.
        """
        left, right = self.children[index : index+2]
        right.keys.insert(0, self.keys[index])

        if left.children:
            right.children.insert(0, left.children[-1])
            del left.children[-1]

        self.keys[index] = left.keys[-1]
        del left.keys[-1]


    def transfer_key_counter_clockwise(self, index):
        """
        Let child be self's index-th child and let sibling be the right sibling of
        child. This method transfers the smallest key of sibling to self, replacing
        its index-th key. Then the replaced key and the leftmost child of sibling
        are transferred to child.
        """
        left, right = self.children[index : index+2]
        left.keys.append(self.keys[index])

        if not right.is_leaf():
            left.children.append(right.children[0])
            del right.children[0]

        self.keys[index] = right.keys[0]
        del right.keys[0]


    def grow_child(self, index, min_keys):
        """
        Returns self's index-th child after increasing its number of
        keys by either:
            - Transferring a key from a direct sibling that contains
              more than min_keys keys or,
            - Merging with a sibling that contains at most min_keys
            keys.
        """
        child = self.children[index]
        left_sibling = (index > 0) and self.children[index-1]
        right_sibling = (index < self.num_keys()) and self.children[index+1]

        if left_sibling and left_sibling.num_keys() > min_keys: # We check if the left sibling and the number of keys in the left sibling > min keys 
            self.transfer_key_clockwise(index-1) # in this possition we transfer the key in the clockwise

        elif right_sibling and right_sibling.num_keys() > min_keys: # # otherwise  if the right siblinf and the number of key in the right sibling > min key
            self.transfer_key_counter_clockwise(index) # we transfer the the key in the opposite direction on the clockwise

        else:
            shared_key_index = (index - 1) if left_sibling else index
            child = self.merge_children(shared_key_index) # otherwise we merge the children in the left sibling

        return child 
        