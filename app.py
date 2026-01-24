from flask import Flask, jsonify, request, render_template
import string
import random
from collections import Counter, defaultdict
import math

##### PERCENT UNIQUE #####
def pct_unique(s: str):
    n = len(s)
    unique_chars = len(set(s))
    return unique_chars / n

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

##### PALINDROMIC BLOCKS (NO MONO-CHARACTER BLOCKS) #####
def palindromic_blocks_all(text: str):
    text_length = len(text)

    # ---- Odd-length palindromes ----
    for center_index in range(text_length):
        expansion_radius = 1
        best_left = None
        best_right = None

        while (
            center_index - expansion_radius >= 0 and
            center_index + expansion_radius < text_length and
            text[center_index - expansion_radius] ==
            text[center_index + expansion_radius]
        ):
            best_left = center_index - expansion_radius
            best_right = center_index + expansion_radius
            expansion_radius += 1

        if best_left is not None:
            result = text[best_left : best_right + 1]
            if len(set(result)) > 1:
                yield result

    # ---- Even-length palindromes ----
    for left_center in range(text_length - 1):
        expansion_radius = 0
        best_left = None
        best_right = None

        while (
            left_center - expansion_radius >= 0 and
            left_center + expansion_radius + 1 < text_length and
            text[left_center - expansion_radius] ==
            text[left_center + expansion_radius + 1]
        ):
            best_left = left_center - expansion_radius
            best_right = left_center + expansion_radius + 1
            expansion_radius += 1

        if best_left is not None:
            result = text[best_left : best_right + 1]
            if len(set(result)) > 1:
                yield result

##### CHARACTER BLOCKS #####
def character_blocks(text: str):
    text_length = len(text)
    index = 0

    while index < text_length:
        start_index = index
        current_char = text[index]

        while index + 1 < text_length and text[index + 1] == current_char:
            index += 1

        end_index = index
        block_length = end_index - start_index + 1

        if block_length > 1:
            yield text[start_index : end_index + 1]

        index += 1

##### VOWEL TO CONSONANT RATIO Z-SCORE #####
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

##### STRING ENTROPY #####
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

##### FINAL SCORE #####
def generate_scored_string(length):
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))

    points = 0

    repeated_substrings_list = repeated_substrings(random_string)
    palindromes = list(palindromic_blocks_all(random_string))
    char_blocks = list(character_blocks(random_string))
    percent_unique = pct_unique(random_string)
    z_score = vowel_z_score(random_string)
    entropy = string_entropy(random_string)

    return {
        "string": random_string,
        "repeated_substrings": repeated_substrings_list,
        "palindromes": palindromes,
        "character_blocks": char_blocks,
        "percent_unique": percent_unique,
        "vowel_z_score": z_score,
        "entropy": entropy,
        "points": points
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

