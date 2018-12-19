fname = "hightemp.txt"
with open(fname) as data_file:

    set_ken = set()
    for line in data_file:
        cols = line.split("\t")
        set_ken.add(cols[0])

for n in set_ken:
    print(n)

"""
このプログラムをファイルにソートして落とす
Python test0017.py | sort > result.txt

cut -f 1 hightemp.txt | sort | uniq > result_test.txt

確認
diff --report-identical-files result.txt result_test.txt
"""
