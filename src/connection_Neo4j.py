from neo4j import GraphDatabase

NEO4J_URI="neo4j+s://c0a80f67.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="tNszpLC8O-GMTQ2sjj1yUNI9ZwU4Vzqaic2Q4p0CUd4"


def connection():
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        with driver.session() as session:
            result = session.run("RETURN 'Connexion réussie à Neo4j !' AS message")
            print(result.single()["message"])
        driver.close()
    except Exception as e:
        print(f"Erreur de connexion à Neo4j : {e}")

if __name__ == "__main__":
    connection()
