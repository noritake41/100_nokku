fname = "hightemp.txt"
lines = open(fname).readlines()
lines.sort(key=lambda line: float(line.split("\t")[2]), reverse = True)

for line in lines:
    print(line, end=" ")


"""
python test0018.py > result.txt

sort hightemp.txt --key=3,3 --numeric-sort --reverse > result_test.txt

diff --report-identical-files result.txt result_test.txt
"""
