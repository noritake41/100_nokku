import MeCab
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

nouns = set()
nouns_test = []
lines = neco_lines()
for line in lines:
    for morpheme in line:
        if morpheme['pos'] == '名詞' and morpheme['pos1'] == 'サ変接続':
            nouns.add(morpheme['surface'])
            nouns_test.append(morpheme['surface'])

print(sorted(nouns, key=nouns_test.index))
