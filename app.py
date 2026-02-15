import functions_imports as fi
from flask import Flask, jsonify, request, render_template

###########################################
############### FINAL SCORE ###############
###########################################
def generate_scored_string(length, word = None, debug = False):
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
    vowel_ratio, vowel_ratio_rarity = fi.vowel_ratio_rarity_z_score(random_string)
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
            char_blocks_bonus += ((2 * fi.letter_values[char])**1.4) * ((len(block[2]))**4.6)

    for chunk in repeated_chunks:
        for char in chunk:
            repeated_chunks_bonus += ((2 * fi.letter_values[char])**1.2)*3*(repeated_chunks[chunk]**5)

    remaining_bonuses = (palindrome_bonus +
                        words_within_bonus +  
                        char_blocks_bonus +
                        repeated_chunks_bonus)*length_bonus * bigram_bonus
    
    sub_total_points = (letter_points * 
                    length_bonus * 
                    entropy_bonus * 
                    vowel_ratio_bonus * 
                    bookend_bonus) + remaining_bonuses
    
    total_points = (sub_total_points ** (1.2)) / fi.RARITY_SCALAR

    card_rarity = fi.get_component_rarity("total_points", total_points, length)
    
    #xrfympwprlimlegatorf
    letter_points_bar_percent =         fi.get_component_rarity_bar_percent("letter_points",letter_points,length)
    words_within_bonus_bar_percent =    fi.get_component_rarity_bar_percent("words_within_bonus",words_within_bonus,length)*1.5 if words_within_bonus else 0
    palindrome_bonus_bar_percent =      fi.get_component_rarity_bar_percent("palindrome_bonus",palindrome_bonus,length) if palindrome_bonus else 0
    char_blocks_bonus_bar_percent =     fi.get_component_rarity_bar_percent("char_blocks_bonus",char_blocks_bonus,length) if char_blocks_bonus else 0
    repeated_chunks_bonus_bar_percent = fi.get_component_rarity_bar_percent("repeated_chunks_bonus",repeated_chunks_bonus,length)*.5 if repeated_chunks_bonus else 0
    entropy_bar_percent =               fi.get_component_rarity_bar_percent("entropy",entropy,length)
    vowel_ratio_bar_percent =           fi.get_component_rarity_bar_percent("vowel_ratio", vowel_ratio,length)
    bookend_bonus_bar_percent =         fi.get_component_rarity_bar_percent("bookend_bonus",bookend_bonus,length) if bookend else 0
    bigram_bonus_bar_percent =          fi.get_component_rarity_bar_percent("bigram_bonus",bigram_bonus,length)
    
    # print(
    # f"letter_points_bar_percent:         {letter_points_bar_percent}\n"
    # f"words_within_bonus_bar_percent:    {words_within_bonus_bar_percent}\n"
    # f"palindrome_bonus_bar_percent:      {palindrome_bonus_bar_percent}\n"
    # f"char_blocks_bonus_bar_percent:     {char_blocks_bonus_bar_percent}\n"
    # f"repeated_chunks_bonus_bar_percent: {repeated_chunks_bonus_bar_percent}\n"
    # f"entropy_bar_percent:               {entropy_bar_percent}\n"
    # f"vowel_ratio_bar_percent:           {vowel_ratio_bar_percent}\n"
    # f"bookend_bonus_bar_percent:         {bookend_bonus_bar_percent}\n"
    # f"bigram_bonus_bar_percent:          {bigram_bonus_bar_percent}"
    # )

    
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
        "bigram_bonus": round(bigram_bonus, 5),
        "total_points": round(total_points),
        "card_rarity": card_rarity,
        "entropy_bar_percent": round(entropy_bar_percent, 5),
        "vowel_ratio_bar_percent": round(vowel_ratio_bar_percent, 5),
        "bookend_bonus_bar_percent": round(bookend_bonus_bar_percent, 5),
        "bigram_bonus_bar_percent": round(bigram_bonus_bar_percent, 5),
        "letter_points_bar_percent": round(letter_points_bar_percent, 5),
        "words_within_bonus_bar_percent": round(words_within_bonus_bar_percent, 5),
        "palindrome_bonus_bar_percent": round(palindrome_bonus_bar_percent, 5),
        "char_blocks_bonus_bar_percent": round(char_blocks_bonus_bar_percent, 5),
        "repeated_chunks_bonus_bar_percent": round(repeated_chunks_bonus_bar_percent, 5)
    }

# Load Trie Once
english_trie = fi.load_dictionary_trie("dict.txt")

# APPLICATION SETUP
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("scratch.html")

@app.route("/generate_test_string")
def generate_test_string():
    test_strings_string = str(request.args.get("test_string")).lower()
    test_strings_string = test_strings_string.replace("%20", "")

    test_strings_list = [item[:fi.LEN_LIMIT].strip().lower() for item in test_strings_string.split(",")][:fi.ROLL_LIMIT]
    #rolls = int(request.args.get("roll_count", 1))

    invalid = False
    for ts in test_strings_list:
        if (not ts.isalpha()) or (len(ts)<2):
            invalid = True

    invalid_string = "invalidinput"
    if invalid:
        results = [generate_scored_string(len(invalid_string), invalid_string)]
    else:
        results = [generate_scored_string(len(test_string), test_string) for test_string in test_strings_list]

    return jsonify(results)

@app.route("/generate")
def generate():
    length = min(fi.LEN_LIMIT, int(request.args.get("length", 10)))
    rolls = min(fi.ROLL_LIMIT, int(request.args.get("roll_count", 25)))
    results = []

    debug = 0

    if debug == 1:
        while len(results) < rolls:
            res = generate_scored_string(length)
            if res["card_rarity"] in {"Legendary", "Mythical"}:
                results.append(res)
    else:
        results = [generate_scored_string(length) for _ in range(rolls)]
    return jsonify(results)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run()