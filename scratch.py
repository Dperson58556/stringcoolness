import random
import string
import csv
from collections import Counter, defaultdict
import math
from functools import lru_cache
import matplotlib.pyplot as plt
import statistics
import functions_imports as fi

english_trie = fi.load_dictionary_trie("dict.txt")

def generate_scored_string(length):
    ##### GENERATE RANDOM STRING #####
    random_string = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=length))

    ##### GRAB PARAMETERS #####
    words_within = fi.find_words_in_string(random_string, english_trie, min_length=3)

    repeated_substrings_list = fi.repeated_substrings(random_string)
    repeated_1_strs = list(filter(lambda item: item[1] == 1, repeated_substrings_list))
    repeated_2_plus_strs = list(filter(lambda item: item[1] > 1, repeated_substrings_list)) 

    palindromes = list(fi.palindromic_blocks_all(random_string))
    char_blocks = list(fi.character_blocks(random_string))
    percent_unique = fi.pct_unique(random_string)
    z_score = fi.vowel_z_score(random_string)
    entropy = fi.string_entropy(random_string)
    bookend = fi.maximal_bookend(random_string)

    ##### CALCULATE POINTS #####
    letter_points = 0
    length_bonus = 0
    entropy_bonus = 0
    total_points = 0

    # BONUSES
    for letter in random_string:
        letter_points += (fi.letter_values[letter] * ()
    #letter_points += (fi.letter_values[letter] for letter in random_string)
    length_bonus = 1 + ((length**1.25)/20)
    
    total_points = letter_points * length_bonus

    return round(total_points)
    # return {
    #     "random_string": random_string,
    #     "repeated_1_strs": repeated_1_strs,
    #     "repeated_2_plus_strs": repeated_2_plus_strs,
    #     "bookend": bookend,
    #     "palindromes": palindromes,
    #     "char_blocks": char_blocks,
    #     "words_within": words_within,
    #     "percent_unique": round(percent_unique,5),
    #     "z_score": round(z_score, 5),
    #     "entropy": round(entropy, 5),
    #     "total_points": round(total_points)
    # }

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

import math

def vowel_z_score(s: str) -> float:
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


def create_histogram(data, data2, bins=10, title="Histogram", xlabel="Value", ylabel="Frequency", pcolor ='skyblue'):
    # Create histogram
    plt.figure(figsize=(18, 6))
    #plt.hist(data, bins=bins, color=pcolor, edgecolor='black', density=True)
    plt.hist2d(data, data2, bins=bins, cmap='Blues')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

test_strings = [
    "abcdefghijklmnopqrstuvwxyz",
    "aaaaaaaaaaaaaaaaaaaaaaaaaa",
    "zzzzzzzzzzzzzzzzzzzzzzzzzz",
    "zyxwvutsrqponmlkjihgfedcab",
    "ababababababababababababab",
    "abcabcabcabcabcabcabcabcab",
    "aaaaaaaaaaaaabbbbbbbbbbbbb",
    "pqowkjldsanfbhajsdlknajfnh"]

# while True:
#     rs = ''.join(random.choices(string.ascii_lowercase, k=length))
#     rs_ent = string_entropy(rs)
#     if rs_ent <= 2.10:
#         print(f"{rs}: {rs_ent:.4f} bits/char")
# print()
# for item in test_strings:
#     z= vowel_z_score(item)
#     ent = string_entropy(item)
#     comp = z / ent if ent != 0 else 0.0
#     print(f"{item}: {z:8.4f}, {ent:8.4f}, {comp:8.4f}")
# print()

# with open("100k_sample.txt", "w") as f:
#     alllines =  []
#     for _ in range(100000):
#         s = ''.join(random.choices(string.ascii_lowercase, k=16))
#         alllines.append((s,  vowel_z_score(s), string_entropy(s)))

#     sortedz  = sorted(alllines, key=lambda x: x[1])

#     for elem in sortedz:
#         f.write(f"{elem[0]}, {elem[1]}, {elem[2]}\n")

# with open("100k_sample.txt", "r") as f:
#     lines = f.readlines()
#     vowel_zscores = []
#     entropies = []
#     for line in lines:
#         parts = line.strip().split(", ")
#         s = parts[0]
#         vowel_zscores.append(float(parts[1]))
#         entropies.append(float(parts[2]))

#     for i in range(10):
#         print(f"{vowel_zscores[i*1000]:.6f}, {entropies[i*1000]:.6f}, {vowel_zscores[i*1000] / entropies[i*1000]:.6f}")

# for _ in range(10):

def percent_unique(s):
    n = len(s)
    unique_chars = len(set(s))
    return unique_chars / n


def lengths_dist_heatmap():
    lengths = []
    score = []

    N = 1000

    for L in range(2, 33):
        for _ in range(N):
            s = rs = ''.join(random.choices(string.ascii_lowercase, k=L))
            lengths.append(L)
            score.append(score(s))

    plt.hist2d(
        score,
        lengths,
        bins=[200, 31],      # 100 score bins, 32 length bins
        cmap="inferno"
    )
    plt.xlabel("score(random_string)")
    plt.ylabel("string length")
    plt.colorbar(label="count")
    plt.show()

#lengths_dist_heatmap()
# length = 12
# for i in range(20):
#     rs = ''.join(random.choices(string.ascii_lowercase, k=length))
#     rs_zscore = abs(vowel_z_score(rs))
#     rs_ent = string_entropy(rs)
#     print(f"{rs}: z={rs_zscore:8.4f}, e={rs_ent:7.4f}, compsite={rs_zscore / rs_ent:10.4f}")

# million_trials_vowel_zscores = []
# million_trials_entropies = []
# for i in range(1000000):
#     rs = ''.join(random.choices(string.ascii_lowercase, k=length))
#     rs_zscore = vowel_z_score(rs)
#     million_trials_vowel_zscores.append(rs_zscore)
#     rs_ent = string_entropy(rs)
#     million_trials_entropies.append(rs_ent)


# create_histogram(million_trials_vowel_zscores, bins=50, title="Vowel Z-Scores Distribution", xlabel="Vowel Z-Score", ylabel="Frequency")
# create_histogram(million_trials_entropies, bins=250, title="Entropy Distribution", xlabel="Vowel Z-Score", ylabel="Frequency", pcolor='red')
# test = ""
# for i in range(32):
#     test += 'a'
#     print(f"{vowel_z_score(test):.6f}, {test}")