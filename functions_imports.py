import string
import random
from collections import Counter, defaultdict
import math
import json
import matplotlib.pyplot as plt
from english_bigrams import ENGLISH

# The above two imports are failing because the correct syntax should be:
# from random_string_detector.bigrams.english import ENGLISH
############################ STRUCTURE-RELATED PARAMETERS ############################

##### PERCENT UNIQUE #####
def pct_unique(s: str):
    n = len(s)
    unique_chars = len(set(s))
    return unique_chars / n
##### REPEATED SUBSTRINGS #####
def repeated_substrings(s: str):
    n = len(s)
    positions = defaultdict(list)

    # Record positions of all substrings
    for i in range(n):
        for j in range(i + 1, n + 1):
            positions[s[i:j]].append(i)

    repeated = []
    # Compute non-overlapping counts
    for substr, starts in positions.items():
        L = len(substr)
        starts.sort()
        count = 0
        last_end = -1

        for i in starts:
            if i >= last_end:
                count += 1
                last_end = i + L

        if count >= 2 and L >= 2:
            repeated.append((substr, L, count))
    
    repeated.sort(key=lambda x: (-x[1], x[0]))

    # Keep only maximal repeats
    result = []
    for substr, length, count in repeated:
        subsumed = False
        for kept_substr, kept_len, kept_count in result:
            if (
                kept_count == count and
                substr in kept_substr
            ):
                subsumed = True
                break

        if not subsumed:
            result.append((substr, length, count))

    # Sort longest first
    return result

##### PALINDROMIC BLOCKS (NO MONO-CHARACTER BLOCKS) #####
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
                yield best_left, best_right, result

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
                yield best_left, best_right, result

##### BOOKENDS #####
def maximal_bookend(text: str):
    n = len(text)
    max_k = n // 2

    for k in range(max_k, 0, -1):
        if text[:k] == text[-k:][::-1]:
            return k, text[:k], text[-k:]

    return None

##### CHARACTER BLOCKS #####
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
            yield start_index, end_index, text[start_index : end_index + 1]

        index += 1

##### VOWEL TO CONSONANT RATIO Z-SCORE #####
def vowel_ratio_rarity_z_score(s: str) -> float:
    """
    Computes the Z-score of the observed vowel count
    against the expected vowel ratio (5/26).

    Z = (V - n*p) / sqrt(n*p*(1-p))
    """
    s = s.lower()
    n = len(s)
    if n == 0:
        return 0.0

    vowels = set("aeiou")
    V = sum(1 for c in s if c in vowels)

    p = 5 / 26
    expected = n * p
    variance = n * p * (1 - p)

    if variance == 0:
        return 0.0

    return (V - expected) / math.sqrt(variance)

##### STRING ENTROPY #####
def string_entropy(s: str) -> float:
    """
    Computes Shannon entropy (bits per character)
    over the observed character distribution.
    """
    n = len(s)
    if n == 0:
        return 0.0

    counts = Counter(s)
    entropy = 0.0

    for count in counts.values():
        p = count / n
        entropy -= p * math.log2(p)

    return entropy

def entropy_avg(x):
    a = 15.89321934
    b = -0.8297682291
    c = -0.8237059174
    d = 0.01270597934
    e = -14.2437712

    entropy_mean = (
        a * x**(1/8)
        + b * x**(1/4)
        + c * x**(1/2)
        + d * x
        + e
    )
    return (entropy_mean)

def entropy_avg_std(x):
    a = -0.002459635337
    b = 0.3639055228
    c = 2.334252499
    d = 0.2123435647

    entropy_std = (
        a * x
        + b * x**(-1)
        + c * x**(-2)
        + d
    )
    return (entropy_std)

entropy_avgs = [entropy_avg(x) for x in range(1,33)]
entropy_avg_stds = [entropy_avg_std(x) for x in range(1,33)]

def entropy_rarity_z_score(s):
    e = string_entropy(s)
    rarity_z_score = (e - entropy_avg(len(s))) / entropy_avg_std(len(s))
    return e, rarity_z_score

############################ ENGLISH-RELATED PARAMETERS ############################

##### GIVE EACH LETTER A VALUE #####
letter_values = {
    'a': 1,  'b': 3,  'c': 3,  'd': 2,
    'e': 1,  'f': 4,  'g': 2,  'h': 4,
    'i': 1,  'j': 8,  'k': 5,  'l': 1,
    'm': 3,  'n': 1,  'o': 1,  'p': 3,
    'q': 10, 'r': 1,  's': 1,  't': 1,
    'u': 1,  'v': 4,  'w': 4,  'x': 8,
    'y': 4,  'z': 10
}

##### CREATE TRIE #####
class TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self):
        self.children = {}
        self.is_word = False

##### CHECK IF WORD HAS VOWELS #####
def has_vowel(word: str) -> bool:
    VOWELS = set("aeiouy")
    return any(ch in VOWELS for ch in word)

##### LOAD WORDS INTO TRIE #####
def load_dictionary_trie(path: str, min_length: int = 3) -> TrieNode:
    root = TrieNode()

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if len(word) < min_length:
                continue

            if has_vowel(word) == False:
                continue

            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]

            node.is_word = True

    return root

##### FIND ENGLISH WORDS IN STRING #####
def find_words_in_string(s: str, trie: TrieNode, min_length: int = 3):
    results = []
    n = len(s)

    for i in range(n):
        node = trie
        j = i

        while j < n:
            ch = s[j]
            if ch not in node.children:
                break

            node = node.children[ch]
            length = j - i + 1

            if node.is_word and length >= min_length:
                results.append((i, j, s[i:j + 1]))

            j += 1

    results.sort(key=lambda x: x[1]-x[0], reverse=True)
    return results

def digram_frequencies():
    freqs = {}
    with open("english_digraph_frequencies.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(" ")
            digram = parts[0]
            frequency = float(parts[1])
            freqs[digram] = frequency
    return freqs

##### SCORE RELATED PARAMETERS #####
score_rarity_percentiles = {}
with open("score_rarity_percentiles.json", "r") as f:
    score_rarity_percentiles = json.load(f)

def get_rarity_from_score(total_points, length):
    
    if total_points < float(score_rarity_percentiles[f"row{length}"][6]): # < 75th Percentile
        return "Common"
    elif total_points < float(score_rarity_percentiles[f"row{length}"][7]): # < 90th Percentile
        return "Uncommon"
    elif total_points < float(score_rarity_percentiles[f"row{length}"][8]): # < 99th Percentile
        return "Rare"
    elif total_points < float(score_rarity_percentiles[f"row{length}"][9]): # < 99.9th Percentile
        return "Epic"
    else:
        return "Legendary"