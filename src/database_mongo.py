from pymongo import MongoClient
from src.config import MONGO_URI, MONGO_DB_NAME

def connexion_mongo():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
        print("Connexion à MongoDB réussie")
        return client, client[MONGO_DB_NAME]
    except Exception as e:
        print(f"Erreur de connexion à MongoDB : {e}")
        return None, None

def deconnexion_mongo(client):
    try:
        client.close()
        print("Déconnexion de MongoDB effectuée")
    except Exception as e:
        print(f"Erreur lors de la déconnexion de MongoDB : {e}")
