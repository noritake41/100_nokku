from itertools import groupby
fname = "hightemp.txt"

lines = open(fname).readlines()
kens = [line.split("\t")[0] for line in lines]

kens.sort()
result = [(ken, len(list(group))) for ken, group in groupby(kens)]

result.sort(key=lambda ken: ken[1], reverse=True)

for ken in result:
    print("{ken}({count})".format(ken=ken[0], count=ken[1]))


"""
cut -f 1 hightemp.txt | sort | uniq -c > result_test.txt
"""
