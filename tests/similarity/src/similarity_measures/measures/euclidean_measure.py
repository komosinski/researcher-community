from tests.similarity.src.similarity_measures.measures.measure import Measure
import numpy as np


class EuclideanMeasure(Measure):
    def get(self, vec1: list, vec2: list) -> float:
        euclidean = np.linalg.norm(vec1 - vec2)
        return euclidean
