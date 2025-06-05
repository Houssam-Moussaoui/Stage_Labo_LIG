import requests
from bs4 import BeautifulSoup
import os 
import hashlib



# Chemin absolu vers le dossier 'src'
SRC_DIR = os.path.dirname(__file__)
# Racine du projet (un niveau au-dessus de 'src')
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, os.pardir))

# Dossier de cache HTML
CACHE_DIR = os.path.join(PROJECT_ROOT, "bd_html")
os.makedirs(CACHE_DIR, exist_ok=True)




def url_to_filename(url: str) -> str:
    """
    Transforme l'URL en un nom de fichier unique et valide, via un hash MD5.
    """
    h = hashlib.md5(url.encode("utf-8")).hexdigest()
    return f"{h}.html"



def extraction_donnee_fiche(fiche,):


    filename = url_to_filename(fiche)
    file_path = os.path.join(CACHE_DIR, filename)

    html =None




    if(os.path.exists(file_path)): # on vérifie si le fichier existe déjà dans notre base de donnée (bd_html)
        print(f"fichier {file_path} existe déjà dans bd_html")
        with open(file_path,"r",encoding='utf-8') as f:  # si oui , on lit directement le fichier associé 
            html = f.read()
            return html
            
    
    else: #sinon on va le lire avec requests et le stocker dans bd_html , et le marquer dans notre dico ens_fiches
        print(f"fichier {file_path}n'existe pas dans bd_html")

        reponse = requests.get(fiche)

        if(reponse.status_code==200):
            html = BeautifulSoup(reponse.text,"lxml")

            with open(file_path,'a',encoding='utf-8') as f:
                f.write(html.text)
                return html.text


            
        else:
            print("Erreur dans la lecture de la fiche  : ",fiche)
            return ""


    
    

    