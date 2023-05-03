from clusim.clustering import Clustering, print_clustering
import clusim.sim as sim
import json
import os
import networkx as nx


def _add_leafs(dendrogram, cluster = 0, elm2clu_dict={}):
    result = nx.DiGraph()
    for direction in ['left', 'right']:
        if type(dendrogram[direction]) is str:
            elm2clu_dict[dendrogram[direction]] = [cluster]
            result.add_node(cluster)
            cluster += 1
    for direction in ['left', 'right']:
        if dendrogram[direction] and type(dendrogram[direction]) is not str:
            result, elm2clu_dict, cluster = _add_leafs(dendrogram[direction],  cluster, elm2clu_dict)
    return result, elm2clu_dict, cluster

def _dict_to_cluster(dendrogram, result=None, cluster=0, clusters=[], elm2clu_dict={}):
    if result is None:
        result, elm2clu_dict, cluster = _add_leafs(dendrogram, cluster=0, elm2clu_dict={})
    c = list()
    for direction in ['left', 'right']:
        if dendrogram[direction] and type(dendrogram[direction]) is not str:
            result, cluster, elm2clu_dict = _dict_to_cluster(dendrogram[direction], result, cluster, clusters, elm2clu_dict)
            c.append(int(cluster))
    for direction in ['left', 'right']:
        if type(dendrogram[direction]) is str:
            result.add_edge(cluster, elm2clu_dict[dendrogram[direction]][0])
    for _c in c:
        result.add_edge(cluster, _c - 1)
    cluster += 1
    return result, cluster, elm2clu_dict

def tree_similarity(tree1, tree2, similarity_measure='jaccard_index'):
    """
    Calculates similarity measure of two trees given in our format

    Parameters
    ----------
    tree1 : First tree in our format.
    tree2 : Second tree in our format.
    similarity_measure: Measure used to calculate similarity, available measures:
    'jaccard_index', 'rand_index', 'adjrand_index', 'fowlkes_mallows_index', 'fmeasure', 'purity_index', 'classification_error',
    'czekanowski_index', 'dice_index', 'sorensen_index', 'rogers_tanimoto_index', 'southwood_index', 'pearson_correlation', 'corrected_chance',
    'sample_expected_sim', 'nmi', 'mi', 'adj_mi', 'rmi', 'vi', 'geometric_accuracy', 'overlap_quality', 'onmi', 'omega_index'

    Returns
    -------
    Measured similarity
    """
    d1_cluster, _, elm2clu_dict1 = _dict_to_cluster(tree1)
    clu1 = Clustering(hier_graph=d1_cluster, elm2clu_dict=elm2clu_dict1)
    d2_cluster, _, elm2clu_dict2 = _dict_to_cluster(tree2)
    clu2 = Clustering(hier_graph=d2_cluster, elm2clu_dict=elm2clu_dict2)
    return eval('sim.' + similarity_measure + '(clu1, clu2)')
