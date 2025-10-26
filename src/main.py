from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, Response,  JSONResponse
from src.routers.movie_router import movie_router
from fastapi import status

app = FastAPI()

@app.middleware('http')
async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    try:
        return await call_next(request)
    except Exception as e:
        content = f"exc: {str(e)}"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content=content, status_code=status_code)
    

@app.get("/", tags=["Home"])
def home():
    return PlainTextResponse(content="Home", status_code=200)

## Incluir el router de películas
app.include_router(movie_router, prefix="/movies", tags=["Movies"]) # <-- Agregamos el prefijo y las etiquetas para el router y que solo tengamos que cambiar aqui de ser necesario