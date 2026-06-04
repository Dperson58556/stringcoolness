import numpy as np
from collections import Counter

# ---------- 1. PALINDROMES of fixed length x ----------

def count_palindromes_length_x(samples, x):
    """
    Count windows of length x that are palindromes.
    samples: (n, y) int array.  Returns: (n,) int array.
    """
    n, y = samples.shape
    if x > y:
        return np.zeros(n, dtype=np.int32)
    if x == 1:
        return np.full(n, y, dtype=np.int32)  # every single char is a palindrome

    n_windows = y - x + 1
    # Stack all windows: shape (n, n_windows, x)
    # Compare position i to position x-1-i for i < x//2
    half = x // 2
    # Build window-start indices
    # For each window w in [0, n_windows), characters are samples[:, w:w+x]
    # We can compare two slices: left half vs reversed right half
    left_idx  = np.arange(half)                         # 0..half-1
    right_idx = x - 1 - left_idx                        # x-1..x-half

    # Gather: for each window start w, samples[:, w + left_idx] vs samples[:, w + right_idx]
    window_starts = np.arange(n_windows)[:, None]       # (n_windows, 1)
    left_positions  = window_starts + left_idx[None, :]   # (n_windows, half)
    right_positions = window_starts + right_idx[None, :]  # (n_windows, half)

    left_chars  = samples[:, left_positions]   # (n, n_windows, half)
    right_chars = samples[:, right_positions]  # (n, n_windows, half)

    is_palindrome = (left_chars == right_chars).all(axis=2)  # (n, n_windows)
    return is_palindrome.sum(axis=1).astype(np.int32)

def longest_palindrome(samples):
    """Length of the longest palindromic substring per row. Uses Manacher per row."""
    n, y = samples.shape
    out = np.empty(n, dtype=np.int32)
    for i in range(n):
        out[i] = _manacher_longest(samples[i])
    return out

def _manacher_longest(arr):
    # Standard Manacher with a sentinel. arr is 1-D int array.
    # Insert sentinel -1 between characters.
    s = np.full(2 * len(arr) + 1, -1, dtype=np.int32)
    s[1::2] = arr
    p = np.zeros(len(s), dtype=np.int32)
    c = r = 0
    best = 0
    for i in range(len(s)):
        mirror = 2 * c - i
        if i < r:
            p[i] = min(r - i, p[mirror])
        a, b = i + p[i] + 1, i - p[i] - 1
        while a < len(s) and b >= 0 and s[a] == s[b]:
            p[i] += 1
            a += 1
            b -= 1
        if i + p[i] > r:
            c, r = i, i + p[i]
        if p[i] > best:
            best = p[i]
    return int(best)

# ---------- 2. RUNS of length exactly x ----------

def count_runs_length_x(samples, x):
    """Maximal runs of identical chars with length exactly x."""
    n, y = samples.shape
    if x > y:
        return np.zeros(n, dtype=np.int32)

    # boundary[:, i] = 1 if position i starts a new run (i==0 or differs from prev)
    diff = np.ones((n, y), dtype=bool)
    diff[:, 1:] = samples[:, 1:] != samples[:, :-1]
    # Each True in `diff` is a run start. Run length = distance to next start (or end).
    out = np.zeros(n, dtype=np.int32)
    for i in range(n):
        starts = np.flatnonzero(diff[i])
        lengths = np.diff(np.append(starts, y))
        out[i] = int((lengths == x).sum())
    return out

# ---------- 3. BOOKENDS ----------

def count_bookends_length_x(samples, x):
    """
    1 if first x chars == reverse of last x chars, else 0.
    (Per-string indicator; aggregating over many samples gives the probability.)
    """
    n, y = samples.shape
    if 2 * x > y:
        # Definitionally allow x up to floor(y/2); above that, prefix and suffix overlap.
        return np.zeros(n, dtype=np.int32)
    prefix = samples[:, :x]
    suffix_rev = samples[:, y - x:][:, ::-1]
    return (prefix == suffix_rev).all(axis=1).astype(np.int32)

