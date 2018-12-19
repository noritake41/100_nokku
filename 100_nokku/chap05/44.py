import CaboCha
import re
import pydot_ng as pydot

fname = 'neko.txt.tmp'
fname_parsed = 'neko.txt.cabocha.tmp'

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
            surface += morph.surface
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

def neco_lines():
    with open(fname_parsed) as file_parsed:
        chunks = dict()
        idx = -1

        for line in file_parsed:
            if line == 'EOS\n':
                if len(chunks) > 0:
                    sorted_tuple = sorted(chunks.items(), key=lambda x: x[0])
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

def graph_from_edges_ex(edge_list, directed=False):
    if directed:
        graph = pydot.Dot(graph_type='digraph')
    else:
        graph = pydot.Dot(graph_type='graph')

    for edge in edge_list:
        id1 = str(edge[0][0])
        label1 = str(edge[0][1])
        id2 = str(edge[1][0])
        label2 = str(edge[1][1])

        graph.add_node(pydot.Node(id1, label=label1))
        graph.add_node(pydot.Node(id2, label=label2))

        graph.add_edge(pydot.Edge(id1, id2))

    return graph

with open(fname, mode='w') as out_file:
    out_file.write(input('文字列を入力してください--> '))

parse_neko()

for chunks in neco_lines():
    edges = []
    for i, chunk in enumerate(chunks):
        if chunk.dst != -1:
            src = chunk.normalized_surface()
            dst = chunks[chunk.dst].normalized_surface()
            if src != '' and dst != '':
                edges.append(((i, src), (chunk.dst, dst)))

    if len(edges) > 0:
        graph = graph_from_edges_ex(edges, directed=True)
        graph.write_png('result.png')
