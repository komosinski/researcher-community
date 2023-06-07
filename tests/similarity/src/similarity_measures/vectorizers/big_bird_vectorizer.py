from tests.similarity.src.similarity_measures.vectorizers.vectorizer import Vectorizer
import numpy as np
from pathlib import Path
from transformers import AutoTokenizer, BigBirdModel


class BigBirdVectorizer(Vectorizer):

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("google/bigbird-roberta-base", use_fast=False)
        self.model = BigBirdModel.from_pretrained("google/bigbird-roberta-base", use_fast=False)

    def transform(self, corpus: list) -> list:
        results = []
        for doc in corpus:
            inputs =self.tokenizer(doc, return_tensors="pt")
            outputs = self.model(**inputs)
            results.append(outputs)
        return results
