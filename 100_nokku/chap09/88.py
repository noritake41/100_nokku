import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

fname_dict_index_t = 'dict_index_t'
fname_matrix_x300 = 'matrix_x300'

def cos_sim(vec_a, vec_b):
    norm_ab = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if norm_ab != 0:
        return np.dot(vec_a, vec_b) / norm_ab
    else:
        return -1

with open(fname_dict_index_t, 'rb') as data_file:
        dict_index_t = pickle.load(data_file)

matrix_x300 = io.loadmat(fname_matrix_x300)['matrix_x300']

vec_England = matrix_x300[dict_index_t['England']]
distances = [cos_sim(vec_England, matrix_x300[i])
        for i in range(0, len(dict_index_t))]

index_sorted = np.argsort(distances)
keys = list(dict_index_t.keys())
for index in index_sorted[-2:-12:-1]:
    print('{}\t{}'.format(keys[index], distances[index]))
