import pdftotext
from nltk.tokenize import word_tokenize
import nltk.corpus
from nltk.stem import WordNetLemmatizer
from nltk import PorterStemmer


class PdfToTextTransformer:

    @staticmethod
    def lower_text(text):
        return text.lower()

    @staticmethod
    def remove_stopwords(text):
        stopwords = nltk.corpus.stopwords.words('english')
        text = [i for i in text if i not in stopwords]
        text = [i for i in text if 3 < len(i) < 14]
        return text

    @staticmethod
    def remove_punctuation_words(text):
        words_list = []
        punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~0123456789"""
        for word in text:
            split = [char for char in word]
            if not any(x in punctuation for x in split):
                words_list.append(word)
        return words_list

    @staticmethod
    def lemmatizer(text):
        wordnet_lemmatizer = WordNetLemmatizer()
        lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
        return lemm_text

    @staticmethod
    def stemming(text):
        porter_stemmer = PorterStemmer()
        stem_text = [porter_stemmer.stem(word) for word in text]
        return stem_text

    def preprocess_text(self, text):
        text = self.lower_text(text)
        text = word_tokenize(text)
        text = self.remove_stopwords(text)
        text = self.remove_punctuation_words(text)
        text = self.lemmatizer(text)
        text = self.stemming(text)
        text = " ".join(text)
        return text

    # Extract text from PDF file
    def get_text(self, file):
        with open(file, "rb") as f:
            pdf = pdftotext.PDF(f)
        text = "\n\n".join(pdf)
        text = self.preprocess_text(text)
        return text

