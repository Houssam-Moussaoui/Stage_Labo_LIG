
from config import *


class Data:
    
    def __init__(self,idx:int):

        dico_metadata = {
                "annee": "",
                "etab_uai": "",
                "etab_nom": "",
                "tc": "",
                "tf": "",
                "nm": "",
                "fl": "",
                "app": "",
                "int": "",
                "amg": "",
                "aut": "",
                "region": "",
                "departement": "",
                "commune": "",
                "gps_lon": "",
                "gps_lat": "",
                "nmc": "",
                "gta": "",
                "dataviz": "",
                "etab_url": ""
            }

        self.text = ""
        self.metadata = dico_metadata
        self.idx = idx # pour retrouver son indice dans liste_data

    
    def setText(self,text):
        self.text = text

    def getText(self):
        return self.text
    
    def setMetadata(self,metdata):
        self.metadata = metdata

    def getMetadata(self):
        return self.metadata
    
    def getIdx(self): #return le message à coder pour devenir un vector : mélange entre qlq metadonnée et text parsé de fiche HTML
        return self.idx
    
    def getdataÀcoder(self):
        metadata = self.getMetadata()
        output = ""
        for key, val in MAPPING.items():
            value = str(metadata.get(key, ""))
            output += f"{val} : {value}\n"
        output += f"\n---\nDescription formation :\n{self.getText()}"
        return output




    


    