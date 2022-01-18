from gensim import corpora, models, similarities
from gensim.utils import simple_preprocess
import numpy as np
from open_science import db
from open_science.enums import MatrixEnum
from open_science.models import Matrix, PaperRevision, CalibrationPaper


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

def file_to_matrix(path):
    tfidf_similarities = corpora.MmCorpus.load(path)
    tfidf_matrix = np.array(tfidf_similarities, dtype="float64")
    return tfidf_matrix

def matrix_to_file(tfidf_matrix):
    path = 'tfidf_matrix.mm'
    tfidf_matrix.save(path)
    save_tfidf_matrix(path)


# returns list with all calibration papers and paper revisions preprocessed texts
def get_all_papers_texts():
    all_paper_texts = []

    all_paper_revisions = PaperRevision.query.all()
    all_calibration_papers = CalibrationPaper.query.all()
    all_papers = sorted(all_paper_revisions + all_calibration_papers, key=lambda paper: paper.id)
    all_paper_texts = [paper.preprocessed_text for paper in all_papers]

    return all_paper_texts



# returns similarities matrix created from preprocessed texts
def create_similarities_matrix():
    similarities_matrix = []

    all_paper_texts = get_all_papers_texts()
    dictionary = get_dictionary_from_db()
    tokenized_list = [simple_preprocess(doc) for doc in all_paper_texts]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')
    corpus_tfidf = tfidf[corpus]

    tfidf_similarities = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))
    similarities_matrix = np.array(tfidf_similarities[corpus_tfidf], dtype="float64")
    
    save_similarities_matrix(similarities_matrix)
    return similarities_matrix

# returns tfidf matrix created from preprocessed texts
def create_tfidf_matrix():
    tfidf_matrix = []

    all_paper_texts = get_all_papers_texts()
    dictionary = get_dictionary_from_db()
    tokenized_list = [simple_preprocess(doc) for doc in all_paper_texts]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')

    tfidf_similarities = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))
    
    matrix_to_file(tfidf_similarities)
    return tfidf_matrix


# saves given matrix as tfidf matrix in matrices table in database
def save_tfidf_matrix(tfidf_matrix_path):
    # current_tfidf_matrix_path = Matrix.query.get(MatrixEnum.TFIDF.value)
    # if current_tfidf_matrix_path is None:
    #     new_tfidf_matrix_path = Matrix(
    #         id = MatrixEnum.TFIDF.value,
    #         path = tfidf_matrix_path
    #     )
    #     db.session.add(new_tfidf_matrix_path)
    # else:
    #     current_tfidf_matrix_path = tfidf_matrix_path
    # db.session.commit()
    return tfidf_matrix_path


# saves given matrix as similarities matrix in matrices table in database
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
        similarities_matrix = file_to_matrix(current_similarities_matrix.path)
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


def create_dictionary():
    dictionary = []

    all_paper_texts = get_all_papers_texts()
    texts = [[text for text in doc.split()] for doc in all_paper_texts]
    dictionary = corpora.Dictionary(texts)
    dictionary_to_file(dictionary)

    return dictionary


def get_dictionary():
    dictionary_path = ''

    # current_dictionary_path = Dictionary.query.get(Dictionary.DICTIONARY.path)
    # if current_dictionary is not None:
    #     dictionary_path = current_dictionary_path
    # else:
    #     dictionary_path = None

    dictionary = file_to_dictionary(dictionary_path)
    return dictionary


def save_dictionary_path_to_db(dictionary_file_path):
    # current_dictionary_file_path = Dictionary.query.get(DictionaryEnum.DICTIONARY.value)
    # if current_dictionary_file_path is None:
    #     new_dictionary_file_path = Dictionary(
    #         id=DictionaryEnum.DICTIONARY.value,
    #         path=dictionary_file_path
    #     )
    #     db.session.add(new_dictionary_file_path)
    # else:
    #     current_dictionary_file_path.path = dictionary_file_path
    #
    # db.session.commit()
    return dictionary_file_path


def update_dictionary():
    dictionary = get_dictionary()
    return dictionary


def file_to_dictionary(file_path):
    return corpora.Dictionary.load(file_path)


def dictionary_to_file(dictionary):
    file_path = 'dictionary.dict'
    dictionary.save(file_path)
    save_dictionary_path_to_db(file_path)