from tests.similarity.src.similarity_measures.similarity_measure import SimilarityMeasure
from pathlib import Path
from gensim.models import TfidfModel
from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from gensim import similarities
from tests.similarity.src.similarity_measures.measures.euclidean_measure import EuclideanMeasure
from tests.similarity.src.similarity_measures.vectorizers.glove_vectorizer import GloveVectorizer


class GloveCosineEuclideanMeasure(SimilarityMeasure):
    def __init__(self):
        super().__init__()
        self.similarity = EuclideanMeasure()
        self.vectorizer = GloveVectorizer()

    def get_similarity(self, file_1: Path, file_2: Path) -> float:
        corpus = [simple_preprocess(self.text_extractor.get_text(i)) for i in [file_1, file_2]]
        if self.spell_corrector:
            corpus = [[self.spell_corrector.correct(i) for i in j] for j in corpus]
        corpus = self.vectorizer.transform(corpus)
        sim = self.similarity.get(corpus[0], corpus[1])
        return sim

    def get_vector(self, file: Path):
        corpus = [simple_preprocess(self.text_extractor.get_text(i)) for i in [file]]
        if self.spell_corrector:
            corpus = [[self.spell_corrector.correct(i) for i in j] for j in corpus]
        corpus = self.vectorizer.transform(corpus)
        return corpus[0]

    def build_dictionary(self, a):
        pass

#example usage
if __name__ == '__main__':
    p = Path("../../data/raw/dendrogram_1/1-s2.0-S2405844020301584-main.pdf")
    p1 = Path("../../data/raw/dendrogram_1/1-s2.0-S2773139123000010-main.pdf")
    sim = GloveCosineSimilarityMeasure()
    #sim.build_dictionary([p, p1])
    #print(sim.get_similarity(p, p1))
    print(sim.get_similarity(p, p1))




