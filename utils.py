# Auxilliary functions to be used in the actual program
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def draw_with_labels(G,label):
    pos=nx.spring_layout(G)
    nx.draw_networkx(G,pos)
    labels = nx.get_edge_attributes(G,label)
    nx.draw_networkx_edge_labels(G,pos,edge_labels = labels)

def assign_weights(G):
    # G is a networkx undirected time labelled graph
    wtG = nx.Graph()
    for edge in G.edges():
        (u,v) = edge
        wt = np.inf
        for nbr in nx.neighbors(G,u):
            if nbr == v: continue
            if abs(G.edges[u,nbr]['time'] - G.edges[u,v]['time']) < wt:
                wt = abs(G.edges[u,nbr]['time'] - G.edges[u,v]['time'])
        for nbr in nx.neighbors(G,v):
            if nbr == u: continue
            if abs(G.edges[v,nbr]['time'] - G.edges[u,v]['time']) < wt:
                wt = abs(G.edges[v,nbr]['time'] - G.edges[u,v]['time'])
        wtG.add_edge(u,v,weight=wt)
    return wtG

def adj_fillinf(Gw):
    Aw = nx.adjacency_matrix(Gw,weight = 'weight')
    Ad = Aw.todense().astype(np.float64)
    Ad[Ad == 0] = np.inf
    np.fill_diagonal(Ad,0)
    return Ad

