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
                'pos1': res_cols[1]
            }
            morphemes.append(morpheme)

            if res_cols[1] == '句点':
                yield morphemes
                morphemes = []

parse_neko()

word_counter = Counter()
for line in neco_lines():
    word_counter.update([morpheme['surface'] for morpheme in line])

list_word = word_counter.most_common()

counts = list(zip(*list_word))[1]

fp = FontProperties(fname='/Users/administrator/Library/Fonts/azuki.ttf')

plt.scatter(range(1, len(counts) + 1), counts)

plt.xlim(1, len(counts) + 1)
plt.ylim(1, counts[0])

plt.xscale('log')
plt.yscale('log')

plt.title("39. Zipfの法則", fontproperties=fp)
plt.xlabel('出現度順位', fontproperties=fp)
plt.ylabel('出現頻度', fontproperties=fp)

plt.grid(axis='both')

plt.show()
