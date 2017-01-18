#!/usr/bin/env python3
# Code Challenge 02 - Word Values Part II - a simple game
# http://pybit.es/codechallenge02.html

import itertools
import random
import sys
from data import DICTIONARY, LETTER_SCORES, POUCH

NUM_LETTERS = 7


# re-use from challenge 01
def calc_word_value(word):
    """Calc a given word value based on Scrabble LETTER_SCORES mapping"""
    return sum(LETTER_SCORES.get(char.upper(), 0) for char in word)


# re-use from challenge 01
def max_word_value(words):
    """Calc the max value of a collection of words"""
    return max(words, key=calc_word_value)

def draw_letters():
    """Draw NUM_LETTERS letters randomly from POUCH"""
    return random.sample(POUCH, NUM_LETTERS)

def get_user_input(draw):
    """Read the user input and validate it"""
    user_word = input("Form a valid word: ")
    if user_word.lower() not in DICTIONARY:
        print("Unknown word: {}".format(user_word))
        sys.exit(1)

    if any(x not in draw for x in user_word.upper()):
        print("Can not build {} from letters".format(user_word))
        sys.exit(1)

    return user_word

def get_possible_dict_words(draw):
    """Calculate possible words by generating all permutations from draw and
    checking if the words are in DICTIONARY"""
    return [word for word in _get_permutations_draw(draw)
            if word.lower() in DICTIONARY]

def _get_permutations_draw(draw):
    """Generate all permutations with 1 to NUM_LETTERS letters from draw"""
    return ("".join(word) for i in range(1, NUM_LETTERS + 1)
            for word in itertools.permutations(draw, i))

def main():
    """Main function"""
    # Draw letters
    cur_letters = draw_letters()
    print("Letters drawn: {}".format(str(", ".join(cur_letters))))

    # Get user input, validate and score
    user_word = get_user_input(cur_letters)
    user_score = calc_word_value(user_word)
    print("Word chosen: {} (value: {})".format(user_word.upper(), user_score))

    # Get possible words
    possible_words = get_possible_dict_words(cur_letters)

    # Get optimal word, its score and calculate score
    optimal_word = max_word_value(possible_words)
    optimal_score = calc_word_value(optimal_word)
    print("Optimal word possible: {} (value: {})".format(optimal_word,
                                                         optimal_score))
    print("You scored: {:.1f}".format(100 * user_score/optimal_score))

if __name__ == "__main__":
    main()
