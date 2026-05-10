import itertools
import string

# Generate all lowercase three-letter strings
letters = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
three_letter_strings = [''.join(p) for p in itertools.product(letters, repeat=3)]

with open('dict.txt', 'r') as f:
    valid_words = set(word.strip().lower() for word in f if len(word.strip()) == 3)

with open('three_letter_strings.txt', 'w') as f:
    for s in three_letter_strings:
        is_valid = s in valid_words
        f.write(f"{s},{is_valid}\n")
