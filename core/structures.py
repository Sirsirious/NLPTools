import sys, re

DEFAULT_SENTENCE_BOUNDARIES = [r'(?<=[0-9]|[^0-9.])(\.)(?=[^0-9.]|[^0-9.]|[\s]|$)',r'\.{2,}',r'\!+',r'\:+',r'\?+']
DEFAULT_PUNCTUATIONS = [r'(?<=[0-9]|[^0-9.])(\.)(?=[^0-9.]|[^0-9.]|[\s]|$)',
                        r'\.{2,}',r'\!+',r'\:+',r'\?+',r'\,+',r'\(|\)|\[|\]|\{|\}|\<|\>']

class Document:
    """
    The Document is the main structure of our NLP process. It wraps the document being treated. A Document is composed of sentences and is iterable.
    Attributes
    ----------
    raw : str
        The raw text string passed as input to be sentencized.
    sentences : list of Sentence
        The list of sentences after sentencizing.

    """

    def __init__(self, document_text):
        """
        Parameters
        ----------
        document_text : str
            Text to be sentencized. Initialization immediately sentencizes the input text based on the input parameters. The sentences are also immediately tokenized.
        """

        self.raw = document_text
        self.sentences = sentencize(self.raw)
        self._index = 0

    def __getitem__(self, key):
        return self.sentences[key]

    def __repr__(self):
        return self.raw

    def __str__(self):
        return self.raw

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.sentences):
            result = self.sentences[self._index]
            self._index+=1
            return result
        raise StopIteration

    def __len__(self):
        return len(self.sentences)

class Sentence:
    """
    Sentences are divisions of a Document. They are usually separated by punctuations. Sentences are divided into tokens. One can iterate over sentence tokens.
    Attributes
    ----------
    start_pos: int
        The starting position of the sentence in the raw Document.
    end_pos: int
        The ending position of the sentence in the raw Document. Includes punctuation position.
    previous_sentence: Sentence or None
        A pointer to the previous Sentence in a linked list manner. Prepared for future navigation.
    next_sentence: Sentence or None
        A pointer to the next Sentence in a linked list manner. Prepared for future navigation.
    tokens : list of Token
        The list of Tokens after tokenizing.

    Methods
    -------
    get: str
        Returns the string representation of the Sentence.

    """

    def __init__(self, start_position, end_position, raw_document_reference):
        """
        Parameters
        ----------
        start_position : int
            The starting position of the sentence in the raw Document.
        end_position : int
            The ending position of the sentence in the raw Document. Includes punctuation position.
        raw_document_reference: string
            The raw document string where the sentence is localized.
        """

        self.start_pos = int(start_position)
        self.end_pos = int(end_position)
        self._document_string = raw_document_reference
        self.next_sentence = None
        self.previous_sentence = None
        self.tokens = tokenize(self._document_string[self.start_pos:self.end_pos])
        self._index = 0

    def get(self):
        return self._document_string[self.start_pos:self.end_pos]

    def __getitem__(self, key):
        return self.tokens[key]

    def __repr__(self):
        return self.get()

    def __str__(self):
        return self.get()

    def __eq__(self, other):
        return self.get() == other

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.tokens):
            result = self.tokens[self._index]
            self._index+=1
            return result
        raise StopIteration

    def __len__(self):
        return len(self.tokens)

class Token:
    """
    Tokens are divisions of a Sentence. They are usually separated by whitespaces. Punctuations are also tokens.
    Attributes
    ----------
    start_pos: int
        The starting position of the Token in the Sentence.
    end_pos: int
        The ending position of the Token in the Sentence.
    previous_token: Token or None
        A pointer to the previous Token in a linked list manner. Prepared for future navigation. First Token in a sentence is always SOS - acronym for Start of Sentence.
    next_token: Token or None
        A pointer to the next Token in a linked list manner. Prepared for future navigation. Last Token in a sentence is always EOS - acronym for End of Sentence.
    SOS: boolean
        Is the Token the start of a Sentence?
    EOS: boolean
        Is the Token the end of a Sentence?
    PoS: string or None
        The token predicted Part of Speech.
    Methods
    -------
    get: str
        Returns the string representation of the Token.
    """

    def __init__(self, start_position, end_position, raw_sentence_reference, SOS = False, EOS = False):
        """
        Parameters
        ----------
        start_position : int
            The starting position of the Token in the Sentence.
        end_position : int
            The ending position of the Token in the Sentence.
        raw_sentence_reference: str
            The Sentence string where the token is localized. It may be a substring of a raw Document representation.
        SOS: boolean, optional
            Creates a Start of Sentence Token. This influence Token representation and printing.
        EOS: boolean, optional
            Creates a End of Sentence Token. This influence Token representation and printing.
        """

        self.start_pos = int(start_position)
        self.end_pos = int(end_position)
        self._sentence_string = raw_sentence_reference
        self.next_token = None
        self.previous_token = None
        self.SOS = SOS
        self.EOS = EOS
        self.PoS = None
        self.raw = self._sentence_string[self.start_pos:self.end_pos]
        self.repr = self.raw

    def get(self):
        if self.SOS:
            return '<SOS>'
        elif self.EOS:
            return '<EOS>'
        else:
            return self.repr

    def __repr__(self):
        return self.get()

    def __str__(self):
        return self.get()

    def __eq__(self, other):
        return self.get() == other

