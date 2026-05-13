# =========================================
# IMPORT LIBRARIES
# =========================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="Spotify EDA Dashboard",
    layout="wide"
)

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv("data/cleaned/spotify_cleaned.csv")

# =========================================
# SIDEBAR FILTERS
# =========================================

st.sidebar.header("🎛 Dashboard Filters")

# Genre Filter
genre_list = sorted(df['track_genre'].unique())

selected_genre = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + genre_list
)

# Explicit Content Filter
selected_explicit = st.sidebar.selectbox(
    "Explicit Content",
    ["All", True, False]
)

# Popularity Range Filter
popularity_range = st.sidebar.slider(
    "Popularity Range",
    0,
    100,
    (0, 100)
)

# =========================================
# APPLY FILTERS
# =========================================

filtered_df = df.copy()

# Genre Filter
if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df['track_genre'] == selected_genre
    ]

# Explicit Filter
if selected_explicit != "All":
    filtered_df = filtered_df[
        filtered_df['explicit'] == selected_explicit
    ]

# Popularity Range Filter
filtered_df = filtered_df[
    (filtered_df['popularity'] >= popularity_range[0]) &
    (filtered_df['popularity'] <= popularity_range[1])
]

# =========================================
# DASHBOARD TITLE
# =========================================

st.title("🎵 Spotify Analytics Dashboard")

st.markdown("""
Explore Spotify music trends, audio characteristics,
and popularity insights using interactive visualizations.
""")

# =========================================
# KPI SECTION
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Tracks",
    len(filtered_df)
)

col2.metric(
    "Average Popularity",
    round(filtered_df['popularity'].mean(), 2)
)

col3.metric(
    "Average Danceability",
    round(filtered_df['danceability'].mean(), 2)
)

col4.metric(
    "Average Energy",
    round(filtered_df['energy'].mean(), 2)
)

# =========================================
# POPULARITY DISTRIBUTION
# =========================================

st.subheader("📊 Popularity Distribution")

fig, ax = plt.subplots(figsize=(12, 5))

sns.histplot(
    filtered_df['popularity'],
    bins=30,
    kde=True,
    ax=ax
)

ax.set_title("Distribution of Track Popularity")
ax.set_xlabel("Popularity")
ax.set_ylabel("Count")

st.pyplot(fig)

# =========================================
# TOP GENRES BY AVERAGE POPULARITY
# =========================================

st.subheader("🎼 Top Genres by Average Popularity")

# Calculate top genres
top_genres = (
    filtered_df.groupby('track_genre')['popularity']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Create figure
fig2, ax2 = plt.subplots(figsize=(12, 6))

# Create barplot
sns.barplot(
    x=top_genres.values,
    y=top_genres.index,
    ax=ax2
)

# Titles and labels
ax2.set_title("Top 10 Genres by Average Popularity")
ax2.set_xlabel("Average Popularity")
ax2.set_ylabel("Genre")

# Display chart
st.pyplot(fig2)

# =========================================
# POPULARITY VS DANCEABILITY
# =========================================

st.subheader("💃 Popularity vs Danceability")

# Create figure
fig3, ax3 = plt.subplots(figsize=(12, 6))

# Scatterplot
sns.scatterplot(
    data=filtered_df,
    x='danceability',
    y='popularity',
    alpha=0.5,
    ax=ax3
)

# Titles and labels
ax3.set_title("Popularity vs Danceability")
ax3.set_xlabel("Danceability")
ax3.set_ylabel("Popularity")

# Display chart
st.pyplot(fig3)


# =========================================
# CORRELATION HEATMAP
# =========================================

st.subheader("🔥 Correlation Heatmap")

# Select numerical columns
numerical_df = filtered_df.select_dtypes(
    include=['int64', 'float64']
)

# Correlation matrix
corr_matrix = numerical_df.corr()

# Create figure
fig4, ax4 = plt.subplots(figsize=(12, 8))

# Heatmap
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    ax=ax4
)

# Title
ax4.set_title("Correlation Heatmap")

# Display chart
st.pyplot(fig4)

# =========================================
# KEY INSIGHTS SECTION
# =========================================

st.markdown("---")

st.subheader("📌 Key Insights")

st.markdown("""
- High-popularity tracks generally exhibit moderate-to-high danceability and energy levels.

- Spotify track popularity is influenced by multiple interacting audio characteristics rather than a single dominant feature.

- Genres such as K-pop, pop-film, and chill demonstrate strong popularity performance.

- Danceability and energy show moderate positive relationships across tracks.

- Listener engagement patterns vary significantly across different genres and musical styles.
""")

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption(
    "Spotify EDA Dashboard | Built with Streamlit, Python, Pandas, and Seaborn 🚀"
)