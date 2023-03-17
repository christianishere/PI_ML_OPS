# Importante librerías necesarias
from fastapi import FastAPI
from typing import Optional
import pandas as pd
#from pydantic import BaseModel

app = FastAPI()

#http://127.0.0.1:8000

#para hacer validación de datos con biblioteca BaseModel
#class Libro(BaseModel):
#        titulo: str
#        autor: str
#        paginas: int
#        editorial: str


@app.get("/")
async def welcome():
    return "Bienvenido !! Ud encontrará aquí sus películas y series favoritas y mucho más !!!"

@app.get("/index")
async def index():
    return "Los cuatro métodos de búsqueda (funciones) son las funciones 1. get_max_duration, 2. get_score_count, 3. get_count_platform y 4. get_actor"



df = pd.read_csv('datasets/full_titles.csv')





@app.get("/max_duration")
def get_max_duration(year: Optional[int] = None, platform: Optional[str] = None, duration_type: Optional[str] = 'min'):
    # Crear una copia del DataFrame original para evitar modificar los datos originales
    df_copy = df.copy()
    
    # Aplicar los filtros opcionales si se especifican
    if year is not None:
        df_copy = df_copy[df_copy["release_year"] == year]
    if platform is not None:
        df_copy = df_copy[df_copy["platform"].str.contains(platform, case=False)]
    if duration_type is not None:
        df_copy = df_copy[df_copy["duration_type"] == duration_type]
    
    # Encontrar la película con la mayor duración
    max_duration = df_copy["duration_int"].max()
    max_duration_movie = df_copy[df_copy["duration_int"] == max_duration].iloc[0]
    
    # Crear un diccionario con los datos de la película con mayor duración
    result = {
        "Título": max_duration_movie["title"],
        "Plataforma": max_duration_movie["platform"],
    #    "Director": max_duration_movie["director"],
    #    "Año": max_duration_movie["release_year"],
        "Duración": f"{max_duration_movie['duration_int']} {max_duration_movie['duration_type']}"
    }
    
    return result

#@app.get("/max_duration2")
#async def get_max_duration(year: Optional[int] = None, platform: Optional[str] = None, duration_type: Optional[str] = 'min'):

#    if duration_type is not None and duration_type not in ['min', 'season']:
#        return("La duración debe ser una de las siguientes: min, season")
    
    # Filtramos por solo peliculas (NOTA: Según una consulta de sli.do este paso no debe de ser realizado)
    # df_movies = df[df.type == 'movie']

#    df_movies = df

    # Aplicar los filtros OPCIONALES
#    if year:
#         df_movies = df_movies[df_movies.release_year == year]

#    if platform:
        # Pasamos platform a minusculas por si un usuario lo escribe en mayusculas
#        platform = platform.lower()
        # Controlamos que la plataforma ingresada sea correcta
#        platforms = ["amazon", "disney", "hulu", "netflix"]
#        if platform not in platforms:
#            return ("Plataforma incorrecta! Debe ingresar una de las siguientes: amazon, disney, hulu, netflix")
#        df_movies = df_movies[df_movies.platform == platform]

#    if duration_type:
        # Controlamos que el duration_type sea valido
#        duration_type = duration_type.lower()
#        df_movies = df_movies[df_movies.duration_type == duration_type]

#    if not df_movies.empty:
#        max_duration_movie = df_movies.sort_values('duration_int', ascending=False).iloc[0]['title']
#    else:
#        return("No se encontró ninguna pelicula con los parametros dados.")    

#    return {"Película de mayor duración": max_duration_movie}
