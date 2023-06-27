from tests.similarity.src.utils.similarity_for_classification import SimilarityForClassification
from tests.similarity.src.similarity_measures.original_tfidf_similarity_measure import TfidfSimilarityMeasure
from tests.similarity.src.similarity_measures.glove_cosine_similarity_measure import GloveCosineSimilarityMeasure
from tests.similarity.src.similarity_measures.glove_euclidean_similarity_measure import GloveCosineEuclideanMeasure
from tests.similarity.src.similarity_measures.bigbird_cosine_similarity import BigBirdCosineSimilarityMeasure
from tests.similarity.src.similarity_measures.tinybert_cosine_similarity import TinyBertCosineSimilarityMeasure

if __name__ == '__main__':
    results = {}
    measure = GloveCosineSimilarityMeasure()
    sim = SimilarityForClassification('../../data/raw/categories_dataset/', measure,
                                      'Glove based similarity')
    results['Glove based similarity'] = sim.get_accuracy()

    measure = TfidfSimilarityMeasure()
    sim = SimilarityForClassification('../../data/raw/categories_dataset/', measure,
                                      'Tfidf based similarity')
    results['Tfidf based similarity'] = sim.get_accuracy()



    for c in [256, 512]:
        measure = TinyBertCosineSimilarityMeasure(c)
        sim = SimilarityForClassification('../../data/raw/categories_dataset/', measure, 'TinyBert - context_len: ' + str(c))
        results['TinyBert' + str(c)] = sim.get_accuracy()

        measure = BigBirdCosineSimilarityMeasure(c)
        sim = SimilarityForClassification('../../data/raw/categories_dataset/', measure, 'BigBird - context_len: ' + str(c))
        results['BigBird' + str(c)] = sim.get_accuracy()
        print(results)

    measure = BigBirdCosineSimilarityMeasure(1024)
    sim = SimilarityForClassification('../../data/raw/categories_dataset/', measure, 'BigBird - context_len: ' + str(1024))
    results['BigBird' + str(1024)] = sim.get_accuracy()

    measure = BigBirdCosineSimilarityMeasure(128)
    sim = SimilarityForClassification('../../data/raw/categories_dataset/', measure, 'BigBird - context_len: ' + str(128))
    results['BigBird' + str(128)] = sim.get_accuracy()
    print(results)



