import networkx as nx
import os.path
import random

save_path = "/Users/rohit/Desktop/CMI/DS/TDA/TTF/data"

for i in range(10):

    filename = os.path.join(save_path,f"g{i+1}.gml")

    G = nx.gnm_random_graph(7,10)

    for (u,v) in G.edges():
        G.edges[u,v]['time'] = random.randint(0,100)

    nx.write_gml(G,filename)