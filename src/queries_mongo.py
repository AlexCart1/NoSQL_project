# Requêtes MongoDB

def get_all_movies(db):
    #Retourne les films dans 'movies'.
   
    try:
        return list(db.movies.find({}))
    except Exception as e:
        print(f" Erreur lors de la récupération des films :\n\t{e}")
        return []

def get_movie_by_title(db, title):
    #Rcherche un film par titre
    
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

    #Retourne les films sortis en telle année.

    try:
        return list(db.movies.find({"year": year}))
    except Exception as e:
        print(f" Erreur lors de la récupération des films par année :\n\t{e}")
        return []


# Question une a une 
def get_year_with_most_movies(db):
    #Question 1
    #Retourne l'année qui a le plus de films et le nombre total.

    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    return list(db["movies"].aggregate(pipeline))

def count_movies_after_1999(db):
    return db["movies"].count_documents({"year": {"$gt": 1999}})

def get_movies_count_per_year(db):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    return list(db.movies.aggregate(pipeline))

def movie_sort_years(db):
    return list(db.movies.find({}, {"_id": 0, "year": 1}).sort("year", 1))

def get_all_genres(db):
    genres = []
    v = db.movies.find({}, {"genre": 1, "_id": 0})
    
    for doc in v:
        if "genre" in doc:
            genres += [g.strip() for g in doc["genre"].split(",")]
    
    return list(set(genres))

def get_max_revenue(db):
    # Trouver le film avec le plus grand revenu
    return db.movies.find({
        "Revenue (Millions)": { "$exists": True, "$ne": "", "$type": "double" }
    }).sort("Revenue (Millions)", -1).limit(1)

def get_rea_with_more_than_5_movies(db):
    pipeline = [
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}}, 
        {"$sort": {"count": -1}} 
    ]
    return list(db.movies.aggregate(pipeline))

def list_per_genre(db, genre):
    movies = db.movies.find(
        { "genre": { "$regex": genre, "$options": "i" } },  
        { "_id": 0, "Revenue (Millions)": 1 } 
    )
    revenue_list = [movie["Revenue (Millions)"] for movie in movies if "Revenue (Millions)" in movie]
    return revenue_list

def get_top_3_movies_by_metascore(db, minima_year):
    maxima_year = minima_year + 9  # La période couvre 10 ans
    
    # Trouver les films dont l'année est entre minima_year et maxima_year, triés par Metascore
    top_movies = list(db.movies.find({
        "year": { "$gte": minima_year, "$lte": maxima_year },
        "Metascore": { "$exists": True, "$ne": "" }  # Assurer que Metascore existe
    }).sort("Metascore", -1).limit(3))  # Trier par mtascore et limiter à 3 films
    
    return top_movies

def get_longest_movie_by_genre(db, genre):

    movie = db.movies.find({ "genre": { "$regex": genre, "$options": "i" }, "Runtime (Minutes)": { "$exists": True } }).sort("Runtime (Minutes)", -1).limit(1)  
    return list(movie)

def get_high_rated_high_revenue_movies(db):
    # tous les films de la vue "high_rated_high_revenue_movies"
    movies = list(db.high_rated_high_revenue_movies.find())
    
    return movies

def get_sorted_runtime_revenue(db):
    result = db.movies.find({},{"_id": 0, "Runtime (Minutes)": 1, "Revenue (Millions)": 1}).sort({"Runtime (Minutes)": 1})
    return list(result)
