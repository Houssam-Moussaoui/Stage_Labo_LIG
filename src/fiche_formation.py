import requests
from bs4 import BeautifulSoup
import os 
import hashlib
import pickle




# Chemin absolu vers le dossier 'src'
SRC_DIR = os.path.dirname(__file__)
# Racine du projet (un niveau au-dessus de 'src')
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, os.pardir))

# Dossier de faiss
DATA_ENTREE_DIR = os.path.join((os.path.join(PROJECT_ROOT, "data"))  , "data_entree"   )
os.makedirs(DATA_ENTREE_DIR, exist_ok=True)






def url_to_filename(url: str) -> str:
    """
    Transforme l'URL en un nom de fichier unique et valide, via un hash MD5.
    """
    h = hashlib.md5(url.encode("utf-8")).hexdigest()
    return f"{h}.pkl"



def extraction_donnee_fiche(formation):

    fiche = fiche = formation.get('fiche')

    filename = url_to_filename(fiche)
    file_path = os.path.join(DATA_ENTREE_DIR, filename)




    if(os.path.exists(file_path)):
        print(f"fichier {file_path} existe déjà dans data_html")
        #with open(file_path,"rb") as f:  # si oui , on lit directement le fichier associé 
            #data = pickle.load(f)
            #normalement , on a pas besoin de ici de faire des choses !!!!
    else:

        # les metadonnées - facile

        elm = {"text":"" ,
                "metadonnee":{ 
                    "annee": "",
                    "etab_uai":"",
                    "etab_nom":"",
                    "tc":""
                },
                "in":0
            }

        
        
        elm = extraction_metadonnee(elm , formation)

        #2 le text html depuis fiche

        print(f"fichier {file_path}n'existe pas dans data_html")

        reponse = requests.get(fiche)

        if(reponse.status_code==200):
            html = BeautifulSoup(reponse.text,"lxml")

            titre_html = html.find("h2",class_="fr-h3 fr-my-1w")
            if(titre_html):
                titre = titre_html.text.strip() 

            badges =   html.find_all("span",class_="fr-badge pca-badge-custom") #Établissement - FORMATION
            badges_text = [  badge.text  for badge in badges]
            badges_text_str = ""
            for badge in badges_text:
                badges_text_str += badge


            infos = html.find_all("div" ,class_="fr-col-sm-12 fr-col-lg-6 fr-pt-3w") #Présentation de la formation -À savoir -Grille d’analyse des candidatures définie par la commission d'examen des voeux de la formation -L’examen des candidatures par les formations-Établissement - Rechercher une personne avec qui échanger


            presentation =    infos[0].find("div" ,class_="word-break-break-word").text

            a_savoir = html.find("h4",string = "À savoir").find_parent("div", class_="fr-col-sm-12 fr-col-lg-6 fr-pt-3w")



            frais_scolarite_normal = ""
            h6_normal = html.find('h6', string=lambda text: text and "Par année" in text)

            if h6_normal:
                p_normal = h6_normal.find_next_sibling('p')
                if p_normal:
                    frais_scolarite_normal = (p_normal.text.strip())  



            frais_scolarite_boursier = ""
            h6_boursier = html.find('h6', string=lambda text: text and "Par année pour les étudiants boursiers" in text)

            if h6_boursier:
                p_boursier = h6_boursier.find_next_sibling('p')
                if p_boursier:
                    frais_scolarite_boursier = (p_boursier.text.strip())  

                        

            # CVEC
            cvec_texte = ""
            cvec_lien = ""
            h6_cvec = html.find('h6', string=lambda text: text and "Contribution Vie Etudiante et de Campus" in text)

            if h6_cvec:
                p_cvec = h6_cvec.find_next_sibling('p')
                if p_cvec:
                    cvec_texte = p_cvec.text.strip()
                    CVEC_LIEN =  "https://cvec.etudiant.gouv.fr/"  # fixe 


            #langues 

            langues = None
            langues_str = ""
            langues_section = html.find("section",id="acc-lang-opt")

            if langues_section:
                langues =  [' '.join(langue.text.replace('\n', ' ').replace('\t', ' ').split())    for langue in langues_section.ul.find_all("li") ]
                for langue in langues:
                    langues_str += langue            


            #adresse

            adresse = ""
            site_etablissement =""
            h4_adresse = html.find("h4",string=lambda text: text and "Établissement" in text)

            if(h4_adresse):
                p_adresse = h4_adresse.find_next_sibling('p')
                if(p_adresse):
                    adresse = p_adresse.text
            




            elm["text"] = titre +"\n"+ badges_text_str +"\n"+ presentation +"\n"+ frais_scolarite_normal +"\n"+frais_scolarite_boursier  +"\n"+ cvec_texte +"\n"+cvec_lien +"\n"+langues_str 

            elm["in"] = 0

            with open(file_path,'wb',) as f:
                pickle.dump(elm,f)


            
        else:
            print("Erreur dans la lecture de la fiche  : ",fiche)
            




    
    

    
def extraction_metadonnee(elm,formation):

    elm["metadonnee"]["annee"] = formation.get('annee')
    elm["metadonnee"]["etab_uai"] = formation.get('etab_uai')
    elm["metadonnee"]["etab_nom"] = formation.get('etab_nom')
    elm["metadonnee"]["tc"] = formation.get('tc')
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


    dataivz = formation.get('dataviz')  
    etab_url = formation.get('etab_url')

    gps = formation.get('etab_gps', {})
    lon = gps.get('lon')
    lat = gps.get('lat')

    nmc = formation.get('nmc')
    gta = formation.get('gta')

    return elm