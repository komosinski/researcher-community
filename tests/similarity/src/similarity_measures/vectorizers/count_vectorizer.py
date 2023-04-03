from .vectorizer import Vectorizer
from sklearn.feature_extraction import text


class CountVectorizer(Vectorizer):

    def transform(self, corpus: list) -> list:
        vectorizer = text.CountVectorizer()
        a = vectorizer.fit_transform(corpus)
        return a.toarray()
