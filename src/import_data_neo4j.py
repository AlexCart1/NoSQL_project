from pymongo import MongoClient
from database_mongo import connexion_mongo
from database_neo4j import connexion_neo4j, deconnexion_neo4j
from neo4j import GraphDatabase

# Connexino à db mongo & à neo4j
# Pour chaque films, noeud films, noeuds genres, noeuds acteurs

def get_movies_from_mongo():
    client, db = connexion_mongo()
    if db is None:
        print("Échec de la connexion à MongoDB.")
        return []
    movies_collection = db['movies']
    return list(movies_collection.find())

# Enlever les apostrophes sinon contraintes sur calcul et autre....
def escape_quotes(text):
    if text is not None:
        return text.replace("'", "\\'")
    return ""


def create_constraints(driver):
    with driver.session() as session:
        session.run("CREATE CONSTRAINT film_title_unique IF NOT EXISTS FOR (f:Film) REQUIRE f.title IS UNIQUE")
        session.run("CREATE CONSTRAINT actor_name_unique IF NOT EXISTS FOR (a:Actor) REQUIRE a.name IS UNIQUE")
        session.run("CREATE CONSTRAINT genre_name_unique IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE")

#Noeud film
def create_film_node(tx, title, year, revenue, director, votes):
    title = escape_quotes(title)
    director = escape_quotes(director)

    query_parts = [f"title: '{title}'"]
    if year:
        query_parts.append(f"year: {int(year)}")
    if revenue not in ("", None):
        try:
            query_parts.append(f"revenue: {float(revenue)}")
        except:
            pass
    if director:
        query_parts.append(f"director: '{director}'")
    if votes not in ("", None):
        try:
            query_parts.append(f"votes: {int(votes)}")
        except:
            pass

    query = f"MERGE (f:Film {{{', '.join(query_parts)}}})"
    tx.run(query)


#Noeud acteur
def create_actor_node(tx, actor_name):
    actor_name = escape_quotes(actor_name)
    query = "MERGE (a:Actor {name: $name})"
    tx.run(query, name=actor_name)

#neouds genre
def create_genre_node(tx, genre):
    genre = escape_quotes(genre)
    query = "MERGE (g:Genre {name: $name})"
    tx.run(query, name=genre)

#Relation
def create_relationship(tx, film_title, actor_name, genre):
    film_title = escape_quotes(film_title)
    actor_name = escape_quotes(actor_name)
    genre = escape_quotes(genre)

    query_actor = (
        "MATCH (f:Film {title: $film_title}), (a:Actor {name: $actor_name}) "
        "MERGE (a)-[:ACTED_IN]->(f)"
    )
    tx.run(query_actor, film_title=film_title, actor_name=actor_name)

    query_genre = (
        "MATCH (f:Film {title: $film_title}), (g:Genre {name: $genre}) "
        "MERGE (f)-[:BELONGS_TO]->(g)"
    )
    tx.run(query_genre, film_title=film_title, genre=genre)

#main 
def insert_movies_into_neo4j():
    driver = connexion_neo4j()
    if driver:
        create_constraints(driver)

        with driver.session() as session:
            movies = get_movies_from_mongo()

            for film in movies:
                title = film.get('title')
                year = film.get('year')
                revenue = film.get('Revenue (Millions)', 0)
                director = film.get('Director')
                votes = film.get('Votes')
                genres = film.get('genre', '').split(',')
                actors = film.get('Actors', '').split(',')

                session.execute_write(create_film_node, title, year, revenue, director, votes)

                for genre in genres:
                    if genre.strip():
                        session.execute_write(create_genre_node, genre.strip())

                for actor in actors:
                    if actor.strip():
                        session.execute_write(create_actor_node, actor.strip())
                        session.execute_write(create_relationship, title, actor.strip(), genres[0])

        deconnexion_neo4j(driver)


# executer une fois pour import les donnés ( sinon match n delete n dans neo4j)
if __name__ == "__main__":
    insert_movies_into_neo4j()
