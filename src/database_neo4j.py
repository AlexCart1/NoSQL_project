
#https://neo4j.com/docs/api/python-driver/current/  codelien

from neo4j import GraphDatabase
#from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
#Utiliser pour le import dataneo pcq il est déjà dans src
from src.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
def connexion_neo4j():
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        driver.verify_connectivity()
        print("Connexion à Neo4j réussie")
        return driver
    except Exception as e:
        print(f"Erreur de connexion à Neo4j : {e}")
        return None

def deconnexion_neo4j(driver):
    try:
        driver.close()
        print("Déconnexion de Neo4j effectuée")
    except Exception as e:
        print(f"Erreur lors de la déconnexion de Neo4j : {e}")
