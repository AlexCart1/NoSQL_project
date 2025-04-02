# Connexions injectées depuis app.py
import matplotlib.pyplot as plt
from src.queries_mongo import *
from src.queries_neo4j import *
import numpy as np
import os
mongo_db = None
neo4j_driver = None


def question_1():
    print("\n\tLancement de la question 1")
    result = get_year_with_most_movies(mongo_db)
    top = result[0]
    year = top["_id"]
    count = top["count"]
    print(f"\n L'année {year} possède le plus de films avec {count} films.")
    

def question_2():
    print("\n\tLancement de la question 2")
    count = count_movies_after_1999(mongo_db)
    print(f"\n Il y a {count} films sortis après l'année 1999.")

def question_3():
    print("\n\tLancement de la question 4")
    year = 2007
    movies = get_movies_by_year(mongo_db, year)

    metascores = [film["Metascore"] for film in movies]
    avg = sum(metascores) / len(metascores)
    print(f"\nLa moyenne des Metascores des films sortis en {year} est : {avg:.2f}")



def question_4():
    print("\n\tLancement de la question 4")
    movies = movie_sort_years(mongo_db)
    
    years = [movie["year"] for movie in movies if "year" in movie]
    if not years:
        print("Aucune année trouvée.")
    
    unique_years = sorted(set(years))
    
    year_counts = [years.count(year) for year in unique_years]
    
    print("Fermer le graphique pour continuer.")

    plt.bar(unique_years, year_counts, color='skyblue')
    plt.xlabel("Année")
    plt.ylabel("Nombre de films")
    plt.title("Nombre de films par année")
    plt.tight_layout()
    plt.savefig("doc/question_4.png")
    plt.show()


    from src.queries_mongo import get_all_genres

def question_5():
    print("\n\tLancement de la question 5")
    genres = get_all_genres(mongo_db)

    print(f"\nGenres disponibles dans la base ({len(genres)}) :")
    for g in sorted(genres):
        print(f"- {g}")

def question_6():
    print("\n\tLancement de la question 6")
    movie = get_max_revenue(mongo_db)

    for m in movie:
        print(f"Le film qui a généré le plus de revenu est : {m['title']} avec {m['Revenue (Millions)']} millions de dollars.")

 

def question_7():
    print("\n\tLancement de la question 7")
    rea = get_rea_with_more_than_5_movies(mongo_db)
    if not rea:
        print("0 réalisateurs avec plus de 5 films")
    else:
        print(f"\nRéalisateurs avec + de 5 films :")
        for var in rea:
            print(f"- {var['_id']} avec {var['count']} films.")

def question_8():
    print("\n\tLancement de la question 8")
    
    # Récupérer tous les genres
    genres = get_all_genres(mongo_db)
    list_average_per_genre = []

    max_average = 0
    max_genre = ""

    for genre in sorted(genres):

        liste = list_per_genre(mongo_db, genre)

        if liste:

            filtered_list = []
            for value in liste:
                try:
                    filtered_list.append(float(value))
                except ValueError:
                    continue

            if filtered_list:
                average = sum(filtered_list) / len(filtered_list)
                list_average_per_genre.append(average)
                
                if average > max_average:
                    max_average = average
                    max_genre = genre
    """
    print("Moyennes des revenus par genre :")
    for i in range(len(list_average_per_genre)):
        print(f"La moyenne des revenus pour le genre '{genres[i]}' est : {list_average_per_genre[i]:.2f} millions")"""
    
    print(f"\nLe Genre {max_genre} a le revenu le plus élevé avec une moyenne de {max_average:.2f} millions.")


def question_9():
    print("\n\tLancement de la question 9")
    
    minima_year = 1700
    while (minima_year < 2025) :
        minima_year += 10
        top_movies = get_top_3_movies_by_metascore(mongo_db, minima_year)
    
        if top_movies:
            print(f"\nLes 3 meilleurs films de {minima_year}-{minima_year + 9} sont :")
            for movie in top_movies:
                print(f"{movie['title']} - {movie['year']} - MetaScore: {movie['Metascore']}")


def question_10():
    print("\n\tLancement de la question 10")
    
    genres = get_all_genres(mongo_db)
    
    for genre in sorted(genres):
        longest_movie = get_longest_movie_by_genre(mongo_db, genre)
        if longest_movie:
            movie = longest_movie[0] 
            print(f"Genre : '{genre}' --- {movie['title']} --- {movie['Runtime (Minutes)']} minutes ;")
        else:
            print(f"Aucun film trouvé pour le genre '{genre}'.")

def question_11():
    print("\n\tLancement de la question 11")
    
    # Récupérer les films de la vue "high_rated_high_revenue_movies"
    high_rated_movies = get_high_rated_high_revenue_movies(mongo_db)
    
    if high_rated_movies:
        print(f"Films avec un Metascore > 80 et des revenus > 50 millions :")
        for movie in high_rated_movies:
            print(f"- {movie['title']} ({movie['year']}), Metascore: {movie['Metascore']}, Revenue: {movie['Revenue (Millions)']} millions")
    else:
        print("Aucun film trouvé avec un Metascore supérieur à 80 et des revenus supérieurs à 50 millions.")



