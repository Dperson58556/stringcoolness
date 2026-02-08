import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def heatmap_component(df, component):
    sub = df[df["component"] == component]
    pivot = sub.pivot(index="length", columns="metric", values="value")

    # order percentiles numerically
    pivot = pivot[sorted(pivot.columns, key=lambda x: float(x) if x != "mean" else -1)]

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        pivot,
        norm=None,
        cmap="viridis",
        cbar_kws={"label": "Value"}
    )
    plt.title(f"{component} rarity heatmap")
    plt.xlabel("Metric")
    plt.ylabel("Length")
    plt.tight_layout()
    plt.show()


def plot_percentile_vs_length(df, *components, percentile):
    """
    Plot one percentile vs length for multiple components.

    Example:
        plot_percentile_vs_length(
            df,
            "remaining_bonuses",
            "basic_bonuses",
            "bigram_bonus",
            percentile="90"
        )
    """
    plt.figure()

    for component in components:
        sub = df[
            (df["component"] == component) &
            (df["metric"] == percentile)
        ].sort_values("length")

        if sub.empty:
            print(f"Warning: no data for component '{component}' at percentile {percentile}")
            continue

        plt.plot(
            sub["length"],
            sub["value"],
            marker="o",
            label=component
        )

    plt.xlabel("String Length")
    plt.ylabel(f"{percentile} Percentile Value")
    plt.title(f"{percentile} percentile vs length")
    #label data values on plot
    for i, row in sub.iterrows():
        plt.text(row["length"], row["value"], f"{row['value']:.2f}", fontsize=8, ha="center", va="bottom")
    #plt.yscale("log")   # crucial for tail behavior
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def load_rarity_data(path) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def plot_components_at_length(df, length, metric="99.0"):
    sub = df[
        (df["length"] == length) &
        (df["metric"] == metric)
    ].sort_values("value", ascending=False)

    plt.figure(figsize=(10, 4))
    plt.bar(sub["component"], sub["value"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(f"{metric} value")
    plt.title(f"Component comparison at length {length} ({metric})")
    plt.yscale("log")
    plt.tight_layout()
    plt.show()

def plot_means(df, components=None):
    means = df[df["metric"] == "mean"]

    if components:
        means = means[means["component"].isin(components)]

    plt.figure()
    for comp, sub in means.groupby("component"):
        sub = sub.sort_values("length")
        plt.plot(sub["length"], sub["value"], label=comp)

    plt.xlabel("Length")
    plt.ylabel("Mean value")
    plt.title("Mean rarity contribution vs length")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)
    plt.show()

def to_long_dataframe(raw: dict) -> pd.DataFrame:
    """
    Returns a DataFrame with columns:
    length, component, metric, value
    metric ∈ {"mean", "25", "50", "75", "90", "99.0", "99.9", "99.99", "99.999"}
    """
    rows = []

    for length_key, components in raw.items():
        length = int(length_key.split("_")[1])

        for component, stats in components.items():
            # mean
            rows.append({
                "length": length,
                "component": component,
                "metric": "mean",
                "value": stats["mean"]
            })

            # percentiles
            for pct, val in stats["percentiles"].items():
                rows.append({
                    "length": length,
                    "component": component,
                    "metric": pct,
                    "value": val
                })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    #raw = load_rarity_data("score_component_percentiles.json")
    raw = load_rarity_data("score_component_percentiles.json")
    df = to_long_dataframe(raw)

    plot_percentile_vs_length(df, "entropy_rarity", "vowel_ratio_rarity", percentile="mean")
    plot_percentile_vs_length(df, "entropy_rarity", "vowel_ratio_rarity", percentile="25")
    plot_percentile_vs_length(df, "entropy_rarity", "vowel_ratio_rarity", percentile="50")
    plot_percentile_vs_length(df, "entropy_rarity", "vowel_ratio_rarity", percentile="75")
    plot_percentile_vs_length(df, "entropy_rarity", "vowel_ratio_rarity", percentile="90")
    plot_percentile_vs_length(df, "entropy_rarity", "vowel_ratio_rarity", percentile="99.0")
    plot_percentile_vs_length(df, "entropy_rarity", "vowel_ratio_rarity", percentile="99.9")
    plot_percentile_vs_length(df, "entropy_rarity", "vowel_ratio_rarity", percentile="99.99")
    plot_percentile_vs_length(df, "entropy_rarity", "vowel_ratio_rarity", percentile="99.999")
    
    #plot_components_at_length(df, length=16, metric="90")
    #plot_means(df)
    #heatmap_component(df, "remaining_bonuses")
