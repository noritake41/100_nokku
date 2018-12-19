fname = 'hightemp.txt'
with open(fname) as data_file, \
        open('col1.txt', mode='w') as col1_file, \
        open('col2.txt', mode='w') as col2_file:
    for line in data_file:
        cols = line.split('\t')
        col1_file.write(cols[0] + '\n')
        col2_file.write(cols[1] + '\n')


"""
UNIXコマンド
cut -f 1 hightemp.txt > col1_test.txt
diff --report-identical-files col1.txt col1_test.txt
cut -f 2 hightemp.txt > col2_test.txt
diff --report-identical-files col2.txt col2_test.txt
"""
