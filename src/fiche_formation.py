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
            
    
    else: #sinon on va le lire avec requests et le stocker dans bd_html 
        print(f"fichier {file_path}n'existe pas dans bd_html")

        reponse = requests.get(fiche)

        if(reponse.status_code==200):
            html = BeautifulSoup(reponse.text,"lxml")

            titre = html.find("h2",class_="fr-h3 fr-my-1w").text

            badges = html.find_all("span",class_="fr-badge pca-badge-custom") #Établissement - FORMATION
            badges_str = ""

            for badge in badges:
                badges_str+=badge.text

            infos = html.find_all("div" ,class_="fr-col-sm-12 fr-col-lg-6 fr-pt-3w") #Présentation de la formation -À savoir -Grille d’analyse des candidatures définie par la commission d'examen des voeux de la formation -L’examen des candidatures par les formations-Établissement - Rechercher une personne avec qui échanger


            presentation =    infos[0].find("div" ,class_="word-break-break-word").p.text

            a_savoir = infos[1].text 


            adresse = infos[4].text



            res = titre +"\n"+badges_str+"\n"+presentation+"\n"+a_savoir+"\n"+adresse






            with open(file_path,'a',encoding='utf-8') as f:
                
                f.write(res)
                return res


            
        else:
            print("Erreur dans la lecture de la fiche  : ",fiche)
            return ""


    
    

    