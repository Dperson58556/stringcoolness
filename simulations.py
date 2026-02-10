import random
import string
import json
import csv
import heapq
from collections import Counter, defaultdict
import math
from functools import lru_cache
import matplotlib.pyplot as plt
import statistics
import functions_imports as fi
import numpy as np
from multiprocessing import Pool, cpu_count
import signal
from itertools import count, product
import os


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

# Load Trie Once
english_trie = fi.load_dictionary_trie("dict.txt")

###########################################
############### FINAL SCORE ###############
###########################################
def generate_scored_string(length, word = None, debug = False):
    ##### GENERATE RANDOM STRING #####
    random_string = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=length))
    if word:
        random_string = word

    #### GRAB PARAMETERS #####
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
    vowel_ratio = fi.vowel_ratio(random_string)
    vowel_ratio_rarity = fi.vowel_ratio_rarity_z_score(random_string)
    entropy, entropy_rarity = fi.entropy_rarity_z_score(random_string)
    entropy = fi.string_entropy(random_string)
    bookend = fi.maximal_bookend(random_string)

    #### CALCULATE POINTS #####
    letter_points = 0
    length_bonus = 0
    entropy_bonus = 0
    vowel_ratio_bonus = 0
    palindrome_bonus = 0
    bookend_bonus = 0
    words_within_bonus = 0
    repeated_chunks_bonus = 0
    char_blocks_bonus = 0
    bigram_bonus = 0 ##################### NOT IMPLEMENTED YET #####################
    total_points = 0

    # BONUSES
    letter_points           = sum((2 * fi.letter_values[letter] * (repeated_1_strs[letter] if letter in repeated_1_strs else 1)) for letter in random_string)
    length_bonus            = 1 + ((length**1.25)/20)
    entropy_bonus           = 1 + 3.2 * abs(entropy_rarity)
    vowel_ratio_bonus       = 1 + 3 * abs(vowel_ratio_rarity)
    bookend_bonus           = bookend[0]*3.5 if bookend is not None else 1
    bigram_bonus            = 1 + ( sum(fi.ENGLISH.get(random_string[i:i+2], 0) for i in range(len(random_string)-1)) / 350)##################### NOT IMPLEMENTED YET #####################
    
    for palindrome in palindromes:
        palindrome_letter_bonus = 0
        for char in palindrome[2]:
            palindrome_letter_bonus += fi.letter_values[char]
        palindrome_bonus += ( (palindrome_letter_bonus) * 4 * (len(palindrome[2])**3))
    
    for word in words_within:
        for char in word[2]:
            words_within_bonus += fi.letter_values[char]*(len(word[2])**5)

    for block in char_blocks:
        for char in block[2]:
            char_blocks_bonus += ((2 * fi.letter_values[char])**1.4) * ((len(block[2]))**4)

    for chunk in repeated_chunks:
        for char in chunk:
            repeated_chunks_bonus += ((2 * fi.letter_values[char])**1.2)*3*(repeated_chunks[chunk]**5)

    basic_bonuses = (letter_points * 
                    length_bonus * 
                    entropy_bonus * 
                    vowel_ratio_bonus * 
                    bookend_bonus)
    
    remaining_bonuses = (palindrome_bonus +
                        words_within_bonus +  
                        char_blocks_bonus +
                        repeated_chunks_bonus)*length_bonus * bigram_bonus
    
    sub_total_points = basic_bonuses + remaining_bonuses
    
    total_points = (sub_total_points ** (1.2)) / fi.RARITY_SCALAR

    # card_rarity = fi.get_component_rarity("total_points", total_points, length)
    
    
    # letter_points_bar_percent = min(100.0, fi.get_component_rarity_bar_percent("letter_points", letter_points, length) * 100)
    # words_within_bonus_bar_percent = min(100.0, fi.get_component_rarity_bar_percent("words_within_bonus", words_within_bonus, length) * 100)
    # palindrome_bonus_bar_percent = min(100.0, fi.get_component_rarity_bar_percent("palindrome_bonus", palindrome_bonus, length) * 100)
    # char_blocks_bonus_bar_percent = min(100.0, fi.get_component_rarity_bar_percent("char_blocks_bonus", char_blocks_bonus, length) * 100)
    # repeated_chunks_bonus_bar_percent = min(100.0, fi.get_component_rarity_bar_percent("repeated_chunks_bonus", repeated_chunks_bonus, length) * 100)

    
    # entropy_bar_percent = min(100.0, fi.get_component_rarity_bar_percent("entropy_rarity", entropy_rarity, length) * 100)
    # vowel_ratio_bar_percent = min(100.0, fi.get_component_rarity_bar_percent("vowel_ratio_rarity", vowel_ratio_rarity, length) * 100)
    # bookend_bonus_bar_percent = min(100.0, fi.get_component_rarity_bar_percent("bookend_bonus", 0 if bookend_bonus==1 else bookend_bonus, length) * 100)
    # bigram_bonus_bar_percent = min(100.0, fi.get_component_rarity_bar_percent("bigram_bonus", bigram_bonus - 1, length) * 100)
    
    
    
    return {
        # "random_string": random_string,
        # "repeated_1_strs": repeated_1_strs,
        # "repeated_chunks": repeated_chunks,
        # "bookend": bookend,
        # "palindromes": palindromes,
        # "char_blocks": char_blocks,
        # "char_blocks_dict": char_blocks_dict,
        # "words_within": words_within,
        "entropy": round(entropy, 5),
        "vowel_ratio": round(vowel_ratio, 5),
        "percent_unique": round(percent_unique,5),
        # "vowel_ratio_rarity": round(vowel_ratio_rarity, 5),
        # "entropy_rarity": round(entropy_rarity, 5),
        "letter_points": letter_points,
        # "length_bonus": round(length_bonus, 5),
        # "entropy_bonus": round(entropy_bonus, 5),
        "vowel_ratio_bonus": round(vowel_ratio_bonus, 5),
        "bookend_bonus": round(bookend_bonus, 5),
        "palindrome_bonus": round(palindrome_bonus, 5),
        "words_within_bonus": round(words_within_bonus, 5),
        "char_blocks_bonus": round(char_blocks_bonus, 5),
        "repeated_chunks_bonus": round(repeated_chunks_bonus, 5),
        "bigram_bonus": round(bigram_bonus, 5),
        "basic_bonuses": round(basic_bonuses, 5),
        "remaining_bonuses": round(remaining_bonuses, 5),
        "total_points": round(total_points)#,
    #     "card_rarity": card_rarity,
    #     "entropy_bar_percent": round(entropy_bar_percent, 5),
    #     "vowel_ratio_bar_percent": round(vowel_ratio_bar_percent, 5),
    #     "bookend_bonus_bar_percent": round(bookend_bonus_bar_percent, 5),
    #     "bigram_bonus_bar_percent": round(bigram_bonus_bar_percent, 5),
    #     "letter_points_bar_percent": round(letter_points_bar_percent, 5),
    #     "words_within_bonus_bar_percent": round(words_within_bonus_bar_percent, 5),
    #     "palindrome_bonus_bar_percent": round(palindrome_bonus_bar_percent, 5),
    #     "char_blocks_bonus_bar_percent": round(char_blocks_bonus_bar_percent, 5),
    #     "repeated_chunks_bonus_bar_percent": round(repeated_chunks_bonus_bar_percent, 5)
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

# test_strings = [
#     "abcdefghijklmnopqrstuvwxyz",
#     "aaaaaaaaaaaaaaaaaaaaaaaaaa",
#     "zzzzzzzzzzzzzzzzzzzzzzzzzz",
#     "zyxwvutsrqponmlkjihgfedcab",
#     "ababababababababababababab",
#     "abcabcabcabcabcabcabcabcab",
#     "aaaaaaaaaaaaabbbbbbbbbbbbb",
#     "pqowkjldsanfbhajsdlknajfnh"]

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

# N = 10000
# L = 12
# scores = []
# for i in range(N):
#     s = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=L))
#     be = generate_scored_string(L, s)
#     if be["bigram_bonus"] > 150:
#         scores.append([i, be["random_string"], be["total_points"], be["bigram_bonus"]])

# scores.sort(key=lambda x: x[3], reverse=True)
# for i, elem in enumerate(scores[:25]):
#     print(f"{i:2}: {elem[0]:8}: {elem[1]} => {elem[2]}  (bigram: {elem[3]})")

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

############## SCORE STATISTICS GENERATION ##############

# scores = []
# print("LENGTH,MEAN,25TH PERCENTILE,50TH PERCENTILE,75TH PERCENTILE,90TH PERCENTILE,99TH PERCENTILE,99.9TH PERCENTILE,99.99TH PERCENTILE, 99.999TH PERCENTILE")
# for L in range(3, 33):
#     score   = []
#     mean_numerator = 0

#     score = np.fromiter(
#         (generate_scored_string(L)["total_points"] for _ in range(N)),
#         dtype=np.int32,
#         count=N
#     )
#     mean_numerator = np.sum(score)
#     print(f"{L},{mean_numerator / N},{np.percentile(score, [25, 50, 75, 90, 99, 99.9, 99.99, 99.999])}")

def run_length(L, N=10_000_000):
    print(f"Begin length {L}")
    scores = np.fromiter(
        (generate_scored_string(L)["total_points"] for _ in range(N)),
        dtype=np.int32,
        count=N
    )
    p = np.percentile(scores, [25, 50, 75, 90, 99, 99.9, 99.99, 99.999])
    print(f"Completed length {L}")
    return L, scores.mean(), p

# if __name__ == "__main__":

#     alphabet = string.ascii_lowercase
#     pcts = []
#     for L in range(2, 6):
#         N = 26 ** L
#         scores = np.empty(N, dtype=np.int32)
#         pct = []

#         i = 0
#         for tup in product(alphabet, repeat=L):
#             results = generate_scored_string(L,''.join(tup))
#             scores[i] = results["total_points"]
#             if i % 100000 == 0:
#                 print(f"Length {L}: Processed {i}/{N} ({(i/N)*100:.2f}%)")
#             i += 1

#         pct = np.percentile(
#             scores,
#             [25, 50, 75, 90, 99, 99.9, 99.99, 99.999]
#         )

#         pcts.append(pct)

#     with open("score_rarity_percentiles_multithreaded_2.json", "a") as f:
#         f.write("{\n")
#         f.write(f'"row1": [MEAN,25PCTILE,50PCTILE,75PCTILE,90PCTILE,99PCTILE,99.9PCTILE,99.99PCTILE,99.999PCTILE],\n')
#         for i, pct in enumerate(pcts):
#             mean = scores[i].mean()
#             f.write(f'"row{i + 2}": [{mean},{pct[0]},{pct[1]},{pct[2]},{pct[3]},{pct[4]},{pct[5]},{pct[6]},{pct[7]}],\n')

#     with Pool() as p:
#         results = p.map(run_length, range(6, 33))

#     with open("score_rarity_percentiles_multithreaded_2.json", "a") as f:
#         for res in results:
#             L = res[0]
#             mean = res[1]
#             p = res[2]
#             f.write(f'"row{L}": [{mean},{p[0]},{p[1]},{p[2]},{p[3]},{p[4]},{p[5]},{p[6]},{p[7]}],\n')
#         f.write("}\n")

# ############## CREATE HISTOGRAM OF SCORES ##############

# alphabet = string.ascii_lowercase
# scores = []
# L = 4
# N = 26 ** L

# for i, tup in enumerate(product(alphabet, repeat=L)):
#     results = generate_scored_string(L, ''.join(tup))
#     scores.append(results["entropy_rarity"])
#     if i % 50000 == 0:
#         print(f"Processed {i}/{N} ({100 * i / N:.2f}%)")


# create_histogram(scores, bins=100, title="Score Distribution", xlabel="Score", ylabel="Frequency")


# ---- CONFIG ----

# COMPONENTS = [
#     "vowel_ratio_rarity",
#     "entropy_rarity",
#     "letter_points",
#     "bookend_bonus",
#     "palindrome_bonus",
#     "words_within_bonus",
#     "char_blocks_bonus",
#     "repeated_chunks_bonus",
#     "bigram_bonus",
#     "basic_bonuses",
#     "remaining_bonuses",
# ]

COMPONENTS = [
    "entropy",
    "vowel_ratio",
    "percent_unique",
    "letter_points",
    "vowel_ratio_bonus",
    "bookend_bonus",
    "palindrome_bonus",
    "words_within_bonus",
    "char_blocks_bonus",
    "repeated_chunks_bonus",
    "bigram_bonus",
    "basic_bonuses",
    "remaining_bonuses",
    "total_points"
]

PERCENTILES = [25, 50, 75, 90, 99, 99.9, 99.99, 99.999]

OUTPUT_FILE = "score_component_percentiles_with_std_dev_only_entropy_and_vowel_ratio_2_thru_5.json"

# ----------------

def run_exact_distributions_to_5():
    alphabet = string.ascii_lowercase
    output = {}

    print("Starting exact distribution calculations, L = 2 to 5...")
    for L in range(2, 6):
        print(f"\n=== Processing L = {L} ===")

        N = 26 ** L

        num_components = len(COMPONENTS)

        # Allocate component-major storage:
        # shape = (component, sample)
        data = np.empty((num_components, N), dtype=np.float32)

        for i, tup in enumerate(product(alphabet, repeat=L)):
            results = generate_scored_string(L, ''.join(tup))

            for c, name in enumerate(COMPONENTS):
                data[c, i] = results[name]

            if i % 50_000 == 0:
                print(f"  {i}/{N} ({100 * i / N:.2f}%)")

        # Compute stats per component
        L_stats = {}

        for c, name in enumerate(COMPONENTS):
            values = data[c]

            L_stats[name] = {
                "mean": float(values.mean()), 
                "std_deviation": float(values.std()),
                "percentiles": {
                    str(p): float(v)
                    for p, v in zip(
                        PERCENTILES,
                        np.percentile(values, PERCENTILES)
                    )
                }
            }

        output[f"length_{L}"] = L_stats

        # Explicitly free memory before next L
        del data

    # Write JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nDone. Results written to {OUTPUT_FILE}")


N_TOTAL = 10_000_000
# N_TOTAL = 300
# Reservoir for mid-quantiles
MID_PCTS = [25, 50, 75, 90]
RESERVOIR_SIZE = 50_000

# Heaps for extreme tail only
TAIL_PCTS = {
    99:   1e-2,
    99.9:   1e-3,
    99.99:  1e-4,
    99.999: 1e-5,
}
L_VALUES = range(6,33)

# def merge_means(results):
#     total = sum(r[0] for r in results)
#     merged = {k: 0.0 for k in COMPONENTS}

#     for count, means, _, _ in results:
#         for k in COMPONENTS:
#             merged[k] += means[k] * count

#     for k in merged:
#         merged[k] /= total

#     return merged

def merge_variances(results):
    merged_mean = {k: 0.0 for k in COMPONENTS}
    merged_M2   = {k: 0.0 for k in COMPONENTS}
    total_n = 0

    for n, means, M2s, _, _ in results:
        if total_n == 0:
            merged_mean = means.copy()
            merged_M2   = M2s.copy()
            total_n = n
            continue

        for k in COMPONENTS:
            delta = means[k] - merged_mean[k]
            new_n = total_n + n

            merged_M2[k] += (
                M2s[k] +
                delta * delta * total_n * n / new_n
            )

            merged_mean[k] += delta * n / new_n

        total_n = new_n

    stddevs = {
        k: math.sqrt(merged_M2[k] / total_n)
        for k in COMPONENTS
    }

    return total_n, merged_mean, stddevs

def merge_heaps(results):
    merged = {
        k: {p: [] for p in TAIL_PCTS}
        for k in COMPONENTS
    }

    for _, _, _, _, heaps in results:
        for comp in COMPONENTS:
            for pct in TAIL_PCTS:
                merged[comp][pct].extend(heaps[comp][pct])

    for comp in COMPONENTS:
        for pct, frac in TAIL_PCTS.items():
            k = max(1, int(N_TOTAL * frac))
            merged[comp][pct] = heapq.nlargest(k, merged[comp][pct])

    return merged

def reservoir_update(reservoir, seen, value):
    if len(reservoir) < RESERVOIR_SIZE:
        reservoir.append(value)
    else:
        j = random.randint(0, seen - 1)
        if j < RESERVOIR_SIZE:
            reservoir[j] = value

def merge_reservoirs(results):
    merged = {k: [] for k in COMPONENTS}

    for _, _, _, reservoirs, _ in results:
        for k in COMPONENTS:
            merged[k].extend(reservoirs[k])

    for k in COMPONENTS:
        if len(merged[k]) > RESERVOIR_SIZE:
            merged[k] = random.sample(merged[k], RESERVOIR_SIZE)

    return merged


def mc_worker(args):
    L, N = args
    pid = os.getpid()

    means = {k: 0.0 for k in COMPONENTS}
    M2s   = {k: 0.0 for k in COMPONENTS}
    reservoirs = {k: [] for k in COMPONENTS}
    heaps = {
        k: {p: [] for p in TAIL_PCTS}
        for k in COMPONENTS
    }

    count = 0

    for i in range(1, N + 1):
        r = generate_scored_string(L)
        count += 1

        for name in COMPONENTS:
            v = r[name]

            # Welford update
            delta = v - means[name]
            means[name] += delta / count
            delta2 = v - means[name]
            M2s[name] += delta * delta2

            # reservoir (25–90)
            reservoir_update(reservoirs[name], count, v)

            # tail heaps (99+)
            for pct, frac in TAIL_PCTS.items():
                k = max(1, int(N_TOTAL * frac))
                h = heaps[name][pct]

                if len(h) < k:
                    heapq.heappush(h, v)
                elif v > h[0]:
                    heapq.heapreplace(h, v)

        if i % 20_000 == 0:
            print(f"length_{L}, PID={pid}: {i:,}/{N:,}")

    return count, means, M2s, reservoirs, heaps

def run_monte_carlo():
    workers = cpu_count()
    output = {}

    for L in L_VALUES:
        print(f"\n=== Monte Carlo L={L} ===")

        per_worker = N_TOTAL // workers
        tasks = [(L, per_worker)] * workers

        with Pool(workers) as pool:
            results = pool.map(mc_worker, tasks)

        total_n, means, stddevs = merge_variances(results)
        reservoirs = merge_reservoirs(results)
        heaps = merge_heaps(results)

        L_out = {}

        for comp in COMPONENTS:
            mid = np.percentile(reservoirs[comp], MID_PCTS)

            tail = {
                str(p): min(heaps[comp][p])
                for p in TAIL_PCTS
            }

            L_out[comp] = {
                "mean": means[comp],
                "std_dev": stddevs[comp],
                "percentiles": {
                    "25": mid[0],
                    "50": mid[1],
                    "75": mid[2],
                    "90": mid[3],
                    **tail
                }
            }

        output[f"length_{L}"] = L_out

    with open(OUTPUT_FILE, "a") as f:
        json.dump(output, f, indent=2)

    print("\nDone.")

if __name__ == "__main__":
    #run_exact_distributions_to_5()
    try:
        run_exact_distributions_to_5()
        #run_monte_carlo()
    except Exception as e:
        print(type(e), str(e)[:500])
        raise

# def mc_worker(args):
#     L, N = args
#     pid = os.getpid()

#     means = {k: 0.0 for k in COMPONENTS}
#     M2s   = {k: 0.0 for k in COMPONENTS}
#     reservoirs = {k: [] for k in COMPONENTS}
#     heaps = {
#         k: {p: [] for p in TAIL_PCTS}
#         for k in COMPONENTS
#     }

#     count = 0

#     for i in range(1, N + 1):
#         r = generate_scored_string(L)
#         count += 1

#         for name in COMPONENTS:
#             v = r[name]

#             delta = v - means[name]
#             means[name] += delta / count
#             delta2 = v - means[name]
#             M2s[name] += delta * delta2

#             # reservoir for mid percentiles
#             reservoir_update(reservoirs[name], count, v)

#             # tail heaps
#             for pct, frac in TAIL_PCTS.items():
#                 k = max(1, int(N_TOTAL * frac))
#                 h = heaps[name][pct]

#                 if len(h) < k:
#                     heapq.heappush(h, v)
#                 elif v > h[0]:
#                     heapq.heapreplace(h, v)

#         if i % 20_000 == 0:
#             print(f"L={L}, PID={pid}: {i:,}/{N:,} ({100 * i / N:.2f}%)")

#     return count, means, M2s, reservoirs, heaps


# def run_monte_carlo():
#     workers = cpu_count()
#     output = {}

#     for L in L_VALUES:
#         print(f"\n=== Monte Carlo L={L} ===")

#         per_worker = N_TOTAL // workers
#         tasks = [(L, per_worker)] * workers

#         with Pool(workers) as pool:
#             results = pool.map(mc_worker, tasks)

#         means = merge_means(results)
#         std_deviations = merge_std_devs(results)
#         reservoirs = merge_reservoirs(results)
#         heaps = merge_heaps(results)

#         L_out = {}

#         for comp in COMPONENTS:
#             mid = np.percentile(reservoirs[comp], MID_PCTS)

#             tail = {
#                 str(p): min(heaps[comp][p])
#                 for p in TAIL_PCTS
#             }

#             L_out[comp] = {
#                 "mean": means[comp],
#                 "std_deviations": std_deviations[comp],
#                 "percentiles": {
#                     "25": mid[0],
#                     "50": mid[1],
#                     "75": mid[2],
#                     "90": mid[3],
#                     **tail
#                 }
#             }

#         output[f"length_{L}"] = L_out

#     with open(OUTPUT_FILE, "a") as f:
#         json.dump(output, f, indent=2)

#     print("\nDone.")



