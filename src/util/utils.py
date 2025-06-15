import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
from bs4 import BeautifulSoup


def recherche(question : str , k : int , model :  SentenceTransformer , df  ,file_faiss:str ) :
    index = faiss.read_index(file_faiss)
    query_embedding = model.encode([question]).astype("float32")
    distances, indices = index.search(query_embedding, k)

    print("Résultats similaires :")
    for i, idx in enumerate(indices[0]):
        print(f" {i+1}. {df.iloc[idx]} (distance: {distances[0][i]:.2f})")




def jsonTostring(elm):

    liste_meta = []



    meta = elm.get("metadonnee", {})

    mapping = {
        "annee": "Année",
        #"etab_uai": "Code établissement (UAI)",
        "etab_nom": "Nom de l'établissement",
        #"tc": "Code de la formation",
        "tf": "Type de formation",
        "nm": "Nom de la formation",
        "fl": "Filière",
        "app": "Formation en apprentissage",
        "int": "Internat",
        "amg": "Aménagements spécifiques",
        "aut": "Autres informations",
        "region": "Région",
        "departement": "Département",
        "commune": "Ville",
        "adresse_complete": "Adresse complète",
        #"gps_lon": "Longitude",
        #"gps_lat": "Latitude",
        "nmc": "Nom complet",
        #"gta": "Code GTA",
        #"dataviz": "Lien Dataviz",
        "etab_url": "Site web de l'établissement"
    }

    for key, label in mapping.items():
        val = meta.get(key)
        if val:
            liste_meta.append(f"{label} : {str(val).strip()}")

    return "\n".join(liste_meta)





        
        
        
def est_page_erreur(html: str) -> bool:
    """Renvoie True si la page est une 404 ou une page d'erreur Parcoursup"""
    soup = BeautifulSoup(html, "lxml")

    # 1. Cherche un titre "Erreur 404"
    h1 = soup.find("h1")
    if h1 and "oups" in h1.text.lower():
        return True

    # 2. Cherche le message connu
    if "Erreur 404" in html or "la page que vous demandez n'existe pas" in html:
        return True
        


    return False
