import pickle, os

from nlptools.utils.word_utils import inflect_noun_singular

class AbstractLemmatizer:
    def lemmatize():
        pass

class DictionaryLemmatizer(AbstractLemmatizer):

    dict_directory = os.path.join(os.path.dirname(__file__), "../preloaded/dictionaries/lemmas/word_lemma_dict.p")

    def __init__(self):
        self.lemma_dict = pickle.load(open(self.dict_directory,'rb'))

    def lemmatize(self, word, pos, lemmatize_plurals=True):
        if word is None:
            return ''
        if pos is None:
            pos = ''
        word = str(word).lower()
        pos = str(pos).upper()
        if word in self.lemma_dict:
            if pos in self.lemma_dict[word]:
                return self.lemma_dict[word][pos]
        if pos == "NOUN" and lemmatize_plurals:
            return inflect_noun_singular(word)
        return word
