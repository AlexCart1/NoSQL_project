import json
from pymongo import MongoClient
import os

movies_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "movies.json") #Pour le with open 

url_mongo = "mongodb+srv://cartiaux:8nDWEXS7HXNair3c@projectsql.yim3r.mongodb.net/"
name_db = "entertainment"
collection = "movies"

def get_client():
    try :
        client = MongoClient(url_mongo)
        db = client[name_db]
        print("La connexion est réussie, Atlas")
        return db
    except Exception as e:
        print(f" Erreur de connexion à MongoDB:\n\t {e}")
        return None
        
def import_movies():
    db = get_client()
    #if not db: marche pas
    if db is None:
        return None
    
    collection_movies = db[collection]

    if collection_movies.count_documents({}) > 0:
        print("Déjà importé")
    
    try:
        with open(movies_file_path, "r", encoding="utf-8") as file:
            movies = [json.loads(line) for line in file]
    
        if movies:
            collection_movies.insert_many(movies)
        else:
            print("fichier vide")
            
        print("importation reussi")
    
    except Exception as e:
        print(f" Erreur d'importation à Atlas du fichier movies?json:\n\t {e}")

if __name__ == "__main__":
    import_movies()


