import unittest
from clustering import clustering_based_k_anon
from models.gentree import GenTree
from models.numrange import NumRange
import random
import pdb

A_tree= []

def init():
    global A_tree
    A_tree = []
    tree_temp = {}
    tree = GenTree('*')
    tree_temp['*'] = tree
    lt = GenTree('1,5', tree)
    tree_temp['1,5'] = lt
    rt = GenTree('6,10', tree)
    tree_temp['6,10'] = rt
    for i in range(1, 11):
        if i <= 5:
            t = GenTree(str(i), lt, True)
        else:
            t = GenTree(str(i), rt, True)
        tree_temp[str(i)] = t
    numrange = NumRange(['1', '2', '3', '4', '5',
                        '6', '7', '8', '9', '10'], dict())
    A_tree.append(tree_temp)
    A_tree.append(numrange)

class functionTest(unittest.TestCase):
    def test1_k_member(self):
        init()
        data = [['6', '1', 'haha'],
                ['6', '1', 'test'],
                ['8', '2', 'haha'],
                ['8', '2', 'test'],
                ['4', '1', 'hha'],
                ['4', '1', 'hha'],
                ['4', '3', 'hha'],
                ['4', '3', 'hha']]
        result, eval_r = clustering_based_k_anon(A_tree, data, 2)
        try:
            self.assertTrue(abs(eval_r[0] - 0) < 0.05)
        except AssertionError:
            print (data)
            print (result)
            print (eval_r)
            self.assertEqual(0, 1)

    def test2_k_member(self):
        init()
        data = [['6', '1', 'haha'],
                ['6', '1', 'test'],
                ['8', '2', 'haha'],
                ['8', '2', 'test'],
                ['4', '1', 'hha'],
                ['4', '2', 'hha'],
                ['4', '3', 'hha'],
                ['4', '4', 'hha']]
        result, eval_r = clustering_based_k_anon(A_tree, data, 2)
        try:
            self.assertTrue(abs(eval_r[0] - 2.77) < 0.05)
        except AssertionError:
            print (data)
            print (result)
            print (eval_r)
            self.assertEqual(0, 1)

if __name__ == '__main__':
    unittest.main()
