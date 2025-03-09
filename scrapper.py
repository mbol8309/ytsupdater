import requests
import urllib
from classes import Movie, Torrent, Genre, DB
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import time
from random import randint
from configs import Config

config = Config()

def QueryYTS(filters:dict = {}, page=1, until_page=-1, until = lambda x: True, partial_update=True) -> list :
    baseurl = f"{config.yts_url}/api/v2/list_movies.json"
    default_filters = dict(
        quality = "1080p",
        sort_by="year",
        minimun_rating = 7,
        page = page
    )
    default_filters.update(filters)
    allmovies = []
    movies_id = set()
    inner_until_page = until_page
    if until_page == -1:
        inner_until_page = page + 1

    current_page = page

    while current_page < inner_until_page:
        default_filters['page'] = current_page


        url_param = urllib.parse.urlencode(default_filters)
        fullurl = f"{baseurl}?{url_param}"
        print(f"Query: {fullurl}")
        try:
            data = requests.get(fullurl, headers={
                    "Accept" : "application/json",
                    "User-Agent": "insomnia/2023.5.8"
                })
            if data.status_code != 200:
                print("Error on request")
            response = data.json()
            response_data = response['data']
            if until_page==-1:
                inner_until_page = int(response_data['movie_count'] / response_data['limit'])

            movies = response_data['movies']

            #movies with duplicated
            for m in movies:
                if not until(m): # si no se cumple esta accion devuelve lo que tiene
                    return allmovies

                if m['id'] not in movies_id:
                    allmovies.append(m)
                    movies_id.add(m['id'])
                    if partial_update:
                        if len(allmovies) >= 20:
                            print(f"Writing to DB {len(allmovies)} films")
                            writeToDB(allmovies, config.sqlite_filename)
                            allmovies = []
        except Exception as e:
            print(f"Hard times, and exception: {e}")

        current_page+=1
        print('Waiting something to prevent block')
        forHowMuch = randint(2,5)
        print(f"Waiting for {forHowMuch} seconds", end='')
        for i in range(forHowMuch):
            print(".", end='', flush=True)
            time.sleep(1)
    return allmovies


def writeToDB(movies: list, filename="movies.sqlite"):
    # for m in movies_distint:
    #     print(f"{m['title']} - {m['rating']}")

    dbfile = filename

    engine = create_engine(f"sqlite:///{dbfile}")
    Session = sessionmaker(bind=engine)
    session = Session()
    DB.create(dbfile)

    for m in movies:
        movie, isMovieNew = DB.get_or_createMovie(session, m)
        if movie is not None:
            if isMovieNew:
                print(f"Adding new film: {movie.title}")

            for torrent_data in m['torrents']:
                torrent, isTorrentNew = DB.get_or_createTorrent(session, movie.id, torrent_data)
                if torrent is not None:
                    if isTorrentNew:
                        print(f"New torrent. Film: {movie.title} quality:{torrent.quality}")
            if "genres" in m:
                for genres_title in m['genres']:
                    genre, isGenreNew = DB.get_or_createGenre(session, movie.id, genres_title)
                    if isGenreNew:
                        print(f"New genre found: {genre.title}")

        session.commit()




