import unittest
from Btree import BTree,BTreeNode
import time

class TestBtree(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        super(TestBtree, self).__init__(*args, **kwargs)
        self.btree = BTree(2)
        list = [0,3,5,10,15,20,25,30]
        for x in list:
            self.btree.insert_key(x)
        self.btree.delete_key(3)
        

            
    def test_search(self):
        self.assertTrue(self.btree.search_key(10))
        self.assertFalse(self.btree.search_key(50))
        

    def test_delete(self):
        self.assertTrue(self.btree.search_key(3)==None)
        self.assertFalse(self.btree.search_key(15)==None)
    


    def test_with_dot(self):
        B = BTree(2)
        list = [i for i in range(20)]

        for key in list:
            B.insert_key(key)
            B.print_with_dot()
            time.sleep(2)

        for key in list:
            B.delete_key(key)
            B.print_with_dot()
            time.sleep(3)

        
        
      

if __name__ == '__main__':
    unittest.main()