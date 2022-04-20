from clustering import clustering_based_k_anon
from tools.read_adult_data import read_data as read_adult
from tools.read_adult_data import read_tree as read_adult_tree
import sys
import copy
import pdb
import random
import cProfile
import matplotlib.pyplot as plt

DATA_SELECT = 'a'
DEFAULT_K = 2
__DEBUG = True
x= []
y= []

def extend_result(val):
    """
    separated with ',' if it is a list
    """
    if isinstance(val, list):
        return ','.join(val)
    return val


def write_to_file(result, k):
    """
    write the anonymized result to anonymized.data
    """
    with open("data/anonymized_k_is_%d.data" %k, "w") as output:
        for r in result:
            output.write(';'.join(map(extend_result, r)) + '\n')
 

def get_results(a_trees, data, k=DEFAULT_K):
    print ("run clustering_based_k_anon")
    data_back = copy.deepcopy(data)
    while (k < 11):
        print ("K=%d" % k)
        result, eval_result = clustering_based_k_anon(a_trees, data, k)
        write_to_file(result, k)
        data = copy.deepcopy(data_back)
        print ("NCP (degree of information loss): %0.2f" % eval_result[0] + "%")
        x.append(k)
        y.append(eval_result[0])
        print ("Running time: %0.2f" % eval_result[1] + " seconds")
        print()
        k= k+1
    get_graph(x, y)

def get_graph(x, y):
    plt.plot(x,y)
    plt.xlabel('Value of K')
    plt.ylabel('Degree of information loss')
    plt.title("Line graph showing an increase of k and the effect on utility of information")
    plt.show()

if __name__ == '__main__':
    FLAG = 'trial'
    LEN_ARGV = len(sys.argv)
    try:
        DATA_SELECT = sys.argv[1]
        FLAG = sys.argv[2]
    except IndexError:
        pass
    INPUT_K = 5
    # read record
    if DATA_SELECT == 'a':
    	print ("Adult data")
    	DATA = read_adult()
    	A_TREES = read_adult_tree()
    if __DEBUG:
        print (sys.argv)
    if FLAG == 'trial':
        get_results(A_TREES, DATA)
    else:
        try:
            INPUT_K = int(FLAG)
            get_result_one(A_TREES, DATA, INPUT_K)
        except ValueError:
            print ("Usage: python anonymizer for k-member")
            print ("a: adult dataset")
            print ("example: python anonymizer a kmember k")
    # anonymized dataset is stored in result
    print ("Finish Cluster based K-Anon!!")
