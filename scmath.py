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
    #random_string = 'lblblblblbghyghyghyghy'

    ##### GRAB PARAMETERS #####
    words_within = fi.find_words_in_string(random_string, english_trie, min_length=3)

    repeated_1_strs = {}
    repeated_chunks = {}
    for elem in fi.repeated_substrings(random_string):
        if elem[1] == 1:
            repeated_1_strs[elem[0]] = elem[2]
        else:
            repeated_chunks[elem[0]] = elem[2]

    palindromes = list(fi.palindromic_blocks_all(random_string))
    char_blocks = list(fi.character_blocks(random_string))
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
    entropy_bonus           = 1 + abs(entropy_rarity)
    vowel_ratio_bonus       = 1 + abs(vowel_ratio_rarity)
    bookend_bonus           = bookend[0]*5 if bookend is not None else 1
    
    for palindrome in palindromes:
        palindrome_letter_bonus = 0
        for char in palindrome[2]:
            palindrome_letter_bonus += fi.letter_values[char]
        palindrome_bonus += ( (palindrome_letter_bonus) * 3 * (len(palindrome[2])**2))
    
    for word in words_within:
        for char in word[2]:
            words_within_bonus += fi.letter_values[char]*(len(word[2])**4)

    for block in char_blocks:
        for char in block[2]:
            char_blocks_bonus += (fi.letter_values[char]*2*(len(block[2])**3))

    for chunk in repeated_chunks:
        for char in chunk:
            repeated_chunks_bonus += fi.letter_values[char]*2*(repeated_chunks[chunk]**2)

    remaining_bonuses = (palindrome_bonus +
                        words_within_bonus +  
                        char_blocks_bonus +
                        repeated_chunks_bonus)
    
    total_points = (letter_points * 
                    length_bonus * 
                    entropy_bonus * 
                    vowel_ratio_bonus * 
                    bookend_bonus) + remaining_bonuses
    return random_string, total_points
    # return {
    #     "random_string": random_string,
    #     "repeated_1_strs": repeated_1_strs,
    #     "repeated_chunks": repeated_chunks,
    #     "bookend": bookend,
    #     "palindromes": palindromes,
    #     "char_blocks": char_blocks,
    #     "words_within": words_within,
    #     "percent_unique": round(percent_unique,5),
    #     "vowel_ratio_rarity": round(vowel_ratio_rarity, 5),
    #     "entropy": round(entropy, 5),
    #     "entropy_rarity": round(entropy_rarity, 5),
    #     "letter_points": letter_points,
    #     "length_bonus": round(length_bonus, 5),
    #     "entropy_bonus": round(entropy_bonus, 5),
    #     "vowel_ratio_bonus": round(vowel_ratio_bonus, 5),
    #     "bookend_bonus": round(bookend_bonus, 5),
    #     "palindrome_bonus": round(palindrome_bonus, 5),
    #     "words_within_bonus": round(words_within_bonus, 5),
    #     "char_blocks_bonus": round(char_blocks_bonus, 5),
    #     "repeated_chunks_bonus": round(repeated_chunks_bonus, 5),
    #     "total_points": round(total_points)
    # }

def lengths_dist_heatmap():
    lengths = []
    score = []

    N = 1000

    for L in range(3, 16):
        for _ in range(N):
            #s = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=L))
            
            points = generate_scored_string(L)
            lengths.append(L)
            score.append(points)

    fi.plt.hist2d(
        score,
        lengths,
        bins=[200, 13],      # 100 score bins, 32 length bins
        cmap="inferno"
    )
    fi.plt.xlabel("score(random_string)")
    fi.plt.ylabel("string length")
    fi.plt.colorbar(label="count")
    fi.plt.show()



# N = 100000
# entropies = 0

# def entropy_avg(x):
#     a = 15.89321934
#     b = -0.8297682291
#     c = -0.8237059174
#     d = 0.01270597934
#     e = -14.2437712

#     entropy_mean = (
#         a * x**(1/8)
#         + b * x**(1/4)
#         + c * x**(1/2)
#         + d * x
#         + e
#     )
#     return (entropy_mean)

# def entropy_avg_std(x):
#     a = -0.002459635337
#     b = 0.3639055228
#     c = 2.334252499
#     d = 0.2123435647

#     entropy_std = (
#         a * x
#         + b * x**(-1)
#         + c * x**(-2)
#         + d
#     )
#     return (entropy_std)

# entropy_avgs = [entropy_avg(x) for x in range(1,33)]
# entropy_avg_stds = [entropy_avg_std(x) for x in range(1,33)]

# def entropy_rarity_z_score(s):
#     e = fi.string_entropy(s)
#     rarity_z_score = (e - entropy_avgs[len(s)-1]) / entropy_avg_stds[len(s)-1]
#     return e, rarity_z_score

# def std_dev(values, entropy_mean):
#     return math.sqrt(
#         sum((x - entropy_mean) ** 2 for x in values) / (N - 1)
#     )
# #print(entropy_avgs)
# # for L in range(1, 33):
# #     trials = []

# #     for _ in range(N):
# #         s = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=L))
# #         e = fi.string_entropy(s)
# #         entropies += e #score.append(points)
# #         trials.append(e)
# #     #print(f"{entropies / N}")
# #     print(f"{std_dev(trials, entropy_avgs[L-1])}")
# #lengths_dist_heatmap()
N = 1000000
i = 0
while True:
    s, score = generate_scored_string(16)
    if score>=70000:
        print(f"{i} {s} {score:.2f}")
    i += 1
