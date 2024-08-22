import gensim.matutils
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from open_science import app
from open_science.models import User
import os
from text_processing.search_engine import get_similar_users_to_user
import plotly.express as px
import pandas as pd
import open_science.models as db_models
from text_processing.similarity_matrix import get_dictionary
from gensim.utils import simple_preprocess
from gensim import models

def get_user_id_ranking_dict():
    user_id_ranking_dict = {}

    user_id_revisions_ids_dict = {user.id: [revision.id for revision in user.rel_created_paper_revisions] +\
                                  [calibration_paper.id for calibration_paper in user.rel_calibration_papers]
                                  for user in User.query.filter(User.id != 0).all()}

    all_paper_revisions = db_models.PaperRevision.query.all()
    all_calibration_papers = db_models.CalibrationPaper.query.all()
    all_paper_texts = [paper.preprocessed_text for paper in all_paper_revisions + all_calibration_papers]
    dictionary = get_dictionary()
    tokenized_list = [simple_preprocess(doc) for doc in all_paper_texts]
    corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
    tfidf = models.TfidfModel(corpus, smartirs='ntc')
    for user_id, revisions_ids in user_id_revisions_ids_dict.items():
        if revisions_ids:
            _, ranking_array = get_similar_users_to_user(user_id, user_id_revisions_ids_dict)
            # user_id_ranking_dict[user_id] = ranking_array
        all_papers = [i for i in all_calibration_papers if i.author == user_id]
        if not all_papers:
            continue
        all_paper_texts = [paper.preprocessed_text for paper in all_papers]
        tokenized_list = [simple_preprocess(doc) for doc in all_paper_texts]
        corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
        corpus_tfidf = tfidf[corpus[0]]
        user_id_ranking_dict[user_id] = gensim.matutils.sparse2full(corpus_tfidf, length=len(dictionary))

    return user_id_ranking_dict


def create_save_users_plot():
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=100)
    user_id_ranking_dict = get_user_id_ranking_dict()
    ranking_list = [ranking for ranking in user_id_ranking_dict.values()]
    users_ids_with_initals = get_users_ids_with_initials()
    if user_id_ranking_dict:
        pca = PCA(n_components=2, random_state=42)  # TODO can reuse the calculated 3D PCA and just use the two first dimensions for 2D
        standardized_pca = pca.fit_transform(ranking_list)
        print("Explained variance ratio:", pca.explained_variance_ratio_)
        # saving file for debugging or external analysis:
        # file_save_dir = os.path.join(app.config['ROOTDIR'], app.config['USERS_PLOT_2D_FILE_PATH'])
        # r = np.array(ranking_list)
        # np.savetxt("ranking_nameyourdataset.csv", r, delimiter=",")
        plt.scatter(standardized_pca[:, 0], standardized_pca[:, 1], marker='')
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        for i, id in enumerate(user_id_ranking_dict.keys()):
            ax.annotate(users_ids_with_initals[id], (standardized_pca[:, 0][i], standardized_pca[:, 1][i]), ha="center", va="center", color='blue')

    users_plot_url = os.path.join(app.config['ROOTDIR'], app.config['USERS_PLOT_2D_FILE_PATH'])
    plt.savefig(users_plot_url, dpi=200, bbox_inches="tight")
    plt.close(fig)


# This function creates an interactive 3D plot for the main page.
# It uses the get_similar_users_to_user() function to create the matrix of dissimilarity of all users in the system.
def create_save_users_plot_3d_old():
    user_id_ranking_dict = get_user_id_ranking_dict()
    ranking_list = [ranking for ranking in user_id_ranking_dict.values()]
    users_ids_with_initals = get_users_ids_with_initials()
    if user_id_ranking_dict:
        pca = PCA(n_components=3, random_state=42)
        standarlized_pca = pca.fit_transform(ranking_list) #TODO check input data (expected distances / coordinates?)
        df = pd.DataFrame(standarlized_pca, columns=['x', 'y', 'z'])
        fig = px.scatter_3d(df, x='x', y='y', z='z', title='The map of researcher.community', text = [users_ids_with_initals[id] for id in user_id_ranking_dict.keys()])
        fig.update_layout(scene=dict(
           xaxis=dict(backgroundcolor='rgba(200,200,200,0.9)', showbackground=True), # alpha does not seem to be implemented properely, and moreover axis background planes (when show=True) obscure/cover labels
           yaxis=dict(backgroundcolor='rgba(200,200,200,0.9)', showbackground=True),
           zaxis=dict(backgroundcolor='rgba(200,200,200,0.9)', showbackground=True)))
        fig.update_scenes(xaxis_title_text="",yaxis_title_text="",zaxis_title_text="")
        fig.update_layout(scene=dict(xaxis=dict(showticklabels=False),yaxis=dict(showticklabels=False),zaxis=dict(showticklabels=False)))
    else:
        fig = px.scatter_3d()

    users_plot_url_3d = os.path.join(app.config['ROOTDIR'], app.config['USERS_PLOT_3D_FILE_PATH'])
    fig.write_html(users_plot_url_3d) # , title='The map of researcher.community') # setting HTML title not always supported


def create_save_users_plot_3d():
    user_id_ranking_dict = get_user_id_ranking_dict()
    ranking_list = [ranking for ranking in user_id_ranking_dict.values()]
    users_ids_with_initals = get_users_ids_with_initials()
    pca = PCA(n_components=3, random_state=42)
    standarlized_pca = pca.fit_transform(ranking_list)
    df = pd.DataFrame(standarlized_pca, columns=['x', 'y', 'z'])
    users_plot_url_3d = os.path.join(app.config['ROOTDIR'], app.config['USERS_PLOT_3D_FILE_PATH'])

    if user_id_ranking_dict:
        df['text'] = [users_ids_with_initals[id] for id in user_id_ranking_dict.keys()]
        df['id'] = user_id_ranking_dict.keys()
    else:
        print("No data available to save")

    df.to_json(users_plot_url_3d, orient='records', lines=True)


# Returns dict that contains ids of all users paired with names initials in uppercase
def get_users_ids_with_initials():
    users = User.query.filter(User.id != 0).all()
    return { user.id: f'{user.first_name[0]}{user.second_name[0]}'.upper() for user in users}
