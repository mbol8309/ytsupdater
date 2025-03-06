from scrapper import QueryYTS, writeToDB
from dbFilter import MovieQuery, get_filters
from torrent import addMoviesTorrents
from classes import Movie
import inquirer

filename = "movies.sqlite"
movie_select = []

def buscar():
    list_movies = QueryYTS(until=lambda m: m['year']>=2025)
    if len(list_movies) == 0:
        print("No se encontraron peliculas")
        return;
    writeToDB(list_movies, filename)
    

def filtrar():
    movie_query = MovieQuery(filename)
    filters = get_filters()
    movie_query = movie_query.get_movies(filters, Movie.rating.desc())
    format = "{0.title}.{0.year}({0.rating})"
    diccionario = {format.format(m): m for m in movie_query}
    options = [f"{m.title}.{m.year}({m.rating})" for m in movie_query]
    #seleccionar
    pregunta = [inquirer.Checkbox("seleccion", message="Selecciona opciones", choices=options)]
    respuesta = inquirer.prompt(pregunta)
    global movie_select
    movie_select = [diccionario[op] for op in respuesta["seleccion"]]

def descargar():
    addMoviesTorrents(movie_select)    
    
#get films from yts web page
# print("Scrape for new films")
options = ["1. Buscar peliculas", "2. Filtrar peliculas", "3. Descargar peliculas","4. Salir"]
pregunta = [inquirer.List("seleccion", message="Selecciona opciones", choices=options)]
while True:
    respuesta = inquirer.prompt(pregunta)
    if respuesta["seleccion"] == options[0]:
        buscar()
    elif respuesta["seleccion"] == options[1]:
        filtrar()
    elif respuesta["seleccion"] == options[2]:
        descargar()
    elif respuesta["seleccion"] == options[3]:
        exit(0)
    else:
        print("Opción no válida")
        exit(1)








