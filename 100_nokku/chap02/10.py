fname = '/Users/administrator/Documents/hightemp.txt'
count = 0
with open(fname) as data_file:
    for line in data_file:
        count += 1
print(count)


"""
UNIXコマンド
wc -line hightemp.txt では通らない
wc -l hightemp.txt
"""
