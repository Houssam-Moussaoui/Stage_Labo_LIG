
import pandas as pd
from config import *


from row_to_data import extraction_data 
from gestion_faiss import init_model_and_index ,encode_and_add_to_index
from concurrent.futures import ThreadPoolExecutor, as_completed






def extract_and_collect_data(idx,row):  
    # Convertit une ligne du DataFrame en un objet Data
    if idx in lien_vide:
            return
    
    print("traitement de ",idx)
    return extraction_data(row,idx) # on passe d'une ligne de dataframe à un data avec attribut text : donnée de html , et attribut metadonne qui est dico des metadonnes (type de formation , département ...)
   



def main():

    df = pd.read_json(DATAFRAME_JSON)

    # setup pou base vectoriel et embedding
    model , index = init_model_and_index()

    # liste avec des sites avec problèmes:
    sites_problem = []

    # Liste pour stocker les objets Data extraits
    liste_data = []


    # Version avec Threads
    # with ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 4)) as executor:
    #     futures = [ executor.submit(extract_and_collect_data(idx,row))  for idx,row in df.iterrows() if  idx<20  ]

    #     for future in as_completed(futures):
    #         try:
    #             data = future.result()
    #             liste_data.append(data)
                
    #         except Exception as e:
    #             print("[ERREUR THREAD] :", e)


    # Version séquentielle
    for idx, row in df.iterrows() :
         if(idx<3):
            data = extract_and_collect_data(idx,row,model,index)
            liste_data.append(data)

    # Encodage des objets Data en vecteurs et ajout à l'index FAISS
    encode_and_add_to_index(liste_data,model,index)
    

        
        
main()
print(lien_vide)






