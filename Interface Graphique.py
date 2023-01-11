from MLib import * #Le projet utilise MLib version 0.4.0, allez visiter mon site pour en savoir plus: https://matto.glitch.me/?mlib=go
from Projet import *

TAILLE=(700, 500) #La taille de la fenêtre

fenetre=display.set_mode(TAILLE) #Création de la fenêtre pygame
app = MFenetre(fenetre, "Mon app", afficherFps=True) #Création de la fenêtre MLib
image = MImage("", (0, 50), (500, 450), app, imageAlignement="FC") #Création de l'élément graphique où sera affiché l'image
outilInterface = MTexte("Outil", (502, 50), (196, 498), app, bordureLargeur=2, borduresLargeurs=[None, None, None, None], policeTaille=36, texteAlignement="CH") #Interface pour les outils
outilTitre = MTexte("Ouvrez un outil", (48, 50), (100, 50), outilInterface, bordureLargeur=0, policeTaille=16, texteAlignement="CH") #Nom de l'outil sélectionné
ouvrir = MBouton("Ouvrir une image", (2, 2), (146, 46), app, actionAuSurvol="policeTaille=22", bordureLargeur=2, policeTaille=20, texteAlignement="CC")
#Bouton pour ouvrir une image
ouvrirInterface = MWidget((0, 50), (500, 450), app) #Widget qui contient tout le nécessaire pour ouvrir une image
ouvrirInterface.set_visible(False) #Interface invisible de base
ouvrirEntreeTexte = MEntreeTexte((25, 25), (450, 50), ouvrirInterface, bordureLargeur=2, ligneMax=2, longueurMax=126, policeTaille=16, texteAlignement="GC") #Entrée texte qui contient le lien de l'image
ouvrirIllustration = MImage("", (100, 80), (300, 300), ouvrirInterface, imageAlignement="FC")
ouvrirValider = MBouton("Valider", (200, 390), (100, 50), ouvrirInterface, actionAuSurvol="policeTaille=22", policeTaille=20, texteAlignement="CC")

pixelliser = MBouton("Pixelliser", (150, 2), (146, 46), app, actionAuSurvol="policeTaille=22", bordureLargeur=2, policeTaille=20, texteAlignement="CC")
pixelliserInterface = MWidget((2, 2), (192, 494), outilInterface) #Interface de pixellisation dans l'onglet outil
pixelliserInterface.set_visible(False) #Interface invisible de base
pixelliserTitreNLargeur = MTexte("Largeur pixels:", (0, 75), (192, 30), pixelliserInterface, policeTaille=26, texteAlignement="CH") #Titre pour rentrer n de largeur
pixelliserEntreeNLargeur = MEntreeTexte((50, 125), (92, 30), pixelliserInterface, caracteresAutorises="1234567890", policeTaille=22, longueurMax=8) #Entrer de n de largeur
pixelliserValider = MBouton("Valider", (52, 400), (88, 35), pixelliserInterface, policeTaille=20, actionAuSurvol="policeTaille=22", texteAlignement="CC") #Bouton pour valider la pixellisation

ancienLien = "" #Variable permettant de savoir quel était l'image de la frame d'avant dans l'illustration d'ouverture pour ne pas la changer à chaque frame
ancienLienImage = "" #Variable permettant de savoir quel était l'image de la frame d'avant pour ne pas la changer à chaque frame
imageOriginal = "" #Dernière image ouverte par l'utilisateur
imageLien = "" #Image affiché

while True:
    app.frame() #Update de la fenêtre MLib
    
    if ouvrir.get_isFocused(): #Si le bouton pour ouvrir un lien d'image clické
        image.set_visible(False)
        ouvrirInterface.set_visible(True)
    elif pixelliser.get_isFocused(): #Si le bouton pour pixelliser l'image est clické
        outilTitre.set_texte("Pixelliser")
        pixelliserInterface.set_visible(True)
        
    if image.get_visible():
        if ancienLienImage != imageLien:
            image.set_imageLien(imageLien)
            ancienLienImage = imageLien

    if ouvrir.get_visible(): #Si l'interface de lien d'image est clické
        lien = ouvrirEntreeTexte.get_texte()
        lienInfo = fichierInfo(lien, "Image")
        if lien != ancienLien:
            if lienInfo["Existe"] and (lienInfo["Extension"] == "png" or lienInfo["Extension"] == "jpg"):
                ouvrirIllustration.set_imageLien(lienInfo["LienFormate"])
            else:
                ouvrirIllustration.set_imageLien("")
        ancienLien = lien
        
        if ouvrirValider.get_isFocused() and lienInfo["Existe"]:
            imageLien = lienInfo["LienFormate"]
            image.set_visible(True)
            ouvrirInterface.set_visible(False)

    if pixelliser.get_visible():
        lienInfo = fichierInfo(imageLien, "Image")
        if imageLien != "" and pixelliserEntreeNLargeur.get_texte() != "" and int(pixelliserEntreeNLargeur.get_texte()) > lienInfo["ImageTaille"][0]:
            pixelliserEntreeNLargeur.set_texte(str(lienInfo["ImageTaille"][0]))

        if pixelliserValider.get_isFocused() and lienInfo["Existe"]:
            imageTemp = defi3(lienInfo["LienFormate"], int(pixelliserEntreeNLargeur.get_texte()))
            imageTemp.save("temp.png")
            imageLien = "temp.png"


    display.flip() #Update de la fenêtre pygame