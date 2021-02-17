from os import listdir
from os.path import isfile, join
import plotly.graph_objects as go
import networkx as nx
import plotly.graph_objects as go # or plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

from matplotlib import pylab
import matplotlib.pyplot as plt
import networkx as nx
import csv

reader=csv.reader(open("./Duplication_Detection/results/urls.csv", newline=''))
urls = [a for a in reader]
urls
word_count = {int(i[2]):int(i[0]) for i in urls}
url_dict = {int(i[2]):i[1] for i in urls}
path = "./Duplication_Detection/results/"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
onlyfiles = [i for i in onlyfiles if '.txt' in i]
files = []
for file in onlyfiles:
    f = open(path+file, "r")
    files.append(eval(f.read()))

groups = [j for i in files for j in i]
docs = [j for i in groups for j in i]
len(docs)
final_docs = [[i[0], list(set(i[2]) & set(i[3]))] for i in docs]
G = nx.Graph()
duplicate_count = 2
nodes = list(set([i[0] for i in final_docs if len(i[1]) > duplicate_count] + [j for i in final_docs for j in i[1] if len(i[1]) > duplicate_count]))
edges = []
for i in final_docs:
    for j in i[1]:
        if i[0] != j and len(i[1])>duplicate_count:
            edges.append((i[0], j))
G.add_nodes_from(nodes)
for e in edges:
    G.add_edge(*e)

print(nx.info(G))



def save_graph(graph, file_name):
    # initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos)
    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
    plt.savefig(file_name)
    plt.show()
    pylab.close()
    del fig

# save_graph(G,'out.png')
pos=nx.spring_layout(G)

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append(str(adjacencies[0])+' - # of connections: '+str(len(adjacencies[1]))+" <a href='https://plotly.com>grdg</a>")

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

fig = go.FigureWidget(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=True),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=True))
                )


def update_point(trace, points, selector):
    print('points.poin_inds')

fig.data[0].on_click(update_point)

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)