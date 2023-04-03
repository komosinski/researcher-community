from abc import ABC, abstractmethod
from pathlib import Path


class Vectorizer:

    @abstractmethod
    def transform(self, corpus: list) -> list:
        raise NotImplementedError
