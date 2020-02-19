import sys, pickle, re, os

#sys.path.append('../')
from ..core.structures import Sentence, Token, tokenize

class AbstractTagger:
    def tag(sentence):
        pass

class MLTagger(AbstractTagger):

    models_directory = os.path.join(os.path.dirname(__file__),"../preloaded/models/pos_tagging/")
    models = {'penn_crf':('penn_treebank_crf_postagger.sav','sklearn'), 'ud_crf':('ud_crf_postagger.sav','sklearn')}

    def __init__(self, model = 'penn_crf', force_ud=False):
        self.model_name = model
        self.model = TaggerWrapper(pickle.load(open(self.models_directory+self.models[model][0], 'rb')), self.models[model][1])
        self.force_ud = force_ud

    def tag(self, sentence):
        input_sentence = sentence
        if not isinstance(sentence, Sentence):
            input_sentence = Sentence(0, len(sentence), sentence)
        reformed_sentence = [token.get() for token in input_sentence.tokens[1:-1]]
        features = [self._extract_features(reformed_sentence, idx) for idx in range(len(reformed_sentence))]
        tags = self.model.predict(features)
        if self.force_ud and "ud" not in self.model_name:
            tags = [self._penn_to_ud(tag) for tag in tags]
        for token_idx in range(1, len(input_sentence.tokens)-1):
            input_sentence.tokens[token_idx].PoS = tags[token_idx-1]
        return input_sentence

    def _extract_features(self, sentence, index):
        return {
            'word':sentence[index],
            'is_first':index==0,
            'is_last':index ==len(sentence)-1,
            'is_capitalized':sentence[index][0].upper() == sentence[index][0],
            'is_all_caps': sentence[index].upper() == sentence[index],
            'is_all_lower': sentence[index].lower() == sentence[index],
            'is_alphanumeric': int(bool((re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])',sentence[index])))),
            'prefix-1':sentence[index][0],
            'prefix-2':sentence[index][:2],
            'prefix-3':sentence[index][:3],
            'prefix-3':sentence[index][:4],
            'suffix-1':sentence[index][-1],
            'suffix-2':sentence[index][-2:],
            'suffix-3':sentence[index][-3:],
            'suffix-3':sentence[index][-4:],
            'prev_word':'' if index == 0 else sentence[index-1],
            'next_word':'' if index < len(sentence) else sentence[index+1],
            'has_hyphen': '-' in sentence[index],
            'is_numeric': sentence[index].isdigit(),
            'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
            }

    def _penn_to_ud(self, tag):
        """Simple function mapping penn treebank tags to UD tags. Imply in data loss. UD is more human readable.
        Source: https://universaldependencies.org/tagset-conversion/en-penn-uposf.html
        """
        if tag in ["NN","NNS"]:
            return "NOUN"
        elif tag in ["NNP", "NNPS"]:
            return "PROPN"
        elif "JJ" in tag or tag == "AFX":
            return "ADJ"
        elif tag in ["#","$","SYM"]:
            return "SYM"
        elif tag in "\",-LRB--RRB-.:\'\'" or tag == "HYPH":
            return "PUNCT"
        elif tag == "CC":
            return "CCONJ"
        elif tag == "CD":
            return "NUM"
        elif tag in ["EX", "PRP", "WP"]:
            return "PRON"
        elif tag in ["FW","LS","NIL"]:
            return "X"
        elif tag in ["IN", "RP"]:
            return "ADP"
        elif tag in ["DT","PDT", "PRP$", "WDT","WP$"]:
            return "DET"
        elif tag in ["POS","TO"]:
            return "PART"
        elif "RB" in tag or tag == "WBR":
            return "ADV"
        elif tag == "UH":
            return "INTJ"
        elif "VB" in tag or tag == "MD":
            return "VERB"
        else:
            return "X"

class TaggerWrapper:
    types = ['sklearn','keras']
    def __init__(self, tagger, type):
        self.type = type
        self.tagger = tagger

    def predict(self, feature_list):
        if self.type == "sklearn":
            return self.tagger.predict_single(feature_list)
