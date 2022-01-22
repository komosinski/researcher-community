from gensim import corpora, models, similarities
from gensim.utils import simple_preprocess
import numpy as np
from open_science import app
import open_science.models as db_models


# returns list with all calibration papers and paper revisions preprocessed texts
def get_all_papers_texts():
    all_paper_texts = []

    all_paper_revisions = db_models.PaperRevision.query.all()
    all_calibration_papers = db_models.CalibrationPaper.query.all()
    all_papers = sorted(all_paper_revisions + all_calibration_papers, key=lambda paper: paper.id)
    all_paper_texts = [paper.preprocessed_text for paper in all_papers]

    return all_paper_texts


def create_dictionary():
    dictionary = []

    all_paper_texts = get_all_papers_texts()
    texts = [[text for text in doc.split()] for doc in all_paper_texts]
    dictionary = corpora.Dictionary(texts)

    return dictionary


def save_dictionary(dictionary):
    dictionary_url = app.config['DICTIONARY_URL']
    dictionary.save(dictionary_url)


def get_dictionary():
    dictionary = []

    dictionary_url = app.config['DICTIONARY_URL']
    dictionary = corpora.Dictionary.load(dictionary_url)

    return dictionary


# new_text is array of strings
def update_dictionary(new_text):
    dictionary = get_dictionary()
    new_words = [[text for text in doc.split()] for doc in new_text]
    dictionary.add_documents(new_words)
    save_dictionary(dictionary)

    return dictionary


# returns tfidf matrix created from preprocessed texts
def create_tfidf_matrix():
    tfidf_matrix = []

    all_paper_texts = get_all_papers_texts()
    dictionary = get_dictionary()
    tokenized_list = [simple_preprocess(doc) for doc in all_paper_texts]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')
    tfidf_matrix = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))

    return tfidf_matrix


# saves given matrix as tfidf matrix in matrices table in database
def save_tfidf_matrix(tfidf_matrix):
    tfidf_matrix_url = app.config['TFIDF_MATRIX_URL']
    tfidf_matrix.save(tfidf_matrix_url)


def get_tfidf_matrix():
    tfidf_matrix = []

    tfidf_matrix_url = app.config['TFIDF_MATRIX_URL']
    tfidf_matrix = corpora.Dictionary.load(tfidf_matrix_url)

    return tfidf_matrix


# returns similarities matrix created from preprocessed texts
def create_similarities_matrix():
    similarities_matrix = []

    all_paper_texts = get_all_papers_texts()
    dictionary = get_dictionary()
    tokenized_list = [simple_preprocess(doc) for doc in all_paper_texts]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')
    corpus_tfidf = tfidf[corpus]

    tfidf_matrix = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))
    similarities_matrix = np.array(tfidf_matrix[corpus_tfidf], dtype="float64")

    return similarities_matrix


# saves given matrix as similarities matrix in matrices table in database
def save_similarities_matrix(similarities_matrix):
    similarities_matrix_url = app.config['SIMILARITIES_MATRIX_URL']
    np.save(similarities_matrix_url, similarities_matrix)


def get_similarities_matrix():
    similarities_matrix = []

    tfidf_similarities_url = app.config['TFIDF_MATRIX_URL']
    similarities_matrix = corpora.Dictionary.load(tfidf_similarities_url)

    return similarities_matrix


def update_similarity_matrix(new_article):
    similarity_matrix = get_similarities_matrix()
    matrix_tfidf = get_tfidf_matrix()
    dictionary = get_dictionary()
    new_text = dictionary.doc2bow(new_article.split())
    new_article_similarities = matrix_tfidf[new_text]
    similarity_matrix_add_column = np.column_stack((similarity_matrix, new_article_similarities))
    new_article_similarities = np.append(new_article_similarities, 1.00)
    similarity_matrix = np.row_stack(similarity_matrix_add_column, new_article_similarities)
    save_similarities_matrix(similarity_matrix)

    return similarity_matrix
