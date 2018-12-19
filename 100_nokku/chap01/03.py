s = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."

t = s.split(" ")

r = []

for i in t:
    r.append(len(i) - i.count(',') - i.count('.'))

print(r)
