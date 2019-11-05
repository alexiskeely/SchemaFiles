# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 07:58:48 2019

@author: alexi
"""

#%%
import networkx as nx
import matplotlib.pyplot as plt

edges=[['G','PE'],['PE','LR'],['LR', 'DP'],['DP','PDP'],['DP','DDP'],['C','G'],['G','title'],['G','summary'],['G','note']]
G=nx.Graph()

G.add_edges_from(edges)
plt.figure()   
pos = nx.random_layout(G)



classes = ['G','PE','C','DP','LR']
literals = ['title','summary','note']


nx.draw_networkx_nodes(G,pos,nodelist=classes,edge_color='black',width=1,linewidths=1,\
node_size=500,node_color='pink',alpha=0.9)
nx.draw_networkx_nodes(G,pos,nodelist=literals,edge_color='black',width=1,linewidths=1,\
node_size=500,node_color='purple',alpha=0.9)

labels={node:node for node in G.nodes()}


nx.draw_networkx_labels(G, pos, labels, font_size=16)
nx.draw_networkx_edge_labels(G,pos,edge_labels={('PE','LR'):'releasedLocally',\
('G','PE'):'platformEdition',('LR', 'DP'):'distributedAs',('DP','PDP'):'subClass',('DP','DDP'):'subClass'},font_color='red')
plt.axis('off')
plt.show()

#%%

