from scrapper import QueryYTS, writeToDB
from dbFilter import MovieQuery, common_filters
from torrent import addMoviesTorrents
from classes import Movie

#get films from yts web page
print("Scrape for new films")
list_movies = QueryYTS(until=lambda m: m['year']>=2024)

print(f"Save films in db. Extracted {len(list_movies)} movies")
filename = "movies.sqlite"
writeToDB(list_movies, filename)

print("Query for films based on filters")
movie_query = MovieQuery(filename)
movies = movie_query.get_movies(common_filters, Movie.rating.desc())

print("Adding torrent to client")
addMoviesTorrents(movies)



