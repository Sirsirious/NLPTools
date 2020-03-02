import pickle, os

dict_directory = os.path.join(os.path.dirname(__file__),"../preloaded/dictionaries/lemmas/irregular_noun_dict.p")

def inflect_noun_singular(word):
    irregular_dict = pickle.load(open(dict_directory,'rb'))
    consonants = "bcdfghjklmnpqrstwxyz"
    vowels = "aeiou"
    word = str(word).lower()
    if len(word) < 2:
        return word
    if word in irregular_dict:
        return irregular_dict[word]
    if word.endswith('s'):
        if len(word) > 3:
            #Leaves, wives, thieves
            if word.endswith('ves'):
                if len(word[:-3]) > 2:
                    return word.replace('ves','f')
                else:
                    return word.replace('ves','fe')
            #Parties, stories
            if word.endswith('ies'):
                return word.replace('ies','y')
            #Tomatoes, echoes
            if word.endswith('es'):
                if word.endswith('ses') and word[-4] in vowels:
                    return word[:-1]
                if word.endswith('zzes'):
                    return word.replace('zzes','z')
                return word[:-2]
            if word.endswith('ys'):
                return word.replace('ys','y')
            return word[:-1]
    return word
