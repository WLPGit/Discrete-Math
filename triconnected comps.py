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
    a, b = [x.replace('\n', '') for x in i.split(':')]
    if b != 'None':
        G.add_edge(a, b)
        G.add_edge(b, a)
    else:
        G.add_node(a)

#nx.connected_components(G)
        
k_components = nx.k_components(G)[3]

for i in k_components:
    for j in i:
        print(j)
    print()
