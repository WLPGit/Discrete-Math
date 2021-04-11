with open('countries.txt') as f:
    countries = [i.replace('\n', '') for i in f.readlines()]

delimiter = ':'

clist = []

for i in countries:
    this = i.split()
    if len(this) == 1:
        clist.append(this[0] + ':None\n')
    if len(this) == 2:
        clist.append(this[0] + ":" + this[1] + '\n')
    if len(this) == 3:
        clist.append(this[0] + ":" + this[1] + " " + this[2] + '\n')
print(clist)
with open('countries_fixed.txt', 'w') as f:
    for i in clist:
        f.write(i)
