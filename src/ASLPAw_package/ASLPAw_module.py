'''
ASLPAw - This is a Adaptive Speaker-listener Lable Propagation Algorithm package.
Copyright (C) 2019-2021  sosei

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import random
from networkx.classes.graph import Graph
from networkx.classes.digraph import DiGraph
from networkx.classes.multigraph import MultiGraph
from networkx.classes.multidigraph import MultiDiGraph
from multivalued_dict_package import *
from shuffle_graph_package import shuffle_graph

__all__ = ['ASLPAw']

def _ASLPAw_networkx(data_graph: 'graph', Repeat_T: int, seed: int) -> 'DirectedGraph':
    
    from count_dict_package import count_dict
    from similarity_index_of_label_graph_package import similarity_index_of_label_graph_class
    
    def MVDict_to_WDiGraph(mvd: multivalued_dict) -> 'DirectedGraph':
        from collections import Counter
        
        WDG = DiGraph()
        for _out_node, _value_list in mvd.items():
            WDG.add_weighted_edges_from((_out_node, _in_node, _weight) for _in_node, _weight in Counter(_value_list).items())
        return WDG
    
    def remove_low_frequency_label(community_label_list_for_nodes: multivalued_dict) -> DiGraph:
        from sklearn.ensemble import IsolationForest
        digraph_of_node_labels_and_frequencies = DiGraph()
        for graph_of_node, label_list_of_nodes in community_label_list_for_nodes.items():
            digraph_of_node_labels_and_frequencies.add_node(graph_of_node)
            label_set = set(label_list_of_nodes)
            dict_of_frequency_of_label = dict(sorted([(label_list_of_nodes.count(label_item), label_item) for label_item in label_set], key = lambda frequency_and_label: frequency_and_label[0], reverse = True))
            dict_of_sn_and_frequency = dict([(sequence_number, frequency_of_label) for sequence_number, frequency_of_label in enumerate(dict_of_frequency_of_label.keys(), 1)])
            list_of_mapping_points = []
            for sequence_number, frequency_of_label in dict_of_sn_and_frequency.items():
                list_of_mapping_points.extend([[sequence_number]] * frequency_of_label)
            clf = IsolationForest(n_estimators = 120, contamination = 'auto')
            clf.fit(list_of_mapping_points)
            for sequence_number, frequency_of_label in dict_of_sn_and_frequency.items():
                if clf.predict([[sequence_number]])[0] == 1:
                    label_item = dict_of_frequency_of_label.__getitem__(frequency_of_label)
                    digraph_of_node_labels_and_frequencies.add_edge(graph_of_node, label_item, weight = frequency_of_label)
        return digraph_of_node_labels_and_frequencies
    
    def weight_normalization(WDG: DiGraph, normalization_parameter: float) -> DiGraph:
        for _edge in WDG.edges:
            WDG[_edge[0]][_edge[1]]['weight'] /= normalization_parameter
        return WDG
    
    community_label_list_for_nodes = multivalued_dict([[node_of_graph, node_of_graph] for node_of_graph in data_graph.nodes])
    
    random.seed(seed)
    
    similarity_index_of_label_graph = similarity_index_of_label_graph_class()
    
    for _t in range(Repeat_T):
        data_graph = shuffle_graph(data_graph)
        for data_graph_node, dict_of_adjvex in data_graph.adjacency():
            weight_of_community_label_for_adjvex = count_dict()
            for adjvex in dict_of_adjvex.keys():
                if data_graph.is_multigraph():
                    weight_of_edge = sum(value_of_edge.get('weight', 1) for value_of_edge in dict_of_adjvex.__getitem__(adjvex).values())
                else:
                    weight_of_edge = dict_of_adjvex.__getitem__(adjvex).get('weight', 1)
                community_label_for_adjvex = random.choice(community_label_list_for_nodes.__getitem__(adjvex))
                weight_of_community_label_for_adjvex[community_label_for_adjvex] += weight_of_edge
            community_label_for_node = max(weight_of_community_label_for_adjvex, key = weight_of_community_label_for_adjvex.__getitem__, default = data_graph_node)
            community_label_list_for_nodes.update({data_graph_node: community_label_for_node})
    
    digraph_of_node_labels_and_frequencies = weight_normalization(remove_low_frequency_label(community_label_list_for_nodes), _t + 1)
    return digraph_of_node_labels_and_frequencies
    
def ASLPAw(data_graph: 'graph', Repeat_T: int = 30, seed: int = None, graph_package = 'NetworkX') -> 'DirectedGraph':
    '''
        Returns a graph of the edges of each node with its own community tag node.
        
        ASLPAw can be used for disjoint and overlapping community detection and works on weighted/unweighted and directed/undirected networks. ASLPAw is adaptive with virtually no configuration parameters.
        
        Parameters
        ----------
        data_graph : graphs
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
        AdjacencyView({0: {2: {'weight': 0.9}}, 2: {2: {'weight': 0.9333333333333333}}, 1: {6: {'weight': 0.6}}, 6: {6: {'weight': 1.0}}, 3: {2: {'weight': 0.6}}, 4: {2: {'weight': 0.8666666666666667}}, 5: {2: {'weight': 0.9333333333333333}}, 7: {6: {'weight': 1.0}}, 8: {6: {'weight': 0.9666666666666667}}, 9: {6: {'weight': 0.9333333333333333}}, 10: {6: {'weight': 0.8666666666666667}}, 11: {6: {'weight': 0.9666666666666667}}, 12: {12: {'weight': 1.0333333333333334}}, 13: {12: {'weight': 0.9666666666666667}}, 14: {12: {'weight': 1.0}}, 15: {12: {'weight': 1.0}}, 16: {12: {'weight': 1.0}}, 17: {12: {'weight': 1.0}}})
        
        >>> data_graph = relaxed_caveman_graph(3, 6, 0.39, seed = 65535)
        >>> ASLPAw(data_graph, seed=65535).adj
        AdjacencyView({0: {1: {'weight': 0.9333333333333333}}, 1: {1: {'weight': 1.0}}, 2: {1: {'weight': 1.0}}, 3: {1: {'weight': 0.9666666666666667}}, 4: {1: {'weight': 1.0}}, 5: {1: {'weight': 0.9666666666666667}}, 6: {}, 7: {7: {'weight': 0.7666666666666667}}, 8: {}, 9: {13: {'weight': 0.4}, 6: {'weight': 0.26666666666666666}}, 13: {13: {'weight': 0.6333333333333333}}, 10: {1: {'weight': 0.5666666666666667}}, 11: {7: {'weight': 0.6333333333333333}}, 12: {12: {'weight': 0.4666666666666667}, 13: {'weight': 0.4}}, 14: {13: {'weight': 0.5666666666666667}}, 15: {13: {'weight': 0.5333333333333333}, 12: {'weight': 0.3333333333333333}}, 16: {13: {'weight': 0.43333333333333335}}, 17: {13: {'weight': 0.43333333333333335}, 12: {'weight': 0.4}}})
    '''
    
    if graph_package == 'NetworkX':
        return _ASLPAw_networkx(data_graph, Repeat_T, seed)
    elif graph_package == 'SNAP':
        pass
    elif graph_package == 'graph-tool':
        pass
    elif graph_package == 'igraph':
        pass
    else:
        raise ValueError(f'The value "{data_graph}" of the parameter "data_graph" is not one of "NetworkX", "SNAP", "graph-tool" or "igraph"!')
