# Create a node
import os
#from typing_extensions import Self
from Btree_Node import BTreeNode

#from isort import file

# Create a btree       
class BTree:
    file_path = "./tree.dot"
    """
    B-Tree data structure.
    """
    def __init__(self, degree):
        self.root = BTreeNode([], [])
        self.min_keys = degree - 1 
        self.max_keys = 2*degree - 1
        
    def insert_key(self, key):
        """
        Inserts key in the b-tree.
        """
        if self.root.num_keys() == self.max_keys:
            self.root = BTreeNode([], [self.root])
            self.root.split_child(0)
        node = self.root 
        while not node.is_leaf():
            index = node.search_key(key)
            child = node.children[index]
            if child.num_keys() == self.max_keys:
                node.split_child(index)

                if node.keys[index] < key:
                    index += 1
            node = node.children[index] 
        node.insert_key(key)
        
    def search_key(self, key):
        """
        Returns an empty b-tree with the given degree.
        Note: Assumes degree > 1.
        """
        (node, index) = self.root, self.root.search_key(key)
        while not node.contains_key(key, index) and not node.is_leaf():
            node = node.children[index]
            index = node.search_key(key)

        return (node, index) if node.contains_key(key, index) else None
    
    def delete_key(self, key):
        """
        Deletes key from the b-tree.
        """
        node = self.root
        while not node.is_leaf():
            index = node.search_key(key)

            if node.contains_key(key, index):
                left, right = node.children[index : index+2]

                if left.num_keys() > self.min_keys:
                    node.keys[index] = node.deep_predecessor(index)
                    (node, key) = (left, node.keys[index])

                elif right.num_keys() > self.min_keys:
                    node.keys[index] = node.deep_successor(index) 
                    (node, key) = (right, node.keys[index])

                else:
                    node = node.merge_children(index)

            else:
                child = node.children[index]
                if child.num_keys() <= self.min_keys:
                   child = node.grow_child(index, self.min_keys)
                node = child
                    
        node.delete_key(key)
        
    def print_tree(self, x, l=0):
        """
        Print the tree
        @param x le nb de keys
        @param l level
        
        """
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(x.children) > 0:
            for i in x.children:
                self.print_tree(i, l)

    """
    Print BTree with dot
    """
    def print_nodes(self, node=BTreeNode):
            file = open(BTree.file_path, "a")

            self.print_one_node(node)

            if node.is_leaf():
                pass
            else:
                for child in node.get_children():
                    self.print_nodes(child)
            file.close()
            return
    
    def print_one_node(self, node):
        file = open(BTree.file_path, "a")

        file.write("\"[")
        for key in node.get_keys():
            file.write(" {}".format(key))
        file.write(" ]\"\n")

        file.close()
        return

    def link_parent_with_child(self, node=BTreeNode):

        if node.is_leaf():

            return
        else:
            for child in node.get_children():
                self.print_one_node(node)
                file = open(BTree.file_path, "a")
                file.write(" -> \n")
                file.close()
                self.print_one_node(child)

            for child in node.get_children():
                self.link_parent_with_child(child)
        return

    def print_with_dot(self):
        if os.path.isfile(BTree.file_path):
            os.remove(BTree.file_path)

        self.entete_pour_dot()

        self.print_nodes(self.root)

        self.link_parent_with_child(self.root)

        file = open(BTree.file_path, "a")
        file.write("}")
        file.close()
        return

    def entete_pour_dot(self):
        file = open(BTree.file_path, "a")

        file.write("digraph \"BTree\" {\n node [fontname=\"DejaVu-Sans\", shape=circle]\n ")
        #file.write()
        file.close()
        return