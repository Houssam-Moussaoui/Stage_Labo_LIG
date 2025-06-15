
import pandas as pd
from config import *


from row_to_data import extraction_data 
from gestion_faiss import data_to_vector ,addVector , init_model_and_index



def main():


    df = pd.read_json(DATAFRAME_JSON)




    # setup pou base vectoriel et embedding
    
    model , index = init_model_and_index()

    


    for idx, row in df.iterrows(): #on s'est arrete à 1149  ne focntionne pas 
        if idx in LIEN_VIDE :
            continue
        if( idx <= 3000): #1265 problem
            print("traitement de ",idx)
            data = extraction_data(row,idx) # on passe d'une ligne de dataframe à un data avec attribut text : donnée de html , et attribut metadonne qui est dico des metadonnes (type de formation , département ...)
            
            vector = data_to_vector(data,model) # on passe au vector  

            addVector(vector,index) # on ajoute à notre base de donnée faiss

        

main()






