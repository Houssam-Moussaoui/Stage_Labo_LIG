import os
from bs4 import BeautifulSoup

from config import *
from data import Data

from util.utils import est_page_erreur





def extraction_data(formation,idx):

    data  = Data(idx)

    extraction_metadonnee(formation,data) # on extrait tous les attribut de la ligne de formation

    url_fiche = os.path.join(HTML_DIR,f'{idx}.html')

    extraction_data_text_from_url(url_fiche,data) #lire le fichier idx.html qui correspond à la fiche de parcoursup et extraire du text 
    

    return data




def extraction_metadonnee(formation,data):

    metadata = data.getMetadata()

    metadata["annee"] = formation.get("annee")
    metadata["etab_uai"] = formation.get("etab_uai")
    metadata["etab_nom"] = formation.get("etab_nom")
    metadata["tc"] = formation.get("tc")

    metadata["tf"] = formation.get("tf", [None])[0] if formation.get("tf") else None
    metadata["nm"] = formation.get("nm", [None])[0] if formation.get("nm") else None
    metadata["fl"] = formation.get("fl", [None])[0] if formation.get("fl") else None
    metadata["app"] = formation.get("app", [None])[0] if formation.get("app") else None
    metadata["int"] = formation.get("int")
    metadata["amg"] = formation.get("amg", [None])[0] if formation.get("amg") else None
    metadata["aut"] = formation.get("aut", [None])[0] if formation.get("aut") else None

    metadata["region"] = formation.get("region")
    metadata["departement"] = formation.get("departement")
    metadata["commune"] = formation.get("commune")
    

    
    # Données GPS
    gps = formation.get("etab_gps", {})
    metadata["gps_lon"] = gps.get("lon")
    metadata["gps_lat"] = gps.get("lat")
    
    # Divers
    metadata["nmc"] = formation.get("nmc")
    metadata["gta"] = formation.get("gta")
    metadata["dataviz"] = formation.get("dataviz")
    metadata["etab_url"] = formation.get("etab_url")

    data.setMetadata(metadata)

    return data



def extraction_data_text_from_url(url_fiche,data):

    with open(f"{url_fiche}","r") as f:
        html = f.read()

    
    soup = BeautifulSoup(html,"lxml")

    
    #extraction de titre de formation
    titre_html = soup.find("h2",class_="fr-h3 fr-my-1w")
    if(titre_html):
        titre = titre_html.text.strip() 

    badges =   soup.find_all("span",class_="fr-badge pca-badge-custom") #Établissement - FORMATION
    badges_text = [  badge.text  for badge in badges]
    badges_text_str = ""
    for badge in badges_text:
        badges_text_str += badge


    infos = soup.find_all("div" ,class_="fr-col-sm-12 fr-col-lg-6 fr-pt-3w") #Présentation de la formation -À savoir -Grille d’analyse des candidatures définie par la commission d'examen des voeux de la formation -L’examen des candidatures par les formations-Établissement - Rechercher une personne avec qui échanger


    presentation =    infos[0].find("div" ,class_="word-break-break-word").text

    a_savoir = soup.find("h4",string = "À savoir").find_parent("div", class_="fr-col-sm-12 fr-col-lg-6 fr-pt-3w")



    frais_scolarite_normal = ""
    h6_normal = soup.find('h6', string=lambda text: text and "Par année" in text)

    if h6_normal:
        p_normal = h6_normal.find_next_sibling('p')
        if p_normal:
            frais_scolarite_normal = (p_normal.text.strip())  



    frais_scolarite_boursier = ""
    h6_boursier = soup.find('h6', string=lambda text: text and "Par année pour les étudiants boursiers" in text)

    if h6_boursier:
        p_boursier = h6_boursier.find_next_sibling('p')
        if p_boursier:
            frais_scolarite_boursier = (p_boursier.text.strip())  

                

    # CVEC
    #cvec_texte = ""
    #cvec_lien = ""
    #h6_cvec = soup.find('h6', string=lambda text: text and "Contribution Vie Etudiante et de Campus" in text)

    #if h6_cvec:
    #    p_cvec = h6_cvec.find_next_sibling('p')
    #    if p_cvec:
    #        cvec_texte = p_cvec.text.strip()
    #        CVEC_LIEN =  "https://cvec.etudiant.gouv.fr/"  # fixe 


    #langues 

    langues = None
    langues_str = ""
    langues_section = soup.find("section",id="acc-lang-opt")

    if langues_section:
        langues =  [' '.join(langue.text.replace('\n', ' ').replace('\t', ' ').split())    for langue in langues_section.ul.find_all("li") ]
        for langue in langues:
            langues_str += langue            


    #adresse

    adresse = ""
    site_etablissement =""
    h4_adresse = soup.find("h4",string=lambda text: text and "Établissement" in text)

    if(h4_adresse):
        p_adresse = h4_adresse.find_next_sibling('p')
        if(p_adresse):
            adresse = p_adresse.text
    

    
    texte = titre + '\n' + presentation +'\n' + frais_scolarite_normal +'\n' + frais_scolarite_boursier +'\n' + langues_str  # c'est assez grand pour le modèle LLM qu'on utilise
    data.setText(texte)


