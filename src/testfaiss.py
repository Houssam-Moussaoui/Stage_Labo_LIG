import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from api_parcoursup import main

fiches = main()


# Initialiser le modèle d'embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Créer les embeddings pour chaque texte
texts = [fiche["text"] for fiche in fiches]
embeddings = model.encode(texts).astype("float32")

# Créer l’index FAISS (distance L2)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Stocker les métadonnées séparément (liste parallèle)
metadata_store = [fiche["metadonnee"] for fiche in fiches]

# Requête utilisateur
query = "Je cherche une formation en informatique à Bordeaux"
query_embedding = model.encode([query]).astype("float32")

# Recherche dans FAISS
k = 2
distances, indices = index.search(query_embedding, k)

# Affichage des résultats avec métadonnées
print("Résultats similaires :")
for i, idx in enumerate(indices[0]):
    print(f"{i+1}. {texts[idx]} (distance: {distances[0][i]:.2f})")
    print("   Métadonnées :", metadata_store[idx])
