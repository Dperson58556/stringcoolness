import random
import string
import csv
from collections import Counter, defaultdict
import math
from functools import lru_cache
import matplotlib.pyplot as plt
import statistics
import functions_imports as fi
import numpy as np

# Load Trie Once
english_trie = fi.load_dictionary_trie("dict.txt")

###########################################
############### FINAL SCORE ###############
###########################################
def generate_scored_string(length, word = None):
    ##### GENERATE RANDOM STRING #####
    random_string = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=length))
    if word:
        random_string = word

    ##### GRAB PARAMETERS #####
    words_within = fi.find_words_in_string(random_string, english_trie, min_length=3)

    repeated_1_strs = {}
    char_counts = dict(fi.Counter(random_string))
    for char in char_counts:
        repeated_1_strs[char] = char_counts[char]

    repeated_chunks = {}
    for elem in fi.repeated_substrings(random_string):
        repeated_chunks[elem[0]] = elem[2]

    palindromes = list(fi.palindromic_blocks_all(random_string))
    palindromes.sort(key=lambda x: len(x[2]), reverse = True)

    char_blocks = list(fi.character_blocks(random_string))
    char_blocks.sort(key=lambda x: len(x[2]), reverse = True)

    char_blocks_dict = {}
    for elem in char_blocks:
        if elem[2] not in char_blocks_dict:
            char_blocks_dict[elem[2]] = 1
        else:
            char_blocks_dict[elem[2]] += 1
    percent_unique = fi.pct_unique(random_string)
    vowel_ratio_rarity = fi.vowel_ratio_rarity_z_score(random_string)
    entropy, entropy_rarity = fi.entropy_rarity_z_score(random_string)
    bookend = fi.maximal_bookend(random_string)

    ##### CALCULATE POINTS #####
    letter_points = 0
    length_bonus = 0
    entropy_bonus = 0
    vowel_ratio_bonus = 0
    palindrome_bonus = 0
    bookend_bonus = 0
    words_within_bonus = 0
    repeated_chunks_bonus = 0
    char_blocks_bonus = 0
    total_points = 0

    # BONUSES
    letter_points           = sum((fi.letter_values[letter] * (repeated_1_strs[letter] if letter in repeated_1_strs else 1)) for letter in random_string)
    length_bonus            = 1 + ((length**1.25)/20)
    entropy_bonus           = 1 + 2 * abs(entropy_rarity)
    vowel_ratio_bonus       = 1 + 2 * abs(vowel_ratio_rarity)
    bookend_bonus           = bookend[0]*4 if bookend is not None else 1
    
    for palindrome in palindromes:
        palindrome_letter_bonus = 0
        for char in palindrome[2]:
            palindrome_letter_bonus += fi.letter_values[char]
        palindrome_bonus += ( (palindrome_letter_bonus) * 3 * (len(palindrome[2])**2))**(length_bonus)
    
    for word in words_within:
        for char in word[2]:
            words_within_bonus += fi.letter_values[char]*(len(word[2])**4.5)**(length_bonus)

    for block in char_blocks:
        for char in block[2]:
            char_blocks_bonus += (fi.letter_values[char]*2*(len(block[2])**3))**(length_bonus)

    for chunk in repeated_chunks:
        for char in chunk:
            repeated_chunks_bonus += fi.letter_values[char]*2*(repeated_chunks[chunk]**2)**(length_bonus)

    remaining_bonuses = (palindrome_bonus +
                        words_within_bonus +  
                        char_blocks_bonus +
                        repeated_chunks_bonus)
    
    total_points = (letter_points * 
                    length_bonus * 
                    entropy_bonus * 
                    vowel_ratio_bonus * 
                    bookend_bonus) + remaining_bonuses

    return {
        # "random_string": random_string,
        # "repeated_1_strs": repeated_1_strs,
        # "repeated_chunks": repeated_chunks,
        # "bookend": bookend,
        # "palindromes": palindromes,
        # "char_blocks": char_blocks,
        # "char_blocks_dict": char_blocks_dict,
        # "words_within": words_within,
        # "percent_unique": round(percent_unique,5),
        # "vowel_ratio_rarity": round(vowel_ratio_rarity, 5),
        # "entropy": round(entropy, 5),
        # "entropy_rarity": round(entropy_rarity, 5),
        # "letter_points": letter_points,
        # "length_bonus": round(length_bonus, 5),
        # "entropy_bonus": round(entropy_bonus, 5),
        # "vowel_ratio_bonus": round(vowel_ratio_bonus, 5),
        # "bookend_bonus": round(bookend_bonus, 5),
        # "palindrome_bonus": round(palindrome_bonus, 5),
        # "words_within_bonus": round(words_within_bonus, 5),
        # "char_blocks_bonus": round(char_blocks_bonus, 5),
        # "repeated_chunks_bonus": round(repeated_chunks_bonus, 5),
        "total_points": round(total_points)
    }


