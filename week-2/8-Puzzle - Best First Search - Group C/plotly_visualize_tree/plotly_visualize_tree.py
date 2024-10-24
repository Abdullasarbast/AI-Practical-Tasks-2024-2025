import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go


def plot_tree_with_edges_and_labels(edges, labels):
    vertices = set()
    for edge in edges:
        vertices.update(edge)
    nr_vertices = len(vertices)

    G = Graph(nr_vertices, directed=True)

    G.add_edges(edges)

    lay = G.layout('rt')

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G)
    E = [e.tuple for e in G.es]

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]

    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                             y=Ye,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=Xn,
                             y=Yn,
                             mode='markers',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=18,
                                         color='#6175c1',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=labels,
                             hoverinfo='text',
                             opacity=0.8
                             ))

    def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
        L = len(pos)
        if len(text) != L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = []
        for k in range(L):
            if labels[k] == '0':
                annotations.append(
                    dict(
                        text=labels[k],
                        x=pos[k][0], y=2 * M - pos[k][1],
                        xref='x1', yref='y1',
                        font=dict(color='rgb(255, 0, 0)', size=font_size),
                        showarrow=False)
                )
            else:
                annotations.append(
                    dict(
                        text=labels[k],
                        x=pos[k][0], y=2 * M - pos[k][1],
                        xref='x1', yref='y1',
                        font=dict(color=font_color, size=font_size),
                        showarrow=False)
                )
        return annotations

    axis = dict(showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.update_layout(title='Tree with Custom Edges and Reingold-Tilford Layout',
                      annotations=make_annotations(position, labels),
                      font_size=12,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )
    fig.show()
