import requests
from bs4 import BeautifulSoup


def extraction_donnee_fiche(fiche):
    reponse = requests.get(fiche)

    if(reponse.status_code==200):
        html = BeautifulSoup(reponse.text,"lxml")

        #print(html.text)
    else:
        print("Erreur dans la lecture de la fiche  : ",fiche)
        return -1

    