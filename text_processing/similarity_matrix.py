from gensim import corpora, models, similarities
from gensim.utils import simple_preprocess
import numpy as np
import open_science.models as db_models
import os
# ImportError, use current_app instead
# from open_science import app
from flask import current_app as app


# returns list with all calibration papers and paper revisions preprocessed texts
def get_all_papers_texts():
    all_paper_texts = []

    all_paper_revisions = db_models.PaperRevision.query.all()
    all_calibration_papers = db_models.CalibrationPaper.query.all()
    all_papers = sorted(all_paper_revisions + all_calibration_papers, key=lambda paper: paper.id)
    all_paper_texts = [paper.preprocessed_text for paper in all_papers]

    return all_paper_texts


# We have to create it each time matrix is created to know
# which row in matrix corresponds to which paper
def create_matrix_mapping_array():
    similarities_matrix_mapping = []

    all_paper_revisions = db_models.PaperRevision.query.all()
    all_calibration_papers = db_models.CalibrationPaper.query.all()
    all_papers = sorted(all_paper_revisions + all_calibration_papers, key=lambda paper: paper.id)
    similarities_matrix_mapping = [paper.id for paper in all_papers]

    return similarities_matrix_mapping


# Creates new dictionary from text in database
def create_dictionary():
    dictionary = []

    all_paper_texts = get_all_papers_texts()
    texts = [[text for text in doc.split()] for doc in all_paper_texts]
    dictionary = corpora.Dictionary(texts)

    return dictionary


# Save dictionary to the file
def save_dictionary(dictionary):
    dictionary_url = os.path.join(app.config['ROOTDIR'],
                                  app.config['DICTIONARY_URL'])
    dictionary.save(dictionary_url)


# Get dictionary from file
def get_dictionary():
    dictionary = []

    dictionary_url = os.path.join(app.config['ROOTDIR'],
                                  app.config['DICTIONARY_URL'])
    dictionary = corpora.Dictionary.load(dictionary_url)

    return dictionary


# new_text is array of strings
# Adds new added words that didn't appear in dictionary
def update_dictionary(new_article):
    dictionary = get_dictionary()
    new_words = [[text for text in doc.split()] for doc in new_article]
    dictionary.add_documents(new_words)
    save_dictionary(dictionary)

    return dictionary


def save_tfidf_matrix_mapping_array(tfidf_matrix_mapping_array):
    tfidf_matrix_mapping_array_url = os.path.join(app.config['ROOTDIR'],
                                                  app.config['TFIDF_MATRIX_MAPPING_ARRAY_URL'])
    np.save(tfidf_matrix_mapping_array_url, tfidf_matrix_mapping_array)


def get_tfidf_matrix_mapping_array():
    tfidf_matrix_mapping_array = []

    tfidf_matrix_mapping_array_url = os.path.join(app.config['ROOTDIR'],
                                                  app.config['TFIDF_MATRIX_MAPPING_ARRAY_URL'])
    tfidf_matrix_mapping_array = np.load(tfidf_matrix_mapping_array_url, tfidf_matrix_mapping_array)

    return tfidf_matrix_mapping_array


# returns tfidf matrix created from preprocessed texts
def create_tfidf_matrix():
    tfidf_matrix = []

    all_paper_texts = get_all_papers_texts()
    tfidf_matrix_mapping_array = create_matrix_mapping_array()
    save_tfidf_matrix_mapping_array(tfidf_matrix_mapping_array)

    dictionary = get_dictionary()
    tokenized_list = [simple_preprocess(doc) for doc in all_paper_texts]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')
    tfidf_matrix = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))

    return tfidf_matrix


# saves given matrix as tfidf matrix in matrices table in database
def save_tfidf_matrix(tfidf_matrix):
    tfidf_matrix_url = os.path.join(app.config['ROOTDIR'],
                                    app.config['TFIDF_MATRIX_URL'])
    tfidf_matrix.save(tfidf_matrix_url)


# Get tf-idf model from file
def get_tfidf_matrix():
    tfidf_matrix = []

    tfidf_matrix_url = os.path.join(app.config['ROOTDIR'],
                                    app.config['TFIDF_MATRIX_URL'])
    tfidf_matrix = corpora.Dictionary.load(tfidf_matrix_url)

    return tfidf_matrix


# Create new model with updated dictionary
def update_tfidf_matrix():
    tfidf_matrix = []

    all_paper_texts = get_all_papers_texts()
    tfidf_matrix_mapping_array = create_matrix_mapping_array()
    save_tfidf_matrix_mapping_array(tfidf_matrix_mapping_array)

    dictionary = get_dictionary()
    tokenized_list = [simple_preprocess(doc) for doc in all_paper_texts]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')
    tfidf_matrix = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))
    save_tfidf_matrix(tfidf_matrix)

    return tfidf_matrix


def save_similarities_matrix_mapping_array(similarities_matrix_mapping_array):
    similarities_matrix_mapping_array_url = os.path.join(app.config['ROOTDIR'],
                                                         app.config['SIMILARITIES_MATRIX_MAPPING_ARRAY_URL'])
    np.save(similarities_matrix_mapping_array_url, similarities_matrix_mapping_array)


def get_similarities_matrix_mapping_array():
    similarities_matrix_mapping_array = []

    similarities_matrix_mapping_array_url = os.path.join(app.config['ROOTDIR'],
                                                         app.config['SIMILARITIES_MATRIX_MAPPING_ARRAY_URL'])
    similarities_matrix_mapping_array = np.load(similarities_matrix_mapping_array_url,
                                                similarities_matrix_mapping_array)

    return similarities_matrix_mapping_array


# returns similarities matrix created from preprocessed texts
def create_similarities_matrix():
    similarities_matrix = []

    all_paper_texts = get_all_papers_texts()
    similarities_matrix_mapping_array = create_matrix_mapping_array()
    save_similarities_matrix_mapping_array(similarities_matrix_mapping_array)

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
    similarities_matrix_url = os.path.join(app.config['ROOTDIR'],
                                           app.config['SIMILARITIES_MATRIX_URL'])
    np.save(similarities_matrix_url, similarities_matrix)


# Get similarity matrix from file
def get_similarities_matrix():
    similarities_matrix = []

    similarities_matrix_url = os.path.join(app.config['ROOTDIR'],
                                           app.config['SIMILARITIES_MATRIX_URL'])
    similarities_matrix = np.load(similarities_matrix_url, similarities_matrix)

    return similarities_matrix


# Calculate similarity of new article to all articles in th system
# Add this values to similarity matrix as column and row with 1.00 as similarity to itself
def update_similarity_matrix(new_article):
    similarity_matrix = get_similarities_matrix()
    matrix_tfidf = get_tfidf_matrix()
    dictionary = get_dictionary()
    new_text = dictionary.doc2bow(new_article.split())
    new_article_similarities = matrix_tfidf.get_similarities(new_text)
    if len(new_article_similarities) == len(similarity_matrix):
        similarity_matrix_add_column = np.column_stack((similarity_matrix, new_article_similarities))
        new_article_similarities = np.append(new_article_similarities, 1.00)
        similarity_matrix = np.row_stack((similarity_matrix_add_column, new_article_similarities))
        save_similarities_matrix(similarity_matrix)

    return similarity_matrix
