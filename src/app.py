from src import questions
from src.database_mongo import connexion_mongo, deconnexion_mongo
from src.database_neo4j import connexion_neo4j, deconnexion_neo4j

def menu():
    print("\nProjet NoSQL - Menu principal")
    #Connection aux databases
    mongo_client, mongo_db = connexion_mongo()
    neo4j_driver = connexion_neo4j()

    if not mongo_client or not neo4j_driver:
        print("Connexion échouée. Fermeture.")
        return
    
    # maj variable du code questions.py 
    questions.mongo_db = mongo_db
    questions.neo4j_driver = neo4j_driver

    while True:
        print("\nChoisissez une question de 1 à 30, ou 0 pour quitter")
        try:
            choice = int(input("Entrez le nombre (int) de la question : "))
            if choice == 0:
                break
            elif 1 <= choice <= 30:
                getattr(questions, f"question_{choice}")()
                print("\n----------------------------------------------------------")
            else:
                print("Choisissez une question de 1 à 30, ou 0 pour quitter")
        except Exception as e:
            print(f"Erreur : {e}")

    deconnexion_mongo(mongo_client)
    deconnexion_neo4j(neo4j_driver)
