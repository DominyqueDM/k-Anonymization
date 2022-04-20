from models.gentree import GenTree
from models.numrange import NumRange
from tools.tools import cmp_str
import pickle
import functools
import pdb

A_NAMES = ['age', 'workclass', 'education','marital_status', 'occupation', 'relationship',
             'race', 'sex', 'hours_per_week',
             'origin_country', 'income']
# 7 attributes are chose as QI attributes
# age treated as numeric attributes
# only matrial_status and workclass has well defined generalization hierarchies.
# other categorical attributes only have 2-level generalization hierarchies.
QI_INDEX = [0, 1, 3, 4, 6, 7, 9]
IS_CAT = [False, True, True, True, True, True, True]
SA_INDEX = -1

__DEBUG = False


def read_data():
    """
    read microda for *.txt and return read data
    """
    QI_num = len(QI_INDEX)
    data = []
    numeric_dict = []
    for i in range(QI_num):
        numeric_dict.append(dict())
    # oder categorical attributes in intuitive order
    # here, we use the appear number
    data_file = open('data/adult.data', 'rU')
    for line in data_file:
        line = line.strip()
        # remove empty and incomplete lines
        # only 30162 records will be kept
        if len(line) == 0 or '?' in line:
            continue
        # remove double spaces
        line = line.replace(' ', '')
        temp = line.split(',')
        ltemp = []
        for i in range(QI_num):
            index = QI_INDEX[i]
            if IS_CAT[i] is False:
                try:
                    numeric_dict[i][temp[index]] += 1
                except:
                    numeric_dict[i][temp[index]] = 1
            ltemp.append(temp[index])
        ltemp.append(temp[SA_INDEX])
        data.append(ltemp)
    # pickle numeric attributes and get NumRange
    for i in range(QI_num):
        if IS_CAT[i] is False:
            static_file = open('data/adult_' + A_NAMES[QI_INDEX[i]] + '_static.pickle', 'wb')
            sort_value = list(numeric_dict[i].keys())
            sort_value.sort(key=functools.cmp_to_key(cmp_str))
            pickle.dump((numeric_dict[i], sort_value), static_file)
            static_file.close()
    return data


def read_tree():
    """read tree from data/tree_*.txt, store them in att_tree
    """
    att_names = []
    att_trees = []
    for t in QI_INDEX:
        att_names.append(A_NAMES[t])
    for i in range(len(att_names)):
        if IS_CAT[i]:
            att_trees.append(read_tree_file(att_names[i]))
        else:
            att_trees.append(read_pickle_file(att_names[i]))
    return att_trees


def read_pickle_file(att_name):
    """
    read pickle file for numeric attributes
    return numrange object
    """
    try:
        static_file = open('data/adult_' + att_name + '_static.pickle', 'rb')
        (numeric_dict, sort_value) = pickle.load(static_file)
    except:
        print ("Pickle file not exists!!")
    static_file.close()
    result = NumRange(sort_value, numeric_dict)
    return result


def read_tree_file(treename):
    """read tree data from treename
    """
    leaf_to_path = {}
    att_tree = {}
    prefix = 'data/adult_'
    postfix = ".txt"
    treefile = open(prefix + treename + postfix, 'rU')
    att_tree['*'] = GenTree('*')
    if __DEBUG:
        print ("Reading Tree" + treename)
    for line in treefile:
        # delete \n
        if len(line) <= 1:
            break
        line = line.strip()
        temp = line.split(';')
        # copy temp
        temp.reverse()
        for i, t in enumerate(temp):
            isleaf = False
            if i == len(temp) - 1:
                isleaf = True
            # try and except is more efficient than 'in'
            try:
                att_tree[t]
            except KeyError:
                att_tree[t] = GenTree(t, att_tree[temp[i - 1]], isleaf)
    if __DEBUG:
        print ("Nodes No. = %d" % att_tree['*'].support)
    treefile.close()
    return att_tree
