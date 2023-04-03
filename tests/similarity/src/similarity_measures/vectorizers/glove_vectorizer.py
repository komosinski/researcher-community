from tests.similarity.src.similarity_measures.vectorizers.vectorizer import Vectorizer
import numpy as np
from pathlib import Path


class GloveVectorizer(Vectorizer):

    def __init__(self):
        glove_file = Path("../../data/embeddings/glove.6B.50d.txt")
        self.model = self.load_glove_model(glove_file)

    def load_glove_model(self, glove_file):
        print("Loading Glove Model")
        with open(glove_file, encoding="utf8") as f:
            content = f.readlines()
        model = {}
        for line in content:
            splitLine = line.split()
            word = splitLine[0]
            embedding = np.array([float(val) for val in splitLine[1:]])
            model[word] = embedding
        print("Done.", len(model), " words loaded!")
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
