import json
import os
from os.path import isfile, join
from pathlib import Path
from tests.similarity.src.utils.gentree import gentree
from tests.similarity.src.similarity_measures.original_tfidf_similarity_measure import TfidfSimilarityMeasure
from tests.similarity.src.similarity_measures.glove_cosine_similarity_measure import GloveCosineSimilarityMeasure
from tests.similarity.src.utils.tree_similarity import tree_similarity


def run_tfidf_comparison():
    data_dir = [Path('../../data/raw/dendrogram_1'), Path('../../data/raw/dendrogram_2'),
                Path('../../data/raw/dendrogram_3')]
    for dendrogram in data_dir:
        file_paths = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(dendrogram) for f in filenames]
        file_paths = [os.path.abspath(i) for i in file_paths]
        file_paths= [i for i in file_paths if i.endswith('.pdf')]
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


if __name__ == '__main__':
    #run_tfidf_comparison()
    run_glove_comparison()