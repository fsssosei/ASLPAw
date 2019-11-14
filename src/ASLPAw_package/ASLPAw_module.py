import random
from multivalued_dict_package import *
from shuffle_graph_package import *
from count_dict_package import count_dict
from networkx.classes.graph import Graph
from networkx.classes.digraph import DiGraph
from networkx.classes.multigraph import MultiGraph
from networkx.classes.multidigraph import MultiDiGraph

__all__: list = ['ASLPAw']

def __ASLPAw_networkx(data_graph: 'graph', Repeat_T: int, seed: int) -> 'DirectedGraph':
    def __remove_low_frequency_label(community_label_queues_for_nodes: multivalued_dict) -> DiGraph:
        from sklearn.ensemble import IsolationForest
        digraph_of_node_labels_and_frequencies = DiGraph()
        for graph_of_node, label_list_of_nodes in community_label_queues_for_nodes.items():
            digraph_of_node_labels_and_frequencies.add_node(graph_of_node)
            label_set = set(label_list_of_nodes)
            dict_of_frequency_of_label = dict(sorted([(label_list_of_nodes.count(label_item), label_item) for label_item in label_set], key = lambda frequency_and_label: frequency_and_label[0], reverse = True))
            dict_of_sn_and_frequency = dict([(sequence_number, frequency_of_label) for sequence_number, frequency_of_label in enumerate(dict_of_frequency_of_label.keys(), 1)])
            list_of_mapping_points = []
            for sequence_number, frequency_of_label in dict_of_sn_and_frequency.items():
                list_of_mapping_points.extend([[sequence_number]] * frequency_of_label)
            clf = IsolationForest(n_estimators = 120, contamination = 'auto', behaviour = 'new')
            clf.fit(list_of_mapping_points)
            for sequence_number, frequency_of_label in dict_of_sn_and_frequency.items():
                if clf.predict([[sequence_number]])[0] == 1:
                    label_item = dict_of_frequency_of_label.__getitem__(frequency_of_label)
                    digraph_of_node_labels_and_frequencies.add_edge(graph_of_node, label_item, weight = frequency_of_label)
        return digraph_of_node_labels_and_frequencies
    
    community_label_queues_for_nodes = multivalued_dict([[node_of_graph, node_of_graph] for node_of_graph in data_graph.nodes])
    
    random.seed(seed)
    
    shuffle_number = calculate_number_of_shuffles_required_under_default_random_function(data_graph.number_of_nodes())
    
    for _t in range(Repeat_T):
        data_graph = shuffle_graph(data_graph, shuffle_number, seed)
        for data_graph_node, dict_of_adjvex in data_graph.adjacency():
            weight_of_community_label_for_adjvex = count_dict()
            for adjvex in dict_of_adjvex.keys():
                if data_graph.is_multigraph():
                    weight_of_edge = 0
                    for value_of_edge in dict_of_adjvex.__getitem__(adjvex).values():
                        weight_of_edge += value_of_edge.get('weight', 1)
                else:
                    weight_of_edge = dict_of_adjvex.__getitem__(adjvex).get('weight', 1)
                community_label_for_adjvex = random.choice(community_label_queues_for_nodes.__getitem__(adjvex))
                weight_of_community_label_for_adjvex[community_label_for_adjvex] += weight_of_edge
            community_label_for_node = max(weight_of_community_label_for_adjvex, key = weight_of_community_label_for_adjvex.__getitem__, default = data_graph_node)
            community_label_queues_for_nodes.update({data_graph_node: community_label_for_node})
    
    digraph_of_node_labels_and_frequencies = __remove_low_frequency_label(community_label_queues_for_nodes)
    return digraph_of_node_labels_and_frequencies
    
def ASLPAw(data_graph: 'graph', Repeat_T: int = 30, seed: int = None, graph_package = 'NetworkX') -> 'DirectedGraph':
    '''
        Returns a graph of the edges of each node with its own community tag node.
        
        ASLPAw can be used for disjoint and overlapping community detection and works on weighted/unweighted and directed/undirected networks. ASLPAw is adaptive with virtually no configuration parameters.
        
        Parameters
        ----------
        data_graph : graph
            A graph object. According to the package selected by the parameter graph_package, "data_graph" can accept graph objects of the corresponding type. However, any package you choose can accept a "NetworkX" object.
        
        Repeat_T : integer
            ASLPAw is an iterative process, this parameter sets the number of iterations.
        
        seed : integer, random_state, or None (default)
            Indicator of random number generation state.
        
        Returns
        -------
        communities : DirectedGraph
            Each node uses a community discovery map with a weighted edge pointing to its own community tag node.
        
        Examples
        --------
        >>> from networkx.generators.community import relaxed_caveman_graph
        >>> data_graph = relaxed_caveman_graph(3, 6, 0.22, seed = 65535)
        >>> ASLPAw(data_graph, seed=65535).adj
        AdjacencyView({0: {1: {'weight': 30}}, 1: {6: {'weight': 15}, 1: {'weight': 14}}, 6: {6: {'weight': 31}}, 2: {1: {'weight': 30}}, 3: {1: {'weight': 29}}, 4: {1: {'weight': 30}}, 5: {1: {'weight': 30}}, 7: {6: {'weight': 30}}, 8: {6: {'weight': 29}}, 9: {6: {'weight': 29}}, 10: {6: {'weight': 25}}, 11: {6: {'weight': 28}}, 12: {15: {'weight': 19}}, 15: {15: {'weight': 24}}, 13: {15: {'weight': 22}}, 14: {15: {'weight': 22}}, 16: {15: {'weight': 19}}, 17: {15: {'weight': 19}}})
        
        >>> data_graph = relaxed_caveman_graph(3, 6, 0.39, seed = 65535)
        >>> ASLPAw(data_graph, seed=65535).adj
        AdjacencyView({0: {3: {'weight': 25}}, 3: {3: {'weight': 27}}, 1: {3: {'weight': 26}}, 2: {3: {'weight': 28}}, 4: {3: {'weight': 29}}, 5: {3: {'weight': 29}}, 6: {6: {'weight': 30}}, 7: {6: {'weight': 30}}, 8: {6: {'weight': 21}}, 9: {6: {'weight': 27}}, 10: {3: {'weight': 20}}, 11: {6: {'weight': 27}}, 12: {15: {'weight': 16}, 6: {'weight': 13}}, 15: {}, 13: {6: {'weight': 19}}, 14: {6: {'weight': 20}}, 16: {15: {'weight': 17}, 6: {'weight': 12}}, 17: {15: {'weight': 18}, 6: {'weight': 12}}})
    '''
    
    if graph_package == 'NetworkX':
        return __ASLPAw_networkx(data_graph, Repeat_T, seed)
    elif graph_package == 'SNAP':
        pass
    elif graph_package == 'graph-tool':
        pass
    elif graph_package == 'igraph':
        pass
    else:
        raise ValueError(f'The value "{data_graph}" of the parameter "data_graph" is not one of "NetworkX", "SNAP", "graph-tool" or "igraph"!')
