import functions_imports as fi
import string

english_trie = fi.load_dictionary_trie("top-english-wordlists\\top_english_words_lower_100000.txt")

length = 24
for i in range(100000000):
    random_string = ''.join(fi.random.choices(fi.string.ascii_lowercase, k=length))

    words_within = fi.find_words_in_string(random_string, english_trie, min_length=3)

    if words_within:
        if words_within[0][3] >= 8:
            print(f"{i}: {random_string} {words_within[0]}")