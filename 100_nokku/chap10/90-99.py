#90
import pickle
from collections import OrderedDict
import numpy as np
from scipy import io
import word2vec

fname_input = 'corpus81.txt'
fname_word2vec_out = 'vectors.txt'
fname_dict_index_t = 'dict_index_t'
fname_matrix_x300 = 'matrix_x300'

word2vec.word2vec(train = fname_input, output = fname_word2vec_out, size = 300, threads = 4, binary = 0)

with open(fname_word2vec_out, 'rt') as data_file:
    work = data_file.readline().split(' ')
    size_dict = int(work[0])
    size_x = int(work[1])
    dict_index_t = OrderedDict()
    matrix_x = np.zeros([size_dict, size_x], dtype = np.float64)
    for i, line in enumerate(data_file):
        work = line.strip().split(' ')
        dict_index_t[work[0]] = i
        matrix_x[i] = work[1:]

io.savemat(fname_matrix_x300, {'matrix_x300': matrix_x})
with open(fname_dict_index_t, 'wb') as data_file:
    pickle.dump(dict_index_t, data_file)

#91
fname_input = 'questions-words.txt'
fname_output = 'family.txt'

with open(fname_input, 'rt') as data_file, open(fname_output, 'wt') as out_file:
    target = False
    for line in data_file:
        if target is True:
            if line.startswith(': '):
                break
            print(line.strip(), file = out_file)
        elif line.startswith(': family'):
            target = True

#92
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

fname_dict_index_t = 'dict_index_t'
fname_matrix_x300 = 'matrix_x300'
fname_input = 'family.txt'
fname_output = 'family_out.txt'

def cos_sim(vec_a, vec_b):
    norm_ab = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if norm_ab != 0:
        return np.dot(vec_a, vec_b) / norm_ab
    else:
        return -1

with open(fname_dict_index_t, 'rb') as data_file:
    dict_index_t = pickle.load(data_file)

keys = list(dict_index_t.keys())

matrix_x300 = io.loadmat(fname_matrix_x300)['matrix_x300']

with open(fname_input, 'rt') as data_file, open(fname_output, 'wt') as out_file:
    for line in data_file:
        cols = line.split(' ')
        try:
            vec = matrix_x300[dict_index_t[cols[1]]] - matrix_x300[dict_index_t[cols[0]]] + matrix_x300[dict_index_t[cols[2]]]
            dist_max = -1
            index_max = 0
            result = ''
            for i in range(len(dict_index_t)):
                dist = cos_sim(vec, matrix_x300[i])
                if dist > dist_max:
                    index_max = i
                    dist_max = dist
            result = keys[index_max]
        except KeyError:
            result = ''
            dist_max = -1
        print('{} {} {}'.format(line.strip(), result, dist_max), file = out_file)
        print('{} {} {}'.format(line.strip(), result, dist_max))

#93
fname_input = 'family_out.txt'

with open(fname_input, 'rt') as data_file:
    correct = 0
    total = 0
    for line in data_file:
        cols = line.split(' ')
        total += 1
        if cols[3] == cols[4]:
            correct += 1

print('{} ({}/{})'.format(correct / total, correct, total))

#94
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

fname_dict_index_t = 'dict_index_t'
fname_matrix_x300 = 'matrix_x300'
fname_input = './wordsim353/combined.tab'
fname_output = 'combined_out.tab'

def cos_sim(vec_a, vec_b):
    norm_ab = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if norm_ab != 0:
        return np.dot(vec_a, vec_b) / norm_ab
    else:
        return -1

with open(fname_dict_index_t, 'rb') as data_file:
    dict_index_t = pickle.load(data_file)

matrix_x300 = io.loadmat(fname_matrix_x300)['matrix_x300']

with open(fname_input, 'rt') as data_file, open(fname_output, 'wt') as out_file:
    header = True
    for line in data_file:
        if header is True:
            header = False
            continue
        cols = line.split('\t')
        try:
            dist = cos_sim(matrix_x300[dict_index_t[cols[0]]], matrix_x300[dict_index_t[cols[1]]])
        except KeyError:
            dist = -1
        print('{}\t{}'.format(line.strip(), dist), file = out_file)

#95
import numpy as np

fname_input = 'combined_out.tab'

with open(fname_input, 'rt') as data_file:
    human_score = []
    my_score = []
    N = 0
    for line in data_file:
        cols = line.split('\t')
        human_score.append(float(cols[2]))
        my_score.append(float(cols[3]))
        N += 1

human_index_sorted = np.argsort(human_score)
my_index_sorted = np.argsort(my_score)

human_order = [0] * N
my_order = [0] * N
for i in range(N):
    human_order[human_index_sorted[i]] = i
    my_order[my_index_sorted[i]] = i

total = 0
for i in range(N):
    total += pow(human_order[i] - my_order[i], 2)

result = 1 - (6 * total) / (pow(N, 3) - N)

print(result)

#96
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

fname_dict_index_t = 'dict_index_t'
fname_matrix_x300 = 'matrix_x300'
fname_countries = 'countries.txt'

fname_dict_new = 'dict_index_country'
fname_matrix_new = 'matrix_x300_country'

with open(fname_dict_index_t, 'rb') as data_file:
    dict_index_t = pickle.load(data_file)

matrix_x300 = io.loadmat(fname_matrix_x300)['matrix_x300']

dict_new = OrderedDict()
matrix_new = np.empty([0, 300], dtype = np.float64)
count = 0

with open(fname_countries, 'rt') as data_file:
    for line in data_file:
        try:
            word = line.strip().replace(' ', '_')
            index = dict_index_t[word]
            matrix_new = np.vstack([matrix_new, matrix_x300[index]])
            dict_new[word] = count
            count += 1
        except:
            pass

io.savemat(fname_matrix_new, {'matrix_x300': matrix_new})
with open(fname_dict_new, 'wb') as data_file:
    pickle.dump(dict_new, data_file)

#97
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np
from sklearn.cluster import KMeans

fname_dict_index_t = 'dict_index_country'
fname_matrix_x300 = 'matrix_x300_country'

with open(fname_dict_index_t, 'rb') as data_file:
    dict_index_t = pickle.load(data_file)

matrix_x300 = io.loadmat(fname_matrix_x300)['matrix_x300']

predicts = KMeans(n_clusters = 5).fit_predict(matrix_x300)

result = zip(dict_index_t.keys(), predicts)

for country, category in sorted(result, key = lambda x: x[1]):
    print('{}\t{}'.format(category, country))

#98
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

#99
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

fname_dict_index_t = 'dict_index_country'
fname_matrix_x300 = 'matrix_x300_country'

with open(fname_dict_index_t, 'rb') as data_file:
    dict_index_t = pickle.load(data_file)

matrix_x300 = io.loadmat(fname_matrix_x300)['matrix_x300']

t_sne = TSNE(perplexity = 30, learning_rate = 500).fit_transform(matrix_x300)
print(t_sne)

predicts = KMeans(n_clusters = 5).fit_predict(matrix_x300)

fig, ax = plt.subplots()
cmap = plt.get_cmap('Set1')
for index, label in enumerate(dict_index_t.keys()):
    cval = cmap(predicts[index] / 4)
    ax.scatter(t_sne[index, 0], t_sne[index, 1], marker = '.', color = cval)
    ax.annotate(label, xy = (t_sne[index, 0], t_sne[index, 1]), color = cval)

plt.show()
