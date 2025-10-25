from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler

app = FastAPI()

app.add_middleware(HTTPErrorHandler)


@app.get("/", tags=["Home"])
def home():
    return PlainTextResponse(content="Home", status_code=200)

## Incluir el router de películas
app.include_router(movie_router, prefix="/movies", tags=["Movies"]) # <-- Agregamos el prefijo y las etiquetas para el router y que solo tengamos que cambiar aqui de ser necesario