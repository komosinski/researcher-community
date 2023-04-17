from clusim.clustering import Clustering, print_clustering
import clusim.sim as sim
import json
import os


def _dict_to_cluster(dendrogram, result=None, cluster=0, clusters=[]):
    clusters.append(cluster)
    if result is None:
        result = {}
    if dendrogram['left']:
        if type(dendrogram['left']) is str:
            result[dendrogram['left']] = clusters.copy()
    if dendrogram['right']:
        if type(dendrogram['right']) is str:
            result[dendrogram['right']] = clusters.copy()
    if dendrogram['left']:
        if type(dendrogram['left']) is not str:
            r, cluster = _dict_to_cluster(dendrogram['left'], result, cluster + 1, clusters.copy())
            result.update(r)
    if dendrogram['right']:
        if type(dendrogram['right']) is not str:
            r, cluster = _dict_to_cluster(dendrogram['right'], result, cluster + 1, clusters.copy())
            result.update(r)
    if cluster == 0:
        for key, val in result.items():
            result[key] = list(set(val))
    return result, cluster

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
    d1_cluster = _dict_to_cluster(tree1)[0]
    clu1 = Clustering()
    clu1.from_elm2clu_dict(d1_cluster)
    d2_cluster = _dict_to_cluster(tree2)[0]
    clu2 = Clustering()
    clu2.from_elm2clu_dict(d2_cluster)
    return eval('sim.' + similarity_measure + '(clu1, clu2)')
