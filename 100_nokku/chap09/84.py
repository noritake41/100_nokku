import math
import pickle
from collections import Counter
from collections import OrderedDict
from scipy import sparse, io

fname_counter_tc = 'counter_tc'
fname_counter_t = 'counter_t'
fname_counter_c = 'counter_c'
fname_matrix_x = 'matrix_x'
fname_dict_index_t = 'dict_index_t'
N = 68045254

with open(fname_counter_tc, 'rb') as data_file:
    counter_tc = pickle.load(data_file)
with open(fname_counter_t, 'rb') as data_file:
    counter_t = pickle.load(data_file)
with open(fname_counter_c, 'rb') as data_file:
    counter_c = pickle.load(data_file)

dict_index_t = OrderedDict((key, i) for i, key in enumerate(counter_t.keys()))
dict_index_c = OrderedDict((key, i) for i, key in enumerate(counter_c.keys()))

size_t = len(dict_index_t)
size_c = len(dict_index_c)
matrix_x = sparse.lil_matrix((size_t, size_c))

for k, f_tc in counter_tc.items():
    if f_tc >= 10:
        tokens = k.split('\t')
        t = tokens[0]
        c = tokens[1]
        ppmi = max(math.log((N * f_tc) / (counter_t[t] * counter_c[c])), 0)
        matrix_x[dict_index_t[t], dict_index_c[c]] = ppmi

io.savemat(fname_matrix_x, {'matrix_x': matrix_x})
with open(fname_dict_index_t, 'wb') as data_file:
    pickle.dump(dict_index_t, data_file)
