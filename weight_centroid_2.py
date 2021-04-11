import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

def visual(G, node_c = None):
    plt.plot()
    nx.draw(G, with_labels = True)
    plt.show()

G = nx.Graph()
G.directed = False

with open('filterOut.txt') as f:
    edges = f.readlines()

for i in edges:
    a, b, c = [x.replace('\n', '') for x in i.split(':')]
    c = float(c.replace(',', '.'))
    if b != 'None':
        G.add_edge(a, b, weight = c)
        G.add_edge(b, a, weight = c)
    else:
        G.add_node(a)

largest = max([G.subgraph(c).copy() for c in nx.connected_components(G)], key = len)

spTree = nx.minimum_spanning_tree(largest)

visual(spTree)

fullWeight = nx.algorithms.tree.branchings.branching_weight(spTree)

verticeWeight = {}

for i in spTree.copy():
    finding = spTree.copy()
    finding.remove_node(i)
    subgraphs = max([finding.subgraph(c).copy() for c in nx.connected_components(G)], key = len)
    weights = [nx.algorithms.tree.branchings.branching_weight(subgraphs.subgraph(i).copy()) for i in nx.connected_components(subgraphs)]
    verticeWeight[i] = max(weights)

verticeWeight = {k: v for k, v in sorted(verticeWeight.items(), key=lambda item: item[1])}

minWeight = min(verticeWeight.values())

centroid = [k for k in verticeWeight if verticeWeight[k] == minWeight]

print(verticeWeight)

print()

print(minWeight)

print()

print(centroid)
