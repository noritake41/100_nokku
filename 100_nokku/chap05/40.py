import CaboCha
fname = 'neko.txt'
fname_parsed = 'neko.txt.cabocha'

def parse_neko():
    with open(fname) as data_file, \
            open(fname_parsed, mode='w') as out_file:

        cabocha = CaboCha.Parser()
        for line in data_file:
            out_file.write(
                cabocha.parse(line).toString(CaboCha.FORMAT_LATTICE)
            )

class Morph:
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def __str__(self):
        return 'surface[{}]\tbase[{}]\tpos[{}]\tpos1[{}]'\
            .format(self.surface, self.base, self.pos, self.pos1)


def neco_lines():
    with open(fname_parsed) as file_parsed:

        morphs = []
        for line in file_parsed:

            if line == 'EOS\n':
                yield morphs
                morphs = []

            else:
                if line[0] == '*':
                    continue

                cols = line.split('\t')
                res_cols = cols[1].split(',')

                morphs.append(Morph(
                    cols[0],
                    res_cols[6],
                    res_cols[0],
                    res_cols[1]
                ))

        raise StopIteration

parse_neko()

for i, morphs in enumerate(neco_lines(), 1):

    if i == 3:
        for morph in morphs:
            print(morph)
        break
