from sklearn import metrics
import json
import os


def _dict_to_cluster(dendrogram, result=None, cluster=0):
    if result is None:
        result = {}
    for direction in ['left', 'right']:
        if type(dendrogram[direction]) is str:
            result[dendrogram[direction]] = cluster
    for direction in ['left', 'right']:
        if dendrogram[direction] and type(dendrogram[direction]) is not str:
            r, cluster = _dict_to_cluster(dendrogram[direction], result, cluster + 1)
            result.update(r)
    return result, cluster

def tree_similarity(tree1, tree2, similarity_measure='fowlkes_mallows_score'):
    """
    Calculates similarity measure of two trees given in our format

    Parameters
    ----------
    tree1 : First tree in our format.
    tree2 : Second tree in our format.
    similarity_measure: Measure used to calculate similarity, available measures from scikit:
    'rand_score', 'adjusted_rand_score', 'fowlkes_mallows_score'...
    Returns
    -------
    Measured similarity
    """
    d1_cluster = _dict_to_cluster(tree1)[0]
    d2_cluster = _dict_to_cluster(tree2)[0]
    l1, l2 = [], []
    for k in d1_cluster.keys():
        l1.append(d1_cluster[k])
        l2.append(d2_cluster[k])
    return eval('metrics.' + similarity_measure + '(l1, l2)')
