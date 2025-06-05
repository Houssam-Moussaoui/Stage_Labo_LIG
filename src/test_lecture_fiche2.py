import requests
from bs4 import BeautifulSoup


reponse = requests.get("https://dossierappel.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_ta_cod=2249&typeBac=0&originePc=0")

html = BeautifulSoup(reponse.text,"lxml")



titre = html.find("h2",class_="fr-h3 fr-my-1w").text

badges = html.find_all("span",class_="fr-badge pca-badge-custom") #Établissement - FORMATION

infos = html.find_all("div" ,class_="fr-col-sm-12 fr-col-lg-6 fr-pt-3w") #Présentation de la formation -À savoir -Grille d’analyse des candidatures définie par la commission d'examen des voeux de la formation -L’examen des candidatures par les formations-Établissement - Rechercher une personne avec qui échanger


presentation =    infos[0].find("div" ,class_="word-break-break-word").p.text

a_savoir = infos[1].text.replace("  "," ")

            


print(f"titre : {titre} \n badges : {badges} \n presentation : {presentation} \n à savoir : {a_savoir}")





