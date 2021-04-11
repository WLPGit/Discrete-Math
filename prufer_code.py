import networkx as nx
import matplotlib.pyplot as plt

def visual(G, node_c = None):
    plt.plot()
    nx.draw(G, with_labels = True)
    plt.show()

G = nx.Graph()

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

names = {}
for k, v in enumerate(spTree):
    names[v] = k

print(names)

print()

spTree = nx.relabel_nodes(spTree, names)

print(nx.algorithms.tree.coding.to_prufer_sequence(spTree))

visual(spTree)


