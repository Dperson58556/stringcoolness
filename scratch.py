import random
import string
import csv
from collections import Counter, defaultdict
import math
from functools import lru_cache
import matplotlib.pyplot as plt
import statistics

# def prob(length, rep_threshold, trials) -> float:
#     if rep_threshold > length:
#         return 0.0
#     if rep_threshold == 1:
#         return 1.0

#     hit = 0

#     for t in range(trials):

#         random_string = ''.join(random.choices(alphabet, k=length))
#         mc = Counter(random_string).most_common(1)[0]
#         if mc[1] >= rep_threshold:
#             hit += 1
#             print(f"{random_string}, {mc}")

#     print(f"hits: {hit} / {trials}")
#     return (hit / trials)

# alphabet = string.ascii_lowercase
# LENGTH = 16
# REP_THRESHOLD = 7
# trials = 100000
# OUTPUT_FILE = "at_least_x_repeats_simulated.csv"

# print(f"LENGTH={LENGTH},>=1 repetitions of count {REP_THRESHOLD},trials={trials},{prob(LENGTH, REP_THRESHOLD, trials):.10f}")

# with open(OUTPUT_FILE, "w", newline="") as f:
#     writer = csv.writer(f)

#     header = ["x \\ y"] + list(range(1, LENGTH + 1))
#     writer.writerow(header)


#     for strlen in range(1, LENGTH + 1):
#         row = [strlen]
#         for repcount in range(1, REP_THRESHOLD + 1):
#             row.append(f"{prob(strlen, repcount, trials):.10f}")
#         writer.writerow(row)

# for strlen in range(1, LENGTH + 1):
#     for repcount in range(1, REP_THRESHOLD + 1):
#         print(f"{strlen},{repcount},{prob(strlen, repcount, trials):.10f}")

# def xprob(length, rep) -> float:

#     alphsize = 26
#     if rep > length:
#         return 0.0
#     if rep == 1 :
#         return 1.0

#     valid = (alphsize ** (length-rep+1))
#     total = (alphsize ** length)
#     return valid / total

# def count_strings_at_least_r_repeats(n: int, r: int, k: int) -> int:
#     """
#     Returns the number of length-n strings over an alphabet of size k
#     in which at least one character appears r or more times.
#     """
#     if r > n:
#         return 0.0

#     total = k ** n

#     @lru_cache(None)
#     def count_distributions(letters_left, slots_left):
#         """
#         Counts all ways to assign counts < r to `letters_left` letters
#         summing to `slots_left`, weighted by multinomial contributions.
#         """
#         if letters_left == 0:
#             return 1 if slots_left == 0 else 0
#         if slots_left < 0:
#             return 0

#         result = 0
#         for c in range(min(r, slots_left + 1)):
#             result += count_distributions(
#                 letters_left - 1,
#                 slots_left - c
#             ) / factorial(c)

#         return result

#     complement = factorial(n) * count_distributions(k, n)

#     return (total - int(round(complement))) / total

# for len in range(27, 65):
#     print(f"{count_strings_at_least_r_repeats(len, 12, 26):.15f}")


# def maximal_nonoverlapping_repeated_substrings(s: str):
#     n = len(s)
#     positions = defaultdict(list)
#     char_counts = Counter(s).most_common()

#     # Record positions of all substrings
#     for i in range(n):
#         for j in range(i + 1, n + 1):
#             positions[s[i:j]].append(i)

#     repeated = []
#     # Compute non-overlapping counts
#     for substr, starts in positions.items():
#         L = len(substr)
#         starts.sort()
#         count = 0
#         last_end = -1

#         for i in starts:
#             if i >= last_end:
#                 count += 1
#                 last_end = i + L

#         if count >= 2 and L >= 2:
#             repeated.append((substr, L, count))

#     # specially consider repeated 1-strings (chars)
#     for elem in char_counts:
#         if elem[1]==1:
#             break
#         else:
#             repeated.append((elem[0], 1, elem[1]))
#     # Sort longest first
#     repeated.sort(key=lambda x: (-x[1], x[0]))

#     # Keep only maximal repeats
#     result = []
#     for substr, length, count in repeated:
#         subsumed = False
#         for kept_substr, kept_len, kept_count in result:
#             if (
#                 kept_count == count and
#                 substr in kept_substr
#             ):
#                 subsumed = True
#                 break

#         if not subsumed:
#             result.append((substr, length, count))

#     return result

# debug = 0
# for i in range(100):
#     rs = ''.join(random.choices(string.ascii_lowercase, k=32))
#     #rs = 'abcdefooooghij'
#     list_of_repeats = maximal_nonoverlapping_repeated_substrings(rs)[1:]
#     pruned_repeats = [r for r in list_of_repeats if r[1]>=2]

#     if pruned_repeats:
#         print(f"{rs} -> {pruned_repeats}")
#     if debug==True:
#         break

def generate_scored_string(length):
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))

    crs = Counter(random_string).most_common()

    repeated_chars = []
    rawpoints = 0

    for char, count in crs:
        if count == 1:
            break
        repeated_chars.append({"char": char, "count": count})
        rawpoints += count ** 4

    # block bonus logic
    blockbonus = 1
    accrue = 0
    for i in range(1, length):
        if random_string[i] == random_string[i - 1]:
            accrue += 1
        else:
            accrue = 0
        blockbonus += accrue / length

    counthits = sum(rc["count"] for rc in repeated_chars)
    percent_unique = (length - counthits) / length

    bellcurve = abs(percent_unique - 0.5)
    points = (rawpoints ** (1 + bellcurve)) ** blockbonus if rawpoints > 0 else 0

    return {
        "string": random_string,
        "repeated_chars": repeated_chars,
        "percent_unique": percent_unique,
        "rawpoints": rawpoints,
        "blockbonus": blockbonus,
        "bellcurve": bellcurve,
        "points": points
    }

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
    pct_unique = []

    N = 100000

    for L in range(2, 33):
        for _ in range(N):
            s = rs = ''.join(random.choices(string.ascii_lowercase, k=L))
            lengths.append(L)
            pct_unique.append(percent_unique(s))

    plt.hist2d(
        pct_unique,
        lengths,
        bins=[200, 31],      # 100 score bins, 32 length bins
        cmap="inferno"
    )
    plt.xlabel("score(random_string)")
    plt.ylabel("string length")
    plt.colorbar(label="count")
    plt.show()

##### REPEATED SUBSTRINGS #####
def repeated_substrings(s: str):
    n = len(s)
    positions = defaultdict(list)
    char_counts = Counter(s).most_common()

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

    # specially consider repeated 1-strings (chars)
    for elem in char_counts:
        if elem[1]==1:
            break
        else:
            repeated.append((elem[0], 1, elem[1]))
    # Sort longest first
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

    return result

#print(repeated_substrings("abcccccccccccccccccccc"))

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