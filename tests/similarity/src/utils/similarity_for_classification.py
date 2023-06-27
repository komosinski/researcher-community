from pathlib import Path
import pandas as pd
from tests.similarity.src.similarity_measures.similarity_measure import SimilarityMeasure
from tests.similarity.src.similarity_measures.original_tfidf_similarity_measure import TfidfSimilarityMeasure
from tests.similarity.src.similarity_measures.glove_cosine_similarity_measure import GloveCosineSimilarityMeasure
from tests.similarity.src.similarity_measures.glove_euclidean_similarity_measure import GloveCosineEuclideanMeasure
#from tests.similarity.src.similarity_measures.bigbird_cosine_similarity import BigBirdCosineSimilarityMeasure
#from tests.similarity.src.similarity_measures.tinybert_cosine_similarity import TinyBertCosineSimilarityMeasure
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

class SimilarityForClassification:
    def __init__(self, dirpath: str, measure: SimilarityMeasure, title):
        self.df = pd.read_csv(Path(dirpath + 'categories.csv'))
        self.X = []
        self.y = []
        self.measure = measure
        names = self.get_names()
        files = [Path(dirpath+i) for i in names]
        measure.build_dictionary(files)
        self.process_texts(files)
        self.get_labels(files)
        self.train_svm(title)
        self.train_log_regr(title)
        self.train_svm_linear(title)
        self.labels = ['Chem' 'Med & Dent' 'Pharm'
 'Phys & Astr' 'Soc Sciences']



    def get_names(self):
        return self.df['Name'].values.tolist()

    def get_accuracy(self):
        return self.accuracy

    def process_texts(self, files):
        for f in files:
            self.X.append(self.measure.get_vector(f))

    def get_labels(self, files):
        self.y = self.df['Category'].values.tolist()

    def train_svm(self, title):
        print("SVM" + '  ' + title + '--------------------------------')
        train, test, train_labels, test_labels = train_test_split(self.X,
                                                                  self.y,
                                                                  test_size=0.2,
                                                                  random_state=42)
        clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
        le = preprocessing.LabelEncoder()
        le.fit(list(set(self.y)))
        clf.fit(train, le.transform(train_labels))
        pred = clf.predict(test)
        print(classification_report(le.transform(test_labels), pred , target_names=le.classes_))
        print("Accuracy", accuracy_score(le.transform(test_labels), pred))
        print("F1", f1_score(le.transform(test_labels), pred, average='micro'))
        cm = confusion_matrix(le.transform(test_labels), pred)
        print(le.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = ['Chem', 'Med & Dent', 'Pharm',
 'Phys & Astr', 'Soc Sci'])
        disp.plot(xticks_rotation=45)
        plt.rcParams["figure.figsize"] = (5, 4)
        plt.title(title + " SVM")
        plt.tight_layout()
        #plt.show()
        plt.savefig(Path('../../plots/' + title + '.pdf'))
        self.accuracy = accuracy_score(le.transform(test_labels), pred)
        print("------------------------------------------------------")

    def train_svm_linear(self, title):
        print("SVM" + '  ' + title + '--------------------------------')
        train, test, train_labels, test_labels = train_test_split(self.X,
                                                                  self.y,
                                                                  test_size=0.2,
                                                                  random_state=42)
        clf = make_pipeline(StandardScaler(), SVC(gamma='auto', kernel='linear'))
        le = preprocessing.LabelEncoder()
        le.fit(list(set(self.y)))
        clf.fit(train, le.transform(train_labels))
        pred = clf.predict(test)
        print(classification_report(le.transform(test_labels), pred, target_names=le.classes_))
        print("Accuracy", accuracy_score(le.transform(test_labels), pred))
        print("F1", f1_score(le.transform(test_labels), pred, average='micro'))
        cm = confusion_matrix(le.transform(test_labels), pred)
        print(le.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Chem', 'Med & Dent', 'Pharm',
                                                                           'Phys & Astr', 'Soc Sci'])
        disp.plot(xticks_rotation=45)
        plt.rcParams["figure.figsize"] = (5, 4)
        plt.title(title + " SVM")
        plt.tight_layout()
        # plt.show()
        plt.savefig(Path('../../plots/' + title + ' linear ' + '.pdf'))
        self.accuracy = accuracy_score(le.transform(test_labels), pred)
        print("------------------------------------------------------")

    def train_log_regr(self, title):
        print("Regression" + '  ' + title + '--------------------------------')
        train, test, train_labels, test_labels = train_test_split(self.X,
                                                                  self.y,
                                                                  test_size=0.2,
                                                                  random_state=42)
        clf = LogisticRegression()
        le = preprocessing.LabelEncoder()
        le.fit(list(set(self.y)))
        clf.fit(train, le.transform(train_labels))
        pred = clf.predict(test)
        print(classification_report(le.transform(test_labels), pred, target_names=le.classes_))
        print("Accuracy", accuracy_score(le.transform(test_labels), pred))
        print("F1", f1_score(le.transform(test_labels), pred, average='micro'))
        cm = confusion_matrix(le.transform(test_labels), pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Chem', 'Med & Dent', 'Pharm',
 'Phys & Astr', 'Soc Sci'])
        disp.plot(xticks_rotation=45)
        plt.rcParams["figure.figsize"] = (5, 4)
        plt.title(title + ' log_reg')
        plt.tight_layout()
        # plt.show()
        plt.savefig(Path('../../plots/' + title + '_log_reg' + '.pdf'))
        self.accuracy = accuracy_score(le.transform(test_labels), pred)
        print("------------------------------------------------------")






