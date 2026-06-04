from core import build_2d_table, build_1d_table, write_json, DEFAULT_SEED, MAX_LEN
from measures import (
    count_runs_length_x,
    count_bookends_length_x, longest_bookend,
    shannon_entropy,
    count_english_words_length_x,
    count_repeated_substrings_length_x, longest_repeated_substring,
)

N = 2_000_000   # tune per statistic

def run_runs():
    t = build_2d_table(count_runs_length_x, range(1, MAX_LEN + 1), N)
    write_json("out/runs_length_x.json",
               "count_of_maximal_runs_of_length_exactly_x", t, N, DEFAULT_SEED)

def run_bookends():
    t = build_2d_table(
        count_bookends_length_x,
        range(1, MAX_LEN // 2 + 1),
        N,
        y_min_fn=lambda x: 2 * x,
    )
    write_json("out/bookends_length_x.json",
               "indicator_prefix_x_equals_reverse_suffix_x", t, N, DEFAULT_SEED,
               extra={"notes": "Per-string indicator (0/1). Mean over samples = probability."})
    t2 = build_1d_table(longest_bookend, N, y_min=2)
    write_json("out/longest_bookend.json",
               "longest_x_with_prefix_equals_reverse_suffix", t2, N, DEFAULT_SEED)

def run_entropy():
    t = build_1d_table(shannon_entropy, N)
    write_json("out/entropy.json",
               "shannon_entropy_bits_of_char_distribution", t, N, DEFAULT_SEED,
               extra={"notes": "Low values = clumpy, high values = uniform. Use two-sided rarity."})

def run_english(wordlist="dict.txt"):
    from measures import _load_words
    available = sorted(_load_words(wordlist).keys())
    x_range = [x for x in available if 2 <= x <= MAX_LEN]
    t = build_2d_table(count_english_words_length_x, x_range, N)
    write_json("out/english_words_length_x.json",
               "count_of_length_x_substrings_that_are_english_words",
               t, N, DEFAULT_SEED,
               extra={"wordlist_path": wordlist})

def run_repeats():
    t = build_2d_table(count_repeated_substrings_length_x,
                       range(1, MAX_LEN + 1), N)
    write_json("out/repeated_substrings_length_x.json",
               "count_of_distinct_length_x_substrings_appearing_twice_or_more",
               t, N, DEFAULT_SEED)
    t2 = build_1d_table(longest_repeated_substring, N)
    write_json("out/longest_repeated_substring.json",
               "length_of_longest_repeated_substring", t2, N, DEFAULT_SEED)

if __name__ == "__main__":
    run_runs()
    run_bookends()
    run_entropy()
    run_repeats()
    run_english()  # comment out if you don't have a wordlist yet
    print("All statistics written to out/")
