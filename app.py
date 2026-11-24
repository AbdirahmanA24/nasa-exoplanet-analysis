
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Exoplanet Explorer",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Color palette
BG = "#0B0F19"
PANEL = "#151B2B"
BLUE = "#54699E"
LIGHT = "#C3CEEB"
MUTED = "#8493B5"
GRID = "#263249"

# Custom styling and background animations
st.html("""
<style>

.stApp {
    background: radial-gradient(
        ellipse at bottom,
        #172238 0%,
        #0B0F19 50%,
        #05070D 100%
    );
    color: #C3CEEB;
}

/* Animated background stars */
.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
}

.stApp::before {
    background-image:
        radial-gradient(1px 1px at 25px 40px, white 99%, transparent),
        radial-gradient(1px 1px at 120px 160px, #C3CEEB 99%, transparent),
        radial-gradient(1px 1px at 200px 80px, #54699E 99%, transparent),
        radial-gradient(1px 1px at 70px 210px, white 99%, transparent),
        radial-gradient(1px 1px at 230px 190px, #C3CEEB 99%, transparent);

    background-size: 280px 280px;
    opacity: 0.45;
    animation: starDrift 120s linear infinite;
}

.stApp::after {
    background-image:
        radial-gradient(2px 2px at 80px 120px, #C3CEEB 99%, transparent),
        radial-gradient(1px 1px at 270px 240px, white 99%, transparent),
        radial-gradient(1px 1px at 160px 310px, white 99%, transparent);

    background-size: 380px 380px;
    animation: twinkle 6s ease-in-out infinite alternate;
}

@keyframes starDrift {
    from { background-position: 0 0; }
    to { background-position: 0 -280px; }
}

@keyframes twinkle {
    from { opacity: 0.15; }
    to { opacity: 0.65; }
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes glow {
    from {
        text-shadow: 0 0 15px rgba(84, 105, 158, 0.2);
    }
    to {
        text-shadow: 0 0 35px rgba(84, 105, 158, 0.65);
    }
}

/* Page layout */
[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding: 3rem 2rem;
    margin: 0 auto;
    box-sizing: border-box;
    position: relative;
    z-index: 1;
    animation: fadeIn 0.8s ease-out;
}

/* Main header */
.hero {
    text-align: center;
    padding: 65px 20px 55px;
    margin-bottom: 35px;
    background: radial-gradient(
        ellipse at center,
        rgba(84, 105, 158, 0.14),
        transparent 70%
    );
}

.hero-tag {
    color: #8493B5;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.hero h1.hero-title {
    font-size: clamp(42px, 6vw, 76px);
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.1;
    color: #C3CEEB;
    margin: 0;
    padding: 0;
    animation: glow 5s ease-in-out infinite alternate;
}

.hero-accent {
    color: #849BCF;
}

.hero-description {
    color: #8493B5;
    font-size: 16px;
    line-height: 1.8;
    max-width: 700px;
    margin: 25px auto;
}

.hero-line {
    width: 90px;
    height: 2px;
    background: linear-gradient(
        90deg,
        transparent,
        #C3CEEB,
        transparent
    );
    margin: 30px auto 0;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        rgba(21, 27, 43, 0.9),
        rgba(11, 15, 25, 0.75)
    );

    border: 1px solid rgba(84, 105, 158, 0.35);
    border-radius: 16px;
    padding: 25px 22px;
    min-height: 125px;
    backdrop-filter: blur(12px);

    transition:
        transform 0.3s ease,
        border-color 0.3s ease,
        box-shadow 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: #54699E;
    box-shadow: 0 8px 30px rgba(84, 105, 158, 0.2);
}

[data-testid="stMetricLabel"] {
    color: #8493B5;
}

[data-testid="stMetricValue"] {
    color: #C3CEEB;
    font-size: 36px;
    font-weight: 700;
}

/* Charts and tables */
[data-testid="stPlotlyChart"] {
    background: rgba(21, 27, 43, 0.7);
    border: 1px solid rgba(84, 105, 158, 0.25);
    border-radius: 16px;
    padding: 10px;
    backdrop-filter: blur(8px);
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(84, 105, 158, 0.35);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stTextInput"] input {
    border-radius: 10px;
    color: #C3CEEB;
}

/* Download button */
.stDownloadButton button {
    background: linear-gradient(
        135deg,
        #54699E,
        #35466F
    );
    color: #E4EBFF;
    border: 1px solid #7187B8;
    border-radius: 10px;
    padding: 10px 25px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stDownloadButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 25px rgba(84, 105, 158, 0.4);
    border-color: #C3CEEB;
    color: white;
}

[data-testid="stExpander"] {
    background: rgba(21, 27, 43, 0.65);
    border: 1px solid rgba(84, 105, 158, 0.3);
    border-radius: 12px;
    margin-bottom: 12px;
}

hr {
    border-color: rgba(84, 105, 158, 0.2);
    margin: 35px 0;
}

.footer {
    text-align: center;
    padding: 35px 15px;
    color: #8493B5;
    font-size: 12px;
    line-height: 2;
}

/* Adjust spacing on smaller screens */
@media (max-width: 768px) {
    .block-container {
        padding: 2rem 1rem;
    }

    .hero {
        padding: 40px 10px;
    }

    [data-testid="stMetric"] {
        padding: 15px;
    }

    [data-testid="stMetricValue"] {
        font-size: 26px;
    }
}

/* Respect reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation: none !important;
        transition: none !important;
    }
}

</style>
""")


