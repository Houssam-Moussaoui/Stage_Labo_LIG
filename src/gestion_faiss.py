

import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd


from data import Data
from config import *

file_index_faiss = os.path.join(FAISS_DIR, "index.faiss")

def init_model_and_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    dimension = 384

    if os.path.exists(file_index_faiss):
        index = faiss.read_index(file_index_faiss)
    else:
        index = faiss.IndexFlatL2(dimension)

    return model, index





# def data_to_vector(data: Data ,model : SentenceTransformer ): 

#     #passer de data à vector
#     chaine_à_coder = data.getdataÀcoder()
#     embedding = model.encode(chaine_à_coder).astype("float32")

#     #sauvegarde de data à coder dans fichier .pkl 

#     #fichier_pickle = os.path.join(DATA_DIR,f"{data.getIdx()}.pkl")

#     #with open(fichier_pickle,"w") as f:
#     #    f.write(chaine_à_coder)

#     return embedding




# def addVector(vector,index:faiss.IndexFlatL2  ):

#     index.add(np.array([vector]).astype("float32")  )
#     faiss.write_index(index, file_index_faiss)




def encode_and_add_to_index(liste_data : list[Data],model:SentenceTransformer ,index : faiss.IndexFlatL2 ):



    liste_chaine_à_coder = []
    for data in liste_data:
        if isinstance(data, Data) and data is not None:
            liste_chaine_à_coder.append(data.getdataÀcoder())
        else:
            liste_chaine_à_coder.append('')


    embeddings = model.encode(liste_chaine_à_coder).astype("float32")  

    index.add(embeddings)
    faiss.write_index(index, file_index_faiss)


    


    
    





