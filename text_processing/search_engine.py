import numpy as np

from text_processing.prepocess_text import preprocess_text
from text_processing.similarity_matrix import get_similarities_matrix, get_tfidf_matrix, get_dictionary


def get_similar_users_to_user(user_id, users_dict_id):
    matrix = get_similarities_matrix()
    matrix = np.array(matrix)
    users_id = users_dict_id.keys()
    similarities_matrix = {i: [] for i in users_id}
    ranking = {i: [] for i in users_id}
    ranking_sorted = []

    if users_dict_id[user_id] != []:
        for users in users_dict_id:
            for enteredUser in users_dict_id[user_id]:
                for otherUser in users_dict_id[users]:
                    if otherUser < len(matrix) and enteredUser < len(matrix) and users < len(similarities_matrix):
                        similarities_matrix[users].append(matrix[enteredUser][otherUser])
        for array in similarities_matrix:
            if similarities_matrix[array] == []:
                similarities_matrix[array] = [0.0]
            if array < len(ranking) and array < len(similarities_matrix) and similarities_matrix[array]:
                ranking[array].append(sum(similarities_matrix[array]) / len(similarities_matrix[array]))
        ranking_sorted = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    ranking_users = [i[0] for i in ranking_sorted]
    return ranking_users[1:], np.concatenate(list(ranking.values()), axis=0)


def get_similar_articles_to_articles(article_id, articles_id_list):
    similar_ranking = []
    matrix = get_similarities_matrix()
    article_index = articles_id_list.index(article_id)
    if len(articles_id_list) > 0 and len(matrix) > 0 and article_index < len(matrix):
        similar_ranking = [b[0] for b in
                           sorted(enumerate(matrix[int(article_index)]), key=lambda i: i[1], reverse=True)]
        if len(similar_ranking) > 1:
            similar_ranking = similar_ranking[1:]
    return similar_ranking


def search_articles_by_text(search_text, articles_id_list):
    matrix = get_tfidf_matrix()
    dictionary = get_dictionary()
    query = preprocess_text(search_text).split()
    query = dictionary.doc2bow(query)
    similarites_array = matrix[query]
    similar_ranking = [b[0] for b in sorted(enumerate(similarites_array), key=lambda i: i[1], reverse=True)]
    similar_articles = [articles_id_list[i] for i in similar_ranking]
    return similar_articles


# in: id of article, users id and their articles id dictionary
# out: list of users similar to article
def get_similar_users_to_article(article_id, users_dict_id):
    ranking = []
    matrix = get_similarities_matrix()
    key_list = list(users_dict_id.keys())
    val_list = list(users_dict_id.values())
    if int(article_id) < len(matrix):
        ranking = [b[0] for b in
                   sorted(enumerate(matrix[int(article_id)]), key=lambda i: i[1], reverse=True)]
    ranking_users = []
    if len(ranking) > 1:
        ranking = ranking[1:]
    user = ""
    for article_ranked in ranking:
        for user_articles in users_dict_id.values():
            position = val_list.index(user_articles)
            if article_ranked in user_articles:
                ranking_users.append(key_list[position])
            if int(article_id) in user_articles:
                user = key_list[position]
    ranking_users = list(filter(lambda a: a != user, ranking_users))
    ranking_users = set(ranking_users)
    return ranking_users
