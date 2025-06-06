import requests
import pickle
import os
from fiche_formation import extraction_donnee_fiche






def main():

    data = requests.get("https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-cartographie_formations_parcoursup/exports/json").json()
    count_formation = len(data)
    print( "len est : >>> ",count_formation)
    N = 10
    
    for i in range(N):
        
        formation = data[i]

        if(formation.get('annee')!="2025" ): # on a des éléments vide à cause de ceci dans le tableau , il faut mettre append alors , À FIXER !!!!!!!! > qui me donne 25886 formations en 2025 , assez bien 
            continue 


        extraction_donnee_fiche(formation)

        



