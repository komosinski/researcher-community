from gensim import corpora, models, similarities
from gensim.utils import simple_preprocess
import numpy as np

# Wejście: Lista z przetworzonym tekstem artykułów (lista stringów)
from open_science import db
from open_science.enums import MatrixEnum
from open_science.models import Matrix


def matrix_to_str(matrix):
    matrix_str = ""

    for row in matrix:
        row_str = " ".join([str(value) for value in row])
        matrix_str += row_str + ","

    matrix_str = matrix_str[:-1]

    return matrix_str


def str_to_matrix(matrix_str):
    matrix = []

    matrix_row_strings = matrix_str.split(",")
    matrix_values_strings = [row.split() for row in matrix_row_strings]
    matrix = [list(map(float, row)) for row in matrix_values_strings]
    matrix = np.array(matrix, dtype="float64")

    return matrix


def get_tfidf_matrix_from_text(articles_text):
    texts = [[text for text in doc.split()] for doc in articles_text]
    dictionary = corpora.Dictionary(texts)
    tokenized_list = [simple_preprocess(doc) for doc in articles_text]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')

    tfidf_similarities = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))
    tfidf_matrix = np.array(tfidf_similarities, dtype="float64")

    return tfidf_matrix


# Wejście: Lista z przetworzonym tekstem artykułów (lista stringów)
def get_similarities_matrix_from_text(articles_text):
    texts = [[text for text in doc.split()] for doc in articles_text]
    dictionary = corpora.Dictionary(texts)
    tokenized_list = [simple_preprocess(doc) for doc in articles_text]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')
    corpus_tfidf = tfidf[corpus]

    tfidf_similarities = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))
    similarities_matrix = np.array(tfidf_similarities[corpus_tfidf], dtype="float64")

    return similarities_matrix


def save_tfidf_matrix(tfidf_matrix):
    current_tfidf_matrix = Matrix.query.get(MatrixEnum.TFIDF.value)
    if current_tfidf_matrix is None:
        new_tfidf_matrix = Matrix(
            id=MatrixEnum.TFIDF.value,
            name=MatrixEnum.TFIDF.name,
            matrix=matrix_to_str(tfidf_matrix)
        )
        db.session.add(new_tfidf_matrix)
    else:
        current_tfidf_matrix.matrix = matrix_to_str(tfidf_matrix)

    db.session.commit()


def save_similarities_matrix(similarities_matrix):
    current_similarities_matrix = Matrix.query.get(MatrixEnum.SIMILARITIES.value)
    if current_similarities_matrix is None:
        new_similarities_matrix = Matrix(
            id=MatrixEnum.SIMILARITIES.value,
            name=MatrixEnum.SIMILARITIES.name,
            matrix=matrix_to_str(similarities_matrix)
        )
        db.session.add(new_similarities_matrix)
    else:
        current_similarities_matrix.matrix = matrix_to_str(similarities_matrix)

    db.session.commit()


def get_similarities_matrix_from_db():
    similarities_matrix = []

    current_similarities_matrix = Matrix.query.get(MatrixEnum.SIMILARITIES.value)
    if current_similarities_matrix is not None:
        similarities_matrix = str_to_matrix(current_similarities_matrix.matrix)
    else:
        similarities_matrix = None

    return similarities_matrix


def get_tfidf_matrix_from_db():
    tfidf_matrix = []

    current_tfidf_matrix = Matrix.query.get(MatrixEnum.SIMILARITIES.value)
    if current_tfidf_matrix is not None:
        tfidf_matrix = str_to_matrix(current_tfidf_matrix.matrix)
    else:
        tfidf_matrix = None

    return tfidf_matrix
