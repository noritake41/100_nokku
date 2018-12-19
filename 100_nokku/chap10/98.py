import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

from scipy.cluster.hierarchy import ward, dendrogram
from matplotlib import pyplot as plt

fname_dict_index_t = 'dict_index_country'
fname_matrix_x300 = 'matrix_x300_country'

with open(fname_dict_index_t, 'rb') as data_file:
    dict_index_t = pickle.load(data_file)

matrix_x300 = io.loadmat(fname_matrix_x300)['matrix_x300']

ward = ward(matrix_x300)
print(ward)

dendrogram(ward, labels = list(dict_index_t.keys()), leaf_font_size = 8)
plt.show()
