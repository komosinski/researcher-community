from open_science.extensions import db
from open_science import app
from open_science.models import User, PaperRevision, PrivilegeSet
from similarity_matrix import *
from prepocess_text import *


# users_dict_id - dictionary of users_id articles_id (example: { user1: [article1, article30], user2: [article3, article10] } )
# wejscie: id uzytkownika dla ktorego szukamy podobnych, slownik uzytkiowników i ich id_artykułów
# wyjscie: lista uzytkowników najbardziej podobnych
def get_similar_users(user_id, users_dict_id):
    matrix = get_similarities_matrix()
    users_id = users_dict_id.keys()
    similarities_matrix = {i: [] for i in users_id}
    for users in users_dict_id:
        for enteredUser in users_dict_id[user_id]:
            for otherUser in users_dict_id[users]:
                similarities_matrix[users].append(matrix[enteredUser][otherUser])
    ranking = {i: [] for i in users_id}
    for array in similarities_matrix:
        ranking[array].append(sum(similarities_matrix[array]) / len(similarities_matrix[array]))
    ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    ranking_users = [i[0] for i in ranking]
    return ranking_users[1:]


# wejscie: id artykulu, articles_id_list - lista id artykulow w tej samej kolejnosci co jest dodawana w macierzy
def get_similar_articles(article_id, articles_id_list):
    matrix = get_similarities_matrix()
    article_index = articles_id_list.index(article_id)
    similar_ranking = [b[0] for b in sorted(enumerate(matrix[int(article_index)]), key=lambda i: i[1], reverse=True)]
    similar_ranking = similar_ranking[1:]
    similar_articles = [articles_id_list[i] for i in similar_ranking]
    return similar_articles


#wejscie: wyszukiwany tekst, Lista z przetworzonym tekstem artykułów (lista stringów), lista id artykulow w tej samej kolejnosci co jest dodawana w macierzy
def search_by_text(search_text, articles_text, articles_id_list):
    matrix = get_similarities_matrix()
    texts = [[text for text in doc.split()] for doc in articles_text]
    dictionary = corpora.Dictionary(texts)
    query = preprocess_text(search_text).split()
    query = dictionary.doc2bow(query)
    similarites_array = matrix.get_similarities(query)
    similar_ranking = [b[0] for b in sorted(enumerate(similarites_array), key=lambda i: i[1], reverse=True)]
    similar_articles = [articles_id_list[i] for i in similar_ranking]
    return similar_articles



