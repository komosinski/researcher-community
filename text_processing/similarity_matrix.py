from open_science.extensions import db
from open_science import app
from open_science.models import User, PaperRevision, PrivilegeSet
from gensim import corpora, models, similarities
from gensim.utils import simple_preprocess
import numpy as np


# Tworzenie i odczytywanie macierzy
# Wejście: Lista z przetworzonym tekstem artykułów (lista stringów)
# Zapisanie: macierz (numpy.ndarray)
def calculate_matrix(articles_text):
    texts = [[text for text in doc.split()] for doc in articles_text]
    dictionary = corpora.Dictionary(texts)
    tokenized_list = [simple_preprocess(doc) for doc in articles_text]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')
    corpus_tfidf = tfidf[corpus]
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))
    similarities_matrix = np.array(index[corpus_tfidf], dtype="float64")
    # save matrix to database


def get_similarities_matrix():
    matrix = []
    # get matrix from database
    return matrix
