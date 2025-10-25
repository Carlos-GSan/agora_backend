import datetime
from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field, field_validator
from typing import List

app = FastAPI()

# Consultar y crear datos
class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str
    
class MovieCreate(BaseModel):
    id: int
    title: str
    overview: str = Field(min_length=15, max_length=500)
    year: int = Field(le=datetime.date.today().year, ge=1900)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=20)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "My Movie",
                "overview": "This is a brief description of my movie.",
                "year": 2010,
                "rating": 8.8,
                "category": "Sci-Fi"
            }
        }
    }

    @field_validator('title')
    def validate_title(cls, value):
        if len(value) < 5 or len(value) > 15:
            raise ValueError('Title must be between 5 and 15 characters long')
        return value
    
    
class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str   

movies: List[Movie] = []

@app.get("/", tags=["Home"])
def home():
    return PlainTextResponse(content="Home", status_code=200)

@app.get("/movies/all", tags=["Movies"], status_code=200, response_description="Nos devuelve una respuesta exitosa")
def get_all_movies() -> List[Movie]:
    content =  [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@app.get("/movies", tags=["Movies"])
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)) -> List[Movie]:
    for movie in movies:
        if movie.category.lower() == category.lower():
            return JSONResponse(content=[movie.model_dump()], status_code=200)
    return JSONResponse(content=[], status_code=404)


## Parámetros de ruta
@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)

@app.post("/movies", tags=["Movies"])
def create_movie(movie: MovieCreate) -> List[Movie]:
    new_movie = Movie(**movie.model_dump())
    movies.append(new_movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)
    

@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for idx, m in enumerate(movies):
        if m.id == id:
            updated_movie = m.model_copy(update=movie.model_dump())
            movies[idx] = updated_movie
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
            break
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)
