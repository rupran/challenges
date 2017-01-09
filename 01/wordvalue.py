from data import DICTIONARY, LETTER_SCORES

def load_words():
    with open(DICTIONARY, "r") as infile:
        return [x.strip() for x in infile]

def calc_word_value(word):
    """Calculate the value of the word entered into function
    using imported constant mapping LETTER_SCORES"""
    return sum(LETTER_SCORES[c.upper()] for c in word if c.upper() in LETTER_SCORES)

def max_word_value(in_list=load_words()):
    """Calculate the word with the max value, can receive a list
    of words as arg, if none provided uses default DICTIONARY"""
    return max(((word, calc_word_value(word)) for word in in_list), key=lambda x: x[1])[0]

if __name__ == "__main__":
    pass # run unittests to validate
