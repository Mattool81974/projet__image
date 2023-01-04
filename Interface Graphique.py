from MLib import * #Le projet utilise MLib version 0.4.0, allez visiter mon site pour en savoir plus: https://matto.glitch.me/?mlib=go
from Projet import *

TAILLE=(500, 500) #La taille de la fenêtre

fenetre=display.set_mode(TAILLE) #Création de la fenêtre pygame
app = MFenetre(fenetre, "Mon app", afficherFps=True) #Création de la fenêtre MLib
image = MImage("", (0, 50), (500, 450), app) #Création de l'élément graphique où sera affiché l'image
ouvrir = MBouton("Ouvrir une image", (0, 0), (150, 50), app, actionAuSurvol="policeTaille=22", bordureLargeur=2, policeTaille=20, texteAlignement="CC")
#Bouton pour ouvrir une image
ouvrirInterface = MWidget((0, 50), (500, 450), app) #Widget qui contient tout le nécessaire pour ouvrir une image
ouvrirInterface.set_visible(False) #Interface invisible de base
ouvrirEntreeTexte = MEntreeTexte((25, 25), (450, 50), ouvrirInterface, bordureLargeur=2, ligneMax=2, longueurMax=126, policeTaille=16, texteAlignement="GC") #Entrée texte qui contient le lien de l'image
ouvrirIllustration = MImage("", (100, 80), (300, 300), ouvrirInterface, imageAlignement="JJ")

while True:
    app.frame() #Update de la fenêtre MLib

    if ouvrir.get_isFocused(): #Si le bouton pour ouvrir un lien d'image clické
        image.set_visible(False)
        ouvrirInterface.set_visible(True)

    if ouvrir.get_visible(): #Si l'interface de lien d'image est clické
        lien = ouvrirEntreeTexte.get_texte()
        lienInfo = fichierInfo(lien, "Image")
        if lienInfo["Existe"] and (lienInfo["Extension"] == "png" or lienInfo["Extension"] == "jpg"):
            ouvrirIllustration.set_imageLien(lienInfo["LienFormate"])
        else:
            ouvrirIllustration.set_imageLien("")

    display.flip() #Update de la fenêtre pygame