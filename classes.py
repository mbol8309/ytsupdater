from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from trackers import trackers, recommended
from urllib.parse import quote
import os

# Definir una base de datos declarativa
Base = declarative_base()

movie_genre_association = Table('movie_genre_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

tracker_list = [f"tr={quote(t)}" for t in trackers]
recommended_tracker_list = [f"tr={quote(t)}" for t in recommended]

# Definir el modelo de datos para la tabla "movies"
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    imdb_code = Column(String)
    title = Column(String)
    title_english = Column(String)
    title_long = Column(String)
    slug = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    runtime = Column(Integer)
    summary = Column(String)
    description_full = Column(String)
    synopsis = Column(String)
    yt_trailer_code = Column(String)
    language = Column(String)
    mpa_rating = Column(String)
    background_image = Column(String)
    background_image_original = Column(String)
    small_cover_image = Column(String)
    medium_cover_image = Column(String)
    large_cover_image = Column(String)
    state = Column(String)
    date_uploaded = Column(String)
    date_uploaded_unix = Column(Integer)
    
    # Definir relación con la tabla de torrents
    torrents = relationship("Torrent", back_populates="movie")
    genres = relationship("Genre", secondary=movie_genre_association, back_populates="movies")

    

# Definir el modelo de datos para la tabla "torrents"
class Torrent(Base):
    __tablename__ = 'torrents'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    url = Column(String)
    hash = Column(String)
    quality = Column(String)
    type = Column(String)
    is_repack = Column(String)
    video_codec = Column(String)
    bit_depth = Column(String)
    audio_channels = Column(String)
    seeds = Column(Integer)
    peers = Column(Integer)
    size = Column(String)
    size_bytes = Column(Integer)
    date_uploaded = Column(String)
    date_uploaded_unix = Column(Integer)
    downloaded = Column(Boolean, default=False)  # Indica si el torrent ha sido descargado
    download_folder = Column(String)  # Ruta de la carpeta donde se descargó el torrent
    
    # Definir relación con la tabla de movies
    movie = relationship("Movie", back_populates="torrents")
    
    def getMagnetLink(self):
        return f"magnet:?xt=urn:btih:{self.hash}&dn={quote(self.movie.title)}.{self.quality}&{'&'.join(tracker_list)}"




class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    title = Column(String)

    # Definir relación con la tabla de movies
    movies = relationship("Movie", secondary=movie_genre_association, back_populates="genres")


class DB:
    def create(file: str = "movies.sqlite"):
        if not os.path.exists(file):
            engine = create_engine(f"sqlite:///{file}")
            Base.metadata.create_all(engine)

    def get_or_createMovie(session, data):
        # Buscar si existe una película con el mismo ID
        movie = session.query(Movie).filter_by(id=data["id"]).first()
        if movie:
            return movie, False  # Devolver la película existente y False para indicar que no se creó
        else:
            # Si no existe, crear una nueva película
            movie = Movie(
                id=data["id"],
                url=data["url"],
                imdb_code=data["imdb_code"],
                title=data["title"],
                title_english=data["title_english"],
                title_long=data["title_long"],
                slug=data["slug"],
                year=data["year"],
                rating=data["rating"],
                runtime=data["runtime"],
                summary=data["summary"],
                description_full=data["description_full"],
                synopsis=data["synopsis"],
                yt_trailer_code=data["yt_trailer_code"],
                language=data["language"],
                mpa_rating=data["mpa_rating"],
                background_image=data["background_image"],
                background_image_original=data["background_image_original"],
                small_cover_image=data["small_cover_image"],
                medium_cover_image=data["medium_cover_image"],
                large_cover_image=data["large_cover_image"],
                state=data["state"],
                date_uploaded=data["date_uploaded"],
                date_uploaded_unix=data["date_uploaded_unix"]
            )
            session.add(movie)
            return movie, True  # Devolver la nueva película y True para indicar que se creó

    def get_or_createGenre(session,movie_id, title):
        # Buscar si existe un género con el mismo título en la base de datos
        genre = session.query(Genre).filter_by(title=title).first()
        if genre:
            # Verificar si la película ya tiene asociado este género
            if any(g.id == movie_id for g in genre.movies):
                return genre, False  # El género existe y ya está asociado a la película
        else:
            # Si el género no existe, crear un nuevo género
            genre = Genre(title=title)
            session.add(genre)
        
        # Asociar el género a la película si aún no está asociado
        if movie_id not in [m.id for m in genre.movies]:
            genre.movies.append(session.query(Movie).get(movie_id))
        
        return genre, True  # Devolver el género y True para indicar que se creó o se asoció

    def get_or_createTorrent(session,movie_id, data):
        # Buscar si existe un torrent con el mismo hash y la misma película
        torrent = session.query(Torrent).filter_by(hash=data["hash"], movie_id=movie_id).first()
        if torrent:
            return torrent, False  # Devolver el torrent existente y False para indicar que no se creó
        else:
            # Si no existe, crear un nuevo torrent
            torrent = Torrent(
                movie_id=movie_id,
                url=data["url"],
                hash=data["hash"],
                quality=data["quality"],
                type=data["type"],
                is_repack=data["is_repack"],
                video_codec=data["video_codec"],
                bit_depth=data["bit_depth"],
                audio_channels=data["audio_channels"],
                seeds=data["seeds"],
                peers=data["peers"],
                size=data["size"],
                size_bytes=data["size_bytes"],
                date_uploaded=data["date_uploaded"],
                date_uploaded_unix=data["date_uploaded_unix"]
            )
            session.add(torrent)
            return torrent, True  # Devolver el nuevo torrent y True para indicar que se creó