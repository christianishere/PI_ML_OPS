# Importante librerías necesarias
from fastapi import FastAPI
from typing import Optional
from typing import List, Tuple

import pandas as pd

app = FastAPI()

#http://127.0.0.1:8000



@app.get("/")
async def welcome():
    return "Bienvenido !!! Aquí encontrarás tus películas y series favoritas y mucho más !!!"

@app.get("/index")
async def index():
    return "Los cuatro métodos de búsqueda (funciones) son: 1. get_max_duration, 2. get_score_count, 3. get_count_platform y 4. get_actor"



df = pd.read_csv('datasets/full_titles.csv')


# Creando la función 1: película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN
# (la función debe llamarse get_max_duration(year, platform, duration_type))

@app.get("/max_duration")
def get_max_duration(year: Optional[int] = None, platform: Optional[str] = None, duration_type: Optional[str] = 'min'):
    # Crear una copia del DataFrame original para evitar modificar los datos originales
    df_copy = df.copy()
    
    try:

        # Validando plataforma correcta
        if platform is not None and platform.lower() not in ['amazon', 'disney', 'hulu', 'netflix']:
            raise ValueError("La plataforma debe ser amazon, disney, hulu o netflix.")


        # Aplicando los los filtros opcionales si se especifican
        if year is not None:
            df_copy = df_copy[df_copy["release_year"] == year]
        if platform is not None:
            df_copy = df_copy[df_copy["platform"].str.contains(platform, case=False)]
        if duration_type is not None:
            df_copy = df_copy[df_copy["duration_type"] == duration_type]
    
        # Encontrando la película con la mayor duración
        max_duration = df_copy["duration_int"].max()
        max_duration_movie = df_copy[df_copy["duration_int"] == max_duration].iloc[0]
    
        # Creando un diccionario con los datos de la película con mayor duración
        result = {
            "La película con mayor duración es:" : {
            "Título": max_duration_movie["title"],
            "Plataforma": max_duration_movie["platform"],
    #       "Director": max_duration_movie["director"],
    #        "Año": max_duration_movie["release_year"],
            "Duración": f"{max_duration_movie['duration_int']} {max_duration_movie['duration_type']}"
            }
        }
    
        return result

    except ValueError as e:
        return {"error": str(e)}
    

# Creando la función 2: cantidad de películas por plataforma con un puntaje mayor a XX en determinado año
# la función debe llamarse get_score_count(platform, scored, year)

@app.get("/score_count/{platform}/{scored}/{release_year}")
def get_score_count(platform : str, scored : float, release_year: int):

    try:        
        # Validando plataforma correcta
        if platform is not None and platform.lower() not in ['amazon', 'disney', 'hulu', 'netflix']:
            raise ValueError("La plataforma debe ser amazon, disney, hulu o netflix.")
    
        # Filtrar las películas para la plataforma, año y puntaje especificados
        df_filtered = df[(df.platform == platform) & (df.score > scored) & (df.release_year == release_year) & (df.type == 'movie')]

        # Verificar que hay al menos una película que cumpla con los filtros
        if not df_filtered.empty:
            count = df_filtered.groupby('platform').size()
            return count.to_dict()
        else:
            return("No se encontró nigún título con los parámetros ingresados.")

    except ValueError as e:
        return {"error": str(e)}


# Creando la función 3: cantidad de películas por plataforma con filtro de PLATAFORMA.
# La función debe llamarse get_count_platform(platform)

@app.get("/count_platform/{platform}")
def get_count_platform(platform: str):

    try:        
        # Validando plataforma correcta
        if platform is not None and platform.lower() not in ['amazon', 'disney', 'hulu', 'netflix']:
            raise ValueError("La plataforma debe ser amazon, disney, hulu o netflix.")
    
        #Filtrar las películas para la plataforma
        df_filtered = df[df['id'].str.contains(platform[0], case=False)]

        #luego hago un conteo del tamaño del filtro que hice
        count = len(df_filtered)

        return count

    except ValueError as e:
        return {"error": str(e)}
    

# Creando la función 4: actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))

@app.get("/actor")
def get_actor(platform: str, release_year: int) -> Tuple[int, List[str]]:

    # Validando plataforma correcta
    if platform is not None and platform.lower() not in ['amazon', 'disney', 'hulu', 'netflix']:
        raise ValueError("La plataforma debe ser amazon, disney, hulu o netflix.")

    # Filtrar el dataframe por plataforma y año
    df_filtered = df[(df['platform'] == platform) & (df['release_year'] == release_year)]
    
    # Crear una lista con todos los actores en el dataframe filtrado, excluyendo "no data"
    actors_list = [actor.strip() for cast in df_filtered['cast'] for actor in cast.split(',') if actor.strip() != "no data"]
    
    # Contar cuántas veces aparece cada actor en la lista
    actor_counts = {}
    for actor in actors_list:
        if actor in actor_counts:
            actor_counts[actor] += 1
        else:
            actor_counts[actor] = 1
    
    # Calcular la cantidad máxima de apariciones
    max_appearances = max(actor_counts.values())
    
    # Filtrar los actores que aparecen la cantidad máxima de veces, excluyendo "no data"
    most_common_actors = [actor for actor in actor_counts if actor_counts[actor] == max_appearances and actor != "no data"]
    
    # Devolver el resultado como una tupla con la cantidad máxima y la lista de actores
    return max_appearances, most_common_actors
