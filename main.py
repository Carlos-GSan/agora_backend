from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

movies = [
    {
        "id": 1, 
        "title": "Inception", 
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.", 
        "year": 2010,
        "rating": 8.8,
        "category": "Sci-Fi"
    },
    {
        "id": 2, 
        "title": "The Matrix", 
        "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", 
        "year": 1999,
        "rating": 8.7,
        "category": "Action"
    },
    {
        "id": 3, 
        "title": "Interstellar", 
        "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", 
        "year": 2014,
        "rating": 8.6,
        "category": "Adventure"
    }
]

@app.get("/", tags=["Home"])
def home():
    return {"Hello": "Welcome to the Movie API!"}

@app.get("/movies", tags=["Movies"])
def get_movies():
    return movies


## Parámetros de ruta
@app.get("/movies/{movie_id}", tags=["Movies"])
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return {"Error": "Movie not found"}

## Parámetros de query
@app.get("/movies/", tags=["Movies"])
def get_movies_by_category(category: str, year: int = None):
    filtered_movies = [movie for movie in movies if movie["category"] == category]
    if year:
        filtered_movies = [movie for movie in filtered_movies if movie["year"] == year]
    return filtered_movies
