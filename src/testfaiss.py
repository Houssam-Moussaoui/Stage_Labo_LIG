import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle # A utilsier pour sauvegarder les data , plutot dns fiche_formation.py
from api_parcoursup import main
import os


def lecture_pkl():
    texts = []
    metadata_store = []

    for file in os.listdir(DATA_ENTREE_DIR):
        with open(os.path.join( DATA_ENTREE_DIR  ,file),"rb") as f:
            data = pickle.load(f)

        texts.append(data["text"])
        metadata_store.append(data["metadonnee"])

    return texts,metadata_store


# Chemin absolu vers le dossier 'src'
SRC_DIR = os.path.dirname(__file__)
# Racine du projet (un niveau au-dessus de 'src')
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, os.pardir))

# Dossier de faiss
FAISS_DIR = os.path.join((os.path.join(PROJECT_ROOT, "data"))  , "data_faiss"   )
os.makedirs(FAISS_DIR, exist_ok=True)

DATA_ENTREE_DIR = os.path.join((os.path.join(PROJECT_ROOT, "data"))  , "data_entree"   )


file_index_faiss =os.path.join(FAISS_DIR,"index.faiss")


main()




if( os.path.exists(file_index_faiss)):
    index = faiss.read_index(file_index_faiss)

    

    
else:


    # Initialiser le modèle d'embedding
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Créer les embeddings pour chaque texte
    texts = []
    metadata_store = []
    texts , metadata_store = lecture_pkl()
    embeddings = model.encode(texts).astype("float32")

    # Créer l’index FAISS (distance L2)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    


    #sauvegarde !!!!!!!!!!!!!!
    faiss.write_index(index,file_index_faiss)





# Requête utilisateur
query = "Je cherche une formation en informatique à Bordeaux"
query_embedding = model.encode([query]).astype("float32")

# Recherche dans FAISS
k = 5
distances, indices = index.search(query_embedding, k)

# Affichage des résultats avec métadonnées
print("Résultats similaires :")
for i, idx in enumerate(indices[0]):
    print(f"{i+1}. {texts[idx]} (distance: {distances[0][i]:.2f})")
    print("   Métadonnées :", metadata_store[idx])



