from classes import Movie, Torrent, Genre, DB
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, and_, not_

filedb = "movies.sqlite"

class MovieQuery:
    def __init__(self, engine_url):
        self.engine = create_engine(engine_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_movies(self, filters=None, order_by=None):
        _movies = []
        try:
            query = self.session.query(Movie)
            if filters:
                for filter_condition in filters:
                    query = query.filter(filter_condition)
            if order_by is not None:
                query = query.order_by(order_by)

            _movies = query.all()
        finally:
            return _movies

movie_query = MovieQuery(f'sqlite:///{filedb}')

filters = [
    ~Movie.torrents.any(Torrent.downloaded == True),
    Movie.genres.any(Genre.title == "Action"),
    Movie.rating > 7
]

movies = movie_query.get_movies(filters, Movie.rating.desc())
