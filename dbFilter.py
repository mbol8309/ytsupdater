from classes import Movie, Torrent, Genre, DB
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, and_, not_
from dotenv import load_dotenv
import os

filedb = "movies.sqlite"

class MovieQuery:
    def __init__(self, filedb):
        self.engine = create_engine(f'sqlite:///{filedb}')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_movies(self, filters=None, order_by=None) -> list:
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


def get_filters():
    common_filters = []
    load_dotenv()
    filters =  os.getenv("FILTER")
    try:
        common_filters = eval(filters)
    except:
        common_filters = []
    return common_filters
    



# for movie in movies:
#     torrent = movie.torrents[0]
#     print(torrent.getMagnetLink())