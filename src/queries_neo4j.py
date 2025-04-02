#Fonction de base neo4j
from neo4j import GraphDatabase

def get_actor_with_most_films(driver):
    with driver.session() as session:
        query = """
        MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
        RETURN a.name AS Actor, COUNT(f) AS FilmCount
        ORDER BY FilmCount DESC
        LIMIT 1;
        """
        result = session.run(query)
        actor = result.single()
        if actor:
            print(f"L'acteur ayant joué dans le plus grand nombre de films est {actor['Actor']} avec {actor['FilmCount']} films.")
        else:
            print("Aucun acteur trouvé.")

# queries_neo4j.py

def get_actors_with_anne_hathaway(driver):
    query = """
    MATCH (a:Actor {name: "Anne Hathaway"})-[:ACTED_IN]->(f:Film)<-[:ACTED_IN]-(other:Actor)
    WHERE a <> other
    RETURN DISTINCT other.name AS Actor;
    """
    
    with driver.session() as session:
        result = session.run(query)
        actors = [record["Actor"] for record in result]
    
    return actors



def get_actor_with_highest_revenue(driver):
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
    WHERE f.revenue IS NOT NULL
    RETURN a.name AS Actor, SUM(toFloat(f.revenue)) AS TotalRevenue
    ORDER BY TotalRevenue DESC
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        if record:
            return record["Actor"], round(record["TotalRevenue"], 2)
        else:
            return None, None

def get_average_votes(driver):
    query = """MATCH (f:Film)
    WHERE f.Votes IS NOT NULL
    RETURN avg(toInteger(f.Votes)) AS AverageVotes
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        return record["AverageVotes"] if record else None

def get_director_with_most_distinct_actors(driver):
    query = """
    MATCH (d:Director)-[:DIRECTED]->(f:Film)<-[:ACTED_IN]-(a:Actor)
    RETURN d.name AS Director, COUNT(DISTINCT a.name) AS NbActors
    ORDER BY NbActors DESC
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        if record:
            return record["Director"], record["NbActors"]
        return None, 0

def get_most_connected_films(driver, limit=5):
    query = """
    MATCH (f1:Film)<-[:ACTED_IN]-(a:Actor)-[:ACTED_IN]->(f2:Film)
    WHERE f1 <> f2
    RETURN f1.title AS Film, COUNT(DISTINCT f2) AS NbConnectedFilms
    ORDER BY NbConnectedFilms DESC
    LIMIT $limit
    """
    with driver.session() as session:
        result = session.run(query, limit=limit)
        return [(record["Film"], record["NbConnectedFilms"]) for record in result]
    

def get_top_5_actors_by_directors(driver):
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)<-[:DIRECTED]-(d:Director)
    RETURN a.name AS Actor, COUNT(DISTINCT d.name) AS NbDirectors
    ORDER BY NbDirectors DESC
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        return [(record["Actor"], record["NbDirectors"]) for record in result]

def get_recommended_film(actor_name, driver):
    query = """
    MATCH (f:Film)
    WHERE NOT EXISTS {
      MATCH (:Actor {name: $actor_name})-[:ACTED_IN]->(f)
    }
    RETURN f.title AS RecommendedFilm
    ORDER BY rand()
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query, actor_name=actor_name)
        record = result.single()
        if record:
            return record["RecommendedFilm"]
        return None


    with driver.session() as session:
        result = session.run(query, actor_name=actor_name)
        record = result.single()
        if record:
            return record["RecommendedFilm"], record["Score"]
        return None, None

def create_co_played_relationships(driver):
    query = """
    MATCH (a1:Actor)-[:ACTED_IN]->(f:Film)<-[:ACTED_IN]-(a2:Actor)
    WHERE a1.name < a2.name
    WITH a1, a2, COUNT(f) AS sharedMovies
    WHERE sharedMovies >= 2
    MERGE (a1)-[:CO_PLAYED_IN {films: sharedMovies}]->(a2)
    """
    with driver.session() as session:
        session.run(query)

def get_actor_collaborations(driver, limit=50):
    query = f"""
    MATCH (a1:Actor)-[r:CO_PLAYED_IN]->(a2:Actor)
    RETURN a1.name AS Actor1, a2.name AS Actor2, r.films AS SharedMovies
    ORDER BY SharedMovies DESC
    LIMIT {limit}
    """
    with driver.session() as session:
        result = session.run(query)
        return [(record["Actor1"], record["Actor2"], record["SharedMovies"]) for record in result]
    
def get_films_same_genre_diff_directors(driver):
    query = """
    MATCH (f1:Film)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(f2:Film)
    WHERE f1 <> f2 AND f1.director IS NOT NULL AND f2.director IS NOT NULL AND f1.director <> f2.director
    RETURN DISTINCT f1.title AS Film1, f2.title AS Film2, g.name AS Genre, f1.director AS Director1, f2.director AS Director2
    LIMIT 20
    """
    with driver.session() as session:
        result = session.run(query)
        return result.data()
    
def recommend_films_based_on_actor_preferences(driver, actor_name):
    query = """
    MATCH (a:Actor {name: $actor_name})-[:ACTED_IN]->(:Film)-[:BELONGS_TO]->(g:Genre)
    WITH a, g, COUNT(*) AS freq
    ORDER BY freq DESC
    LIMIT 3

    MATCH (f:Film)-[:BELONGS_TO]->(g)
    WHERE NOT EXISTS {
        MATCH (a)-[:ACTED_IN]->(f)
    }
    RETURN f.title AS RecommendedFilm, g.name AS Genre
    LIMIT 3
    """
    with driver.session() as session:
        result = session.run(query, actor_name=actor_name)
        return [(record["RecommendedFilm"], record["Genre"]) for record in result]
