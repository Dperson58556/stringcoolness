import json
import numpy as np
from pathlib import Path
from datetime import datetime, timezone

ALPHABET_SIZE = 26
MAX_LEN = 32
PERCENTILES = [25, 50, 75, 90, 99, 99.9, 99.99, 99.999]
DEFAULT_SEED = 42

def make_rng(seed=DEFAULT_SEED):
    return np.random.default_rng(seed)

def sample_strings(rng, y, n):
    return rng.integers(0, ALPHABET_SIZE, size=(n, y), dtype=np.int8)

def percentiles_from_values(values, percentiles=PERCENTILES, survival_max=None):
    """
    Returns:
      - percentile ladder (float64, linear interpolation)
      - survival probabilities P(X >= k) for k = 0..survival_max as float64
      - mean, std, max_observed
    """
    values = np.asarray(values)
    n = values.size

    # Linear-interpolated percentiles (numpy default). Always float64.
    pct_values = np.percentile(values.astype(np.float64),
                               percentiles, method="linear")
    out = {str(p): float(v) for p, v in zip(percentiles, pct_values)}
    out["mean"] = float(values.mean(dtype=np.float64))
    out["std"]  = float(values.std(dtype=np.float64))
    out["max_observed"] = float(values.max())

    # After the integer check, for float-valued stats:
    if "survival" not in out:
        # Empirical CDF on a fixed grid (e.g., 1001 points between min and max).
        grid = np.linspace(values.min(), values.max(), 1001)
        cdf = np.searchsorted(np.sort(values), grid, side="right") / np.float64(n)
        out["cdf_grid"] = grid.tolist()
        out["cdf_values"] = cdf.tolist()

    # Survival function P(X >= k) for integer-valued stats.
    # Use float64 division so very small tail probabilities are preserved.
    if survival_max is None:
        survival_max = int(values.max())
    if np.issubdtype(values.dtype, np.integer) or np.all(values == values.astype(np.int64)):
        # Build P(X >= k) for k = 1..survival_max (skip k=0 which is always 1.0)
        counts = np.bincount(values.astype(np.int64),
                             minlength=survival_max + 1).astype(np.float64)
        # tail[k] = sum_{j>=k} counts[j]
        tail = np.cumsum(counts[::-1])[::-1] / np.float64(n)
        # Only store nonzero tail entries to keep JSON compact.
        survival = {str(k): float(tail[k]) for k in range(1, survival_max + 1)
                    if tail[k] > 0.0}
        out["survival"] = survival
        # Floor of resolvable probability with this sample size:
        out["min_resolvable_prob"] = 1.0 / float(n)

    return out

def write_json(path, statistic_name, payload, n_samples, seed, extra=None):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "statistic": statistic_name,
        "alphabet_size": ALPHABET_SIZE,
        "max_length": MAX_LEN,
        "samples_per_cell": n_samples,
        "rng_seed": seed,
        "percentiles_reported": [str(p) for p in PERCENTILES],
        "percentile_method": "linear_interpolation_float64",
        "survival_field": "P(X >= k), float64; absent k means P=0 at this sample size",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "data": payload,
    }
    if extra:
        doc.update(extra)
    with open(path, "w") as f:
        json.dump(doc, f, indent=2)

def build_2d_table(measure_fn, x_range, n_samples, seed=DEFAULT_SEED,
                   y_min_fn=lambda x: x):
    rng = make_rng(seed)
    table = {}
    for x in x_range:
        table[str(x)] = {}
        for y in range(y_min_fn(x), MAX_LEN + 1):
            samples = sample_strings(rng, y, n_samples)
            values = measure_fn(samples, x)
            table[str(x)][str(y)] = percentiles_from_values(values)
    return table

def build_1d_table(measure_fn, n_samples, seed=DEFAULT_SEED, y_min=1):
    rng = make_rng(seed)
    table = {}
    for y in range(y_min, MAX_LEN + 1):
        samples = sample_strings(rng, y, n_samples)
        values = measure_fn(samples)
        table[str(y)] = percentiles_from_values(values)
    return table
