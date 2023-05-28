from tests.similarity.src.similarity_measures.vectorizers.vectorizer import Vectorizer
import numpy as np
from pathlib import Path
from gensim.models import Word2Vec


class Word2VecVectorizer(Vectorizer):

    def __init__(self):
        file = Path("../../data/embeddings/model.bin")
        self.model = self.load_model(file)

    def load_model(self, file):
        print("Loading Word2Vec Model")
        model = Word2Vec.load(file)
        return model

    def transform(self, corpus: list) -> list:
        results = []
        for doc in corpus:
            vectors = []
            for word in doc:
                try:
                    vectors.append(self.model[word])
                except KeyError:
                    pass
            vector = np.mean([vec for vec in vectors], axis=0)
            results.append(vector)
        return results

if __name__ == '__main__':
    s = Word2VecVectorizer()
