import MeCab
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

fname = 'neko.txt'
fname_parsed = 'neko.txt.mecab'

def parse_neko():
    with open(fname) as data_file, \
            open(fname_parsed, mode='w') as out_file:

        mecab = MeCab.Tagger()
        out_file.write(mecab.parse(data_file.read()))

def neco_lines():
    with open(fname_parsed) as file_parsed:

        morphemes = []
        for line in file_parsed:
            cols = line.split('\t')
            if(len(cols) < 2):
                #raise StopIteration
                break
            res_cols = cols[1].split(',')

            morpheme = {
                'surface': cols[0],
                'base': res_cols[6],
                'pos': res_cols[0],
                'pos1': res_cols[1],
            }
            morphemes.append(morpheme)

            if res_cols[1] == '句点':
                yield morphemes
                morphemes = []

parse_neko()

word_counter = Counter()
for line in neco_lines():
    word_counter.update([morpheme['surface'] for morpheme in line])

size = 10
list_word = word_counter.most_common(size)
print(list_word)

list_zipped = list(zip(*list_word))
words = list_zipped[0]
counts = list_zipped[1]

fp = FontProperties(fname='/Users/administrator/Library/Fonts/azuki.ttf')

plt.bar(
    range(0, size),
    counts,
    align='center'
)

plt.xticks(
    range(0, size),
    words,
    fontproperties=fp
)

plt.xlim(
    xmin=-1, xmax=size
)

plt.title(
    '37. 頻度上位10語',
    fontproperties=fp
)
plt.xlabel(
    '出現頻度が高い10語',
    fontproperties=fp
)
plt.ylabel(
    '出現頻度',
    fontproperties=fp
)

plt.grid(axis='y')

plt.show()
