# Specification of similarity calculations

Similarity matrix is created using tf-idf model. First system creates dictionary that store every word in the system and give words an ID. 

text_processing/similarity_matrix.py function:

    def create_dictionary()

After that created is tfidf model. This model creates corpus that shows what words from dictionary appear in specific articles and how often.
Using this corpus tf-idf model changes weights of some words to find the most important. And with tf-idf model we want to create sparse matrix that we can use to find similarities between articles.
Sparse matrix is created using gensim similarities.SparseMatrixSimilarity function that we need to specify its min size, that is the size of the dictionary created before.

text_processing/similarity_matrix.py function:

    def create_tfidf_matrix()

Finally, when we have tf-idf model, we can create similarities between articles by adding to this model whole corpus. 
This will allow us to see similarities between articles. We can add here some specific words, and we will get similarities between these words and all articles in the system.
This functionality is used in function search_articles_by_text in text_processing/similarity_matrix.py file. 

text_processing/similarity_matrix.py function:

    def create_similarities_matrix()

This 3 functions save and read its object to files in its own specific object format for optimization.

## Estimating the similarity between two articles

Similarity between articles is calculated, using the similarity matrix saved in file in text_processing/search_engine.py

    def get_similar_articles_to_articles(article_id, articles_id_list)

We have to give article ID which we search for similar articles and list of ID of articles in system. The result is sorted in a list of most similar articles.

## Estimating the similarity between two researchers

Similarities between users is calculated using similarity matrix saved in file. 

In text_processing/search_engine.py:

    def get_similar_users_to_user(user_id, users_dict_id)

We have to give specific user ID that we search for similar users and list of ID's of users in the system. 
Users similarity is calculated by the average similarity of users articles (we are searching for articles that some user written, then we calculate average similarity to specific user (user_ID in this function)).


## What happens when a user uses "search"

Search by text function uses saved in file tf-idf model. Function calculate similarity between words that user searched and all articles in system. 

    def search_articles_by_text(search_text, articles_id_list)

## What happens when a researcher uploads/updates a paper

First we extract text from pdf, using pdftotext library.

In text_processing/prepocess_text.py file:

    def get_text(file) 

Then we preprocess text which will be saved in database. 

    def preprocess_text(text) in text_processing/prepocess_text.py file

This text is used in creating dictionary and tf-idf model. We only uses preprocess text to calculate similarities.

When we add new article we don't calculate new object every time, instead we add new values to existing object so that we can calculate similarities much faster and more efficient.

## Similarity matrix

Sparsity of the similarity matrix is around 5%. 
With 120 articles
Matrix size =  14 400 values.
In this matrix, there was 720 non-zero values. 
This value depends of articles in the system. 
If function (gensim similarities.SparseMatrixSimilarity), that creates sparse matrix, finds more or less values important, sparsity can be higher or lower.

## Triggers and scheduled events: when and what is recalculated

Scheduled event is calculating all saved objects in files form scratch and creates new scatter plot for the main page.
