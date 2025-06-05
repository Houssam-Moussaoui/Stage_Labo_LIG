import requests
from fiche_formation import extraction_donnee_fiche


def main():

    data = requests.get("https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-cartographie_formations_parcoursup/exports/json").json()
    count_formation = len(data)
    print( "len est : >>> ",count_formation)
    N = 10


    for i in range(N):
        formation = data[i]

        annee = formation.get('annee')
        etab_uai = formation.get('etab_uai')
        etab_nom = formation.get('etab_nom')
        tc = formation.get('tc')
        tf = formation.get('tf', [None])[0] if formation.get('tf') is not None else None
        nm = formation.get('nm', [None])[0] if formation.get('nm') is not None else None
        fl = formation.get('fl', [None])[0] if formation.get('fl') is not None else None
        app = formation.get('app', [None])[0] if formation.get('app') is not None else None
        int_field = formation.get('int')  
        amg = formation.get('amg', [None])[0] if formation.get('amg') is not None else None
        aut = formation.get('aut', [None])[0] if formation.get('aut') is not None else None
        region = formation.get('region')
        departement = formation.get('departement')
        commune = formation.get('commune')
        fiche = formation.get('fiche')

        extraction_donnee_fiche(fiche)


        dataivz = formation.get('dataviz')  
        etab_url = formation.get('etab_url')

        gps = formation.get('etab_gps', {})
        lon = gps.get('lon')
        lat = gps.get('lat')

        nmc = formation.get('nmc')
        gta = formation.get('gta')

        # Exemple d'affichage 
        #print(f" {i+1} | {annee} | {etab_nom} | {nm} | {app} | {commune} ({departement})    |  {fiche }")
        #print(i)






main()