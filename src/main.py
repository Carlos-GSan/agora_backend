from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, Response,  JSONResponse
from src.routers.movie_router import movie_router
from fastapi import status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), "static/")
templates_path = os.path.join(os.path.dirname(__file__), "templates/")

app.mount("/static", StaticFiles(directory=static_path), "static")
templates = Jinja2Templates(directory=templates_path)

@app.middleware('http')
async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    try:
        return await call_next(request)
    except Exception as e:
        content = f"exc: {str(e)}"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content=content, status_code=status_code)
    

@app.get("/", tags=["Home"])
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'message': 'Welcome'})

## Incluir el router de películas
app.include_router(movie_router, prefix="/movies", tags=["Movies"]) # <-- Agregamos el prefijo y las etiquetas para el router y que solo tengamos que cambiar aqui de ser necesario