import requests
import pickle
import os
from fiche_formation import extraction_donnee_fiche






def main():

    data = requests.get("https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-cartographie_formations_parcoursup/exports/json").json()
    count_formation = len(data)
    print( "len est : >>> ",count_formation)
    N = 2000
    DEPART = 1500 # on est arrivé jusqu"à 1499 -> next time on commence depuis 1500
    
    for i in range(DEPART,N):
        
        formation = data[i]

        if(formation.get('annee')!="2025" ): # on a des éléments vide à cause de ceci dans le tableau , il faut mettre append alors , À FIXER !!!!!!!! > qui me donne 25886 formations en 2025 , assez bien 
            continue 

        print(i)

        extraction_donnee_fiche(formation)

        break

        



from concurrent.futures import ThreadPoolExecutor, as_completed

def main2():
    data = requests.get(
        "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-cartographie_formations_parcoursup/exports/json"
    ).json()

    print("len est : >>> ", len(data))
    N = 50  # Nombre de formations à traiter

    formations_2025 = [f for f in data[:N] if f.get("annee") == "2025"]

    # Parallélisation
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(extraction_donnee_fiche, formation) for formation in formations_2025]

        for future in as_completed(futures):
            try:
                future.result()  # On force l'exécution et on capte les erreurs
            except Exception as e:
                print("Erreur lors du traitement :", e)


main()