from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse, Response,  JSONResponse
from src.routers.movie_router import movie_router
from fastapi import status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
import os

def dependency1():
    print("Global Dependency 1")
    
def dependency2():
    print("Global Dependency 2")

app = FastAPI(dependencies=[Depends(dependency1), Depends(dependency2)])

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

# def common_parameters(start_date: str, end_date: str):
#     return {"start_date": start_date, "end_date": end_date}

# CommonDep = Annotated[dict, Depends(common_parameters)]

class CommonDep:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start_date = start_date
        self.end_date = end_date

@app.get('/users')
def get_users(commons: CommonDep = Depends()):
    return f"Users created between {commons.start_date} and {commons.end_date}"

@app.get('/customers')
def get_customers(commons: CommonDep = Depends()):
    return f"Customers created between {commons.start_date} and {commons.end_date}"

## Incluir el router de películas
app.include_router(movie_router, prefix="/movies", tags=["Movies"]) # <-- Agregamos el prefijo y las etiquetas para el router y que solo tengamos que cambiar aqui de ser necesario