import networkx as nx
import matplotlib.pyplot as plt

from eao.portfolio import Portfolio
from eao.serialization import load_from_json
from eao.assets import Transport, ExtendedTransport

def create_graph(portf: Portfolio, file_name: str = None, title = None):
    """ generate a network graph from a portfolio and save to pdf

    Args:
        portf (Portfolio): portfolio object
        file_name (str): file name. Defaults to None (show plot)
    """
    node_size  = 500
    asset_size = 200

    G = nx.DiGraph()
    color_map = [] # node colors
    color_map_edges = [] # node colors
    node_sizes = []
    # add nodes
    for n in portf.nodes:
        G.add_node(n)
        color_map.append('orange')
        node_sizes.append(node_size)
    # my edges between nodes are transport assets
    for a in portf.assets:
        if isinstance(a, (Transport, ExtendedTransport)):
            G.add_edge(a.nodes[0].name, a.nodes[1].name, label = a.name)
            color_map_edges.append('blue')
    # add assets as further nodes (attached to nodes)
    for a in portf.assets:
        if not isinstance(a, (Transport, ExtendedTransport)):   
            G.add_node(a.name)
            color_map.append('grey')
            node_sizes.append(asset_size)
            for n in a.nodes:
                G.add_edge(a.name, n.name, label = '')
                G.add_edge(n.name, a.name, label = '')
                color_map_edges.append('grey')
                color_map_edges.append('grey')
            
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,node_color=color_map, node_size=node_sizes, \
                         alpha = 0.7)
    nx.draw_networkx_edges(G,pos,  edge_color='grey')#color_map_edges)
    nx.draw_networkx_labels(G,pos, font_size=8)
    g_labels = nx.get_edge_attributes(G,'label')
    nx.draw_networkx_edge_labels(G,pos,edge_labels= g_labels, font_size=8)

    if title is None: title = 'Network graph for portfolio'
    plt.title(title)

    plt.axis("off")

    if not file_name is None:
        plt.savefig(file_name)
    else:
        plt.show()
    plt.close()


if __name__ == "__main__" :
    myf = 'demo_portf.json'
    portf = load_from_json(file_name= myf)
    create_graph(portf = portf, file_name='test_graph.pdf')
