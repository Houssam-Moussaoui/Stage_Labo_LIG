from selenium import webdriver 
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()  
driver.get("https://dossierappel.parcoursup.fr/Candidat/carte")

time.sleep(8)

soup = BeautifulSoup(driver.page_source, 'lxml')
courses_cards = soup.find("div", id="courses-cards")


liste_formation_page1 = courses_cards.find_all("div",class_ ="fr-card")

for i in range(len(liste_formation_page1)):

    infos = (liste_formation_page1[i]).find("div",class_="fr-card__content")

    if(infos is None):
        print(i)
    else:

        type = infos.find("div").find("p").text

        infos_str = f'Formation de type {type} ,   '
        
        #infos_str = f'Formation de type {infos.div.p.text} , {infos.h3.title} , {(infos.find("div",class_="fr-card__desc")).p.span.text}  '

        print(infos_str)




driver.quit()