def create_histogram(data, data2=None, bins=10, title="Histogram", xlabel="Value", ylabel="Frequency", pcolor ='skyblue'):
    # Create histogram
    plt.figure(figsize=(18, 6))
    plt.hist(data, bins=bins, color=pcolor, edgecolor='black', density=False)
    #plt.hist2d(data, data2, bins=bins, cmap='Blues')
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
    score   = []

    N = 100

    for L in range(2, 33):
        for _ in range(N):
            #s = ''.join(random.choices(string.ascii_lowercase, k=L))
            #s = "bdashjajherko"
            lengths.append(L)
            score.append(generate_scored_string(L)["total_points"])

                
    plt.hist2d(
        score,
        lengths,
        bins=[100, 30],      # 100 score bins, 32 length bins
        cmap="inferno"
    )
    plt.xlabel("score(random_string)")
    plt.ylabel("string length")
    plt.colorbar(label="count")
    plt.show()

#lengths_dist_heatmap()
# N = 10000000
# for i in range(N):

#lengths_dist_heatmap()
# length = 12
# for i in range(20):
#     rs = ''.join(random.choices(string.ascii_lowercase, k=length))
#     rs_zscore = abs(vowel_z_score(rs))
#     rs_ent = string_entropy(rs)
#     print(f"{rs}: z={rs_zscore:8.4f}, e={rs_ent:7.4f}, compsite={rs_zscore / rs_ent:10.4f}")


N = 100000
L = 12
scores = []
# for _ in range(N):
#     scores.append(generate_scored_string(L)["total_points"])
print("LENGTH,MEAN,MEDIAN,25TH PERCENTILE,50TH PERCENTILE,75TH PERCENTILE,90TH PERCENTILE,99TH PERCENTILE,99.9TH PERCENTILE,99.99TH PERCENTILE")
for L in range(2, 33):
    score   = []
    for _ in range(N):
        score.append(generate_scored_string(L)["total_points"])
        # LENGTH, MEAN, MEDIAN, 25TH PERCENTILE, 50TH PERCENTILE, 75TH PERCENTILE, 90TH PERCENTILE, 99TH PERCENTILE
    print(f"{L},{statistics.mean(score)},{statistics.median(score)},{np.percentile(score, 25)},{np.percentile(score, 50)},{np.percentile(score, 75)},{np.percentile(score, 90)},{np.percentile(score, 99)},{np.percentile(score, 99.9)},{np.percentile(score, 99.99)}")
# t = 0
# while True:
#     s = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=30))
#     be = fi.maximal_bookend(s)
#     if be is not None and be[0]>=5:
        
#     t += 1

# t = 0
# N= 1000
# million_trials_bookends = []
# for i in range(N):
#     s = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=16))
#     be = fi.palindromic_blocks_all(s)
#     if be is not None:
#         million_trials_bookends.append(len(be[2]))
#     else:
#         million_trials_bookends.append(0)


#create_histogram(scores, bins=500, title="Score Distribution", xlabel="Score", ylabel="Frequency")
