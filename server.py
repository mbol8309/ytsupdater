from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic, Optional
from configs import Config
from classes import Movie, Torrent, Genre
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
config = Config()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)
T = TypeVar('T')

class FilterParams(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    rating: Optional[float] = Field(None, ge=0, le=10)
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1)
    marked: Optional[bool] = Field(None)

class FilterGenresParams(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1)
    

class PaginatedResponse(BaseModel, Generic[T]):
    total_items: int
    total_pages: int
    page: int
    per_page: int
    items: List[T]
    
def get_db():
    dbfile = config.sqlite_filename
    engine = create_engine(f"sqlite:///{dbfile}")
    Session = sessionmaker(bind=engine)
    
    db = Session()
    try:
        yield db
    finally:
        db.close()

class GenreBase(BaseModel):
    title: str

# Clase Genre para incluir la información del género con relación a las películas
class GenreResponse(GenreBase):
    id: int
    class Config:
        orm_mode = True
# Esquema Pydantic para la respuesta de Movie
class MovieBase(BaseModel):
    id: int
    title: str
    year: int
    url: str 
    description_full: str
    background_image: str
    small_cover_image: str
    medium_cover_image: str
    large_cover_image: str
    # url = Column(String)
    # imdb_code = Column(String)
    # title = Column(String)
    title_english: str 
    rating: float
    mark_for_download: bool
    # slug = Column(String)
    # year = Column(Integer)
    # rating = Column(Float)
    # runtime = Column(Integer)
    # summary = Column(String)
    # description_full = Column(String)
    # synopsis = Column(String)
    # yt_trailer_code = Column(String)
    # language = Column(String)
    # mpa_rating = Column(String)
    # background_image = Column(String)
    # background_image_original = Column(String)
    # small_cover_image = Column(String)
    # medium_cover_image = Column(String)
    # large_cover_image = Column(String)
    # state = Column(String)
    # date_uploaded = Column(String)
    # date_uploaded_unix = Column(Integer)

class MovieResponse(MovieBase):
    id: int
    genres: List[GenreResponse] = []

    class Config:
        orm_mode = True
        
class MovieMarkForDownload(BaseModel):
    mark_for_download: bool
    
@app.get("/movies/", response_model=PaginatedResponse[MovieResponse])
def read_movies(filter_query: FilterParams = Depends(), db: Session = Depends(get_db)):
    query = db.query(Movie)
    if filter_query.title:
        query = query.filter(Movie.title.ilike(f"%{filter_query.title}%"))
    if filter_query.genre:
        query = query.join(Movie.genres).filter(Genre.title.ilike(f"%{filter_query.genre}%"))
    if filter_query.rating is not None:
        query = query.filter(Movie.rating >= filter_query.rating)
    if filter_query.marked is not None:
        query = query.filter(Movie.mark_for_download == filter_query.marked)
    
    total_items = query.count()
    total_pages = (total_items + filter_query.per_page - 1) // filter_query.per_page
    movies = query.offset((filter_query.page - 1) * filter_query.per_page).limit(filter_query.per_page).all()
    return PaginatedResponse(
        total_items=total_items,
        total_pages=total_pages,
        page=filter_query.page,
        per_page=filter_query.per_page,
        items=movies
    )

@app.get("/genres/", response_model=PaginatedResponse[GenreResponse])
def read_movies(filter_query: FilterGenresParams =Depends(), db: Session = Depends(get_db)):
    query = db.query(Genre)
    if filter_query.title:
        query = query.filter(Genre.title.ilike(f"%{filter_query.title}%"))
    
    total_items = query.count()
    total_pages = (total_items + filter_query.per_page - 1) // filter_query.per_page
    
    genres = query.offset((filter_query.page - 1) * filter_query.per_page).limit(filter_query.per_page).all()
    return PaginatedResponse(
        total_items=total_items,
        total_pages=total_pages,
        page=filter_query.page,
        per_page=filter_query.per_page,
        items=genres
    )
    
@app.patch("/movies/{movie_id}/mark", response_model=MovieResponse)
def mark_movie_for_download(
    movie_id: int,
    movie_data: MovieMarkForDownload,
    db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    movie.mark_for_download = movie_data.mark_for_download
    db.commit()
    db.refresh(movie)
    return movie

@app.get("/movies/{movie_id}", response_model=MovieResponse)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# @app.patch("/movies/{movie_id}/mark")
# def mark_movie_for_download(movie_id: int, db: Session = Depends(get_db)):
#     movie = db.query(Movie).filter(Movie.id == movie_id).first()
#     if movie is None:
#         raise HTTPException(status_code=404, detail="Movie not found")
#     movie.marked_for_download = True
#     db.commit()
#     return {"message": "Movie marked for download"}