n = int(input("数字を入力してください--> "))
if n > 0:
    with open("hightemp.txt") as data_file:
        lines = data_file.readlines()
    for line in lines[-n:]:
        print(line.rstrip())


"""
tail -n 1 hightemp.txt
"""
