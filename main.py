from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = 'Mi aplicacion con FastAPI'
app.version = '0.0.1'

class Movie(BaseModel):
    id:Optional[int]=None
    title:str = Field(min_length= 5, max_length=50)
    overview:str = Field(min_length= 5, max_length=50)
    year:int = Field(default=2023, le=2023)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length= 5, max_length=15)

    class Config:
        schema_extra={
            'example':{
            'id':1,
            'title':'Mi Pelicula',
            'overview':'Mi Descrpcion',
            'year':2023,
            'rating':9.8,
            'category':'accion'
            }
        }

movies = [
    {
    'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
    'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    }
]


@app.get('/',tags=['home'])
def message():
    return HTMLResponse('<h1> Hello world </h1>')

@app.get('/movies',tags=['movies'], response_model= List[Movie],status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    return JSONResponse(status_code=200, content=list(filter(lambda item: item['id'] == id, movies)))
    
    '''for item in movies:
        if item['id'] == id:
            return item
    return[]
    '''

@app.get('/movies/',tags=['movies'], response_model= List[Movie])
def get_movies_by_category(category: str =  Query(min_length=5, max_length=15)) -> List[Movie]:
    data= list(filter(lambda item: item['category'] == category, movies))
    return JSONResponse(content=data)
    
    '''for item in movies:
        if item['category'] == category:
            return item
    return []'''

@app.post('/movies',tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie:Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201,content={'message':'Se registro la pelicula'})

@app.put('/movies/{id}',tags={'movies'},response_model=dict, status_code=200)
def update_movie(id:int,movie:Movie) -> dict:
    for item in movies:
        if item['id']==id:
            item['title']=movie.title
            item['overview']=movie.overview
            item['year']=movie.year
            item['rating']=movie.rating
            item['category']=movie.category
            return JSONResponse(status_code=200,content={'message':'Se ha modificado la pelicula'})
        
@app.delete('/movies/{id}',tags={'movies'},response_model=dict,status_code=200)
def delete_movie(id:int) ->dict:
    for item in movies:
        if item['id']==id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={'message':'Se ha eliminado la pelicula'})
