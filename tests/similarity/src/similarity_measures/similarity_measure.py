from abc import ABC, abstractmethod
from pathlib import Path
from tests.similarity.src.utils.pdf_to_text_transformer import PdfToTextTransformer
from tests.similarity.src.utils.spell_corrector import SpellCorrector


class SimilarityMeasure:

    def __init__(self, use_spell_corrector=False):
        self.dictionary = None
        self.model = None
        self.text_extractor = PdfToTextTransformer()
        if use_spell_corrector:
            self.spell_corrector = SpellCorrector()
        else:
            self.spell_corrector = None
    @abstractmethod
    def get_similarity(self, file_1: Path, file_2: Path) -> float:
        raise NotImplementedError
        