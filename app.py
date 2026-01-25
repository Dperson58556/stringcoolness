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

    ##### GRAB PARAMETERS #####
    words_within = fi.find_words_in_string(random_string, english_trie, min_length=3)

    repeated_substrings_list = fi.repeated_substrings(random_string)
    repeated_1_strs = {}

    for elem in list(filter(lambda item: item[1] == 1, repeated_substrings_list)):
        repeated_1_strs[elem[0]] = elem[2]
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
        letter_points += fi.letter_values[letter] #* (repeated_1_strs[letter] if repeated_1_strs[letter]>0 else 1)
    length_bonus = 1 + ((length**1.25)/20)
    
    total_points = letter_points * length_bonus

    return {
        "random_string": random_string,
        "repeated_1_strs": repeated_1_strs,
        "repeated_2_plus_strs": repeated_2_plus_strs,
        "bookend": bookend,
        "palindromes": palindromes,
        "char_blocks": char_blocks,
        "words_within": words_within,
        "percent_unique": round(percent_unique,5),
        "z_score": round(z_score, 5),
        "entropy": round(entropy, 5),
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


