#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:           Ivan LUCAS
# Copyright:       (c) 2010-15 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------

import Chemins
import shelve
import os
import re
from Utils import UTILS_Fichiers

DICT_TRADUCTIONS = None

def ChargeTraduction(nom=""):
    """ Charge un fichier de langage """
    global DICT_TRADUCTIONS
    dictTraductions = {}
    
    # Recherche le fichier de langage par d�faut ".lang" puis un �ventuel fichier perso ".xlang"
    for extension in ("lang", "xlang") :
        nomFichier = UTILS_Fichiers.GetRepLang(u"%s.%s" % (nom, extension))
        if os.path.isfile(nomFichier) :
            fichier = shelve.open(nomFichier, "r")
            for key, valeur in fichier.items() :
                key = key.decode("iso-8859-15")
                dictTraductions[key] = valeur
            fichier.close()
            
    # M�morise les traductions
    DICT_TRADUCTIONS = dictTraductions
    
    
    
def _(chaine) :
    """ Traduit une cha�ne """
    # Recherche si une traduction existe
    if DICT_TRADUCTIONS != None :
        if chaine in DICT_TRADUCTIONS :
            return DICT_TRADUCTIONS[chaine]
    
    # Sinon renvoie la chaine par d�faut
    return chaine




def GenerationFichierTextes() :
    listeFichiers = os.listdir(os.getcwd())
    listeFichiersTrouves = []
    dictTextes = {}
    
    # Recherche des textes
    exp = re.compile(r"_\(u\".*?\"\)")
    
    for nomFichier in listeFichiers :
    
            if nomFichier.endswith("py") and nomFichier.startswith("DATA_") == False and nomFichier not in ("CreateurMAJ.py", "CreateurANNONCES.py") :
                # Ouverture du fichier
                fichier = open(nomFichier, "r")
                texte = "\n".join(fichier.readlines())
                fichier.close() 
                
                # Analyse du fichier
                listeChaines = re.findall(exp, texte)
                for chaine in listeChaines :      
                    chaine = chaine [4:-2]
                                  
                    valide = False
                    for caract in "abceghijklmopqrtvwxyz" :
                        if caract in chaine.lower() :
                            valide = True
                    if len(chaine) < 2 :
                        valide = False
                    if "Images/" in chaine :
                        valide = False
                    
                    if valide == True :
                        if (chaine in dictTextes) == False :
                            dictTextes[chaine] = []
                        dictTextes[chaine].append(nomFichier)
    
    # G�n�ration du fichier Shelve
    nomFichier = Chemins.GetStaticPath("Databases/Textes.dat")
    if os.path.isfile(nomFichier) :
        flag = "w"
    else :
        flag = "n"
    fichier = shelve.open(nomFichier, flag)
    for texte, listeFichiers in dictTextes.items() :
        fichier[texte] = listeFichiers
    fichier.close()
    print("Generation du fichier de textes terminee.")

def ConvertShelveEnTexte():
    """ Convertit le fichier Textes.dat en fichier Textes.txt """
    # Lecture du fichier dat
    fichier = shelve.open(Chemins.GetStaticPath("Databases/Textes.dat"), "r")
    listeTextes = []
    for texte, listeFichiers in fichier.items() :
        listeTextes.append(texte)
    fichier.close()
    listeTextes.sort() 
    
    # Enregistrement du fichier texte
    fichier = open(UTILS_Fichiers.GetRepTemp("Textes.txt"), "w")
    for texte in listeTextes :
        fichier.write(texte + "\n")
    fichier.close() 
    print("Fini !")

def FusionneFichiers(code="en_GB"):
    # Lecture du fichier xlang
    fichier = shelve.open(UTILS_Fichiers.GetRepLang(u"%s.xlang" % code), "r")
    dictDonnees = {}
    for texte, traduction in fichier.items() :
        if texte != "###INFOS###" :
            dictDonnees[texte] = traduction
    fichier.close()
    
    # Lecture du fichier lang
    fichier = shelve.open(UTILS_Fichiers.GetRepLang(u"%s.lang" % code), "w")
    for texte, traduction in dictDonnees.items() :
        fichier[texte] = traduction
    fichier.close()
    print("Fusion de %d traductions terminee !" % len(dictDonnees))




if __name__ == "__main__":
    GenerationFichierTextes() 
##    ConvertShelveEnTexte()
##    FusionneFichiers("en_GB")
