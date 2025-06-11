import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os
from api_parcoursup import main


# Configuration des chemins
SRC_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, os.pardir))
FAISS_DIR = os.path.join(PROJECT_ROOT, "data", "data_faiss")
DATA_ENTREE_DIR = os.path.join(PROJECT_ROOT, "data", "data_entree")
os.makedirs(FAISS_DIR, exist_ok=True)

# Fichiers persistants
file_index_faiss = os.path.join(FAISS_DIR, "index.faiss")
file_text_store = os.path.join(FAISS_DIR, "all_texts.pkl")
file_metadata_store = os.path.join(FAISS_DIR, "all_metadata.pkl")

def get_new_texts():
    """Récupère uniquement les nouveaux textes non encore indexés"""
    new_texts = []
    new_metadata = []
    
    for file in os.listdir(DATA_ENTREE_DIR):
        file_path = os.path.join(DATA_ENTREE_DIR, file)
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        
        if data.get("in", 0) == 0:  # Si pas encore indexé
            data["in"] = 1  # Marquer comme indexé
            with open(file_path, "wb") as f:
                pickle.dump(data, f)  # Sauvegarder le changement
            
            new_texts.append(data["text"])
            new_metadata.append(data["metadonnee"])
    
    return new_texts, new_metadata

#main()


# Initialisation du modèle
model = SentenceTransformer("all-MiniLM-L6-v2")

# Charger ou créer l'index
if os.path.exists(file_index_faiss):
    index = faiss.read_index(file_index_faiss)
    with open(file_text_store, "rb") as f:
        all_texts = pickle.load(f)
    with open(file_metadata_store, "rb") as f:
        all_metadata = pickle.load(f)
else:
    dimension = 384  # Dimension pour all-MiniLM-L6-v2
    index = faiss.IndexFlatL2(dimension)
    all_texts = []
    all_metadata = []

# Ajouter seulement les nouveaux textes
new_texts, new_metadata = get_new_texts()
if new_texts:
    new_embeddings = model.encode(new_texts).astype("float32")
    index.add(new_embeddings)
    faiss.write_index(index, file_index_faiss)
    
    # Mettre à jour les listes complètes
    all_texts.extend(new_texts)
    all_metadata.extend(new_metadata)
    
    # Sauvegarder les nouvelles listes
    with open(file_text_store, "wb") as f:
        pickle.dump(all_texts, f)
    with open(file_metadata_store, "wb") as f:
        pickle.dump(all_metadata, f)




def recherche(query,model,index,all_texts,all_metadata):
    # Exemple de recherche
    
    query_embedding = model.encode([query]).astype("float32")
    k = 3
    distances, indices = index.search(query_embedding, k)

    print("Résultats similaires :")
    for i, idx in enumerate(indices[0]):
        print(f"{i+1}. {all_texts[idx]} (distance: {distances[0][i]:.2f})")
        print("   Métadonnées :", all_metadata[idx])



query = "Je cherche une formation en informatique à Bordeaux"

query2 = "je cherche une formation public , à Paris ou Lyon ou grenoble , soit en informatique ou histoire ou biologie , langue :anglais"

recherche(query,model,index,all_texts,all_metadata)