def longest_bookend(samples):
    """Largest x such that prefix[:x] == reverse(suffix[-x:])."""
    n, y = samples.shape
    max_x = y // 2
    out = np.zeros(n, dtype=np.int32)
    # Check from largest x downward; first hit wins.
    for x in range(max_x, 0, -1):
        prefix = samples[:, :x]
        suffix_rev = samples[:, y - x:][:, ::-1]
        match = (prefix == suffix_rev).all(axis=1) & (out == 0)
        out[match] = x
        if (out > 0).all():
            break
    return out

# ---------- 4. ENTROPY ----------

def shannon_entropy(samples):
    """Shannon entropy (bits) of the empirical char distribution per string."""
    n, y = samples.shape
    # Bincount per row. Vectorize by offsetting char codes per row.
    K = int(samples.max()) + 1 if samples.size else 1
    K = max(K, 26)  # cap so axis is consistent across rows
    # Build counts per row via advanced indexing.
    counts = np.zeros((n, K), dtype=np.int32)
    rows = np.repeat(np.arange(n), y)
    cols = samples.reshape(-1).astype(np.int64)
    np.add.at(counts, (rows, cols), 1)
    p = counts / y
    # Use np.where to avoid log2(0)
    with np.errstate(divide="ignore", invalid="ignore"):
        terms = np.where(p > 0, -p * np.log2(p), 0.0)
    return terms.sum(axis=1)

# ---------- 5. ENGLISH WORDS ----------

# Load once, group by length.
_WORD_SETS = None
def _load_words(path="wordlist.txt"):
    global _WORD_SETS
    if _WORD_SETS is not None:
        return _WORD_SETS
    by_len = {}
    with open(path) as f:
        for w in f:
            w = w.strip().lower()
            if w.isalpha() and w.isascii():
                by_len.setdefault(len(w), set()).add(w)
    _WORD_SETS = by_len
    return _WORD_SETS

_CHARS = np.array(list("abcdefghijklmnopqrstuvwxyz"))

def _rows_to_strings(samples):
    # Convert int8 (n,y) -> list of length-y str
    return ["".join(_CHARS[row]) for row in samples]

def count_english_words_length_x(samples, x, wordlist_path="wordlist.txt"):
    """Number of length-x substrings that are real English words."""
    n, y = samples.shape
    if x > y:
        return np.zeros(n, dtype=np.int32)
    words = _load_words(wordlist_path).get(x, set())
    if not words:
        return np.zeros(n, dtype=np.int32)
    strings = _rows_to_strings(samples)
    out = np.empty(n, dtype=np.int32)
    for i, s in enumerate(strings):
        c = 0
        for j in range(y - x + 1):
            if s[j:j + x] in words:
                c += 1
        out[i] = c
    return out

# ---------- 6. REPEATED SUBSTRINGS ----------

def count_repeated_substrings_length_x(samples, x):
    """Number of distinct length-x substrings that appear >= 2 times."""
    n, y = samples.shape
    if x > y:
        return np.zeros(n, dtype=np.int32)
    out = np.empty(n, dtype=np.int32)
    for i in range(n):
        row = samples[i]
        counts = Counter()
        for j in range(y - x + 1):
            # hash the window as bytes
            counts[bytes(row[j:j + x])] += 1
        out[i] = sum(1 for v in counts.values() if v >= 2)
    return out

def longest_repeated_substring(samples):
    """Length of the longest substring that appears >= 2 times."""
    n, y = samples.shape
    out = np.zeros(n, dtype=np.int32)
    for i in range(n):
        row_bytes = bytes(samples[i])
        # Binary search on length L; check if any length-L substring repeats.
        lo, hi = 0, y - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            seen = set()
            found = False
            for j in range(y - mid + 1):
                w = row_bytes[j:j + mid]
                if w in seen:
                    found = True
                    break
                seen.add(w)
            if found:
                lo = mid
            else:
                hi = mid - 1
        out[i] = lo
    return out
