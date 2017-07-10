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


# GET NODE POSITION

G = nx.Graph()

for row in cl:
    G.add_node(row[0])

contains_cl = []
for hs in contains:
    for t in cl:
        if hs[1] == t[0]:
            contains_cl.append(hs)


for row in contains_cl:
    for row2 in contains_cl:
        if row[0] == row2[0] and row[1] != row2[1]:
            G.add_edge(row[1], row2[1])


for node in G.nodes():
    G.node[node]['ad_list'] = []
    for edge in G.edges():
        if node == edge[0]:
            G.node[node]['ad_list'].append(edge[1]) 

for node in G.nodes():
    G.node[node]['ad_length'] = len(G.node[node]['ad_list'])

def circle(nedge):
    n = 1 / (nedge + 1)
    if nedge >= 40:
        x = random.uniform(-n,n)
        yhelp = [(1/20 - x)**(0.5), -((1/20 - x)**(0.5))]
        y = random.choice(yhelp)
        return x, y
    if nedge >= 30 and nedge < 40:
        x = random.uniform(-n,n)
        yhelp = [(1/15 - x)**(0.5), -((1/15 - x)**(0.5))]
        y = random.choice(yhelp)
        return x, y
    if nedge >= 5 and nedge < 30:
        x = random.uniform(-n,n)
        yhelp = [(1/10 - x)**(0.5), -((1/10 - x)**(0.5))]
        y = random.choice(yhelp)
        return x, y
    if nedge >= 0 and nedge < 5:
        x = random.uniform(-n/15,n/15)
        yhelp = [(1/5 - x)**(0.5), -((1/5 - x)**(0.5))]
        y = random.choice(yhelp)
        return x, y


for node in G.nodes():
    G.node[node]['pos'] = circle(G.node[node]['ad_length'])


hslist = []
for node in G.nodes():
    hslist.append(node)


edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')


for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]


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


for node in G.nodes():
    node_trace['x'].append(G.node[node]['pos'][0])
    node_trace['y'].append(G.node[node]['pos'][1])



# COLORING NODES


for node, adjacencies in enumerate(G.adjacency_list()):
    node_trace['marker']['color'].append(len(adjacencies))
    node_info = hslist[node] + "   " + '# of connections: ' + str(len(adjacencies))
    node_trace['text'].append(node_info)



# CREATE NODE NETWORK

fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
    title='<br>Graph über gemeinsames Auftreten von Hashtags',
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

