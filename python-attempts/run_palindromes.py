from core import build_2d_table, build_1d_table, write_json, DEFAULT_SEED, MAX_LEN
from measures import count_palindromes_length_x, longest_palindrome

N_SAMPLES = 2_000_000   # bump to 10_000_000 for production-quality 99.999th percentile

# Fixed-length palindrome counts: x in 2..MAX_LEN, y in x..MAX_LEN
table = build_2d_table(
    measure_fn=count_palindromes_length_x,
    x_range=range(2, MAX_LEN + 1),
    n_samples=N_SAMPLES,
    seed=DEFAULT_SEED,
)
write_json("out/palindromes_length_x.json",
           "count_of_length_x_palindromic_substrings",
           table, N_SAMPLES, DEFAULT_SEED,
           extra={"notes": "Counts overlapping windows. x=1 omitted (trivially y)."})

# Bonus: longest palindromic substring per string length
table1d = build_1d_table(longest_palindrome, N_SAMPLES, DEFAULT_SEED)
write_json("out/longest_palindrome.json",
           "length_of_longest_palindromic_substring",
           table1d, N_SAMPLES, DEFAULT_SEED)

print("Done. Wrote out/palindromes_length_x.json and out/longest_palindrome.json")
