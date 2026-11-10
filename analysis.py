import pandas as pd
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
print(ranked_df[["pl_name", "earth_similarity_score"]].head(10))

ranked_df.to_csv("data/ranked_exoplanets.csv", index=True)