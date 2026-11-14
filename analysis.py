import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("data/exoplanets.csv")
## examining data

# print(df.info())
# print(df.head())
# print(df.shape)
# returns how many missing values each column has
# print(df.isnull().sum())


# clean out planets that have an empty radius or insolation
clean_df = df.dropna(subset=["pl_rade", "pl_insol"])
# print(clean_df.shape)

## filter out potentially rocky planets
rocky_df = clean_df[clean_df["pl_rade"] <= 1.8]
# print(rocky_df.shape)

candidates_df = rocky_df[(rocky_df["pl_insol"] >= 0.35) & (rocky_df["pl_insol"] <= 1.5)
]
# print(candidates_df.shape)
# print(candidates_df[["pl_name", "pl_rade", "pl_insol"]].head(10))

# calculates how far each planets measurements deviate from Earth's
# lower score = more similar to Earth
candidates_df = candidates_df.copy()
candidates_df["earth_similarity_score"] = (
    abs(candidates_df["pl_rade"] - 1) +
    abs(candidates_df["pl_insol"] - 1)
)

# ranking planets
ranked_df = candidates_df.sort_values(
    "earth_similarity_score",
    ascending=True
)
# print(ranked_df[["pl_name", "earth_similarity_score"]].head(10))

ranked_df.to_csv("data/ranked_exoplanets.csv", index=False)

# numpy section

energy_df = clean_df.dropna(subset=["st_lum", "pl_orbsmax"]).copy()
energy_df = energy_df[energy_df["pl_orbsmax"] > 0].copy()
energy_df = energy_df[energy_df["pl_insol"] > 0].copy()
# print("planets available for energy calculations: ", len(energy_df))
energy_df["calculated_insol"] = (
    np.power(10, energy_df["st_lum"]) /
    np.square(energy_df["pl_orbsmax"])
)
# print(energy_df[["pl_name", "pl_insol", "calculated_insol"]].head(10))

energy_df["percent_difference"] = (
    np.abs(energy_df["calculated_insol"] - energy_df["pl_insol"])
    /
    energy_df["pl_insol"]
) * 100
average_difference = np.mean(energy_df["percent_difference"])
# print("average percent difference:", average_difference)
largest_differences = energy_df.sort_values(
    "percent_difference",
    ascending=False
)
# print(
#     largest_differences [
#         ["pl_name", "pl_insol", "calculated_insol", "percent_difference"]
#     ].head(5)
# )

median_difference = np.median(energy_df["percent_difference"])
# print("average difference:", average_difference)
# print("median difference:", median_difference)


# MATPLOTLIB VISUALIZATIONS

import matplotlib.pyplot as plt

# Color palette
BG = "#0B0F19"
PANEL = "#151B2B"
BLUE = "#54699E"
LIGHT = "#C3CEEB"
GRID = "#334155"

# Global chart styling
plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": PANEL,
    "axes.edgecolor": GRID,
    "axes.labelcolor": LIGHT,
    "text.color": LIGHT,
    "xtick.color": LIGHT,
    "ytick.color": LIGHT,
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "grid.color": GRID,
    "grid.alpha": 0.4,
    "savefig.facecolor": BG
})


# 1. EXOPLANET SCATTER PLOT

fig, ax = plt.subplots(figsize=(11, 7))

ax.scatter(
    candidates_df["pl_insol"],
    candidates_df["pl_rade"],
    color=BLUE,
    alpha=0.75,
    s=65,
    edgecolors=LIGHT,
    linewidths=0.4,
    label="Exoplanet Candidates"
)

# Highlight Earth
ax.scatter(
    1, 1,
    color=LIGHT,
    s=180,
    marker="*",
    label="Earth",
    zorder=5
)

ax.set_title("EXOPLANET DISCOVERY", pad=25)
ax.set_xlabel("Stellar Insolation (Earth = 1)", labelpad=12)
ax.set_ylabel("Planetary Radius (Earth = 1)", labelpad=12)

ax.grid(True, linestyle="--", alpha=0.25)
ax.set_axisbelow(True)

ax.legend(
    facecolor=PANEL,
    edgecolor=GRID,
    labelcolor=LIGHT,
    loc="upper right"
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

plt.savefig(
    "figures/exoplanet_scatter.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# 2. TOP 10 EXOPLANET RANKINGS

top10 = ranked_df.head(10)

fig, ax = plt.subplots(figsize=(11, 7))

bars = ax.barh(
    top10["pl_name"],
    top10["earth_similarity_score"],
    color=BLUE,
    height=0.65,
    alpha=0.9
)

# Highlight the best-ranked candidate
bars[0].set_color(LIGHT)

ax.invert_yaxis()

ax.set_title("TOP 10 EARTH-LIKE EXOPLANETS", pad=25)
ax.set_xlabel("Earth Similarity Score (Lower = Better)", labelpad=12)

# Display scores beside bars
for bar in bars:
    width = bar.get_width()

    ax.text(
        width + 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.3f}",
        va="center",
        color=LIGHT,
        fontsize=10
    )

ax.set_xlim(
    0,
    top10["earth_similarity_score"].max() * 1.2
)

ax.grid(axis="x", linestyle="--", alpha=0.25)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.tight_layout()

plt.savefig(
    "figures/top10_exoplanets.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
