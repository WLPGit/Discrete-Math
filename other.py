import collections
import matchingg
from functools import lru_cache
from operator import itemgetter

def getGraph():
    with open('filterOut.txt') as f:
        countries = [i.replace('\n', '') for i in f.readlines()]
    s = {}
    for i in countries:
        a, b = i.split(':')
        if s.get(a) == None and a != 'None':
            s[a] = []
        if s.get(b) == None and b != 'None':
            s[b] = []
        if b != 'None':
            s[a].append(b)
            s[b].append(a)
    for i in s:
        s[i] = list(set(s[i]))
    return s

def getSizeN(g):
    return len(set(g.keys()))

def getCountries(g, _except=[]):
    countries = list(set(g.keys()))
    for i in _except:
        countries.remove(i)
    return countries

def getSizeM(g):
    with open('filterOut.txt') as f:
        countries = [i.split(':') for i in f.readlines()]
    return len(countries)

def getDelta(g, sortfunc):
    return len(sorted(g.values(), key = sortfunc)[0])


def bfs(graph, root):
    shrts = { i : -1 for i in getCountries(g) }
    visited, queue = set(), collections.deque([root])
    shrts[root] = 0
    t = 1
    x = 1
    while queue:
        k = 0
        for i in range(x):
            vertex = queue.popleft()
            for neighbour in graph[vertex]:
                if shrts[neighbour] == -1:
                    shrts[neighbour] = t
                    queue.append(neighbour)
                    k += 1
        x = k
        t += 1
    return shrts
        
def BronKerbosch(P, N, R = None, X = None): #cliques
    P = set(P)
    R = set() if R is None else R
    X = set() if X is None else X
    if not P and not X:
        
        yield R
    while P:
        v = P.pop()
        yield from BronKerbosch(
            P = P.intersection(N[v]), N = N, R = R.union([v]), X = X.intersection(N[v]))
        X.add(v)

def complementGraph(g, cou):
    graph = g.copy()
    countries = set(cou.copy())

    for i in g:
        neighbours = set(g[i])
        new_neighbours = countries.difference(neighbours)
        graph[i] = list(new_neighbours)

    return graph

def hamilton(graph, start_v):
  size = len(graph)
  # if None we are -unvisiting- comming back and pop v
  to_visit = [None, start_v]
  path = []
  while(to_visit):
    v = to_visit.pop()
    if v : 
      path.append(v)
      if len(path) == size:
        break
      for x in set(graph[v])-set(path):
        to_visit.append(None) # out
        to_visit.append(x) # in
    else: # if None we are comming back and pop v
      path.pop()
  return path

def eulerPath(graph, v, answer = []):
    for i in graph[v]:
        graph[v].remove(i)
        eulerPath(graph, i, answer)
    answer.append(v)
    return answer
"""
def DFS(g, visited, comp, root, c_num):
    visited[root] = True
    comp[root] = c_num

    for i in g[root]:
        if not visited[i]:
            DFS(g, visited, comp, i, c_num)

def connectComps(g):
    visited = {i : False for i in g}
    comp = {}

    c_num = 1

    for i in g:
        if not visited[i]:
            DFS(g, visited, comp, i, c_num)
            c_num += 1
    return comp

def getTriPairs(g):
    pairs = []

    #gg = g.copy()

    num = len(set(connectComps(g.copy()).values()))

    for i in g.copy():
        for j in g.copy():
            gg = g.copy()
            if gg.get(i) != None:
                gg.pop(i)
            if gg.get(j) != None:
                gg.pop(j)
            for k in gg.copy():
                if i in gg[k]:
                    gg[k].remove(i)
                if j in gg[k]:
                    gg[k].remove(j)
            comps = connectComps(gg)
            nm = len(set(comps.values()))
            if nm > num and i != j:
                pairs.append((i, j))
    return pairs

def divideByPairs(g, pairs):
    graphs = []

    for k, v in pairs:
        gg = g.copy()
        if gg.get(k) != None:
            gg.pop(k)
        if gg.get(v) != None:
            gg.pop(v)
        for i in gg.copy():
            if k in gg[i]:
                gg[i].remove(k)
            if v in gg[i]:
                gg[i].remove(v)
                
        comps = connectComps(gg)
        counter = {i + 1 : [] for i in range(len(set(comps.values())))}

        for i in comps:
            counter[comps[i]].append(i)
        
        for i in counter:
            gp = {}
            for j in counter[i]:
                if gp.get(j) == None:
                    gp[j] = []
                for z in gg:
                    if j in gg[z]:
                        gp[j].append(z)
                        if gp.get(z) == None:
                            gp[z] = []
                        gp[z].append(j)
            graphs.append(gp)
    return graphs

def triconnected(g):
    pairs = getTriPairs(g)
    graphs = divideByPairs(g, pairs)
    if len(pairs) > 0:
        for i in graphs:
            triconnected(i)
    return graphs
"""           
g = getGraph()

