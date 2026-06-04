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
import numpy as np
import json
from collections import Counter

ALPHABET_SIZE = 26
MAX_LEN = 32
N_SAMPLES = 10_000_000   # tune per statistic; tail estimation needs this
PERCENTILES = [25, 50, 75, 90, 99, 99.9, 99.99, 99.999]

rng = np.random.default_rng(seed=42)

def sample_strings(y, n):
    # shape (n, y) of ints 0..k-1; treat as characters
    return rng.integers(0, ALPHABET_SIZE, size=(n, y), dtype=np.int8)

def percentiles_for_length(y, measure_fn, n=N_SAMPLES):
    samples = sample_strings(y, n)
    values = measure_fn(samples)         # vectorized -> shape (n,)
    values.sort()
    out = {}
    for p in PERCENTILES:
        idx = min(int(p / 100 * n), n - 1)
        out[str(p)] = float(values[idx])
    return out

def build_table(measure_fn, x_range, name):
    table = {}
    for x in x_range:
        table[str(x)] = {}
        for y in range(1, MAX_LEN + 1):
            if x > y:
                continue
            table[str(x)][str(y)] = percentiles_for_length(
                y, lambda s: measure_fn(s, x)
            )
    with open(f"{name}.json", "w") as f:
        json.dump({"alphabet_size": ALPHABET_SIZE, "samples": N_SAMPLES, "data": table}, f, indent=2)
