# Specification of similarity calculations

Similarity matrix is created using the tf-idf model. First, the system creates the dictionary that stores every word in the system and gives words an ID.

text_processing/similarity_matrix.py function:

    def create_dictionary()

After that, the tf-idf model is created. This model creates a corpus that shows what words from the dictionary appear in specific articles, and how often.
Using this corpus, the tf-idf model changes weights of some words to find the most important ones. And with the tf-idf model, we want to create a sparse matrix that we can use to find similarities between articles.
The sparse matrix is created using the gensim `similarities.SparseMatrixSimilarity` function and we need to specify its min size, that is the size of the dictionary created before.

text_processing/similarity_matrix.py function:

    def create_tfidf_matrix()

Finally, when we have the tf-idf model, we can create similarities between articles by adding to this model the entire corpus. 
This will allow us to calculate similarities between articles. We can add here some specific words, and we will get similarities between these words and all articles in the system.
This functionality is used in function search_articles_by_text in the `text_processing/similarity_matrix.py` file. 

text_processing/similarity_matrix.py function:

    def create_similarities_matrix()

These 3 functions save and read their objects to files in their own specific object format (for efficiency).

## Estimating the similarity between two articles

Similarity between articles is calculated using the similarity matrix saved in the file in `text_processing/search_engine.py`.

    def get_similar_articles_to_articles(article_id, articles_id_list)

We have to provide an article ID for which we search for similar articles, and a list of IDs of articles in the system. The result is sorted in a list of most similar articles.

## Estimating the similarity between two researchers

Similarities between users are calculated using the similarity matrix saved in the file.

In text_processing/search_engine.py:

    def get_similar_users_to_user(user_id, users_dict_id)

We have to provide a specific user ID for which we search for similar users, and a list of IDs of users in the system.
Users similarity is calculated as the average similarity of users' articles; we search for articles that some user authored, then we calculate the average similarity to a specific user (user_ID in this function).


## What happens when a user uses "search"

The "Search by text" function uses the tf-idf model saved in the file. The function calculates the similarity between words that the user searched for and all articles in system. 

    def search_articles_by_text(search_text, articles_id_list)


## What happens when a researcher uploads/updates a paper

First, raw text from the pdf is extraced using the `pdftotext` library.

In text_processing/prepocess_text.py file:

    def get_text(file) 

Then we preprocess the text so that it can be saved in the database. 

    def preprocess_text(text) in text_processing/prepocess_text.py file

This text is used in creating the dictionary and the tf-idf model. We only use the preprocessed text to calculate similarities.

When we add a new article, we don't calculate the entire new object every time. Instead we incrementally add only new values to the existing object so that we can calculate similarities much faster and more efficiently.


## Similarity matrix

For a small set of test articles (120 papers), the sparsity of the similarity matrix is around 5%. 
The matrix size is 120^2=14400 values.
In this matrix, for the test papers, there were 720 non-zero values. 
This amount depends on the particular articles in the system. 
If the function gensim `similarities.SparseMatrixSimilarity` that creates the sparse matrix finds more or less important values, the sparsity ratio can be higher or lower.

Scripts for a more thorough experiment comparing the performance of multiple similarity measures (including embeddings more complex than TFIDF such as Glove, TinyBert and BigBird) are in [in this directory](tests/similarity/).



## Triggers and scheduled events: when and what is recalculated

`update_files.py` calculates all saved objects in files from scratch and creates new scatter plot(s) for the main page (running this script can be added to `crontab`, for example). See also `TEXT_PROCESSING_UPDATE_FILES_ON_UPLOAD` in `config.py`.
