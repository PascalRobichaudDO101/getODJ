#!c:\python34\python.exe
# coding: utf8

"""
Télécharger les nouveaux fichiers PDF de l'ordre du jour sur le site de la Ville de Montréal

Version 1.0, 2015-08-19
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""

__version__ = "$1.0$"
# $Source$

import os
import datetime
import requests
import wget
from bs4 import (
    BeautifulSoup,
    BeautifulStoneSoup, 
)


def afficher_statut_traitement(statut):

    date_heure = datetime.datetime.now()
    statut = statut.strip()
    
    print(statut + ": " + date_heure.strftime('%Y-%m-%d %H:%M:%S') )    
    
    return None
    
    
def getLiensFichiersODJ(LIEN_PREFIXE):

    #url: sera à modifier éventuellement pour télécharger tous les fichiers d'ordre du jour
    url = "http://ville.montreal.qc.ca/portal/page?_pageid=5798,85945578&_dad=portal&_schema=PORTAL&dateDebut=2015"
    liens_PDF2 = []
    
    r = requests.get(url) 
    r.encoding = "utf-8" 

    #Mettre le contenu de la page dans BeautifulSoup
    soup = BeautifulSoup(r.content, "html.parser") 

    liens_PDF = soup.find_all("a",{"class":"eMediumGrey10"}) 
    
    for item in liens_PDF:                                      #Est-ce qu'il y a moyen de faire mieux???
        liens_PDF2.append(LIEN_PREFIXE + item.get('href'))
    
    return liens_PDF2
    

#Vérifie si le lien vers le fichier a déjà été traité
#Les liens sont conservés dans le fichier liens_traites.txt
def estLienTraite(REPERTOIRE, lien):  
    
    reponse = False
    
    with open(REPERTOIRE + "\\liens_traites.txt", 'r') as f:
        
        for ligne in f:   
            
            if lien.strip() in ligne.strip():
                reponse = True  
                break

    return reponse
    

def ajouterLienTraite(REPERTOIRE, lien):
    
    #!!!A corriger: mettre le retour de ligne
    with open(REPERTOIRE + "\\liens_traites.txt", 'a') as f:
        f.write(lien)
        
    return None
    
    
def getFile(REPERTOIRE_PDF, url):
                        
    afficher_statut_traitement("Début du téléchargement de " + url)
    
    #fichier_PDF = os.path.join(REPERTOIRE_PDF, "\\odf.pdf")   ne marche pas avec os.path.join ??!!??
    fichier_PDF = REPERTOIRE_PDF + "\\odf.pdf"
    fichier = wget.download(url, fichier_PDF)                   #Référence: https://bitbucket.org/techtonik/python-wget/src
    
    afficher_statut_traitement("Fin   du téléchargement de " + url)
    
    return None

    
def main():   
    """Partie principale du traitement.

    Télécharger les nouveaux fichiers d'ordre du jour
    """
    #Répertoire de travail su script
    REPERTOIRE = "C:\\ContratsOuvertsMtl"

    # Répertoire où les fichiers PDF sont enregistrés
    REPERTOIRE_PDF = REPERTOIRE + "\\Ordres_du_jour\\PDF"
    
    # Début de l'hyperlien pour télécharger le fichier PDF de l'Ordre du jour
    # Le lien est donné en relatif dans le code HTML de la page
    LIEN_PREFIXE = "http://ville.montreal.qc.ca"

    afficher_statut_traitement("Début de traitement")
    
    #Scraper les liens des fichiers
    liens_PDF = getLiensFichiersODJ(LIEN_PREFIXE)
    
    #Télécharger le fichier s'il n'a pas déjà été traité
    for lien in liens_PDF:

        if not estLienTraite(REPERTOIRE, lien):

            getFile(REPERTOIRE_PDF, lien)
            
            ajouterLienTraite(REPERTOIRE, lien)

    afficher_statut_traitement("Fin  de traitement")
    
    return None
    
    
if __name__ == '__main__':
   main()
