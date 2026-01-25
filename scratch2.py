import functions_imports as fi
import string

# english_trie = fi.load_dictionary_trie("top-english-wordlists\\top_english_words_lower_100000.txt")

# length = 24
# for i in range(100000000):
#     random_string = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=length))

#     words_within = fi.find_words_in_string(random_string, english_trie, min_length=3)

#     if words_within:
#         if words_within[0][3] >= 8:
#             print(f"{i}: {random_string} {words_within[0]}")

source_path = "C:\\Users\\darre\\OneDrive\\Desktop\\stringcoolness\\scrabblewords\\words\\North-American\\NWL2023.txt"
destination_path = "dict.txt"

with open(source_path, "r", encoding="utf-8") as src, \
     open(destination_path, "w", encoding="utf-8") as dst:

    for line in src:
        first_word = line.split(maxsplit=1)[0] if line.strip() else ""
        dst.write((first_word.lower()) + "\n")