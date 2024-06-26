# Auxilliary functions to be used in the actual program
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from random import sample

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

def assign_weights_avg(G):
    wtG = nx.Graph()
    for edge in G.edges():
        (u,v) = edge
        s = 0
        n = 0
        for nbr in nx.neighbors(G,u):
            if nbr == v: continue
            else:
                s += abs(G.edges[u,nbr]['time'] - G.edges[u,v]['time'])
                n += 1
        for nbr in nx.neighbors(G,v):
            if nbr == u: continue
            else:
                s += abs(G.edges[v,nbr]['time'] - G.edges[u,v]['time'])
                n += 1
        if n != 0:
            wtG.add_edge(u,v,weight=s/n)
    return wtG

def adj_fillinf(Gw):
    Aw = nx.adjacency_matrix(Gw,weight = 'weight')
    Ad = Aw.todense().astype(np.float64)
    Ad[Ad == 0] = np.inf
    np.fill_diagonal(Ad,0)
    return Ad

# Function to change graph according to different amount of perturbation required.

def change_graph(G,p):
    n_edges = G.number_of_edges()
    num_ch_edges = int(p * n_edges)
    Ge = G.copy()
    random_edge = sample(list(G.edges()),num_ch_edges)
    # print(random_edge[0])
    random_ptb = sample(list(range(1,5)),1)
    # print(random_ptb[0])
    random_sign = sample([0,1],1)
    # print(random_sign[0])
    for edge in random_edge:
        if random_sign[0] == 0:
            Ge.edges[edge[0],edge[1]]['time'] = Ge.edges[edge[0],edge[1]]['time'] - random_ptb[0]
        elif random_sign[0] == 1:
            Ge.edges[edge[0],edge[1]]['time'] = Ge.edges[edge[0],edge[1]]['time'] + random_ptb[0]
    return Ge

# Function to change the graph for the same class. 1% pertrubation

# def slight_change(G,m):
#     num_ch_edges = m//100
#     Ge = G.copy()
#     random_edge = sample(list(G.edges()),num_ch_edges)
#     # print(random_edge[0])
#     random_ptb = sample(list(range(1,5)),1)
#     # print(random_ptb[0])
#     random_sign = sample([0,1],1)
#     # print(random_sign[0])
#     for edge in random_edge:
#         if random_sign[0] == 0:
#             Ge.edges[edge[0],edge[1]]['time'] = Ge.edges[edge[0],edge[1]]['time'] - random_ptb[0]
#         elif random_sign[0] == 1:
#             Ge.edges[edge[0],edge[1]]['time'] = Ge.edges[edge[0],edge[1]]['time'] + random_ptb[0]
#     return Ge