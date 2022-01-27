from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from open_science import app
from open_science.models import User

from text_processing.search_engine import get_similar_users_to_user

# creates user plot and saves to file with path given in config
def create_save_users_plot():
    all_users = User.query.all()
    users_dict_id = {}
    users_with_articles = []
    for user in all_users:
        users_dict_id[user.id] = [revision.id for revision in user.rel_created_paper_revisions]

    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=100)
    user_matrix = []
    users = list(users_dict_id.keys())
    for user in users:
        _, array = get_similar_users_to_user(user, users_dict_id)
        user_matrix.append(array)
    for array in user_matrix:
        if array != []:
            users_with_articles.append(array)
    if users_with_articles != []:
        pca = PCA(n_components=2, whiten=False, random_state=42)
        standardized_pca = pca.fit_transform(users_with_articles)
        plt.scatter(standardized_pca[:, 0], standardized_pca[:, 1])
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        users_plot_url = app.config['USERS_PLOT_URL']
        plt.savefig(users_plot_url, dpi=200)
        plt.close(fig)

    # TODO: print variance preserved 
    # 3D version