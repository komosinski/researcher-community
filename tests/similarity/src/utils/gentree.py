from collections.abc import Callable
from typing import Any

import numpy as np
from scipy.cluster.hierarchy import linkage


def gentree(documents: list[str], comparison: Callable[[str, str], float]) -> dict[str, dict | str]:
    """
    Generates dendrogram for a set of documents and given comparison function.
    Internally works by invoking single-linkage AHC on upper-triangular distance matrix.

    Parameters
    ----------
    documents : List of documents.
    comparison : Metric function.

    Returns
    -------
    Generated tree in our format.
    """

    dense_mat = np.ndarray(len(documents) * (len(documents) - 1) // 2)
    i = 0
    for e, x in enumerate(documents):
        for y in documents[e + 1:]:
            dense_mat[i] = comparison(x, y)
            i += 1

    linkage_matrix = linkage(dense_mat, 'single')
    nodes: list[Any] = list(documents)

    for left, right, _, _ in linkage_matrix:
        nodes.append({'left': nodes[int(left)], 'right': nodes[int(right)]})

    return nodes[-1]
