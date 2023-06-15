import json
import os
from os.path import isfile, join
from pathlib import Path

import pandas as pd

from tests.similarity.src.utils.gentree import gentree
from tests.similarity.src.similarity_measures.original_tfidf_similarity_measure import TfidfSimilarityMeasure
from tests.similarity.src.similarity_measures.glove_cosine_similarity_measure import GloveCosineSimilarityMeasure
from tests.similarity.src.similarity_measures.glove_similarity_measure import GloveSimilarityMeasure
from tests.similarity.src.similarity_measures.tinybert_cosine_similarity import TinyBertCosineSimilarityMeasure
from tests.similarity.src.similarity_measures.w2v_sim import Word2VecSimilarityMeasure
from tests.similarity.src.similarity_measures.bigbird_similarity import BigBirdimilarityMeasure
from tests.similarity.src.similarity_measures.bigbird_cosine_similarity import BigBirdCosineSimilarityMeasure
from tests.similarity.src.utils.tree_similarity import tree_similarity
from tests.similarity.src.similarity_measures.vectorizers.glove_vectorizer import GloveVectorizer
from tests.similarity.src.similarity_measures.vectorizers.count_vectorizer import CountVectorizer
from tests.similarity.src.similarity_measures.vectorizers.tiny_bert_vectorizer import TinyBertVectorizer
from tests.similarity.src.similarity_measures.vectorizers.word2vec_vectorizer import Word2VecVectorizer
from tests.similarity.src.similarity_measures.measures.cosine_measure import CosineMeasure
from tests.similarity.src.similarity_measures.measures.euclidean_measure import EuclideanMeasure


def run_tfidf_comparison():
    data_dir = [Path('../../data/raw/dendrogram_1'), Path('../../data/raw/dendrogram_2'),
                Path('../../data/raw/dendrogram_3')]
    for dendrogram in data_dir:
        file_paths = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(dendrogram) for f in filenames]
        file_paths = [os.path.abspath(i) for i in file_paths]
        file_paths = [i for i in file_paths if i.endswith('.pdf')]
        tfidf = TfidfSimilarityMeasure()
        tfidf.build_dictionary(file_paths)
        json_built = gentree(file_paths, tfidf)
        json_read = json.load(open(Path(str(dendrogram) + '/dendrogram.json')))
        print(tree_similarity(json_built, json_read))
        print(json_built)
        print(json_read)


def run_glove_comparison():
    data_dir = [Path('../../data/raw/dendrogram_1'), Path('../../data/raw/dendrogram_2'),
                Path('../../data/raw/dendrogram_3')]
    for dendrogram in data_dir:
        file_paths = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(dendrogram) for f in filenames]
        file_paths = [os.path.abspath(i) for i in file_paths]
        file_paths= [i for i in file_paths if i.endswith('.pdf')]
        glove = GloveCosineSimilarityMeasure()
        json_built = gentree(file_paths, glove)
        json_read = json.load(open(Path(str(dendrogram) + '/dendrogram.json')))
        print(tree_similarity(json_built, json_read))
        print(json_built)
        print(json_read)

def run_comparison(similarity_measure, tree_similarity_measure='fowlkes_mallows_score'):
    data_dir = [Path('../../data/raw/dendrogram_1'), Path('../../data/raw/dendrogram_2'),
                Path('../../data/raw/dendrogram_3')]
    dendrograms_similarity = []
    for dendrogram in data_dir:
        file_paths = [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(dendrogram) for f in
                      filenames]
        file_paths = [os.path.abspath(i) for i in file_paths]
        file_paths = [i for i in file_paths if i.endswith('.pdf')]
        if hasattr(similarity_measure, 'build_dictionary'):
            similarity_measure.build_dictionary(file_paths)
        json_built = gentree(file_paths, similarity_measure)
        json_read = json.load(open(Path(str(dendrogram) + '/dendrogram.json')))
        dendrograms_similarity.append(tree_similarity(json_built, json_read, tree_similarity_measure))
    return dendrograms_similarity

if __name__ == '__main__':
    results = {}
    for tree_sim in ['fowlkes_mallows_score', 'adjusted_rand_score']:
        for m in [TfidfSimilarityMeasure(),
                  TinyBertCosineSimilarityMeasure(CosineMeasure(), 256),
                  TinyBertCosineSimilarityMeasure(EuclideanMeasure(), 256),
                  # Word2VecSimilarityMeasure(CosineMeasure()),
                  # Word2VecSimilarityMeasure(EuclideanMeasure()),
                  # BigBirdimilarityMeasure(CosineMeasure(), 256),
                  # BigBirdimilarityMeasure(EuclideanMeasure(), 256),
                  GloveSimilarityMeasure(CosineMeasure()),
                  GloveSimilarityMeasure(EuclideanMeasure())
                  ]:
            try:
                sim = m.similarity.__class__.__name__ if hasattr(m, 'similarity') else "No similarity"
                results[(tree_sim, m.__class__.__name__, sim)] = run_comparison(m, tree_sim)
            except Exception as e:
                print(e)
    df = pd.DataFrame(results)
    print(df)
    df.to_excel("results.xlsx")