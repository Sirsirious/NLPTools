import re
from spellchecker import SpellChecker

class Normalizer:

    def __init__(self):
        self.spellchecker = SpellChecker()

    def normalize_inflections(text):
        pass

    def simplify_punctuation(self, text):
        """
        This function simplifies doubled or more complex punctuation. The exception is '...'.
        """
        if text is None:
            return ''
        correction = str(text)
        correction = re.sub(r'([!?,;])\1+', r'\1', correction)
        correction = re.sub(r'\.{1,}', r'...', correction)
        return correction

    def number_to_text(text):
        pass

    def stopword_removal(text):
        pass

    def whitespace_normalization(text):
        pass

    def spell_correction(self, text):
        """
        Does very simple spell correction normalization using pyspellchecker module.
        """
        if text is None:
            return ''
        corrected = str(text)
        misspells = self.spellchecker.unknown(corrected.split())
        for word in misspells:
            if self.spellchecker.correction(word) == word:
                corrected = corrected.replace(word, self._reduce_exaggerations(word))
            else:
                corrected = corrected.replace(word, self.spellchecker.correction(word))
        return corrected

    def _reduce_exaggerations(self, text):
        correction = str(text)
        return re.sub(r'(.)\1+', r'\1', correction)
