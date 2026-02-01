import functions_imports as fi
from flask import Flask, jsonify, request, render_template

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
        palindrome_bonus += ( (palindrome_letter_bonus) * 3 * (len(palindrome[2])**2))
    
    for word in words_within:
        for char in word[2]:
            words_within_bonus += fi.letter_values[char]*(len(word[2])**4.5)

    for block in char_blocks:
        for char in block[2]:
            char_blocks_bonus += (fi.letter_values[char]*2*(len(block[2])**3))

    for chunk in repeated_chunks:
        for char in chunk:
            repeated_chunks_bonus += fi.letter_values[char]*2*(repeated_chunks[chunk]**2)

    remaining_bonuses = (palindrome_bonus +
                        words_within_bonus +  
                        char_blocks_bonus +
                        repeated_chunks_bonus)*length_bonus
    
    total_points = (letter_points * 
                    length_bonus * 
                    entropy_bonus * 
                    vowel_ratio_bonus * 
                    bookend_bonus) + remaining_bonuses

    card_rarity = fi.get_rarity_from_score(total_points, length)

    return {
        "random_string": random_string,
        "repeated_1_strs": repeated_1_strs,
        "repeated_chunks": repeated_chunks,
        "bookend": bookend,
        "palindromes": palindromes,
        "char_blocks": char_blocks,
        "char_blocks_dict": char_blocks_dict,
        "words_within": words_within,
        "percent_unique": round(percent_unique,5),
        "vowel_ratio_rarity": round(vowel_ratio_rarity, 5),
        "entropy": round(entropy, 5),
        "entropy_rarity": round(entropy_rarity, 5),
        "letter_points": letter_points,
        "length_bonus": round(length_bonus, 5),
        "entropy_bonus": round(entropy_bonus, 5),
        "vowel_ratio_bonus": round(vowel_ratio_bonus, 5),
        "bookend_bonus": round(bookend_bonus, 5),
        "palindrome_bonus": round(palindrome_bonus, 5),
        "words_within_bonus": round(words_within_bonus, 5),
        "char_blocks_bonus": round(char_blocks_bonus, 5),
        "repeated_chunks_bonus": round(repeated_chunks_bonus, 5),
        "total_points": round(total_points),
        "card_rarity": card_rarity
    }

# APPLICATION SETUP
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("scratch.html")

@app.route("/generate_test_string")
def generate_test_string():
    test_string = str(request.args.get("test_string"))
    rolls = int(request.args.get("rolls", 1))

    results = [generate_scored_string(len(test_string), test_string) for _ in range(rolls)]

    return jsonify(results)

@app.route("/generate")
def generate():
    length = int(request.args.get("length", 8))
    rolls = int(request.args.get("rolls", 1))

    results = [generate_scored_string(length) for _ in range(rolls)]

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)


