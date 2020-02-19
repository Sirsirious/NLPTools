import sys

sys.path.append('../')
from ..core.structures import Token

class AbstractStemmer:
    """An Interface to allow for other stemmers to be built. If you want to implement your stemmer, inherit from this class and implement the stem method."""

    def stem(self, word):
        pass

class PorterStemmer(AbstractStemmer):
    """One of the most famous implementations of stemmers. Simple and straightforward, it gets the work done.
    It is based on a measure named {m} and have 5 consecutive steps to achieve the desired output.
    Each of the steps is represented by a method.
    Class Attributes
    ----------
    consonants: str
        A string with all consonant characters (for english)
    special_case: str
        A string with 'y', the special case for english (nor vowel, nor consonant, depends o context)
    vowels: str
        A string containing all vowel characters (for english)

    """

    consonants = "bcdfghjklmnpqrstwxz"
    special_case = "y"
    vowels = "aeiou"

    def stem(self, word):
        """
        Applies stemming to a word.
        Parameters
        ----------
        word: str or Token
            The word or Token word to be lemmatized.
        """

        if isinstance(word, Token):
            word = word.get()
        stem = word.lower().strip()
        stem = self._porter_step_1(stem)
        stem = self._porter_step_2(stem)
        stem = self._porter_step_3(stem)
        stem = self._porter_step_4(stem)
        stem = self._porter_step_5(stem)
        return stem

    def _divide_into_groups(self, word):
        """
        Divides a string into groups of consonants or vowels. Outputs a list of strings with the letters grouped.
        Parameters
        ----------
        word: str
            Word to be divided into groups.
        """

        groups = []
        preceding = ""
        for idx, letter in enumerate(word.lower()):
            if preceding == "":
                preceding = letter
            else:
                if self._compare_same_class(preceding, letter):
                    preceding+= letter
                    if idx == len(word)-1:
                        groups.append(preceding)
                else:
                    groups.append(preceding)
                    preceding = letter
                    if idx == len(word)-1:
                        groups.append(letter)
        return groups

    def _compare_same_class(self, l1, l2):
        """
        Compares two letters (characters) to see if the belong to the same class (consonant or vowel). Outputs a boolean with the result of the comparison.
        Parameters
        ----------
        l1: str
            First letter.
        l2: str
            Second letter.
        """

        if l1 in self.consonants and l2 in self.consonants:
            return True
        elif l1 in self.vowels and l2 in self.vowels:
            return True
        else:
            return False
        return False

    def _determine_class(self, group):
        """
        Determines a class of a group of letters (string). Outputs either 'C' or 'V'.
        Parameters
        ----------
        group: str or list of char
            The letter group to be checked. Usually a substring derived from a word composed of all consonants or all vowels.
        """

        if group[0] in self.consonants:
            return 'C'
        return 'V'

    def _encode_word(self, word):
        """
        Takes an entire word and encodes it into a list of 'C' (consonat) and 'V' (vowel) groups.
        Parameters
        ----------
        word: str
            Word to be encoded.
        """
        encoded = self._divide_into_groups(word)
        classified = [self._determine_class(group) for group in encoded]
        return classified

    def _det_m(self, word):
        """
        Determinse the number of {m} or the number of times the grouping CV repeats in the word. If there's less than one CV between the first consonant and last vowel, the number is 0.
        Examples:
        * Tree, by: m = 0
        * Trouble, oats, trees, ivy: m = 1
        * Troubles, private, oaten: m = 2
        Parameters
        ----------
        word: str
            Word to have {m} calculated.
        """
        classes = self._encode_word(word)
        if len(classes) < 2:
            return 0
        if classes[0] == 'C':
            classes = classes[1:]
        if classes[-1] == 'V':
            classes = classes[:len(classes)-1]
        m = len(classes)//2 if (len(classes)/2) >= 1 else 0
        return m

    def _chk_LT(self, stem, lt):
        """
        Checks wheter a stem endswith one of the letters passed as parameter. Returns a boolean.
        Parameters
        ----------
        stem: str
            The stem to check the condition.
        lt: str
            A string containing the characters to be checked for last position.
        """

        for letter in lt:
            if stem.endswith(letter):
                return True
        return False

    def _chk_v(self, stem):
        """
        Checks wheter the stem contains a vowel.
        Parameters
        ----------
        stem: str
            The stem to check the condition.
        """

        for letter in stem:
            if letter in self.vowels:
                return True
        return False

    def _chk_d(self, stem):
        """
        Checks wheter the stem ends with double consonants.
        Parameters
        ----------
        stem: str
            The stem to check the condition.
        """

        if stem[-1] in self.consonants and stem[-2] in self.consonants:
            return True
        return False

    def _chk_o(self, stem):
        """
        Checks wheter the stem ends with a composition of consonant, vowel consonant, if the last consonant is not w or x or y.
        Parameters
        ----------
        stem: str
            The stem to check the condition.
        """

        if len(stem) <3:
            return False
        if (stem[-3] in self.consonants) and (stem[-2] in self.vowels) and (stem[-1] in self.consonants) and (stem[-1] not in "wxy"):
            return True
        else:
            return False

    def _porter_step_1(self, word):
        """
        First step of the algorithm. Deals with plurals and past participles.
        Parameters
        ----------
        word: str
            The word to be stemmed.
        """

        stem = word
        stepb2 = False
        #Step 1a
        if stem.endswith('sses'):
            stem = stem[:-2]
        elif stem.endswith('ies'):
            stem = stem[:-2]
        elif not stem.endswith('ss') and stem.endswith("s"):
            stem = stem[:-1]
        #Step 1b
        if len(stem) > 4:
            if stem.endswith("eed") and self._det_m(stem) > 0:
                stem = stem[:-1]
            elif stem.endswith("ed"):
                stem = stem[:-2]
                if not self._chk_v(stem):
                    stem = word
                else:
                    stepb2 = True
            elif stem.endswith("ing"):
                stem = stem[:-3]
                if not self._chk_v(stem):
                    stem = word
                else:
                    stepb2 = True
                    #Step 1b.2
        if stepb2:
            if stem.endswith("at") or stem.endswith("bl") or stem.endswith("iz"):
                stem += "e"
            elif self._chk_d(stem) and not (self._chk_LT(stem,"lsz")):
                stem = stem[:-1]
            elif self._det_m(stem)==1 and self._chk_o(stem):
                stem += "e"
        #Step 1c
        if self._chk_v(stem) and stem.endswith('y'):
            stem = stem[:-1]+'i'
        return stem

    def _porter_step_2(self, stem):
        """
        Second step of the algorithm. Removes some terminations.
        Parameters
        ----------
        stem: str
            The stem to be further stemmed.
        """

        pair_tests = [('ational','ate'), ('tional','tion'), ('enci','ence'), ('anci','ance'), ('izer', 'ize'),
                      ('abli','able'), ('alli','al'), ('entli', 'ent'), ('eli', 'e'), ('ousli', 'ous'), ('ization', 'ize'),
                      ('ation', 'ate'), ('ator', 'ate'), ('alism', 'al'), ('iveness', 'ive'), ('fulness', 'ful'),
                      ('ousness', 'ous'), ('aliti','al'), ('ivit', 'ive'), ('biliti','ble')]
        if self._det_m(stem) > 0:
            for term, subs in pair_tests:
                if stem.endswith(term):
                    return stem[:-len(term)]+subs
        return stem

    def _porter_step_3(self, stem):
        """
        Third step of the algorithm. Removes some other terminations.
        Parameters
        ----------
        stem: str
            The stem to be further stemmed.
        """

        pair_tests = [('icate','ic'),('ative',''),('alize','al'),('iciti','ic'),('ical','ic'),('ful',''),('ness','')]
        if self._det_m(stem) > 0:
            for term, subs in pair_tests:
                if stem.endswith(term):
                    return stem[:-len(term)]+subs
        return stem

    def _porter_step_4(self, stem):
        """
        Fourth step of the algorithm. Remove suffixes.
        Parameters
        ----------
        stem: str
            The stem to be further stemmed.
        """

        suffixes_1 = ['al','ance','ence','er','ic','able','ible','ant','ement','ment','ent']
        special_case = 'ion'
        suffixes_2 = ['ou','ism','ate','iti','ous','ive','ize']
        if self._det_m(stem)>1:
            for suffix in suffixes_1:
                if stem.endswith(suffix):
                    return stem[:-len(suffix)]
            if stem.endswith(special_case):
                temp = stem[:-len(special_case)]
                if self._chk_LT(temp, 'st'):
                    return temp
            for suffix in suffixes_2:
                if stem.endswith(suffix):
                    return stem[:-len(suffix)]
        return stem

    def _porter_step_5(self, stem):
        """
        The last step of the algorithm. Tides up what is left.
        Parameters
        ----------
        stem: str
            The stem to be further stemmed.
        """

        temp = stem
        #Step 5a
        if self._det_m(temp)>1 and temp.endswith('e'):
            temp = temp[:-1]
        elif self._det_m(temp) == 1 and (not self._chk_o(temp)) and temp.endswith('e') and len(temp) > 4:
            temp = temp[:-1]
        #Step 5b
        if self._det_m(temp) > 1 and self._chk_d(temp) and self._chk_LT(temp, 'l'):
            temp = temp[:-1]
        return temp
