
from typing import List
from fastapi import Path, Query, APIRouter
from fastapi.responses import JSONResponse
from src.models.movie_model import Movie, MovieCreate, MovieUpdate

movie_router = APIRouter()

movies: List[Movie] = []

@movie_router.get("/all", status_code=200, response_description="Nos devuelve una respuesta exitosa")
def get_all_movies() -> List[Movie]:
    """Nos devuelve todas las películas"""
    content =  [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@movie_router.get("/")
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)) -> List[Movie]:
    for movie in movies:
        if movie.category.lower() == category.lower():
            return JSONResponse(content=[movie.model_dump()], status_code=200)
    return JSONResponse(content=[], status_code=404)


## Parámetros de ruta
@movie_router.get("/{id}")
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)

@movie_router.post("/")
def create_movie(movie: MovieCreate) -> List[Movie]:
    new_movie = Movie(**movie.model_dump())
    movies.append(new_movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)
    

@movie_router.put("/{id}")
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for idx, m in enumerate(movies):
        if m.id == id:
            updated_movie = m.model_copy(update=movie.model_dump())
            movies[idx] = updated_movie
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@movie_router.delete("/{id}")
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
            break
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)
