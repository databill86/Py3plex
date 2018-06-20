## converters
import networkx as nx
from collections import defaultdict

def prepare_for_visualization(multinet):

    layers = defaultdict(list)
    for node in multinet.nodes(data=True):
        layers[node[1]['type']].append(node[0])

    networks = {layer_name : multinet.subgraph(v) for layer_name,v in layers.items()}
    inverse_mapping = {}
    layouts = []
    enumerator = 0
    for name, net in networks.items():
        print("Constructing layout for:",name,"layer.")
        tmp_pos=nx.spring_layout(net)
        for node in net.nodes(data=True):
            coordinates = tmp_pos[node[0]]
            node[1]['pos'] = coordinates
        enumerator+=1
            
    ## construct the inverse mapping
    for k,v in layers.items():
        for x in v:
            inverse_mapping[x] = k

    multiedges = defaultdict(list)
    for edge in multinet.edges(data=True):
        if inverse_mapping[edge[0]] != inverse_mapping[edge[1]]:            
            multiedges[edge[2]['type']].append((edge[0],edge[1]))

    names,networks = zip(*networks.items())
    return (names,networks,multiedges)

def prepare_for_visualization_hairball(multinet):

    layers = defaultdict(list)
    for node in multinet.nodes(data=True):
        layers[node[1]['type']].append(node[0])

    inverse_mapping = {}
    enumerated_layers = {name : ind for ind,name in enumerate(set(list(layers.keys())))}
    for k, v in layers.items():
        for x in v:
            inverse_mapping[x] = enumerated_layers[k]
    ordered_names = [inverse_mapping[x] for x in multinet.nodes()]
    return (ordered_names, multinet)