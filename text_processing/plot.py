from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from open_science import app
from open_science.models import User
import os
from text_processing.search_engine import get_similar_users_to_user
import plotly.express as px
import pandas as pd


def get_user_id_ranking_dict():
    user_id_ranking_dict = {}

    user_id_revisions_ids_dict = {user.id: [revision.id for revision in user.rel_created_paper_revisions]
                                  for user in User.query.filter(User.id != 0).all()}

    for user_id, revisions_ids in user_id_revisions_ids_dict.items():
        if revisions_ids:
            _, ranking_array = get_similar_users_to_user(user_id, user_id_revisions_ids_dict)
            user_id_ranking_dict[user_id] = ranking_array
    return user_id_ranking_dict


def create_save_users_plot():
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=100)
    user_id_ranking_dict = get_user_id_ranking_dict()
    ranking_list = [ranking for ranking in user_id_ranking_dict.values()]
    users_ids_with_initals = get_users_ids_with_initials()
    if user_id_ranking_dict:
        pca = PCA(n_components=2, whiten=False, random_state=42)
        standardized_pca = pca.fit_transform(ranking_list)
        plt.scatter(standardized_pca[:, 0], standardized_pca[:, 1], marker='')
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        for i, id in enumerate(user_id_ranking_dict.keys()):
            ax.annotate(users_ids_with_initals[id], (standardized_pca[:, 0][i], standardized_pca[:, 1][i]), color='blue')

    users_plot_url = os.path.join(app.config['ROOTDIR'], app.config['USERS_PLOT_2D_FILE_PATH'])
    plt.savefig(users_plot_url, dpi=200, bbox_inches="tight")
    plt.close(fig)


# This function create plot for the main page. Plot shows measures of users in the system as interactive 3D plot
# It uses get_similar_users_to_user function for creating matrix of similarity of all users in system.
def create_save_users_plot_3d():
    user_id_ranking_dict = get_user_id_ranking_dict()
    ranking_list = [ranking for ranking in user_id_ranking_dict.values()]
    if user_id_ranking_dict:
        pca = PCA(n_components=3, whiten=False, random_state=42)
        standarlized_pca = pca.fit_transform(ranking_list)
        df = pd.DataFrame(standarlized_pca, columns=['x', 'y', 'z'])
        fig = px.scatter_3d(df, x='x', y='y', z='z')
    else:
        fig = px.scatter_3d()

    users_plot_url_3d = os.path.join(app.config['ROOTDIR'], app.config['USERS_PLOT_3D_FILE_PATH'])
    fig.write_html(users_plot_url_3d)


# Returns dict that contains ids of all users paired with names initials in uppercase
def get_users_ids_with_initials():
    users = User.query.filter(User.id != 0).all()
    return { user.id: f'{user.first_name[0]}{user.second_name[0]}'.upper() for user in users}
