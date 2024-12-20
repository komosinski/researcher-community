import pdftotext
from nltk.tokenize import word_tokenize
import nltk.corpus
from nltk.stem import WordNetLemmatizer
from nltk import PorterStemmer
from flask import current_app as app


def lower_text(text):
    return text.lower()


def remove_stopwords(text):
    stopwords = nltk.corpus.stopwords.words('english')
    text = [i for i in text if i not in stopwords]
    text = [i for i in text if 3 < len(i) < 14]
    return text


def removePunctuationWords(text):
    words_list = []
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~0123456789"""
    for word in text:
        split = [char for char in word]
        if not any(x in punctuation for x in split):
            words_list.append(word)
    return words_list


def lemmatizer(text):
    wordnet_lemmatizer = WordNetLemmatizer()
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemm_text


def stemming(text):
    porter_stemmer = PorterStemmer()
    stem_text = [porter_stemmer.stem(word) for word in text]
    return stem_text

def preprocess_text(text):
    text = lower_text(text)
    text = word_tokenize(text)
    text = remove_stopwords(text)
    text = removePunctuationWords(text)
    text = lemmatizer(text)
    text = stemming(text)
    text = " ".join(text)
    return text

# Extract text from PDF file
def get_text(file):
    with open(file, "rb") as f:
        pdf = pdftotext.PDF(f)
    text = "\n\n".join(pdf)
    text = preprocess_text(text)
    if len(text.split())<app.config['PAPER_MIN_WORDS_COUNT']:
        raise Exception(f"The extracted text has less than {app.config['PAPER_MIN_WORDS_COUNT']} words")
    return text