## Static Functions

def sentencize(raw_input_document, sentence_boundaries = DEFAULT_SENTENCE_BOUNDARIES, delimiter_token='<SPLIT>'):
    """
    Sentencizes a string based on sentence boundaries. Returns a list of Sentences.

    Parameters
    ----------
    raw_input_document: str
        The raw input document in a string format.
    sentence_boundaries: list of str, optional
        A list of regex used to delimit sentence boundaries. Default regex includes correct period splitting, reticences, exclamation mark, question mark and colons.
        The default can be accessed by the global variable DEFAULT_SENTENCE_BOUNDARIES.
    delimiter_token: str, optional
        The token used for document segmentation. Usually a "agnostic" token. Defaults to <SPLIT>.
    """
    working_document = raw_input_document
    punctuation_patterns = sentence_boundaries
    for punct in punctuation_patterns:
        working_document = re.sub(punct, r'\g<0>'+delimiter_token, working_document, flags=re.UNICODE)
    list_of_string_sentences = [x.strip() for x in working_document.split(delimiter_token) if x.strip() != ""]
    list_of_sentences = []
    previous = None
    for sent in list_of_string_sentences:
        start_pos = raw_input_document.find(sent)
        end_pos = start_pos+len(sent)
        new_sentence = Sentence(start_pos, end_pos, raw_input_document)
        list_of_sentences.append(new_sentence)
        if previous == None:
            previous = new_sentence
        else:
            previous.next_sentence = new_sentence
            new_sentence.previous_sentence = previous
            previous = new_sentence
    return list_of_sentences

def tokenize(raw_input_sentence, join_split_text = True, split_text_char = r'\-',
             punctuation_patterns= DEFAULT_PUNCTUATIONS, split_characters = r'\s|\t|\n|\r', delimiter_token='<SPLIT>'):
    """
    Tokenizes a string based on token boundaries. Returns a list of Tokens.

    Parameters
    ----------
    raw_input_sentence: str
        The raw input Sentence in a string format.
    join_split_text: boolean, optional
        Wheter to try to join multi-line text splits, like in the case of "sen-\ntence". Defaults to True.
    split_text_char: str, optional
        The split char used for checking and joining split strings. Defaults to hyphen.
    punctuation_patterns: list of str, optional
        A list of regex used to turn punctuations into tokens. Aside from sentence boundaries, also includes commas and parenthesis.
        The default can be accessed by the global variable DEFAULT_PUNCTUATIONS.
    split_characters: str, optional
        A string with regex for split characters. These are used to do tokenization after the sentence is preprocessed.
        Defaults to any whitespace (\s), any tab char (\t), newlines (\n) and carriage returns (\r).
    delimiter_token: str, optional
        The token used for sentence segmentation. Usually a 'agnostic' token. Defaults to <SPLIT>.
    """

    working_sentence = raw_input_sentence
    #First deal with possible word splits:
    if join_split_text:
        working_sentence = re.sub(r'[a-z]+('+split_text_char+r'[\n])[a-z]+','', working_sentence)
    #Escape punctuation
    for punct in punctuation_patterns:
        working_sentence = re.sub(punct, r" \g<0> ", working_sentence)
    #Split at any split_characters
    working_sentence = re.sub(split_characters, delimiter_token, working_sentence)
    list_of_token_strings = [x.strip() for x in working_sentence.split(delimiter_token) if x.strip() !=""]
    previous = Token(0,0,raw_input_sentence, SOS=True)
    list_of_tokens = [previous]
    for token in list_of_token_strings:
        start_pos = raw_input_sentence.find(token)
        end_pos = start_pos+len(token)
        new_token = Token(start_pos,end_pos,raw_input_sentence)
        list_of_tokens.append(new_token)
        previous.next_token=new_token
        new_token.previous_token=previous
        previous=new_token
    if previous.SOS != True:
        eos = Token(len(raw_input_sentence), len(raw_input_sentence), raw_input_sentence, EOS=True)
        previous.next_token=eos
        eos.previous_token = previous
        list_of_tokens.append(eos)
    return list_of_tokens
