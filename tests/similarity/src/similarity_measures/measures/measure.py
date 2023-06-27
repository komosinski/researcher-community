from abc import ABC, abstractmethod
from pathlib import Path


class Measure:
    @abstractmethod
    def get(self, vec1: list, vec2: list) -> float:
        raise NotImplementedError

