import streamlit as st
import pickle
import pandas as pd
import requests

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

def join_words_with_hyphen(input_string):
    words = input_string.split()
    return '-'.join(words)


st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    movie_link = list(join_words_with_hyphen(i) for i in recommended_movie_names)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        # st.image(recommended_movie_posters[0])
        st.markdown(f'<a href="https://moviesmod.band/download-{movie_link[0]}" target="_blank"><img src="{recommended_movie_posters[0]}" width="150"/></a>', unsafe_allow_html=True)

    with col2:
        st.text(recommended_movie_names[1])
        st.markdown(f'<a href="https://moviesmod.band/download-{movie_link[1]}" target="_blank"><img src="{recommended_movie_posters[1]}" width="150"/></a>', unsafe_allow_html=True)

    with col3:
        st.text(recommended_movie_names[2])
        st.markdown(f'<a href="https://moviesmod.band/download-{movie_link[2]}" target="_blank"><img src="{recommended_movie_posters[2]}" width="150"/></a>', unsafe_allow_html=True)

    with col4:
        st.text(recommended_movie_names[3])
        st.markdown(f'<a href="https://moviesmod.band/download-{movie_link[3]}" target="_blank"><img src="{recommended_movie_posters[3]}" width="150"/></a>', unsafe_allow_html=True)

    with col5:
        st.text(recommended_movie_names[4])
        st.markdown(f'<a href="https://moviesmod.band/download-{movie_link[4]}" target="_blank"><img src="{recommended_movie_posters[4]}" width="150"/></a>', unsafe_allow_html=True)
