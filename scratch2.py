from collections import Counter
import json

score_rarity_percentiles = {}
with open("score_rarity_percentiles.json", "r") as f:
    score_rarity_percentiles = json.load(f)