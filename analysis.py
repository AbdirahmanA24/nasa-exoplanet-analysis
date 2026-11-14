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

# matplotlib section
plt.scatter(
    candidates_df["pl_insol"],
    candidates_df["pl_rade"],
    alpha=0.6,
    color="steelblue",
    label="Exoplanets"
)
plt.scatter(1,1, color="blue", s=100, label="Earth")
plt.xlabel("Insolation (Earth = 1)")
plt.ylabel("Planet Radius (Earth = 1)")
plt.title("Potentially Earth-Like Exoplanets")

plt.grid(True, alpha=0.3)
plt.legend(loc="upper right", bbox_to_anchor=(0,0))
plt.savefig("figures/exoplanet_scatter.png", dpi=300, bbox_inches="tight")
# plt.show()

# second chart
top10 = ranked_df.head(10)
plt.figure(figsize=(10, 6))

plt.barh(
    top10["pl_name"],
    top10["earth_similarity_score"],
    color="steelblue"
)

plt.xlabel("Earth Similarity Score (Lower = Better)")
plt.ylabel("Exoplanet")
plt.title("Top 10 Most Earth-Like Exoplanets")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig(
    "figures/top10_exoplanets.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()