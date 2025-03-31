# Requêtes MongoDB

def get_all_movies(db):
    """
    Retourne tous les films présents dans la collection 'movies'.
    """
    try:
        return list(db.movies.find({}))
    except Exception as e:
        print(f" Erreur lors de la récupération des films :\n\t{e}")
        return []

def get_movie_by_title(db, title):
    """
    Recherche un film par son titre exact.
    """
    try:
        return db.movies.find_one({"title": title})
    except Exception as e:
        print(f" Erreur lors de la recherche du film :\n\t{e}")
        return None


def count_movies(db):
    
    try:
        return db.movies.count_documents({})
    except Exception as e:
        print(f" Erreur lors du comptage des films :\n\t{e}")
        return 0

def get_movies_by_year(db, year):
    """
    Retourne les films sortis en une année donnée.
    """
    try:
        return list(db.movies.find({"year": year}))
    except Exception as e:
        print(f" Erreur lors de la récupération des films par année :\n\t{e}")
        return []

def get_distinct_genres(db):
    """
    Retourne la liste des genres uniques dans la collection.
    """
    try:
        return db.movies.distinct("genre")
    except Exception as e:
        print(f" Erreur lors de la récupération des genres :\n\t{e}")
        return []
