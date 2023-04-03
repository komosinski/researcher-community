from tests.similarity.src.similarity_measures.measures.measure import Measure
import scipy


class CosineMeasure(Measure):
    def get(self, vec1: list, vec2: list) -> float:
        cosine = scipy.spatial.distance.cosine(vec1, vec2)
        return cosine