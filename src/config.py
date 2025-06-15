import os


# Configuration des chemins
SRC_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, os.pardir))
DATAFRAME_JSON = os.path.join(PROJECT_ROOT,'data','fr-esr-cartographie_formations_parcoursup.json') #base donné qui contient les formatiosn sous fomr json
HTML_DIR = os.path.join(PROJECT_ROOT, "data", "data_html")  # chemin où se trouve tous les fichiers .html de tous les fichies
FAISS_DIR = os.path.join(PROJECT_ROOT, "data", "data_faiss")
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "data")



#equivalent de chaque attribut 
MAPPING = {  
    "annee": "Année",
    #"etab_uai": "Code établissement (UAI)",
    "etab_nom": "Nom de l'établissement",
    #"tc": "Code de la formation",
    "tf": "Type de formation",
    "nm": "Nom de la formation",
    "fl": "Filière",
    "app": "Formation en apprentissage",
    "int": "Internat",
    "amg": "Aménagements spécifiques",
    "aut": "Autres informations",
    "region": "Région",
    "departement": "Département",
    "commune": "Ville",
    #"gps_lon": "Longitude",
    #"gps_lat": "Latitude",
    "nmc": "Nom complet",
    #"gta": "Code GTA",
    #"dataviz": "Lien Dataviz",
    "etab_url": "Site web de l'établissement"
}



#lien de fiche vide
LIEN_VIDE = {668,1096,1149,1265}