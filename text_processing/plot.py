from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
import seaborn as sns
from search_engine import get_similar_users_to_user
from similarity_matrix import get_similarities_matrix_from_db

def create_users_plot(users_dict_id):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=100)
    user_matrix = []
    users = list(users_dict_id.keys())
    for user in users:
        _, array = get_similar_users_to_user(user, users_dict_id)
        user_matrix.append(array)
    pca = PCA(n_components=2, whiten=False, random_state=42)
    standardized_pca = pca.fit_transform(user_matrix)
    users_standardized_pca = pd.DataFrame(data=standardized_pca, columns=["x", "y"])
    sns.scatterplot(x="x", y="y", data=users_standardized_pca)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.show()