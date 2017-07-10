import plotly as py
from plotly.graph_objs import *
import csv
import networkx as nx
import matplotlib.pyplot as plt
import random
# import numpy as np
# from sklearn.cluster import KMeans
# GET DATA

contains = []

with open('contains.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=';')
    for row in data:
        contains.append(row)

number = len(contains)


cluster = []
with open('dict.csv', 'r') as csvfile2:
    data2 = csv.reader(csvfile2, delimiter=',')
    for row in data2:
        cluster.append(row)

cl = []
for i in range(0, len(cluster), 2):
    cl.append(cluster[i])





# print(cl)
# number = range(len(contains))

# print(contains)
# print(number)
# test = []
# for i in range(20):
#   test.append(contains[i])


# GET NODE POSITION

G = nx.Graph()

for row in cl:
    G.add_node(row[0])

contains_cl = []
for hs in contains:
    for t in cl:
        if hs[1] == t[0]:
            contains_cl.append(hs)
# print(contains_cl)

for row in contains_cl:
    for row2 in contains_cl:
        if row[0] == row2[0] and row[1] != row2[1]:
            G.add_edge(row[1], row2[1])




b = 0
for a in cl:
    # print(a)
    for node in G.nodes():
        if a[0] == node:
            b = int(a[1]) #+ 
            # print(b)
            b += random.uniform(-1, 1)
            # print(a[1])
            G.node[node]['cluster_x'] = b
            # G.node[node]['cluster_x'] += random.uniform(-1, 1)
            # print(G.node[node]['cluster_x'])


for node in G.nodes():
    G.node[node]['ad_list'] = []
    for edge in G.edges():
        if node == edge[0]:
            G.node[node]['ad_list'].append(edge[1]) 

for node in G.nodes():
    G.node[node]['adjacent_y'] = len(G.node[node]['ad_list'])


# adj = G.adjacency_list()

# print(adj)
# for node in G.nodes():
#     G.node[node]['adjacent_y'] = 0
# for adjacencies in adj:
#     for node in G.nodes():
#         if node in adjacencies:
#             if G.node[node]['adjacent_y'] < len(adjacencies):
#                 G.node[node]['adjacent_y'] = len(adjacencies) + random.uniform(-1, 1)
        # G.node[node]['adjacent_y'] 

hslist = []
for node in G.nodes():
    hslist.append(node)

# for hashtag in hslist:
#     print(G.node[hashtag])


edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')


for edge in G.edges():
    x0, y0 = G.node[edge[0]]['cluster_x'], G.node[edge[0]]['adjacent_y']
    x1, y1 = G.node[edge[1]]['cluster_x'], G.node[edge[1]]['adjacent_y']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]
    # edge_trace['x'] += G.node[edge[0]]['random_x']
    # edge_trace['y'] += G.node[edge[1]]['adjacent_y']


# for edge in G.edges():
#   print(edge)
# print(edge_trace)

node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        # colorscale options
        #'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        #'Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))
# for node in G.nodes():
#     print(G.node[node]['cluster_x'])
# m = 0
for node in G.nodes():
    # G.node[node]['hashtag'] = node
    # for i in node:
    #   m += ord(i)
    # G.node[node]['code'] = m
    # m = 0
    # x =
    # y =
    node_trace['x'].append(G.node[node]['cluster_x'])
    node_trace['y'].append(G.node[node]['adjacent_y'])

# for node in G.nodes():
#   print(G.node[node])
# print(node_trace)

# COLORING NODES


for node, adjacencies in enumerate(G.adjacency_list()):
    node_trace['marker']['color'].append(len(adjacencies))
    # str(adjacencies) 
    node_info = hslist[node] + "   " + '# of connections: ' + str(len(adjacencies))
    node_trace['text'].append(node_info)
    # print(node)
    # print("")
    # print(adjacencies)
    # print("")


# print(edge_trace)
# print(node_trace)


# CREATE NODE NETWORK

fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
    title='<br>Network graph made with Python',
    titlefont=dict(size=16),
    showlegend=False,
    hovermode='closest',
    margin=dict(b=5, l=1, r=1, t=10),
    annotations=[dict(
        text="",
        showarrow=False,
        xref="paper", yref="paper",
        x=0.005, y=-0.002)],
    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

py.offline.plot(fig, filename='Hashtags')


# plotly.offline.plot({
#     "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
#     "layout": Layout(title="hello world")
# })
