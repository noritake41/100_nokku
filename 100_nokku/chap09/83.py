from collections import Counter
import pickle

fname_input = 'context.txt'
fname_counter_tc = 'counter_tc'
fname_counter_t = 'counter_t'
fname_counter_c = 'counter_c'

counter_tc = Counter()
counter_t = Counter()
counter_c = Counter()

work_tc = []
work_t = []
work_c = []
with open(fname_input, 'rt') as data_file:
    for i, line in enumerate(data_file, start=1):

        line = line.strip()
        tokens = line.split('\t')

        work_tc.append(line)
        work_t.append(tokens[0])
        work_c.append(tokens[1])

        if i % 1000000 == 0:
            counter_tc.update(work_tc)
            counter_t.update(work_t)
            counter_c.update(work_c)
            work_tc = []
            work_t = []
            work_c = []
            print('{} done.'.format(i))

counter_tc.update(work_tc)
counter_t.update(work_t)
counter_c.update(work_c)

with open(fname_counter_tc, 'wb') as data_file:
    pickle.dump(counter_tc, data_file)
with open(fname_counter_t, 'wb') as data_file:
    pickle.dump(counter_t, data_file)
with open(fname_counter_c, 'wb') as data_file:
    pickle.dump(counter_c, data_file)

print('N={}'.format(i))
