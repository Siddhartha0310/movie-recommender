import streamlit as st
import pickle
import pandas as pd
import requests

with open('movies.pkl', 'rb') as f:
    movies_list = pickle.load(f)
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

import requests  # Ensure this is imported at the top of your file

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MjdmM2E0ZGI5ODIwNWRiNGM2MmFmNWM0OTNiN2M5YiIsIm5iZiI6MTc2MTgyODI1OS4xMTEsInN1YiI6IjY5MDM1ZGEzYzdlMDFmMTllZTA5Y2U1MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.raj4Qo15RkGW6hsDq5LQBcoY4-IcJh6zysQyJFooaDw"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for bad status codes (e.g., 401 for auth issues)
        data = response.json()
        
        poster_path = data.get('poster_path')  # Safe access; returns None if missing
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"  # Fallback placeholder
    
    except requests.exceptions.RequestException as e:
        print(f"API request failed for movie ID {movie_id}: {e}")  # Log error (or use Streamlit's st.error if in app)
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"  # Error fallback
    except KeyError as e:
        print(f"Unexpected response structure: {e}")
        return "https://via.placeholder.com/500x750?text=Invalid+Data"    

def recommend(movie):
    movie_index= movies_list[movies_list['title']==movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_movie=[]
    recommend_posters=[]
    for i in movie_list:
        movie_id=movies_list.iloc[i[0]].movie_id
        recommend_movie.append(movies_list.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
    return recommend_movie ,recommend_posters


st.title("Movie Recommender system ")

selected_movie_name = st.selectbox('Enter the movie you wanna watch',movies_list['title'].values)

if st.button('Recommend'):
    name,poster= recommendation=recommend(selected_movie_name)
    
    col1, col2,col3,col4,col5 = st.columns(5)

    with col1:
     st.header(name[0])
     st.image(poster[0])

    with col2:
     st.header(name[1])
     st.image(poster[1])

    with col3:
     st.header(name[2])
     st.image(poster[2])

    with col4:
     st.header(name[3])
     st.image(poster[3])

    with col5:
      st.header(name[4])
      st.image(poster[4])

        