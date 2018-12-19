fname = '/Users/administrator/Documents/hightemp.txt'
with open(fname) as data_file:
    for line in data_file:
        print(line.replace('\t', ' '), end='')


"""
UNIXコマンド
sed 's/\t/ /g' hightemp.txt←変化なしだが合っている
tr '\t' ' ' < hightemp.txt
expand -t 1 hightemp.txt
"""
