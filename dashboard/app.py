import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "netflix_titles.csv")

df = pd.read_csv(file_path)

st.title("Netflix Project Dashboard")


df_copy = df.copy()

sns.set_style("whitegrid")

st.subheader("Sample Data")
st.dataframe(df_copy.head(20))



selected_type = st.selectbox("Select Type", df_copy["type"].unique())

filtered_data = df_copy[df_copy["type"] == selected_type]

data = filtered_data.groupby(["release_year", "type"]).size().reset_index(name="count")

st.subheader("Content Growth Over Years")
fig, ax = plt.subplots()

sns.lineplot(x="release_year", y="count", hue="type", data=data, ax=ax)

st.pyplot(fig)

st.markdown("---")

filtered_data["split_genre"] = filtered_data["listed_in"].fillna("").str.split(", ")

exploded_genre = filtered_data.explode("split_genre").dropna()

top_10_genres = exploded_genre["split_genre"].value_counts().head(10)


fig2, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=top_10_genres.values, y=top_10_genres.index, ax=ax, hue=top_10_genres, palette="viridis")
ax.tick_params(axis='x', rotation=45)





filtered_data["clean_dir"] = filtered_data["director"].fillna("").str.split(", ")

exploded_dirs = filtered_data.explode("clean_dir")
exploded_dirs = exploded_dirs[exploded_dirs["clean_dir"] != ""]

top_10_dirs = exploded_dirs["clean_dir"].value_counts().head(10)


fig3, ax = plt.subplots(figsize=(10,6))
sns.barplot(x=top_10_dirs.values, y=top_10_dirs.index, ax=ax , hue=top_10_dirs, palette="plasma")

col1, col2 = st.columns([3, 3])  

with col1:
    st.subheader("Top 10 Genres")
    st.pyplot(fig2)

with col2:
    st.subheader("Top 10 Directors")
    st.pyplot(fig3)

st.markdown("---") 


#  Graph 4
selected_country = st.selectbox(
    "Sample Movies from Selected Country",
    filtered_data["country"].dropna().unique()
)
filtered_country = filtered_data[filtered_data["country"] == selected_country]

top_10_countries = filtered_data["country"].value_counts().head(10)
st.write(filtered_country[["title", "release_year", "duration"]].head(10))

st.subheader("Top 10 Countries")

fig4, ax = plt.subplots(figsize=(10,6))
sns.barplot(x=top_10_countries.index, y = top_10_countries.values, ax=ax, hue = top_10_countries, palette="Oranges")
ax.tick_params(axis='x', rotation=45)

st.pyplot(fig4)

selected_title = st.selectbox(
    "Selected Title Details",
    filtered_data["title"].dropna().unique()
)

filtered_title = filtered_data[filtered_data["title"] == selected_title]
st.write(filtered_title[["title", "type", "release_year", "duration", "country"]])


actor_name = st.text_input("Search by Actor or Actress")

if actor_name:
    actor_filter = filtered_data[
        filtered_data["cast"].fillna("").str.contains(actor_name, case=False)
        ]
    
    st.subheader(f"Results for '{actor_name}'")
    st.write(actor_filter[["title", "release_year", "type", "country"]])
    




