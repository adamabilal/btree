from Btree import  BTree, BTreeNode
import time


def main():

    B = BTree(2)
    
    list = [i for i in range(20) ]
    for key in list:
        B.insert_key(key)
        B.print_with_dot()
        time.sleep(3)
    
    # time.sleep(3)
    # for i in range(11):
    #     B.delete_key(list[i])
    #     B.print_with_dot()
    
    # B.delete_key(11)
    # B.print_with_dot()
    # return

    for key in list:
        B.delete_key(key)
        B.print_with_dot()
        time.sleep(3)

    B.print_tree(B.root)
        
if __name__ == '__main__':
    main()