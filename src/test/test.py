import os
import faiss
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

def recherche(question: str, k: int, model: SentenceTransformer, df, file_faiss: str):
    index = faiss.read_index(file_faiss)
    query_embedding = model.encode([question]).astype("float32")
    distances, indices = index.search(query_embedding, k)

    print("\nRésultats :\n")
    for i, idx in enumerate(indices[0]):
        print(f"{i+1}.Index FAISS : {idx}")
        print(f"   - Distance : {distances[0][i]:.2f}")
        print(f"   - Donnée : \n{df.iloc[idx]}\n")


def main():
    # Vérifie que l'utilisateur a bien passé une question
    if len(sys.argv) < 2:
        print("Erreur  dans entrée de question")
        return
    question = " ".join(sys.argv[1:])
    k = 2 

    model = SentenceTransformer("all-MiniLM-L6-v2")

    df = pd.read_json("/home/moussaoui/stage_lig/Stage_Labo_LIG/data/fr-esr-cartographie_formations_parcoursup.json")
    file = "/home/moussaoui/stage_lig/Stage_Labo_LIG/data/data_faiss/old_index.faiss"

    recherche(question, k, model, df, file)



if __name__ == "__main__":
    main()
