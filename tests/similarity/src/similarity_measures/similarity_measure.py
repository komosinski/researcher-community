from abc import ABC, abstractmethod
from pathlib import Path


class SimilarityMeasure:

    @abstractmethod
    def get_similarity(self, file_1: Path, file_2: Path) -> float:
        raise NotImplementedError
        