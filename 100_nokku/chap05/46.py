import CaboCha
import re

fname = 'neko.txt'
fname_parsed = 'neko.txt.cabocha'
fname_result = 'result.txt'

def parse_neko():
    with open(fname) as data_file, \
            open(fname_parsed, mode='w') as out_file:

        cabocha = CaboCha.Parser()
        for line in data_file:
            out_file.write(cabocha.parse(line).toString(CaboCha.FORMAT_LATTICE))

class Morph:
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def __str__(self):
        return 'surface[{}]\tbase[{}]\tpos[{}]\tpos1[{}]'\
            .format(self.surface, self.base, self.pos, self.pos1)

class Chunk:
    def __init__(self):
        self.morphs = []
        self.srcs = []
        self.dst = -1

    def __str__(self):
        surface = ''
        for morph in self.morphs:
            surface += morph.normalized_surface
        return '{}\tsrcs{}\tdst[{}]'.format(surface, self.srcs, self.dst)

    def normalized_surface(self):
        result = ''
        for morph in self.morphs:
            if morph.pos != '記号':
                result += morph.surface
        return result

    def chk_pos(self, pos):
        for morph in self.morphs:
            if morph.pos == pos:
                return True
        return False

    def get_morphs_by_pos(self, pos, pos1=''):
        if len(pos1) > 0:
            return [res for res in self.morphs
                    if (res.pos == pos) and (res.pos1 == pos1)]
        else:
            return [res for res in self.morphs if res.pos == pos]

    def get_kaku_prt(self):
        prts = self.get_morphs_by_pos('助詞')
        if len(prts) > 1:
            kaku_prts = self.get_morphs_by_pos('助詞', '格助詞')
            if len(kaku_prts) > 0:
                prts = kaku_prts
        if len(prts) > 0:
            return prts[-1].surface
        else:
            return ''

def neco_lines():
    with open(fname_parsed) as file_parsed:
        chunks = dict()
        idx = -1

        for line in file_parsed:
            if line == 'EOS\n':
                if len(chunks) > 0:
                    sorted_tuple = sorted(chunks.items(),key=lambda x: x[0])
                    yield list(zip(*sorted_tuple))[1]
                    chunks.clear()
                else:
                    yield []

            elif line[0] == '*':
                cols = line.split(' ')
                idx = int(cols[1])
                dst = int(re.search(r'(.*?)D', cols[2]).group(1))

                if idx not in chunks:
                    chunks[idx] = Chunk()
                chunks[idx].dst = dst

                if dst != -1:
                    if dst not in chunks:
                        chunks[dst] = Chunk()
                    chunks[dst].srcs.append(idx)
            else:
                cols = line.split('\t')
                res_cols = cols[1].split(',')
                chunks[idx].morphs.append(
                    Morph(
                        cols[0],
                        res_cols[6],
                        res_cols[0],
                        res_cols[1]
                    )
                )
        raise StopIteration

parse_neko()

with open(fname_result, mode='w') as out_file:
    for chunks in neco_lines():
        for chunk in chunks:
            verbs = chunk.get_morphs_by_pos('動詞')
            if len(verbs) < 1:
                continue

            chunks_include_prt = []
            for src in chunk.srcs:
                if len(chunks[src].get_kaku_prt()) > 0:
                    chunks_include_prt.append(chunks[src])
            if len(chunks_include_prt) < 1:
                continue

            chunks_include_prt.sort(key=lambda x: x.get_kaku_prt())

            out_file.write('{}\t{}\t{}\n'.format(
                verbs[0].base,
                ' '.join([chunk.get_kaku_prt() \
                        for chunk in chunks_include_prt]),
                ' '.join([chunk.normalized_surface() \
                        for chunk in chunks_include_prt])
                ))
