import streamlit as st
import pickle
import requests
from dotenv import load_dotenv
import os

load_dotenv()

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
movies_list = movies["title"].values

API_KEY = os.getenv("TMDB_API_KEY")
debug = os.getenv("DEBUG")

st.title("Movie Recommender System")


selected_movie_name = st.selectbox(
    "Select movie that you like?",
    movies_list,
)


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url, timeout=5)
    data = response.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return None


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        tmdb_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(tmdb_id))
    return recommended_movies, recommended_movies_poster


if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.subheader(name)
            if poster:
                st.image(poster)
            else:
                st.text("Poster not available")
