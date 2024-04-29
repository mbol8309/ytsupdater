import requests
import urllib
from classes import Movie, Torrent, Genre, DB
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

def QueryYTS(filters:dict = {}, page=1, until_page=-1, until = lambda x: True) -> list :
    baseurl = "https://yts.uproxy.to/api/v2/list_movies.json"
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

        current_page+=1
    return allmovies


def writeToDB(movies: list):
    # for m in movies_distint:
    #     print(f"{m['title']} - {m['rating']}")

    dbfile = "movies.sqlite"

    engine = create_engine(f"sqlite:///{dbfile}")
    Session = sessionmaker(bind=engine)
    session = Session()
    DB.create(dbfile)

    for m in movies:
        movie, isMovieNew = DB.get_or_createMovie(session, m)
        if isMovieNew:
            print(f"Adding new film: {movie.title}")

        for torrent_data in m['torrents']:
            torrent, isTorrentNew = DB.get_or_createTorrent(session, movie.id, torrent_data)
            if isTorrentNew:
                print(f"New torrent. Film: {movie.title} quality:{torrent.quality}")

        for genres_title in m['genres']:
            genre, isGenreNew = DB.get_or_createGenre(session, movie.id, genres_title)
            if isGenreNew:
                print(f"New genre found: {genre.title}")

        session.commit()


list_movies = QueryYTS(until=lambda m: m['year']>=2024)
writeToDB(list_movies)

