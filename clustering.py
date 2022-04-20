import random
import numpy
import time
from tools.tools import get_num_list_from_str, cmp_str, quasi_to_key
from models.gentree import GenTree
from models.numrange import NumRange
import functools

__DEBUG = False
QI_length = 0
IS_CAT = []
NCP_CACHE = {}
A_trees = []
len_data = 0
QI_range= []

class Cluster(object):

	def __init__(self, mem, gen_result, IF_loss=0.0):
		self.IF_loss= IF_loss
		self.mem= mem
		self.gen_result = gen_result[:]
		self.centre= gen_result[:]
		for i in range(QI_length):
			if IS_CAT[i] is False:
				self.centre[i] = str(sum([float(t[i]) for t in self.mem]) * 1.0/len(self.mem))

	def record_addition(self, record):

		self.mem.append(record)
		self.update_gen_result(record, record)

	def cluster_update(self):

		self.gen_result = cluster_generalization(self.mem)
		for i in range(QI_length):
			if IS_CAT[i]:
				self.centre[i] = self. gen_result[i]
			else: 
				self.centre[i] = str(sum([float(t[i]) for t in self.mem]) * 1.0 / len(self.mem))
		self.IF_loss = len(self.mem) * NCP(self.gen_result)

	def update_gen_result(self, merge_gen_result, centre, num=1):
		"""
		Explanation: updating gen_result and if loss after adding record or merging cluster
		"""

		self.gen_result = generalization(self.gen_result, merge_gen_result)
		current_len = len(self.mem)
		for i in range(QI_length):
			if IS_CAT[i]:
				self.centre[i] = self.gen_result[i]
			else:
				self.centre[i] = str((float(self.centre[i]) * current_len - num) + float(centre[i] * num) / current_len)
				self.IF_loss = len(self.mem) * NCP(self.gen_result)

	def add_record_with_same_quasi(self, record):

		self.mem.append(record)

	def merge_cluster(self, cluster):
		"""
		Merging cluster into self without deleting elements
		"""

		self.mem.extend(cluster.mem)
		self.update_gen_result(cluster.gen_result, cluster.centre, len(cluster))

	def __getitem__(self, item):
		return self.gen_result[item]

	def __len__(self):
		return len(self.mem)

	def __str__(self):
		return str(self.gen_result)

def distance_in_clusters(source, target):
	"""
	This function's purpose is to return the distance between
	the source cluster/record and target cluster/record.
	This uses Normalizes Certainity Penality which penalizes items
	based on the way they are generalized. 
	"""
	source_gen = source
	target_gen = target
	source_length = 1
	target_length = 1
	if isinstance(target, Cluster):
		target_gen = target.gen_result
		target_length = len(target)
	if isinstance(source, Cluster):
		source_gen = source.gen_result
		source_length = len(source)
	if source_gen == target_gen:
		return 0
	gen = generalization(source_gen, target_gen)
	distance = (source_length + target_length) * NCP(gen)
	return distance

def diff_dist(record, cluster):
	"""
	Explanation: This functions need to return IL(c U {r}) - IL(c)
	"""
	IL_cluster_and_record = generalization(record, cluster.gen_result)
	return NCP(IL_cluster_and_record) * (len(cluster) + 1) - cluster.IF_loss


def NCP(record):

	ncp= 0.0
	list_key = quasi_to_key(record)
	try:
		return NCP_cache[list_key]
	except KeyError:
		pass
	for i in range(QI_length):
		width = 0.0
		if IS_CAT[i] is False:
			try:
				float(record[i])
			except ValueError:
				temp = record[i].split(',')
				width = float(temp[1]) - float(temp[0])
		else:
			width = len(A_trees[i][record[i]]) * 1.0
		width /= QI_range[i]
		ncp += width
	NCP_cache[list_key] = ncp
	return ncp

def lowest_common_ancestor(index, item1, item2):
	if item1 == item2:
		return item1
	try: 
		return LCA_cache[index][item1 + item2]
	except KeyError:
		pass
	p1 = A_trees[index][item1].parent[:]
	p2 = A_trees[index][item2].parent[:]
	p1.insert(0, A_trees[index][item1])
	p2.insert(0, A_trees[index][item2])
	min_length= min(len(p1), len(p2))
	last_lca = p1[-1]
	for i in range(1, min_length +1):
		if p1[-i].value == p2[-i].value:
			last_lca = p1[-i]
		else:
			break
	LCA_cache[index][item1 + item2] = last_lca.value
	return last_lca.value