# Cache datasets to avoid reading CSV files on every rerun
@st.cache_data
def load_data():
    df = pd.read_csv("data/exoplanets.csv")
    ranked_df = pd.read_csv("data/ranked_exoplanets.csv")

    ranked_df = ranked_df.sort_values(
        "earth_similarity_score"
    ).reset_index(drop=True)

    return df, ranked_df


df, ranked_df = load_data()

clean_df = df.dropna(subset=["pl_rade", "pl_insol"])

if ranked_df.empty:
    st.error("No candidate planets were found in the ranked dataset.")
    st.stop()


# Calculate insolation using stellar luminosity and orbital distance
energy_df = clean_df.dropna(
    subset=["st_lum", "pl_orbsmax"]
).copy()

energy_df = energy_df[
    (energy_df["pl_orbsmax"] > 0) &
    (energy_df["pl_insol"] > 0)
].copy()

energy_df["calculated_insol"] = (
    np.power(10, energy_df["st_lum"]) /
    np.square(energy_df["pl_orbsmax"])
)

# Compare calculated insolation with recorded NASA values
energy_df["percent_difference"] = (
    np.abs(
        energy_df["calculated_insol"] -
        energy_df["pl_insol"]
    ) / energy_df["pl_insol"]
) * 100

average_difference = np.mean(energy_df["percent_difference"])
median_difference = np.median(energy_df["percent_difference"])


# Apply consistent styling to both Plotly charts
def style_chart(fig, height=450):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial",
            color=LIGHT,
            size=12
        ),
        margin=dict(l=25, r=30, t=40, b=30),
        hoverlabel=dict(
            bgcolor=PANEL,
            bordercolor=BLUE,
            font_color=LIGHT
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=LIGHT),
            orientation="h",
            y=1.12
        )
    )

    fig.update_xaxes(
        gridcolor=GRID,
        zeroline=False,
        linecolor=GRID,
        title_font=dict(color=LIGHT),
        automargin=True
    )

    fig.update_yaxes(
        gridcolor=GRID,
        zeroline=False,
        linecolor=GRID,
        title_font=dict(color=LIGHT),
        automargin=True
    )

    return fig


# Main page header
st.html("""
<div class="hero">
    <div class="hero-tag">
        NASA Exoplanet Archive
    </div>

    <h1 class="hero-title">
        Exoplanet <span class="hero-accent">Explorer</span>
    </h1>

    <div class="hero-description">
        Explore planets beyond our solar system and discover
        how their physical characteristics compare to Earth.
    </div>

    <div class="hero-line"></div>
</div>
""")


# Summary statistics
st.header("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Exoplanets", f"{len(df):,}")
col2.metric("Valid Records", f"{len(clean_df):,}")
col3.metric("Potential Candidates", len(ranked_df))
col4.metric(
    "Best Similarity Score",
    f"{ranked_df['earth_similarity_score'].min():.3f}"
)

st.divider()

st.header("Planetary Analysis")

chart1, chart2 = st.columns(2)

