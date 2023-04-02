from similarity_measure import SimilarityMeasure
from pathlib import Path
from tests.similarity.src.utils.pdf_to_text_transformer import PdfToTextTransformer
from gensim.models import TfidfModel
from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from gensim import similarities
import numpy as np
import gensim.downloader as api

class TfidfSimilarityMeasure(SimilarityMeasure):
    def __init__(self):
        self.dictionary = None
        self.model = None
        self.text_extractor = PdfToTextTransformer()

    #list of all articles to build corpus from
    def build_dictionary(self, article_list: list) -> None:
        corpus = [simple_preprocess(self.text_extractor.get_text(i)) for i in article_list]
        self.dictionary = Dictionary(corpus)
        corpus = [self.dictionary.doc2bow(line) for line in corpus]
        self.model = TfidfModel(corpus, smartirs='ntc')

    def get_similarity(self, file_1: Path, file_2: Path) -> float:
        corpus = [simple_preprocess(self.text_extractor.get_text(i)) for i in [file_1, file_2]]
        corpus = [self.dictionary.doc2bow(line) for line in corpus]
        corpus_tfidf = self.model[corpus]
        tfidf_matrix = similarities.MatrixSimilarity(corpus_tfidf, num_features=len(self.dictionary))
        tfidf_matrix = tfidf_matrix.get_similarities(corpus_tfidf)
        return tfidf_matrix[0][1]

#example usage
if __name__ == '__main__':
    p = Path("../../data/raw/dendrogram_1/1-s2.0-S2405844020301584-main.pdf")
    p1 = Path("../../data/raw/dendrogram_1/1-s2.0-S2773139123000010-main.pdf")
    sim = TfidfSimilarityMeasure()
    sim.build_dictionary([p, p1])
    print(sim.get_similarity(p, p1))

