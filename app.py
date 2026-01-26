import functions_imports as fi
from flask import Flask, jsonify, request, render_template

# Load Trie Once
english_trie = fi.load_dictionary_trie("dict.txt")

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
    repeated_2_plus_strs = {}
    for elem in fi.repeated_substrings(random_string):
        if elem[1] == 1:
            repeated_1_strs[elem[0]] = elem[2]
        else:
            repeated_2_plus_strs[elem[0]] = elem[2]

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
        palindrome_bonus += ( (palindrome_letter_bonus) * (len(palindrome[2])**2))
        
    words_within_bonus      = 1 + (len(words_within) / 10)

    total_points = (letter_points * 
                    length_bonus * 
                    entropy_bonus * 
                    vowel_ratio_bonus * 
                    bookend_bonus #* 
                    #palindrome_bonus * 
                    #words_within_bonus
                )

    return {
        "random_string": random_string,
        "repeated_1_strs": repeated_1_strs,
        "repeated_2_plus_strs": repeated_2_plus_strs,
        "bookend": bookend,
        "palindromes": palindromes,
        "char_blocks": char_blocks,
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
        "total_points": round(total_points)
    }

# APPLICATION SETUP
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
    length = int(request.args.get("length", 8))
    rolls = int(request.args.get("rolls", 1))

    results = [generate_scored_string(length) for _ in range(rolls)]

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)


