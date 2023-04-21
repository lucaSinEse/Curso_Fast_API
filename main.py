from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.title = 'Mi aplicacin con FastAPI'
app.version = '0.0.1'

class Movie(BaseModel):
    id:Optional[int]=None
    title:str
    overview:str
    year:int
    rating:float
    category:str

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

@app.get('/movies',tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id:int):
    return list(filter(lambda item: item['id'] == id, movies))
    
    '''for item in movies:
        if item['id'] == id:
            return item
    return[]
    '''

@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category: str):
    
    return list(filter(lambda item: item['category'] == category, movies))
    
    '''for item in movies:
        if item['category'] == category:
            return item
    return []'''

@app.post('/movies',tags=['movies'])
def create_movie(movie:Movie):
    movies.append(movie)
    return movies

@app.put('/movies/{id}',tags={'movies'})
def update_movie(id:int,movie:Movie):
    for item in movies:
        if item['id']==id:
            item['title']=movie.title
            item['overview']=movie.overview
            item['year']=movie.year
            item['rating']=movie.rating
            item['category']=movie.category
            return movies
        
@app.delete('/movies/{id}',tags={'movies'})
def delete_movie(id:int):
    for item in movies:
        if item['id']==id:
            movies.remove(item)
            return movies