# Scatter plot of candidate planets
with chart1:
    st.subheader("Exoplanet Distribution")
    st.caption("Hover over a planet to view its measurements.")

    fig = px.scatter(
        ranked_df,
        x="pl_insol",
        y="pl_rade",
        hover_name="pl_name",
        hover_data={
            "pl_insol": ":.3f",
            "pl_rade": ":.3f",
            "earth_similarity_score": ":.3f"
        },
        labels={
            "pl_insol": "Insolation (Earth = 1)",
            "pl_rade": "Radius (Earth = 1)",
            "earth_similarity_score": "Similarity Score"
        }
    )

    fig.update_traces(
        name="Candidates",
        showlegend=True,
        marker=dict(
            color=BLUE,
            size=11,
            opacity=0.9,
            line=dict(color=LIGHT, width=0.7)
        )
    )

    # Earth reference point
    fig.add_scatter(
        x=[1],
        y=[1],
        mode="markers",
        name="Earth",
        marker=dict(
            color=LIGHT,
            size=19,
            symbol="star"
        ),
        hovertemplate=(
            "<b>Earth</b><br>"
            "Radius: 1.000<br>"
            "Insolation: 1.000"
            "<extra></extra>"
        )
    )

    # Reference lines for Earth's radius and insolation
    fig.add_vline(
        x=1,
        line_dash="dot",
        line_color=MUTED,
        opacity=0.35
    )

    fig.add_hline(
        y=1,
        line_dash="dot",
        line_color=MUTED,
        opacity=0.35
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        width="stretch",
        theme=None,
        config={"displaylogo": False}
    )


# Rank the ten candidates with the lowest similarity scores
with chart2:
    st.subheader("Top 10 Candidates")
    st.caption("Lower scores indicate greater similarity to Earth.")

    top10 = ranked_df.head(10)

    fig2 = px.bar(
        top10,
        x="earth_similarity_score",
        y="pl_name",
        orientation="h",
        text_auto=".3f",
        labels={
            "earth_similarity_score": "Similarity Score",
            "pl_name": ""
        }
    )

    # Highlight the highest-ranked planet
    bar_colors = [
        LIGHT if i == 0 else BLUE
        for i in range(len(top10))
    ]

    fig2.update_traces(
        marker_color=bar_colors,
        textposition="outside",
        textfont=dict(color=LIGHT, size=11),
        cliponaxis=False
    )

    fig2.update_yaxes(
        autorange="reversed",
        showgrid=False
    )

    fig2.update_xaxes(
        range=[
            0,
            max(0.1, top10["earth_similarity_score"].max() * 1.25)
        ]
    )

    fig2 = style_chart(fig2)

    st.plotly_chart(
        fig2,
        width="stretch",
        theme=None,
        config={"displaylogo": False}
    )

st.divider()


# Display the highest-ranked candidate
st.header("Featured Exoplanet")

best_planet = ranked_df.iloc[0]

st.subheader(best_planet["pl_name"])

col1, col2, col3 = st.columns(3)

col1.metric(
    "Planetary Radius",
    f"{best_planet['pl_rade']:.3f} R⊕"
)

col2.metric(
    "Stellar Insolation",
    f"{best_planet['pl_insol']:.3f} S⊕"
)

col3.metric(
    "Similarity Score",
    f"{best_planet['earth_similarity_score']:.3f}"
)

st.caption(
    "The highest-ranked candidate based on radius and "
    "insolation alone. Habitability is not confirmed."
)

st.divider()


# Search and filter candidate planets
st.header("Explore Exoplanets")

search = st.text_input(
    "Planet Name",
    placeholder="Search for an exoplanet..."
)

col1, col2 = st.columns(2)

with col1:
    radius_range = st.slider(
        "Planetary Radius (Earth Units)",
        min_value=0.0,
        max_value=1.8,
        value=(0.0, 1.8),
        step=0.05
    )

with col2:
    insolation_range = st.slider(
        "Stellar Insolation (Earth Units)",
        min_value=0.35,
        max_value=1.5,
        value=(0.35, 1.5),
        step=0.05
    )

# Filter candidates using the selected ranges
filtered_df = ranked_df[
    (ranked_df["pl_rade"] >= radius_range[0]) &
    (ranked_df["pl_rade"] <= radius_range[1]) &
    (ranked_df["pl_insol"] >= insolation_range[0]) &
    (ranked_df["pl_insol"] <= insolation_range[1])
].copy()

if search:
    filtered_df = filtered_df[
        filtered_df["pl_name"].str.contains(
            search,
            case=False,
            regex=False,
            na=False
        )
    ]

st.caption(
    f"Showing {len(filtered_df)} of {len(ranked_df)} candidates."
)

# Select and rename columns for display
display_df = filtered_df[
    ["pl_name", "pl_rade", "pl_insol", "earth_similarity_score"]
].rename(columns={
    "pl_name": "Exoplanet",
    "pl_rade": "Radius",
    "pl_insol": "Insolation",
    "earth_similarity_score": "Similarity Score"
})

