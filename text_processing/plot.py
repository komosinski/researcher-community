from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from open_science import app
from open_science.models import User

from search_engine import get_similar_users_to_user

# creates user plot and saves to file with path given in config
def create_save_users_plot():
    all_users = User.query.all()
    users_dict_id = {}
    for user in all_users:
        users_dict_id[user.id] = [revision.id for revision in user.rel_created_paper_revisions]

    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=100)
    user_matrix = []
    users = list(users_dict_id.keys())
    for user in users:
        _, array = get_similar_users_to_user(user, users_dict_id)
        user_matrix.append(array)
    pca = PCA(n_components=2, whiten=False, random_state=42)
    standardized_pca = pca.fit_transform(user_matrix)
    # plt.scatter(standardized_pca[:, 0], standarlized_pca[:, 1])
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.show()

    # TODO: Save plot to this path
    users_plot_url = app.config['USERS_PLOT_URL']