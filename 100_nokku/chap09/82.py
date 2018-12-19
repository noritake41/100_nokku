import random
fname_input = 'corpus81.txt'
fname_output = 'context.txt'

with open(fname_input, 'rt') as data_file, \
        open(fname_output, mode='wt') as out_file:
    for i, line in enumerate(data_file):

        tokens = line.strip().split(' ')
        for j in range(len(tokens)):

            t = tokens[j]
            d = random.randint(1, 5)

            for k in range(max(j - d, 0), min(j + d + 1, len(tokens))):
                if j != k:
                    print('{}\t{}'.format(t, tokens[k]), file=out_file)

        if i % 10000 == 0:
            print('{} done.'.format(i))