def question_12():
    print("\n\tLancement de la question 12")
    sorted_films = get_sorted_runtime_revenue(mongo_db)

    valid_films = [film for film in sorted_films if 
                   "Runtime (Minutes)" in film and "Revenue (Millions)" in film and 
                   film["Runtime (Minutes)"] != "" and film["Revenue (Millions)"] != ""]

    runtimes = [film["Runtime (Minutes)"] for film in valid_films]
    revenues = [film["Revenue (Millions)"] for film in valid_films]
    
    if len(runtimes) > 1 and len(revenues) > 1:

        correlation_matrix = np.corrcoef(runtimes, revenues)
        correlation = correlation_matrix[0, 1]
        
        print(f"Corrélation entre Runtime et Revenue : {correlation:.4f}")

        # Visualiser la relation avec un scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(runtimes, revenues, color='skyblue', edgecolors='black', alpha=0.7)

        # Ajouter une ligne de régression
        m, b = np.polyfit(runtimes, revenues, 1)  # Calcul de la pente (m) et de l'ordonnée à l'origine (b)
        plt.plot(runtimes, m * np.array(runtimes) + b, color='red', label=f"Régression linéaire: y = {m:.2f}x + {b:.2f}")

        # Ajouter des labels et un titre
        plt.xlabel("Durée des films (minutes)")
        plt.ylabel("Revenu des films (millions)")
        plt.title(f"Corrélation entre Durée et Revenu des films\nCorrélation: {correlation:.4f}")

        # Afficher la légende
        plt.legend()

        # Afficher le graphique
        plt.tight_layout()
        plt.savefig("doc/question_12.png")
        plt.show()

def question_14():
    get_actor_with_most_films(neo4j_driver)


def question_15():
    print("\n\tLancement de la question 15")
    
    actors = get_actors_with_anne_hathaway(neo4j_driver)
        
    if actors:
        print("Acteurs ayant joué dans des films avec Anne Hathaway :")            
        for actor in actors:
            print(f"- {actor}")
        else:
            print("Aucun acteur trouvé.")


def question_16():
    print("\n\tLancement de la question 16")
    

    actor_name, total_revenue = get_actor_with_highest_revenue(neo4j_driver)
        
    if actor_name:
        print(f"\n\nL'acteur ayant joué dans des films totalisant le plus de revenus est {actor_name} avec {total_revenue} millions de dollars.")
    else:
        print("Aucun acteur trouvé.")

def question_17():
    print("\n\tLancement de la question 17")

    moyenne_votes = get_average_votes(neo4j_driver)

    if moyenne_votes is not None:
        print(f"La moyenne des votes des films est de : {moyenne_votes:.2f}")
    else:
        print("\nAucun vote trouvé.")

def question_20():
    print("\n\tLancement de la question 20")
    
    director, nb_actors = get_director_with_most_distinct_actors(neo4j_driver)

    if director:
        print(f"Réalisateur avec le plus grand nombre d'acteurs distincts est: {director} avec {nb_actors} acteurs")
    else:
        print("Bug")


def question_21():
    print("\n\tLancement de la question 21")

    films = get_most_connected_films(neo4j_driver)
    if films:
        print("Films les plus connectés (ayant le plus d'acteurs en commun avec d'autres films) :")
        for title, count in films:
            print(f"- {title} ({count} connexions)")
    else:
        print("Aucun film trouvé.")


def question_22():
    print("\n\tLancement de la question 22")

    results = get_top_5_actors_by_directors(neo4j_driver)

    if results:
        print("Top 5 des acteurs ayant travaillé avec le plus de réalisateurs différents :")
        for actor, nb in results:
            print(f"- {actor} : {nb} réalisateurs")
    else:
        print("Aucun acteur trouvé.")

def question_23():
    print("\n\tLancement de la question 23")
    actor_name = "Leonardo DiCaprio"  # à remplacer si tu veux un autre acteur

    film = get_recommended_film(actor_name, neo4j_driver)

    if film:
        print(f"Recommandation pour {actor_name} : '{film}'")
    else:
        print(f"Aucune recommandation trouvée pour {actor_name}.")

def question_26():
    print("\n\tLancement de la question 26")
    from src.queries_neo4j import create_co_played_relationships, get_actor_collaborations
    
    create_co_played_relationships(neo4j_driver)
    collaborations = get_actor_collaborations(neo4j_driver)

    if collaborations:
        print("Groupes d'acteurs ayant souvent joué ensemble :")
        for actor1, actor2, count in collaborations:
            print(f"- {actor1} & {actor2} : {count} films en commun")
    else:
        print("Aucune collaboration trouvée.")

def question_27():
    print("\n\tLancement de la question 27")
    
    results = get_films_same_genre_diff_directors(neo4j_driver)
    
    if results:
        print("Films avec genres communs mais réalisateurs différents :")
        for row in results:
            print(f"- '{row['Film1']}' ({row['Director1']}) & '{row['Film2']}' ({row['Director2']}) [Genre commun : {row['Genre']}]")
    else:
        print("Aucune correspondance trouvée.")

def question_28():
    print("\n\tLancement de la question 28")
    actor_name = "Scarlett Johansson"
    films = recommend_films_based_on_actor_preferences(neo4j_driver, actor_name)

    print(f"Films recommandés pour {actor_name} :")
    for film, genre in films:
        print(f"- {film} (genre : {genre})")
