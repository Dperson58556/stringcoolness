import random
import string
import csv
from collections import Counter, defaultdict
import math
from functools import lru_cache
import matplotlib.pyplot as plt
import statistics





##### ENTROPY #####
def string_entropy(s: str) -> float:
    """
    Computes Shannon entropy (bits per character)
    over the observed character distribution.
    """
    n = len(s)                          # length of the string
    if n == 0:                          # avoid division by zero
        return 0.0

    counts = Counter(s)                 # frequency of each character
    entropy = 0.0                       # initialize entropy  

    for count in counts.values():       # calculate entropy
        p = count / n                   # probability of character
        entropy -= p * math.log2(p)     # entropy formula

    return entropy

##### VOWEL DISTRIBUTION Z SCORE #####
def vowel_z_score(s: str) -> float:

    s = s.lower()                           # normalize to lowercase
    n = len(s)                              # length of the string       
    if n == 0:                              # avoid division by zero
        return 0.0

    vowels = set("aeiou")                   # define vowels
    V = sum(1 for c in s if c in vowels)    # count vowels

    p = 5 / 26                              # expected vowel frequency
    expected = n * p                        # expected vowel count 
    variance = n * p * (1 - p)              # variance of vowel count

    if variance == 0:                       # avoid division by zero
        return 0.0

    return (V - expected) / math.sqrt(variance) # z-score formula

##### PALINDROMIC BLOCKS #####
def palindromic_blocks_all(text: str):
    text_length = len(text)

    # ---- Odd-length palindromes ----
    for center_index in range(text_length):
        expansion_radius = 1
        best_left = None
        best_right = None

        while (
            center_index - expansion_radius >= 0 and
            center_index + expansion_radius < text_length and
            text[center_index - expansion_radius] ==
            text[center_index + expansion_radius]
        ):
            best_left = center_index - expansion_radius
            best_right = center_index + expansion_radius
            expansion_radius += 1

        if best_left is not None:
            result = text[best_left : best_right + 1]
            if len(set(result)) > 1:
                yield result

    # ---- Even-length palindromes ----
    for left_center in range(text_length - 1):
        expansion_radius = 0
        best_left = None
        best_right = None

        while (
            left_center - expansion_radius >= 0 and
            left_center + expansion_radius + 1 < text_length and
            text[left_center - expansion_radius] ==
            text[left_center + expansion_radius + 1]
        ):
            best_left = left_center - expansion_radius
            best_right = left_center + expansion_radius + 1
            expansion_radius += 1

        if best_left is not None:
            result = text[best_left : best_right + 1]
            if len(set(result)) > 1:
                yield result


def character_blocks(text: str):
    text_length = len(text)
    index = 0

    while index < text_length:
        start_index = index
        current_char = text[index]

        while index + 1 < text_length and text[index + 1] == current_char:
            index += 1

        end_index = index
        block_length = end_index - start_index + 1

        if block_length > 1:
            yield text[start_index : end_index + 1]

        index += 1


if __name__ == "__main__":

    test_strings = [
    "abcdefghijklmnopqrstuvwxyz",
    "aaaaaaaaaaaaaaaaaaaaaaaaaa",
    "zzzzzzzzzzzzzzzzzzzzzzzzzz",
    "zyxwvutsrqponmlkjihgfedcab",
    "ababababababababababababab",
    "abcabcabcabcabcabcabcabcab",
    "aaaaaaaaaaaaabbbbbbbbbbbbb",
    "pqowkjldsanfbhajsdlknajfnh"
    ]

    debug = False
    #for _ in range(100 if debug == False else 1):
    count = 0
    while True:
        rs = ''.join(random.choices(string.ascii_lowercase, k=32)) if debug == False else "abccdefgcc"
        blocks = list(character_blocks(rs))

        maxlen = max([len(b) for b in blocks]) if len(blocks) > 0 else 0
        if maxlen >= 7:
            print(f"{count} {rs}: {blocks}")
        count += 1
        #print(f"{rs}: {list(palindromic_blocks_all(rs))}")
    # test_string = test_strings[1]
    # print(f"String: {test_string}")
    # print(f"Entropy: {string_entropy(test_string)} bits/char")
    # print(f"Vowel Z-Score: {vowel_z_score(test_string)}")