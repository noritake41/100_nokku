fname_input = 'corpus80.txt'
fname_output = 'corpus81.txt'
fname_countries = 'countries.txt'

set_country = set()
dict_country = {}
with open(fname_countries, 'rt') as data_file:
    for line in data_file:
        words = line.split(' ')
        if len(words) > 1:

            set_country.add(line.strip())

            if words[0] in dict_country:
                lengths = dict_country[words[0]]
                if not len(words) in lengths:
                    lengths.append(len(words))
                    lengths.sort(reverse=True)
            else:
                dict_country[words[0]] = [len(words)]

with open(fname_input, 'rt') as data_file, \
        open(fname_output, mode='wt') as out_file:
    for line in data_file:
        tokens = line.strip().split(' ')
        result = []
        skip = 0
        for i in range(len(tokens)):
            if skip > 0:
                skip -= 1
                continue

            if tokens[i] in dict_country:
                hit = False
                for length in dict_country[tokens[i]]:
                    if ' '.join(tokens[i:i + length]) in set_country:
                        result.append('_'.join(tokens[i:i + length]))
                        skip = length - 1
                        hit = True
                        break
                if hit:
                    continue

            result.append(tokens[i])

        print(*result, sep=' ', end='\n', file=out_file)
