import requests
from bs4 import BeautifulSoup

from utils import nettoyer

reponse = requests.get("https://dossierappel.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_ta_cod=39395&typeBac=0&originePc=0")

html = BeautifulSoup(reponse.text,"lxml")


titre = html.find("h2",class_="fr-h3 fr-my-1w").text.strip() 

badges =   html.find_all("span",class_="fr-badge pca-badge-custom") #Établissement - FORMATION
badges_text = [  badge.text  for badge in badges]


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
langues_section = html.find("section",id="acc-lang-opt")

if langues_section:
    langues =  [' '.join(langue.text.replace('\n', ' ').replace('\t', ' ').split())    for langue in langues_section.ul.find_all("li") ]



#adresse

adresse = ""
site_web =""
h4_adresse = html.find("h4",string=lambda text: text and "Établissement" in text)

if(h4_adresse):
    p_adresse = h4_adresse.find_next_sibling('p')
    if(p_adresse):
        adresse =  nettoyer(p_adresse.text.strip())
        
        # Extraction du site web
        a_site = p_adresse.find('a', id=lambda x: x and 'lien-site-internet' in x)
        if a_site:
            site_web = a_site.get('href', '')





print(adresse)
print(site_web)


