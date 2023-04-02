from autocorrect import Speller

class SpellCorrector:
    def __init__(self):
        self.spell = Speller('en', fast=True)

    def correct(self, word):
        return self.spell(word)


