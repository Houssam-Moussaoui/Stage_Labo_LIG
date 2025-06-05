import requests
from bs4 import BeautifulSoup


reponse = requests.get("https://dossierappel.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_ta_cod=46495&typeBac=0&originePc=0")

html = BeautifulSoup(reponse.text,"lxml")

print(html)