#for i in g:
#    print(i, ':', g[i])

print()

print('|V|:', getSizeN(g))
print('|E|:', getSizeM(g))
print('δ(G):', getDelta(g, lambda x: len(x)))
print('Δ(G):', getDelta(g, lambda x: -len(x)))

shrts = bfs(g, 'Portugal')

#print(shrts)

anyelse = [i for i in shrts if shrts[i] == -1] # path not found

radius = min([max(bfs(g, i).values()) for i in getCountries(g, anyelse)])

diam = max([max(bfs(g, i).values()) for i in getCountries(g)])

center = [i for i in getCountries(g, anyelse) if max(bfs(g, i).values()) == radius]

print('rad(G):', radius)
print('diam(G):', diam)

print()

print('Center:', center)

print()

print('κ(G):', len(list(BronKerbosch(getCountries(g, anyelse), g))))

print('Maximum clique:', sorted(list(BronKerbosch(getCountries(g, anyelse), g)), key = lambda x: -len(x))[0]) # maximum clique

#print('Maximum clique of complement graph:', sorted(list(BronKerbosch(getCountries(g, anyelse), complementGraph(g, getCountries(g, anyelse)))), key = lambda x: -len(x))[0]) # coclique

#print(matchingg.matching(g)) # maximum matching

useless = []

for i in g:
    if len(g[i]) <= 1:
        useless.append(i)
        #print(i, g[i])

hamiltonian_g = g.copy()
for i in useless:
    hamiltonian_g.pop(i)

for i in hamiltonian_g:
    for j in useless:
        if j in hamiltonian_g[i]:
            hamiltonian_g[i].remove(j)

#print(hamilton(hamiltonian_g, "Sweden"))
"""            
visited = {i : False for i in g}
comp = {}

c_num = 1

for i in g:
    if not visited[i]:
        DFS(g, visited, comp, i, c_num)
        c_num += 1
"""
comp = connectComps(g)
num = len(set(comp.values()))

counter = {i + 1 : 0 for i in range(10)}

for i in comp:
    counter[comp[i]] += 1

counter = {k : v for k, v in sorted(counter.items(), key = lambda item: -item[1])}

longest = list(counter.items())[0][0]

maxcomp = {i : [] for i in comp if comp[i] == longest}

for i in maxcomp:
    for city in g[i]:
        if comp[city] == longest:
            maxcomp[i].append(city)
            #if maxcomp.get(city) == None:
            #    maxcomp[city] = []
            #if not i in maxcomp[city]:
            #    maxcomp[city].append(i)
"""
triconnected finding
запускаем в исходном графе алгоритм нахождения пар точек, если пара находится и она разбивает граф на несколько других связных графов, то запускаем алгоритм в каждом из графов
пока будут находится такие пары, они рекурсивно разбиваются
когда пар не останется, каждый из оставшихся связных графов будет являться компонентой трехсвязности

нахождение пары: удаляем 2 вершины, если кол-во компонент связности увеличилось - записываем пару
"""
"""
#print()
#\
print(comp)
#print()
#print(maxcomp)
for i in getTriPairs(maxcomp):
    print(i)
#print(triconnected(maxcomp))

#for i in triconnected(maxcomp):
#    print(i)
"""
