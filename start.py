#!/usr/bin/env python3
from scrapper import QueryYTS, writeToDB
from dbFilter import MovieQuery, get_filters
from torrent import addMoviesTorrents, cleanTorrents
from classes import Movie
from configs import Config
import inquirer
import argparse
from dotenv import load_dotenv
load_dotenv()

config = Config()
filename = config.sqlite_filename
movie_query = MovieQuery(filename)
filters = get_filters()
movie_select = movie_query.get_movies([
    Movie.mark_for_download == True,
])
movie_query = movie_query.get_movies(filters, Movie.rating.desc())



def buscar():
    list_movies = QueryYTS(until=lambda m: m['year']>=int(config.film_year),page=int(config.start_page))
    if len(list_movies) == 0:
        print("No se encontraron peliculas")
        return;
    writeToDB(list_movies, filename)
    

def filtrar():
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
    cleanTorrents()   


def main():
    parser = argparse.ArgumentParser(description="Script para gestionar películas y torrents.")
    parser.add_argument('--buscar', action='store_true', help='Buscar nuevas películas.')
    parser.add_argument('--filtrar', action='store_true', help='Filtrar películas.')
    parser.add_argument('--descargar', action='store_true', help='Descargar películas seleccionadas.')
    args = parser.parse_args()
    if args.buscar:
        buscar()
    # if args.filtrar:
    #     filtrar()
    if args.descargar:
        descargar()
    if not (args.buscar or args.descargar or args.filtrar):
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

if __name__ == "__main__":
    main()






