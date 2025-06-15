


import os
import faiss
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd



#from util.utils import recherche

#from config import *

def recherche(question : str , k : int , model :  SentenceTransformer , df  ,file_faiss:str ) :
    index = faiss.read_index(file_faiss)
    query_embedding = model.encode([question]).astype("float32")
    distances, indices = index.search(query_embedding, k)

    print("Résultats similaires :")
    for i, idx in enumerate(indices[0]):
        print(f"le vrai idx sur data : {idx} ")
        print(f" {i+1}.   {df.iloc[idx]} (distance: {distances[0][i]:.2f})")
        print()
        print()
        

def test1():


    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    question =  "je cherche Licence public"
    q1 = "je cherche une formation un BTS à Lille"
    k = 2



    df = pd.read_json("/home/moussaoui/stage_lig/Stage_Labo_LIG/data/fr-esr-cartographie_formations_parcoursup.json")


    file = "/home/moussaoui/stage_lig/Stage_Labo_LIG/data/data_faiss/old_index.faiss"

    recherche(q1 , k ,model , df, file  )

   # print(df.iloc[10974])


test1()




