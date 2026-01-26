import functions_imports as fi
import math

# Load Trie Once
english_trie = fi.load_dictionary_trie("top-english-wordlists\\top_english_words_lower_50000.txt")

###########################################
############### FINAL SCORE ###############
###########################################
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
    points = 0

    for letter in random_string:
        points += fi.letter_values[letter]

    length_bonus = 1 + (length/50)
    points = round(points ** length_bonus)
    
    return {
        "string": random_string,
        "repeated_chars": repeated_1_strs,
        "repeated_clusters": repeated_2_plus_strs,
        "bookend": bookend,
        "palindromes": palindromes,
        "character_blocks": char_blocks,
        "words_within": words_within,
        "percent_unique": round(percent_unique,5),
        "vowel_z_score": round(z_score, 5),
        "entropy": round(entropy, 5),
        "points": points
    }

def lengths_dist_heatmap():
    lengths = []
    score = []

    N = 10000

    for L in range(2, 33):
        for _ in range(N):
            s = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=L))
            points = 0
            length_bonus = 1 + ((L**1.25)/20)
            for letter in s:
                points += fi.letter_values[letter]
            
            points = points * length_bonus
           
            lengths.append(L)
            score.append(points)

    fi.plt.hist2d(
        score,
        lengths,
        bins=[200, 31],      # 100 score bins, 32 length bins
        cmap="inferno"
    )
    fi.plt.xlabel("score(random_string)")
    fi.plt.ylabel("string length")
    fi.plt.colorbar(label="count")
    fi.plt.show()


N = 100000
entropies = 0

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
    e = fi.string_entropy(s)
    rarity_z_score = (e - entropy_avgs[len(s)-1]) / entropy_avg_stds[len(s)-1]
    return e, rarity_z_score

def std_dev(values, entropy_mean):
    return math.sqrt(
        sum((x - entropy_mean) ** 2 for x in values) / (N - 1)
    )
#print(entropy_avgs)
# for L in range(1, 33):
#     trials = []

#     for _ in range(N):
#         s = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=L))
#         e = fi.string_entropy(s)
#         entropies += e #score.append(points)
#         trials.append(e)
#     #print(f"{entropies / N}")
#     print(f"{std_dev(trials, entropy_avgs[L-1])}")
#lengths_dist_heatmap()

for i in range(N):
    s = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=30))
    r, e = f1.vowel_ratio_rarity_z_score(s)
    if abs(r)>=5:
        print(f"{i} {s} {e:8.4f} {r:8.4f}")
#print(f"{entropies / N}")