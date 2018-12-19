import bz2
fname_input = 'enwiki-20150112-400-r100-10576.txt.bz2'
fname_output = 'corpus80.txt'

with bz2.open(fname_input, 'rt') as data_file, \
        open(fname_output, mode='w') as out_file:
    for line in data_file:

        tokens = []
        for chunk in line.split(' '):
            token = chunk.strip().strip('.,!?;:()[]\'"')
            if len(token) > 0:
                tokens.append(token)

        print(*tokens, sep=' ', end='\n', file=out_file)