if filtered_df.empty:
    st.info("No planets match the selected filters.")

else:
    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
        height=420,
        column_config={
            "Radius": st.column_config.NumberColumn(
                format="%.3f"
            ),
            "Insolation": st.column_config.NumberColumn(
                format="%.3f"
            ),
            "Similarity Score": st.column_config.NumberColumn(
                format="%.3f"
            )
        }
    )

    st.download_button(
        label="Download CSV",
        data=filtered_df.to_csv(index=False),
        file_name="exoplanet_candidates.csv",
        mime="text/csv"
    )

st.divider()


# Results from the NumPy insolation analysis
st.header("Insolation Analysis")

st.write(
    "Comparison of calculated stellar insolation "
    "against recorded NASA measurements."
)

col1, col2, col3 = st.columns(3)

col1.metric("Planets Compared", f"{len(energy_df):,}")
col2.metric("Mean Discrepancy", f"{average_difference:.2f}%")
col3.metric("Median Discrepancy", f"{median_difference:.2f}%")

st.write(
    "The mean discrepancy is influenced by extreme outliers. "
    "Differences may result from measurement uncertainties, "
    "inconsistent source parameters, or assumptions in the model."
)

with st.expander("Largest Insolation Discrepancies"):

    largest_differences = energy_df.sort_values(
        "percent_difference",
        ascending=False
    ).head(5)

    discrepancy_table = largest_differences[
        ["pl_name", "pl_insol", "calculated_insol", "percent_difference"]
    ].rename(columns={
        "pl_name": "Exoplanet",
        "pl_insol": "NASA Insolation",
        "calculated_insol": "Calculated Insolation",
        "percent_difference": "Relative Discrepancy (%)"
    })

    st.dataframe(
        discrepancy_table,
        hide_index=True,
        width="stretch"
    )

st.divider()


# Explain the screening criteria and calculations
st.header("Methodology")

with st.expander("Data Cleaning and Filtering"):
    st.markdown("""
The dataset was processed using Pandas to remove incomplete
records and identify potential candidates.

**Selection criteria:**

- Valid planetary radius and insolation measurements.
- Planetary radius of 1.8 Earth radii or less.
- Stellar insolation between 0.35 and 1.5 Earth flux.

These thresholds are simplified screening criteria rather
than definitive indicators of habitability.
    """)

with st.expander("Earth Similarity Score"):
    st.latex(r"S = |R_p - 1| + |I_p - 1|")

    st.markdown("""
- **S:** Similarity deviation score.
- **R:** Planetary radius relative to Earth.
- **I:** Stellar insolation relative to Earth.

Candidates are ranked by their combined deviation from
Earth's radius and insolation. Lower scores indicate
greater similarity across these two measurements.
    """)

with st.expander("Insolation Calculations"):
    st.latex(r"I = \frac{10^{L}}{a^2}")

    st.markdown("""
- **I:** Estimated insolation in Earth flux.
- **L:** Base-10 logarithm of stellar luminosity relative to the Sun.
- **a:** Orbital semi-major axis in astronomical units.

NumPy was used to calculate insolation across the dataset
and compare the results against NASA's recorded values.
    """)

    st.latex(
        r"D = \frac{|I_{calc} - I_{NASA}|}{I_{NASA}} \times 100"
    )

    st.write(
        "The relative discrepancy measures the percentage "
        "deviation from NASA's recorded insolation."
    )

with st.expander("Limitations"):
    st.markdown("""
This project is an exploratory analysis, not a validated
planetary habitability model.

Factors not considered include:

- Atmospheric composition
- Surface temperature and pressure
- Presence of liquid water
- Stellar radiation
- Orbital eccentricity
- Planetary mass and composition

NASA composite records may contain measurements from
different publications. This may contribute to the
observed insolation discrepancies.

Recorded NASA insolation values are retained for
candidate selection and ranking.
    """)

with st.expander("Data Source and Tools"):
    st.markdown("""
**Dataset:** [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)

**Tools:** Python, Pandas, NumPy, Matplotlib,
Plotly, Streamlit and CSS.
    """)

st.divider()

# Page footer
st.html("""
<div class="footer">
    <p>Exoplanet Explorer · V1.0</p>
    <p>Developed by Abdirahman Ahmed</p>
    <p>Data provided by the NASA Exoplanet Archive</p>
</div>
""")