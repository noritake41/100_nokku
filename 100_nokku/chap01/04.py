s = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."

n = (1, 5, 6, 7, 8, 9, 15, 16, 19)

t = s.split(" ")

r = {}

for (num, word) in enumerate(t, 1):
    if num in n:
        r[word[0:1]] = num
    else:
        r[word[0:2]] = num

print(r)
