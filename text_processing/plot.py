from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from open_science import app
from open_science.models import User
import os
from text_processing.search_engine import get_similar_users_to_user
import plotly.express as px
import pandas as pd


def create_save_users_plot():
    all_users = User.query.all()
    users_dict_id = {}
    users_with_articles = []
    for user in all_users:
        users_dict_id[user.id] = [revision.id for revision in user.rel_created_paper_revisions]
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=100)
    user_matrix = []
    user_ids = []
    users = list(users_dict_id.keys())
    for user in users:
        _, array = get_similar_users_to_user(user, users_dict_id)
        user_matrix.append(array)
    for i, array in enumerate(user_matrix):
        if array != []:
            users_with_articles.append(array)
            user_ids.append(users[i])
    if len(users_with_articles) > 1:
        pca = PCA(n_components=2, whiten=False, random_state=42)
        standardized_pca = pca.fit_transform(users_with_articles)
        plt.scatter(standardized_pca[:, 0], standardized_pca[:, 1])
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        for i, id in enumerate(user_ids):
            ax.annotate(id, (standardized_pca[:, 0][i], standardized_pca[:, 1][i]))
        users_plot_url = os.path.join(app.config['ROOTDIR'], app.config['USERS_PLOT_URL'])
        plt.savefig(users_plot_url, dpi=200)
    plt.close(fig)


# This function create plot for the main page. Plot shows similarities of users in the system as interactive 3D plot
# It uses get_similar_users_to_user function for creating matrix of similarity of all users in system.
def create_save_users_plot_3d():
    all_users = User.query.all()
    users_dict_id = {}
    users_with_articles = []
    for user in all_users:
        users_dict_id[user.id] = [revision.id for revision in user.rel_created_paper_revisions]

    user_matrix = []
    users = list(users_dict_id.keys())
    for user in users:
        _, array = get_similar_users_to_user(user, users_dict_id)
        user_matrix.append(array)
    for array in user_matrix:
        if array != []:
            users_with_articles.append(array)
    if len(users_with_articles) > 1:
        pca = PCA(n_components=3, whiten=False, random_state=42)
        standarlized_pca = pca.fit_transform(users_with_articles)
        df = pd.DataFrame(standarlized_pca, columns=['x', 'y', 'z'])
        fig = px.scatter_3d(df, x='x', y='y', z='z')
        users_plot_url_3d = os.path.join(app.config['ROOTDIR'], app.config['USERS_PLOT_3D_URL'])
        fig.write_html(users_plot_url_3d)