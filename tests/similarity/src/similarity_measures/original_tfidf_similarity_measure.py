from similarity_measure import SimilarityMeasure
from pathlib import Path
from gensim.models import TfidfModel
from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from gensim import similarities
import numpy as np
import gensim.downloader as api
from tests.similarity.src.similarity_measures.vectorizers.count_vectorizer import CountVectorizer

class TfidfSimilarityMeasure(SimilarityMeasure):


    #list of all articles to build corpus from
    def build_dictionary(self, article_list: list) -> None:
        corpus = [simple_preprocess(self.text_extractor.get_text(i)) for i in article_list]
        if self.spell_corrector:
            corpus = [[self.spell_corrector.correct(i) for i in j] for j in corpus]
        self.dictionary = Dictionary(corpus)
        corpus = [self.dictionary.doc2bow(line) for line in corpus]
        self.model = TfidfModel(corpus, smartirs='ntc')

    def get_similarity(self, file_1: Path, file_2: Path) -> float:
        corpus = [simple_preprocess(self.text_extractor.get_text(i)) for i in [file_1, file_2]]
        if self.spell_corrector:
            corpus = [[self.spell_corrector.correct(i) for i in j] for j in corpus]
        corpus = [self.dictionary.doc2bow(line) for line in corpus]
        corpus_tfidf = self.model[corpus]
        tfidf_matrix = similarities.MatrixSimilarity(corpus_tfidf, num_features=len(self.dictionary))
        tfidf_matrix = tfidf_matrix.get_similarities(corpus_tfidf)
        return tfidf_matrix[0][1]





