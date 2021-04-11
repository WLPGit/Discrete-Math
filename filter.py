class Pair():
    def __init__(self, a, b):
        self.first = a
        self.second = b
    def reversed(self):
        return Pair(self.second, self.first)
    def __eq__(self, other):
        if (self.first == other.first and self.second == other.second) or (self.reversed().first == other.first and self.reversed().second == other.second):
            return True
        return False

with open('filter.txt') as f:
    s = [i.replace('\n', '') for i in f.readlines()]

ar = []

for i in s:
    a, b = [j for j in i.split(':')]
    ar.append(Pair(a, b))

final = ar.copy()

for i in range(len(ar)):
    for j in range(i + 1, len(ar)):
        if ar[i] == ar[j]:
            final.remove(ar[i])

with open('filterOut.txt', 'w') as f:
    f.write(str(len(final)) + '\n')
    for i in final:
        f.write(str(i.first) + ' ' + str(i.second) + '\n')
"""
print(len(final))
for i in final:
    print(i.first, i.second)
"""
