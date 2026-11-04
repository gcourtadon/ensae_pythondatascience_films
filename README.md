# ensae_pythondatascience_films
Dépôt de travail de notre projet de datascience sur la base de données MovieLens-32M. 


dataframes de base : 
movies & ratings, ainsi que tags et links.
Dataframes créés :
movies_with_date, a une colonne spéciale pour l'année de sortie, et on y a exclu les 617 films qui n'avaient pas d'année de sortie. 
ratings_movies, a les colonnes suivantes : userId	movieId	rating	timestamp	date (à partir de timestamp)	title	genres	year


Pistes d'exploration :
On peut croiser les données avec celles de imbd et tmdb si on veut, avec la table "links"