def generalization(record1, record2):
    """
    Compute relational generalization result of record1 and record2
    """
    gen = []
    for i in range(QI_length):
        if IS_CAT[i] is False:
            split_number = []
            split_number.extend(get_num_list_from_str(record1[i]))
            split_number.extend(get_num_list_from_str(record2[i]))
            split_number = list(set(split_number))
            if len(split_number) == 1:
                gen.append(split_number[0])
            else:
                split_number.sort(key=functools.cmp_to_key(cmp_str))
                gen.append(split_number[0] + ',' + split_number[-1])
        else:
            gen.append(lowest_common_ancestor(i, record1[i], record2[i]))
    return gen


def get_furthest_record(record, data):
	"""
	Explanantion: If r is a randomly picked record from S (set of records)
	This function finds the furthest record from r
	"""

	max_dist = 0
	max_i = -1
	for i in range(len(data)):
		current = distance_in_clusters(record, data[i])
		if current >= max_dist:
			max_dist = current
			max_i = i
	return max_i

def find_best_record(cluster, data):
	"""
	Explanation: We need to ensure that IL (information loss)
	is minimal therefore we return the record's index with the minimum
	difference on IL
	"""
	min_diff = 100000000000
	min_i = 0
	for i, record in enumerate(data):
		Info_loss_diff = diff_dist(record, cluster)
		if Info_loss_diff < min_diff:
			min_diff = Info_loss_diff
			min_i = i
	return min_i

def find_best_cluster(record, clusters):
	"""
	Explanation: Given a set of clusters and a record, this function
	needs to output a custer such that information loss is minimal
	"""
	min_diff= 1000000000000
	min_i= 0
	best = clusters[0]
	for i, c in enumerate(clusters):
		Info_loss_diff = diff_dist(record, c)
		if Info_loss_diff < min_diff:
			min_dist = Info_loss_diff
			min_i = i
			best = c
	return min_i
	
def clustering_kmember(data, k=25):

	clusters = []
	rand_seed = random.randrange(len(data))
	rand_i = data[rand_seed]
	while len(data) >= k:
			rand_seed = get_furthest_record(rand_i, data)
			rand_i = data.pop(rand_seed)
			cluster = Cluster([rand_i], rand_i)
			while len(cluster) <k:
				rand_seed = find_best_record(cluster, data)
				rand_j = data.pop(rand_seed)
				cluster.record_addition(rand_j)
			clusters.append(cluster)
	while len(data) > 0:
		t = data.pop()
		cluster_i = find_best_cluster(t, clusters)
		clusters[cluster_i].record_addition(t)
	return clusters

def init(a_trees, data, QI_num=-1):
    """
    init global variables
    """
    global A_trees, len_data, QI_range, IS_CAT, QI_length, LCA_cache, NCP_cache
    A_trees = a_trees
    QI_range = []
    IS_CAT = []
    len_data = len(data)
    LCA_cache = []
    NCP_cache = {}
    if QI_num <= 0:
        QI_length = len(data[0]) - 1
    else:
        QI_length = QI_num
    for i in range(QI_length):
        LCA_cache.append(dict())
        if isinstance(A_trees[i], NumRange):
            IS_CAT.append(False)
            QI_range.append(A_trees[i].range)
        else:
            IS_CAT.append(True)
            QI_range.append(len(A_trees[i]['*']))

def clustering_based_k_anon(a_trees, data, k=10, QI_num=-1):
    """
    the main function of clustering based k-anon
    """
    init(a_trees, data, QI_num)
    result = []
    start_time = time.time()
    print("K-Member Clustering beginning")
    clusters = clustering_kmember(data, k)
    rtime = float(time.time() - start_time)
    ncp = 0.0
    for cluster in clusters:
        final_result = []
        for i in range(len(cluster)):
            final_result.append(cluster.gen_result + [cluster.mem[i][-1]])
        result.extend(final_result)
        ncp += cluster.IF_loss
        #print (final_result)
    ncp /= len_data
    ncp /= QI_length
    ncp *= 100
    if __DEBUG:
        print ("NCP=", ncp)
    return (result, (ncp, rtime))

