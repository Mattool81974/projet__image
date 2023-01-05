#Importation des bibliothèques nécessaires (pygame pour le fenêtre et sys pour le contrôle de l'application)
from PIL import Image
from pyperclip import *
from math import *
import os
from pygame import *
from sys import *
from time import time_ns
import pygame
pygame.init()

ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHA_LOWER = "abcdefghijklmnopqrstuvwxyz"
NUMERICS = "1234567890"
SYMBOLS_KEYPAD_LITTLE = " &é\"'(-è_çà)=^$*ù!:;,~#}{[|`\\^@]¤"

def fichierInfo(fichier: str, type: str): #Obtenir des informations sur un fichier
    fichier.replace("\\", "/") #Formater le lien du fichier
    if len(fichier) > 0:
        if fichier[0] == "\"": #Retirez des guillemets au début et à la fin du lien
            fichier = fichier[1:-1]+ fichier[-1]
        if fichier[-1] == "\"":
            fichier = fichier[0:-1]
    extension = "" #Extension du fichier
    imageTaille = (-1, -1) #Taille de l'image si le fichier est un image
    if os.path.exists(fichier): #Si il existe
        extension = fichier.split(".")[-1]
        if type == "Image" and (extension == "png" or extension == "jpg"):  # Caractéristiques images
            image = Image.open(fichier)
            imageTaille = image.size
    retour = {"Existe": os.path.exists(fichier), "Extension": extension, "LienFormate": fichier, "ImageTaille": imageTaille}
    return retour

def strAlphaUpper(strC): #Savoir si le str est entièrement consitué de lettre de l'alphabet en majuscule
    for c in strC:
        if ALPHA_UPPER.count(c) <= 0:
            return False
    return True

def strAlphaLower(strC): #Savoir si le str est entièrement consitué de lettre de l'alphabet en majuscule
    for c in strC:
        if ALPHA_LOWER.count(c) <= 0:
            return False
    return True

def strAlpha(strC): #Savoir si le str est entièrement constitué de lettre de l'alphabet
    for c in strC:
        if (not strAlphaUpper(c)) and (not strAlphaLower(c)):
            return False
    return True

def strContent(strC): #Savoir si le str contient de l'alphabet, nombre ...
    alphaUpper = False
    alphaLower = False
    numerics = False
    for c in strC:
        if ALPHA_UPPER.count(c) > 0:
            alphaUpper = True
        elif ALPHA_LOWER.count(c) > 0:
            alphaLower = True
        elif NUMERICS.count(c) > 0:
            numerics = True
    return alphaUpper, alphaLower, numerics

class MWidget: #Définition d'une classe représentant tout les widgets dans la GUI
    def __init__(self, position, taille, parent = None, arrierePlanCouleur = (255, 255, 255, 1), curseurSurvol = SYSTEM_CURSOR_ARROW, type = "Widget"): #Constructeur d'un widget avec comme paramètre la taille
        self.arrierePlanCouleur = arrierePlanCouleur
        self.curseurSurvol = curseurSurvol
        self.enfant = [] #Attributs de type liste comprenant tout les enfants de la fenêtre
        self.fenetrePrincipale = self #Variable contenant la fenêtre principale
        self.focus = False
        self.isFocused = False
        self.globalPosition = position #Variable contenant la position par rapport à la fenêtre principale
        self.parent = parent #Parent du widget (si None, alors le widget est une fenêtre de base)
        self.position = position
        self.taille = taille
        self.visible = True #Est ce que le widget est visible
        self.type = type #Variable contenant le type de widget
        
        if parent != None:
            self.parent.__nouveauEnfant(self) #Rajouter un enfant au widget parent

        fenetreBuff = self #Variable temporaire pour chercher la fenêtre principale
        while True: #Chercher la fenêtre principale
            if fenetreBuff.type != "Fenetre": #Si le widget anbalysé n'est pas la fenêtre principale
                if fenetreBuff.parent != None: #Si l'objet à un parent
                    fenetreBuff = fenetreBuff.parent #Mettre le widget analysée au parent du widget analysé
                    self.globalPosition = (self.globalPosition[0] + fenetreBuff.position[0], self.globalPosition[1] + fenetreBuff.position[1]) #Changer le position globale de l'objet
                else:
                    break #Quitter la boucle
            else:
                self.fenetrePrincipale = fenetreBuff #Mettre la fenêtre principale au widget analysé
                self.fenetrePrincipale._nouvelleElement(self) #Dire à la fenêtre que cette éléments existe
                break #Quitter la boucle
        
    def __enleverEnfant(self, enfant): #Enlever un enfant à ce widget (fonction privée)
        if self.enfant.count(enfant) > 0:
            self.enfant.remove(enfant)

    def get_arrierePlanCouleur(self): #Retourne la couleur d'arrière plan du widget
        return self.arrierePlanCouleur

    def get_curseurSurvol(self): #Retourne le curseur au survol du widget
        return self.curseurSurvol

    def get_enfant(self): #Retourne tous les enfants du widget
        return self.enfant

    def get_fenetrePrincipale(self): #Retourne la fenetre principale du widget
        return self.fenetrePrincipale

    def get_focus(self): #Retourne si le widget est focus ou non
        return self.focus

    def get_globalPosition(self):
        return self.globalPosition

    def get_isFocused(self): #Retourne si le widget est clické pendant cette frame ou non
        return self.isFocused

    def get_parent(self): #Retourne le parent du widget
        return self.parent

    def get_position(self): #Retourne la position du widget
        return self.position

    def get_rect(self):
        return self.position + self.taille

    def get_survol(self): #Retourne si le widget est survolé par le curseur ou pas
        positionSouris = mouse.get_pos()
        if positionSouris[0] > self.globalPosition[0] and positionSouris[0] < self.globalPosition[0] + self.taille[0] and positionSouris[1] > self.globalPosition[1] and positionSouris[1] < self.globalPosition[1] + self.taille[1]:
            return True
        return False

    def get_type(self): #Retourne le type du widget
        return self.type

    def get_taille(self): #Retourne la taille du widget
        return self.taille

    def get_visible(self): #Retourne si le widget est visible
        return self.visible

    def __nouveauEnfant(self, enfant): #Ajouter un enfant à ce widget (fonction privée)
        if self.enfant.count(enfant) > 0:
            self.enfant.remove(enfant)
        self.enfant.append(enfant)

    def _render(self): #Méthode permettant de renvoyer une image de la fenêtre
        retour = Surface(self.taille, SRCALPHA).convert_alpha() #Création de l'image qui sera retourné à la fin
        retour.fill(self.arrierePlanCouleur)
        if self.get_survol():
            self.fenetrePrincipale.set_curseur(self.curseurSurvol)
        retour = self._renderBeforeHierarchy(retour) #Appel de la fonction pour appliquer un render avec celle des widgets enfants
        for surface in self.enfant: #Application des render des enfants
            if surface.visible: #Si l'enfant est visible
                img = surface._render()
                retour.blit(img, surface.get_rect())
        retour = self._renderAfterHierarchy(retour) #Appel de la fonction pour appliquer un render après celle des widgets enfants
        return retour

    def _renderAfterHierarchy(self, surface): #Méthode permettant de modifier le rendu de render() avant que la hiérarchie soit appliqué, à ré-implémenter
        return surface

    def _renderBeforeHierarchy(self, surface): #Méthode permettant de modifier le rendu de render() avant que la hiérarchie soit appliqué, à ré-implémenter
        return surface

    def set_arrierePlanCouleur(self, couleur): #Change la couleur d'arrière plan du widget
        self.couleur = couleur

    def set_curseurSurvol(self, curseurSurvol): #Change la couleur d'arrière plan du widget
        self.curseurSurvol = curseurSurvol
    
    def set_parent(self, parent): #Retourne le parent du widget
        if self.parent != None:
            self.parent.__enleverEnfant(self)
        parent.__nouveauEnfant(self)
        self.parent = parent

    def set_position(self, position): #Change la position du widget
        self.position = position
        self.globalPosition = position
        fenetreBuff = self #Variable temporaire pour chercher la fenêtre principale
        while True: #Chercher la fenêtre principale
            if fenetreBuff.type != "Fenetre": #Si le widget anbalysé n'est pas la fenêtre principale
                if fenetreBuff.parent != None: #Si l'objet à un parent
                    fenetreBuff = fenetreBuff.parent #Mettre le widget analysée au parent du widget analysé
                    self.globalPosition = (self.globalPosition[0] + fenetreBuff.position[0], self.globalPosition[1] + fenetreBuff.position[1]) #Changer le position globale de l'objet
                else:
                    break #Quitter la boucle
            else:
                self.fenetrePrincipale = fenetreBuff #Mettre la fenêtre principale au widget analysé
                self.fenetrePrincipale._nouvelleElement(self) #Dire à la fenêtre que cette éléments existe
                break #Quitter la boucle

    def set_taille(self, taille): #Change la taille du widget
        self.taille = taille

    def set_visible(self, visible): #Change la visibilité du widget
        self.visible = visible



class MFenetre(MWidget): #Définition d'une classe représentant la fenêtre principale
    def __init__(self, fenetre, titre = "Fenêtre MGui", afficherFps = False, arrierePlanImage="", arrierePlanImageAlignement="GH", arrierePlanImageParSeconde=24, arrierePlanCouleur = (255, 255, 255, 1), curseurSurvol = SYSTEM_CURSOR_ARROW): #Constructeur qui prend la taille en paramètre
        self.toutLesElements = [] #Liste de tout les éléments de la fenêtre
        MWidget.__init__(self, (0, 0), fenetre.get_size(), None, arrierePlanCouleur, curseurSurvol, "Fenetre") #Constructeur parent
        self.afficherFps = afficherFps
        self.arrierePlanImage = None
        self.arrierePlanImageAlignement = arrierePlanImageAlignement
        self.actuelFrameGif = 0 #Frame du gif actuel
        if os.path.exists(arrierePlanImage): #Charger l'image de l'arrière plan
            self.arrierePlanImage = image.load(arrierePlanImage)
        else:
            sep = arrierePlanImage.split(".")
            if sep[-1] == "gif": #Fichier gif split
                self.arrierePlanImage = ""
                for i in range(len(sep) - 1):
                    self.arrierePlanImage += sep[i]
                self.actuelFrameGif = 0
            else: #Le fichier n'existe pas
                self.arrierePlanImage = None
        self.arrierePlanImageParSeconde = arrierePlanImageParSeconde #Vitesse du gif d'arrière plan en images par secondes
        self.arrierePlanImageParSecondeEcoule = 0 #Temps écoulé depuis la dernière update du gif
        self.caplockPressee = False #Savoir si le bouton pour bloquer les majuscule est pressé
        self.ctrlDroitePressee = False #Savoir si le bouton controle droit est pressée
        self.ctrlGauchePressee = False  #Savoir si le bouton controle gauche est pressée
        self.curseur = SYSTEM_CURSOR_ARROW #Curseur de l'application
        self._deltaTime = time_ns() #Variable tampon pour deltaTime
        self.deltaTime = 0 #Temps entre 2 frames
        self.fenetre = fenetre
        self.fps = 0 #Nombre de frames par secondes
        self.fpsMoyen = 0 #Nombre de frames par secondes en moyenne
        self.fpsNb = 0 #Nombre d'actualisation des fps
        self.fpsNbFrame = 0 #Nombre de frame entre 2 actualisations de fps
        self.positionSouris = mouse.get_pos()  # Stocker la position de la souris dans une variable
        self.set_titreFenetre(titre)
        self.shiftPressee = False #Savoir si le bouton pour les majuscule est pressé
        self.tempsDExecution = 0 #Temps d'éxécution depuis le dernier comptage des fps

    def _nouvelleElement(self, element): #Ajouter un élément à la fenêtre
        if self.toutLesElements.count(element) <= 0:
            self.toutLesElements.append(element)
    
    def _renderBeforeHierarchy(self, surface): #Ré-implémentation de la fonction pour afficher l'image d'arrière plan
        img = None #Création de la variable avec l'image a appliquer
        if self.arrierePlanImage != None: #Le fichier est un gif ou n'existe pas
            if type(self.arrierePlanImage) == str: #Le fichier existe
                if os.path.exists(self.arrierePlanImage):
                    fichiers = os.listdir(self.arrierePlanImage)
                    img = image.load(self.arrierePlanImage + "/" + fichiers[self.actuelFrameGif]) #Image a affiché lors de cette frame
                    self.arrierePlanImageParSecondeEcoule += self.deltaTime
                    if self.arrierePlanImageParSecondeEcoule >= 1/(self.arrierePlanImageParSeconde):
                        self.actuelFrameGif += 1 #Changer l'imageu du gif
                        self.arrierePlanImageParSecondeEcoule = 0
                    if self.actuelFrameGif >= len(fichiers): #Actualiser l'image du gif en cas de problème
                        self.actuelFrameGif = 0
            else: #Le fichier est une fichier image normal
                img = self.arrierePlanImage
        if img != None:
            xImg = 0
            yImg = 0
            if self.arrierePlanImageAlignement[0] == "J": #En cas de justification de l'image
                xQuotient = self.taille[0] / img.get_size()[0]
                img = transform.scale(img, (xQuotient * img.get_width(), xQuotient * img.get_height()))
            elif self.arrierePlanImageAlignement[1] == "J":
                yQuotient = self.taille[1] / img.get_size()[1]
                img = transform.scale(img, (yQuotient * img.get_width(), yQuotient * img.get_height()))
                
            if self.arrierePlanImageAlignement[0] == "C": #Gérer selon l'alignement de l'image
                xImg = self.taille[0] / 2 - img.get_size()[0] / 2
            elif self.arrierePlanImageAlignement[0] == "G":
                xImg = self.taille[0] - img.get_size()[0]
            if self.arrierePlanImageAlignement[1] == "C":
                yImg = self.taille[1] / 2 - img.get_size()[1] / 2
            elif self.arrierePlanImageAlignement[0] == "B":
                yImg = self.taille[1] - img.get_size()[1]
            surface.blit(img, (xImg, yImg, 0, 0))
        return surface

    def frame(self): #Actualise une frame de la fenêtre
        self.deltaTime = (time_ns() - self._deltaTime)/pow(10, 9) #Actualiser le delta time en secondes
        self.tempsDExecution += self.deltaTime #Actualiser le temps d'éxécution
        self.fpsNbFrame += 1

        if self.tempsDExecution >= 1: #Actualisation des fps
            self.tempsDExecution -= floor(self.tempsDExecution)
            self.fpsNb += 1
            self.fps = self.fpsNbFrame
            self.fpsNbFrame = 0
            self.fpsMoyen = (self.fpsMoyen + self.fps) / (2)
            if self.afficherFps:
                print("FPS/FPS Moyen:", str(self.fps) + "/" + str(self.fpsMoyen))
        
        self._deltaTime = time_ns() #Préparer le delta time pour le prochain affichage en utilisant _deltaTime

        self.positionSouris = mouse.get_pos() #Stocker la position de la souris dans une variable

        for i in self.toutLesElements:  # Ré-initialiser le focus de frame de chaque éléments
            i.isFocused = False
        
        self.evenement = event.get() #Obtenir tout les évènements
        for evnt in self.evenement: #Chercher dans tout les évènements
            if evnt.type == QUIT: exit() #Si évènement quitter appeler alors quitter
            elif evnt.type == MOUSEBUTTONDOWN: #Si un bouton est clické
                for i in self.toutLesElements: #Ré-initialiser le focus de chaque éléments
                    i.focus = False
                focus = self
                j = 0 #Variable pour vérifier le nombre d'enfant
                while j < len(focus.enfant): #Chercher le widget focus (le plus petit widget et le plus en avant présent sur la route de la souris)
                    i = focus.enfant[j]
                    if i.get_visible() and i.get_globalPosition()[0] < self.positionSouris[0] and self.positionSouris[0] < i.get_globalPosition()[0] + i.get_taille()[0] and i.get_globalPosition()[1] < self.positionSouris[1] and self.positionSouris[1] < i.get_globalPosition()[1] + i.get_taille()[1]:
                        focus = i
                        j = -1
                    j += 1
                focus.focus = True
                focus.isFocused = True
                self.evenement.remove(evnt)
            elif evnt.type == KEYDOWN:
                if evnt.key == K_LSHIFT: #Si la touche pour les majuscules est pressée
                    self.shiftPressee = True
                    self.evenement.remove(evnt)
                if evnt.key == K_LCTRL:  # Si la touche contrôle gauche est pressée
                    self.ctrlGauchePressee = True
                    self.evenement.remove(evnt)
                if evnt.key == K_RCTRL:  # Si la touche contrôle gauche est pressée
                    self.ctrlDroitePressee = True
                    self.evenement.remove(evnt)
                elif evnt.key == K_CAPSLOCK: #Si la touche pour bloquer les majuscule est pressé
                    if self.caplockPressee:
                        self.caplockPressee = False
                    else:
                        self.caplockPressee = True
                    self.evenement.remove(evnt)
            elif evnt.type == KEYUP:
                if evnt.key == K_LSHIFT: #Si la touche pour les majuscules n'est plus pressé
                    self.shiftPressee = False
                    self.evenement.remove(evnt)
                if evnt.key == K_LCTRL:  # Si la touche contrôle gauche n'est plus pressée
                    self.ctrlGauchePressee = False
                    self.evenement.remove(evnt)
                if evnt.key == K_RCTRL:  # Si la touche contrôle gauche n'est plus pressée
                    self.ctrlDroitePressee = False
                    self.evenement.remove(evnt)

        self.set_curseur(self.curseurSurvol) #Initialiser le curseur à une valeur par défaut
        img = self._render()
        self.fenetre.blit(img, self.get_rect())
        mouse.set_cursor(self.curseur)

    def get_actuelFrameGif(self): #Retourne la frame actuel si l'image d'arriere plan est un gif
        return self.actuelFrameGif

    def get_arrierePlanImage(self): #Retourne l'image d'arrière plan
        return self.arrierePlanImage

    def get_arrierePlanImageAlignement(self): #Retourne l'image d'arrière plan alignement
        return self.arrierePlanImageAlignement

    def get_arrierePlanImageParSeconde(self): #Retourne le nombre d'image par seconde a défilé si l'image d'arrière plan est un gif
        return self.arrierePlanImageParSeconde

    def get_arrierePlanImageParSecondeEcoule(self): #Retourne le nombre de seconde écoulé depuis la dernière actualisation de l'image d'arrière plan si celle ci est un gif
        return self.arrierePlanImageParSecondeEcoule

    def get_caplockPressee(self): #Retourne si la touche de vérouillage des majuscule est active.
        return self.caplockPressee

    def get_curseur(self): #Retourne le curseur de la fenêtre
        return self.curseur

    def get_deltaTime(self): #Retourne le deltaTime
        return self.deltaTime

    def get_evenement(self): #Retourne les évènements pygame
        return self.evenement

    def get_fenetre(self): #Retourne la fenêtre pygame sur laquelle afficher le tout
        return self.fenetre

    def get_fps(self): #Retourne le nombre de fps cette seconde
        return self.fps

    def get_fpsMoyen(self): #Retourne le nombre de fps moyen depuis le début de l'application
        return self.fpsMoyen

    def get_positionSouris(self): #Retourne la position de la souris
        return self.positionSouris

    def get_shiftPressee(self): #Retourne si la touche shift est préssé ou non
        return self.shiftPressee

    def get_tempsDExecution(self): #Retourne le temps d'éxécution de l'application
        return self.tempsDExecution

    def get_titreFenetre(self): #Retourne le titre de la fenêtre
        return display.get_caption()

    def get_toutLesElements(self): #Retourne tous les éléments de l'application
        return self.toutLesElements
    
    def set_arrierePlanImage(self, arrierePlanImage): #Change l'image d'arrière plan
        self.arrierePlanImage = arrierePlanImage
        if os.path.exists(arrierePlanImage): #Charger l'image de l'arrière plan
            self.arrierePlanImage = image.load(arrierePlanImage)
        else:
            sep = arrierePlanImage.split(".")
            if sep[-1] == "gif": #Fichier gif split
                self.arrierePlanImage = ""
                for i in range(len(sep) - 1):
                    self.arrierePlanImage += sep[i]
                self.actuelFrameGif = 0
            else: #Le fichier n'existe pas
                self.arrierePlanImage = None

    def set_arrierePlanImageAlignement(self, arrierePlanImageAlignement): #Change l'alignement de l'image d'arrière plan
        self.arrierePlanImageAlignement = arrierePlanImageAlignement

    def set_arrierePlanImageParSeconde(self, arrierePlanImageParSeconde): #Change le nombre d'image par seconde a défilé si l'image d'arrière plan est un gif
        self.arrierePlanImageParSeconde = arrierePlanImageParSeconde
    
    def set_curseur(self, curseur): #Changer le curseur de la fenêtre
        self.curseur = curseur

    def set_titreFenetre(self, titre): #Actualiser le titre de la fenêtre
        self.titre = titre
        display.set_caption(titre)



class MBordure(MWidget): #Définition d'une représentant un widget avec une bordure
    def __init__(self, position, taille, parent, bordureLargeur = 2, bordureCouleur = (0, 0, 0), bordureRayon = 0, borduresLargeurs = [None, None, None, None], borduresRayons=[None, None, None, None], arrierePlanCouleur=(0, 0, 0, 0), curseurSurvol=SYSTEM_CURSOR_ARROW, type="Bordure"): #Constructeur de la classe
        MWidget.__init__(self, position, taille, parent, arrierePlanCouleur, curseurSurvol, type) #Appeler le constructeur de la classe MWidget
        for i in enumerate(borduresLargeurs): #Actualisation des largeurs des bordures
            if borduresLargeurs[i[0]] == None:
                borduresLargeurs[i[0]] = bordureLargeur
        self.bordureLargeur = bordureLargeur
        self.borduresLargeurs = borduresLargeurs
        for i in enumerate(borduresRayons): #Actualisation des rayons des bordures
            if borduresRayons[i[0]] == None:
                borduresRayons[i[0]] = bordureRayon
        self.bordureRayon = bordureRayon
        self.borduresRayons = borduresRayons
        self.bordureCouleur = bordureCouleur
    def _renderBeforeHierarchy(self, surface): #Ré-implémentation de la fonction pour afficher la bordure
        surfaceBordure = Surface(self.taille, SRCALPHA).convert_alpha() #Création de l'image qui contient la bordure
        surfaceBordure.fill((0, 0, 0, 0))
        draw.rect(surfaceBordure, self.bordureCouleur, (0, 0, self.taille[0], self.taille[1]), border_bottom_left_radius=self.borduresRayons[2], border_top_left_radius=self.borduresRayons[3], border_bottom_right_radius=self.borduresRayons[1], border_top_right_radius=self.borduresRayons[0]) #Dessiner la bordure
        draw.rect(surfaceBordure, self.arrierePlanCouleur, (self.borduresLargeurs[3], self.borduresLargeurs[0], self.taille[0] - (self.borduresLargeurs[1] + self.borduresLargeurs[3]), self.taille[1] - (self.borduresLargeurs[2] + self.borduresLargeurs[0])), border_bottom_left_radius=self.borduresRayons[2], border_top_left_radius=self.borduresRayons[3], border_bottom_right_radius=self.borduresRayons[1], border_top_right_radius=self.borduresRayons[0]) #Dessiner l'intèrieur de la bordure
        surface.blit(surfaceBordure, (0, 0, self.taille[0], self.taille[1])) #Coller la bordure sur la surface
        return surface

    def get_bordure(self, i = -1): #Retourne la largeur de la bordure i
        if i == -1:
            return self.bordureLargeur
        return self.borduresLargeurs[i]

    def get_bordureCouleur(self): #Retourne la couleur de la bordure
        return self.bordureCouleur

    def get_bordureRayon(self, i = -1): #Retourne le rayon de la bordure i
        if i == -1:
            return self.bordureRayon
        return self.borduresRayons[i]

    def set_bordure(self, bordureLargeur, i = -1): #Change la largeur de la bordure i
        if i == -1:
            self.bordureLargeur = bordureLargeur
        else:
            self.borduresLargeurs[i] = bordureLargeur

    def set_bordureCouleur(self, couleur): #Cange la couleur de la bordure
        self.bordureCouleur = couleur

    def get_bordureRayon(self, bordureRayon, i = -1): #Change le rayon d'un coin de la bordure i
        if i == -1:
            self.bordureRayon = bordureRayon
        else:
            self.borduresRayons[i] = bordureRayon



class MTexte(MBordure): #Définition d'une classe représentant un texte graphique
    def __init__(self, texte, position, taille, parent, curseur = False, curseurLargeur=2, curseurRepositionnementSouris=False,  curseurTempsDAffichage = 0.4, ligneLongueurMax = -1, ligneMax = 1, longueurMax = -1, policeTaille=12, policeType = "Ariel", texteAlignement = "GH", texteCouleur=(0, 0, 0), bordureCouleur = (0, 0, 0), bordureLargeur = 0, bordureRayon = 0, borduresLargeurs = [None, None, None, None], borduresRayons = [None, None, None, None], arrierePlanCouleur=(0, 0, 0, 0), curseurSurvol=SYSTEM_CURSOR_ARROW, type = "Texte"): #Constructeur
        MBordure.__init__(self, position, taille, parent, bordureLargeur, bordureCouleur, bordureRayon, borduresLargeurs, borduresRayons, arrierePlanCouleur, curseurSurvol, type) #Appel du constructeur parent
        self.curseur = curseur
        self.curseurLargeur = curseurLargeur
        self.curseurPosition = 0 #Défini la position du curseur dans le texte
        self.curseurRepositionnementSouris = curseurRepositionnementSouris #Savoir si la souris peu influencé le positionnement du curseur
        self.curseurTempsDAffichage = curseurTempsDAffichage
        self.curseurTempsDAffichageAffiche = True
        self.curseurTempsDAffichageEcoule = 0 #Temps écoulé depuis le changement de curseur
        if ligneLongueurMax < 0:
            self.ligneLongueurMax = taille[0] - (borduresLargeurs[1] + borduresLargeurs[3])
        else:
            self.ligneLongueurMax = ligneLongueurMax
        self.ligneMax = ligneMax
        self.longueurMax = longueurMax
        self.policeTaille = policeTaille #Affectation des variables de la classe
        if policeType == "defaut":
            policeType = font.get_default_font()
        self.policeType = policeType
        self.texte = texte
        self.textes = texte.split("\n") #Texte split selon les sauts de lignes
        self.textesCoupeParTaille = texte
        self.texteAlignement = texteAlignement
        self.texteCouleur = texteCouleur
        self.texteRect = [(0, 0, 0, 0)]
    def _renderBeforeHierarchy(self, surfaceF): #Ré-implémentation de la fonction pour afficher la bordure
        if self.focus and self.curseur:
            if self.curseurTempsDAffichageEcoule == -1: #Calculer le temps restant à afficher ou non le curseur
                self.curseurTempsDAffichageEcoule = 0
                self.curseurTempsDAffichageAffiche = True
            if self.curseurTempsDAffichageEcoule >= self.curseurTempsDAffichage:
                    while self.curseurTempsDAffichageEcoule >= self.curseurTempsDAffichage:
                        self.curseurTempsDAffichageEcoule -= self.curseurTempsDAffichage
                    if self.curseurTempsDAffichageAffiche:
                        self.curseurTempsDAffichageAffiche = False
                    else:
                        self.curseurTempsDAffichageAffiche = True
                    
        if self.curseurPosition < 0: #Calculer la position du curseur (trop petite ou trop grande)
            self.curseurPosition = 0
        elif self.curseurPosition >= len(self.texte):
            self.curseurPosition = len(self.texte)
        
        xCurseur = 0 #Définir les coordonées du curseur
        yCurseur = 0
        hCurseur = 0

        if len(self.texte) > self.longueurMax and self.longueurMax >= 0: #Vérifier la taille du texte
            self.texte = self.texte[0:self.longueurMax]
        
        surfaceF = MBordure._renderBeforeHierarchy(self, surfaceF) #Appel de la fonction de bordure
        if font.get_fonts().count(self.policeType) <= 0: #Vérification de la police
            self.policeType = "Arial"
        police = font.SysFont(self.policeType, self.policeTaille) #Création de la police

        ligneCurseur = 0  # Variable qui stocke la ligne du curseur
        longueurTotal = 0 #Longueur totale du texte
        texteSurface = []  # Variable qui contient toutes les surfaces du texte
        tailleY = 0  # Variable qui contient la taille de tous les textes
        temp = False #Variable temporaire pour savoir si la position du curseur a été attribué ou non
        temp2 = False  # Variable temporaire secondaire pour savoir si la position du curseur a été attribué ou non

        doitBreak = False
        ligne = ""
        numLigne = 0

        self.textes = []

        if self.curseurRepositionnementSouris and self.isFocused:
            positionSouris = (self.fenetrePrincipale.get_positionSouris()[0] - (self.borduresLargeurs[3] + self.globalPosition[0]), self.fenetrePrincipale.get_positionSouris()[1] - (self.borduresLargeurs[0] + self.globalPosition[1]))
            for c in enumerate(self.texte):  # Générer le texte
                taille = police.size(ligne)
                tailleC = police.size(ligne + c[1])
                longueurTotal += 1
                if positionSouris[0] < tailleC[0] and not temp2:
                    self.curseurPosition = longueurTotal - 1
                    temp2 = True
                    xCurseur = tailleC[0]
                if tailleC[0] <= self.ligneLongueurMax:  # Si la ligne est pas trop longue
                    if c[1] == "\n":
                        if numLigne < self.ligneMax:
                            imageLigne = police.render(ligne, True, self.texteCouleur)
                            tailleY += imageLigne.get_size()[1]
                            texteSurface.append(imageLigne)
                            self.textes.append(ligne)
                            ligne = ""
                            numLigne += 1
                            if not temp:
                                temp2 = False
                        else:
                            numLigne += 1
                            doitBreak = True
                    else:
                        ligne += c[1]
                else:  # Sinon créer un saut de ligne
                    if numLigne < self.ligneMax:
                        imageLigne = police.render(ligne, True, self.texteCouleur)
                        tailleY += imageLigne.get_size()[1]
                        texteSurface.append(imageLigne)
                        self.textes.append(ligne)
                        ligne = c[1]
                        numLigne += 1
                        if not temp:
                            temp2 = False
                    else:
                        numLigne += 1
                        doitBreak = True

                if c[0] == len(self.texte) - 1 or doitBreak:
                    self.textes.append(ligne)
                    numLigne += 1
                    imageLigne = police.render(ligne, True, self.texteCouleur)
                    tailleY += imageLigne.get_size()[1]
                    texteSurface.append(imageLigne)

                if positionSouris[1] <= tailleY and not temp: #Si l'utilisateur a cliqué cette ligne
                    ligneCurseur = numLigne
                    if c[0] == len(self.texte) - 1:
                        if positionSouris[0] > tailleC[0]:
                            self.curseurPosition = longueurTotal
                            xCurseur = tailleC[0]
                    else:
                        if positionSouris[0] > taille[0]:
                            self.curseurPosition = longueurTotal - 1
                            xCurseur = taille[0]
                    temp = True
                    temp2 = True

                if doitBreak:
                    break
        else:
            for c in enumerate(self.texte): #Générer le texte
                tailleC = police.size(ligne + c[1])
                if tailleC[0] <= self.ligneLongueurMax: #Si la ligne est pas trop longue
                    if c[1] == "\n":
                        if numLigne < self.ligneMax:
                            imageLigne = police.render(ligne, True, self.texteCouleur)
                            tailleY += imageLigne.get_size()[1]
                            texteSurface.append(imageLigne)
                            self.textes.append(ligne)
                            ligne = ""
                            numLigne += 1
                        else:
                            doitBreak = True
                    else:
                        ligne += c[1]
                else: #Sinon créer un saut de ligne
                    if numLigne < self.ligneMax:
                        imageLigne = police.render(ligne, True, self.texteCouleur)
                        tailleY += imageLigne.get_size()[1]
                        texteSurface.append(imageLigne)
                        self.textes.append(ligne)
                        ligne = c[1]
                        numLigne += 1
                    else:
                        doitBreak = True

                if c[0] == self.curseurPosition - 1:
                    ligneCurseur = numLigne
                    xCurseur = police.size(ligne)[0]
                    temp = True

                if c[0] == len(self.texte) - 1 or doitBreak:
                    imageLigne = police.render(ligne, True, self.texteCouleur)
                    tailleY += imageLigne.get_size()[1]
                    texteSurface.append(imageLigne)
                    self.textes.append(ligne)

                if doitBreak:
                    break

        if len(texteSurface) <= 0: #Si il n'y a pas de texte à générer
            texteSurface.append(police.render("", True, self.texteCouleur))
            
        multiplier = 1
        xTexte = self.borduresLargeurs[3]
        yTexte = self.borduresLargeurs[0]
        
        if self.texteAlignement[1] == "C": #Calculer l'alignement y du 1er texte
            yTexte = self.taille[1]/2-tailleY/2
        elif self.texteAlignement[1] == "B":
            yTexte = self.taille[1] - (self.borduresLargeurs[2] + tailleY)
            multiplier = -1

        self.texteRect.clear() #Vider les coordonnées des textes
        temp = 0 #Réutilisation de la variable temp
        for c in texteSurface: #Calculer les tailles de chaques texte
            if self.texteAlignement[0] == "C":
                xTexte = self.taille[0]/2 - c.get_size()[0]/2
            elif self.texteAlignement[0] == "D":
                xTexte = self.taille[0] - (self.borduresLargeurs[1] + c.get_size()[0])
             
            if temp == ligneCurseur: #Mettre à jour le curseur
                xCurseur += xTexte
                yCurseur = yTexte
                hCurseur = c.get_size()[1]
                if tailleY == 0:
                    yCurseur = yTexte - hCurseur/2
            temp += 1
                
            surfaceF.blit(c, (xTexte, yTexte, c.get_size()[0], c.get_size()[1]))
            self.texteRect.append((xTexte, yTexte, c.get_size()[0], c.get_size()[1])) #Ajoute des coordonnées aux coordonnées de textes
            yTexte += c.get_size()[1] * multiplier
            
        if self.curseur and self.focus: #Afficher le curseur si nécessaire
            if self.curseurTempsDAffichageAffiche:
                draw.line(surfaceF, self.texteCouleur, (xCurseur, yCurseur), (xCurseur, yCurseur + hCurseur), self.curseurLargeur)
            self.curseurTempsDAffichageEcoule += self.fenetrePrincipale.deltaTime
        else:
            self.curseurTempsDAffichageEcoule = -1
            
        return surfaceF

    def get_curseur(self):
        return self.curseur

    def get_curseurLargeur(self):
        return self.curseurLargeur

    def get_curseurPosition(self):
        return self.curseurPosition

    def get_curseurRepositionnementSouris(self):
        return self.curseurRepositionnementSouris

    def get_curseurTempDAffichage(self):
        return self.curseurTempsDAffichage

    def get_curseurTempsDAffichageAffiche(self):
        return self.curseurTempsDAffichageAffiche

    def get_curseurTempsDAffichageEcoule(self):
        return self.curseurTempsDAffichageEcoule

    def get_ligneLongueurMax(self):
        return self.ligneLongueurMax

    def get_ligneMax(self):
        return self.ligneMax

    def get_longueurMax(self):
        return self.longueurMax

    def get_policeTaille(self):
        return self.policeTaille

    def get_policeType(self):
        return self.policeType
    
    def get_texte(self):
        return self.texte

    def get_textes(self):
        return self.textes

    def get_texteAlignement(self):
        return self.texteAlignement

    def get_texteCouleur(self):
        return self.texteCouleur

    def get_texteRect(self):
        return self.texteRect

    def set_curseur(self, curseur):
        self.curseur = curseur

    def set_curseurLargeur(self, curseurLargeur):
        self.curseurLargeur = curseurLargeur
    
    def set_curseurPosition(self, curseurPosition):
        self.curseurPosition = curseurPosition

    def set_curseurRepositionnementSouris(self, curseurRepositionnementSouris):
        self.curseurRepositionnementSouris = curseurRepositionnementSouris

    def set_curseurTempsDAffichage(self, curseurTempsDAffichage):
        self.curseurTempsDAffichage = curseurTempsDAffichage

    def set_curseurTempsDAffichageAffiche(self, curseurTempsDAffichageAffiche):
        self.curseurTempsDAffichageAffiche = curseurTempsDAffichageAffiche

    def set_curseurTempsDAffichageEcoule(self, curseurTempsDAffichageEcoule):
        self.curseurTempsDAffichageEcoule = curseurTempsDAffichageEcoule

    def set_ligneLongueurMax(self, ligneLongueurMax):
        self.ligneLongueurMax = ligneLongueurMax

    def set_ligneMax(self, ligneMax):
        self.ligneMax = ligneMax

    def set_longueurMax(self, longueurMax):
        self.longueurMax = longueurMax

    def set_policeTaille(self, policeTaille):
        self.policeTaille = policeTaille

    def set_policeType(self, policeType):
        self.policeType = policeType

    def set_texte(self, texte):
        self.texte = texte

    def set_texteAlignement(self, texteAlignement):
        self.texteAlignement = texteAlignement

    def set_texteCouleur(self, texteCouleur):
        self.texteCouleur = texteCouleur



class MBouton(MTexte): #Définition d'une classe représentant un bouton
    def __init__(self, texte, position, taille, parent, actionAuSurvol = "", curseur = False, curseurLargeur=2, curseurRepositionnementSouris=False,  curseurTempsDAffichage = 0.4, ligneLongueurMax = -1, ligneMax = 1, longueurMax = 32, policeTaille=12, policeType = "Ariel", texteAlignement = "GH", texteCouleur=(0, 0, 0), bordureCouleur = (0, 0, 0), bordureLargeur=5, bordureRayon = 0, borduresLargeurs=[None, None, None, None], borduresRayons=[None, None, None, None], arrierePlanCouleur = (255, 255, 255), curseurSurvol = SYSTEM_CURSOR_HAND, type="Bouton"):
        MTexte.__init__(self, texte, position, taille, parent, curseur, curseurLargeur, curseurRepositionnementSouris, curseurTempsDAffichage, ligneLongueurMax, ligneMax, longueurMax, policeTaille, policeType, texteAlignement, texteCouleur, bordureCouleur, bordureLargeur, bordureRayon, borduresLargeurs, borduresRayons, arrierePlanCouleur, curseurSurvol, type)
        self.actionAuSurvol = actionAuSurvol

    def _renderBeforeHierarchy(self, surfaceF):
        taillePolice = self.policeTaille #Plein de variables temporaires pour pouvoir bien utiliser le survol
        texte = self.texte
        if self.get_survol(): #Si l'objet est survolé
            actions = self.actionAuSurvol.split("-")
            for c in actions:
                action = c.split("=")[0]
                if action == "policeTaille":
                    self.policeTaille = int(self.actionAuSurvol.split("=")[1])
                if action == "texte":
                    self.texte = self.actionAuSurvol[len(self.actionAuSurvol.split("=")[1]):len(self.actionAuSurvol)]
        surfaceF = super()._renderBeforeHierarchy(surfaceF)
        self.policeTaille = taillePolice
        self.texte = texte
        return surfaceF

    def get_actionAuSurvol(self):
        return self.actionAuSurvol

    def get_click(self):
        return self.isFocused

    def set_actionAuSurvol(self, actionAuSurvol):
        self.actionAuSurvol = actionAuSurvol


class MEntreeTexte(MTexte): #Définition d'une classe représentant une entrée classe
    def __init__(self, position, taille, parent, caracteresAutorises = "all", texte = "", curseur = True, curseurLargeur=2, curseurRepositionnementSouris=True,  curseurTempsDAffichage = 0.4, ligneLongueurMax = -1, ligneMax = 1, longueurMax = 32, policeTaille=12, policeType = "Ariel", texteAlignement = "GH", texteCouleur=(0, 0, 0), bordureCouleur = (0, 0, 0), bordureLargeur=5, bordureRayon = 0, borduresLargeurs=[None, None, None, None], borduresRayons=[None, None, None, None], arrierePlanCouleur = (255, 255, 255), curseurSurvol = SYSTEM_CURSOR_HAND, type = "EntreeTexte"): #Constructeur d'une entrée texte grâce à la taille, la position, et toutes les variables secondaires
        MTexte.__init__(self, texte, position, taille, parent, curseur, curseurLargeur, curseurRepositionnementSouris, curseurTempsDAffichage, ligneLongueurMax, ligneMax, longueurMax, policeTaille, policeType, texteAlignement, texteCouleur, bordureCouleur, bordureLargeur, bordureRayon, borduresLargeurs, borduresRayons, arrierePlanCouleur, curseurSurvol, type) #Appelle du constructeur de MWidget
        self.caracteresAutorises = caracteresAutorises
    def _renderBeforeHierarchy(self, surface): #Ré-implémentation de la fonction pour afficher l'entrée
        if self.focus: #Si le widget est focus
            for evnt in self.fenetrePrincipale.evenement: #Chercher les évènements du clavier
                if evnt.type == KEYDOWN:
                    caractere = evnt.unicode #Obtenir le code unicode de la touche
                    moveCurseur = len(caractere) #Stocker le mouvement du curseur
                    if evnt.key == K_BACKSPACE:
                        caractere = ""
                        if self.curseurPosition > 0:
                            self.texte = self.texte[0:self.curseurPosition-1] + self.texte[self.curseurPosition:len(self.texte)]
                            moveCurseur = -1
                    elif evnt.key == K_TAB:
                        moveCurseur = 4
                        caractere = "    "
                    elif evnt.key == K_RETURN:
                        moveCurseur = 1
                        caractere = "\n"
                    elif evnt.key == K_LEFT:
                        self.curseurTempsDAffichageAffiche = True
                        self.curseurTempsDAffichageEcoule = 0
                        caractere = ""
                        moveCurseur = -1
                    elif evnt.key == K_RIGHT:
                        self.curseurTempsDAffichageAffiche = True
                        self.curseurTempsDAffichageEcoule = 0
                        caractere = ""
                        moveCurseur = 1
                    elif evnt.key == K_v and (self.fenetrePrincipale.ctrlDroitePressee or self.fenetrePrincipale.ctrlGauchePressee):
                        caractere = paste()
                        moveCurseur = len(caractere)
                    elif evnt.key == K_UP:
                        self.curseurTempsDAffichageAffiche = True
                        self.curseurTempsDAffichageEcoule = 0
                        dernierOffset = 0
                        moveCurseur = 0
                        caractere = ""
                        tailleTotal = 0 #Taille totale du texte
                        for c in enumerate(self.textes):
                            offset = 0
                            tailleTotal += len(c[1])
                            if len(self.texte) > tailleTotal and self.texte[tailleTotal] == "\n":
                                offset = 1
                                tailleTotal += 1
                            if self.curseurPosition + len(c[1]) == tailleTotal:
                                tailleTotal += 1

                            if tailleTotal > self.curseurPosition or c[0] == len(self.textes) - 1: #Si le curseur est dans la ligne étudié
                                posCurseur = (len(c[1]) - ((tailleTotal - offset) - self.curseurPosition)) - offset #Calculé l'équivalent position du curseur
                                if c[0] > 0:
                                    if posCurseur > len(self.textes[c[0] - 1]): #Si le curseur est trop grand pour la ligne d'en haut
                                        posCurseur = len(self.textes[c[0] - 1]) - offset
                                    self.curseurPosition = (tailleTotal - (len(c[1]) + (len(self.textes[c[0] - 1]) + dernierOffset))) + posCurseur #Placé le curseur sur la ligne d'au dessus
                                break
                            elif tailleTotal == self.curseurPosition: #Si le curseur est à la fin de la ligne étudié
                                self.curseurPosition = tailleTotal - len(c[1]) - (1 - offset)
                                break
                            dernierOffset = offset
                    elif evnt.key == K_DOWN:
                        self.curseurTempsDAffichageAffiche = True
                        self.curseurTempsDAffichageEcoule = 0
                        moveCurseur = 0
                        caractere = ""
                        tailleTotal = 0  # Taille totale du texte
                        for c in enumerate(self.textes):
                            offset = 0
                            tailleTotal += len(c[1])
                            if len(self.texte) > tailleTotal and self.texte[tailleTotal] == "\n":
                                offset = 1
                                tailleTotal += 1
                            if tailleTotal > self.curseurPosition:  # Si le curseur est dans la ligne étudié
                                posCurseur = (len(c[1]) - (tailleTotal - self.curseurPosition)) + offset  # Calculé l'équivalent position du curseur
                                if c[0] < len(self.textes) - 1:
                                    if posCurseur > len(self.textes[c[0] + 1]):  # Si le curseur est trop grand pour la ligne d'en bas
                                        posCurseur = len(self.textes[c[0] + 1])
                                    self.curseurPosition = tailleTotal + posCurseur  # Placé le curseur sur la ligne d'au dessous
                                break
                            elif tailleTotal == self.curseurPosition and len(self.textes) > c[0] + 1:  # Si le curseur est à la fin de la ligne étudié
                                self.curseurPosition = tailleTotal + len(self.textes[c[0] + 1]) + offset
                                break
                    if self.caracteresAutorises == "all" or self.caracteresAutorises.count(caractere) > 0: #Si le caractère est authorisé
                        if len(self.texte) + len(caractere) <= self.longueurMax or self.longueurMax < 0: #Si le texte n'est pas trop long
                            self.texte = self.texte[0:self.curseurPosition] + caractere + self.texte[self.curseurPosition:len(self.texte)] #Ajouter le caractère au texte
                            self.curseurPosition += moveCurseur
                    self.fenetrePrincipale.evenement.remove(evnt)
        else:
            curseurTempsDAffichageEcoule = -1
        super()._renderBeforeHierarchy(surface)
        return surface

    def get_caracteresAutorises(self):
        return self.caracteresAutorises

    def set_caracteresAutorises(self, caracteresAutorises):
        self.caracteresAutorises = caracteresAutorises
        
class MImage(MBordure): #Définition d'une classe widget représentant une image
    def __init__(self, imageLien, position, taille, parent, imageAlignement="CC", bordureLargeur = 2, bordureCouleur = (0, 0, 0), bordureRayon = 0, borduresLargeurs = [None, None, None, None], borduresRayons=[None, None, None, None], arrierePlanCouleur=(0, 0, 0, 0), curseurSurvol=SYSTEM_CURSOR_ARROW, type="Image"):
        MBordure.__init__(self, position, taille, parent, bordureLargeur, bordureCouleur, bordureRayon, borduresLargeurs, borduresRayons, arrierePlanCouleur, curseurSurvol, type) #Appel du constructeur parent
        self.imageAlignement = imageAlignement
        self.imageLien = imageLien
        if imageLien != "":
            self._image = image.load(self.imageLien)
            self._imageShowed = image.load(self.imageLien)
            self._ancienneImageTaille = self._imageShowed.get_size()
    def _renderBeforeHierarchy(self, surface): #Fonction réimplémenter de MWidget
        if self.imageLien != "":
            xImage = self.borduresLargeurs[3] #Position x de l'image
            yImage = self.borduresLargeurs[0] #Position y de l'image
            wImage = 1 #Taux d'aggrandissement de l'image dans sa largeur
            hImage = 1 #Taux d'aggrandissement de l'image dans sa hauteur
            if self.imageAlignement[0] == "F": #Rentrer
                ratioConteneur = (self.taille[0] - (self.borduresLargeurs[1] + self.borduresLargeurs[3]))/(self.taille[1] - (self.borduresLargeurs[0] + self.borduresLargeurs[2])) #Ratio du widget
                ratioImage = self._image.get_size()[0]/self._image.get_size()[1] #Ratio de l'image
                if ratioImage > ratioConteneur:
                    wImage = (self.taille[0] - (self.borduresLargeurs[1] + self.borduresLargeurs[3]))/self._image.get_size()[0]
                    hImage = wImage
                else:
                    wImage = (self.taille[1] - (self.borduresLargeurs[0] + self.borduresLargeurs[2]))/self._image.get_size()[1]
                    hImage = wImage
                
                if self.imageAlignement[1] == "C": #La position de l'image
                    if ratioImage > ratioConteneur:
                        yImage = self.taille[1]/2 - (hImage*self._image.get_size()[1])/2
                    else:
                        xImage = self.taille[0]/2 - (wImage*self._image.get_size()[0])/2
                elif self.imageAlignement[1] == "D" or self.imageAlignement[1] == "B":
                    if ratioImage > ratioConteneur:
                        yImage = (self.taille[1] - self.borduresLargeurs[2]) - (hImage*self._image.get_size()[1])
                    else:
                        xImage = (self.taille[0] - self.borduresLargeurs[1]) - (wImage*self._image.get_size()[0])
            else:
                if self.imageAlignement[0] == "C": #Centrer
                    xImage = -self._image.get_size()[0]/2 + self.taille[0] / 2
                elif self.imageAlignement[0] == "D": #Vers la droite
                    xImage = (-self._image.get_size()[0]) + self.taille[0] - self.borduresLargeurs[1]
                elif self.imageAlignement[0] == "J":
                    wImage = (self.taille[0] - (self.borduresLargeurs[0] + self.borduresLargeurs[2]))/self._image.get_size()[0]
            
                yImage = self.borduresLargeurs[0] #Position y de l'image
                if self.imageAlignement[1] == "C": #Centrer
                    yImage = -self._image.get_size()[1]/2 + self.taille[1] / 2
                elif self.imageAlignement[1] == "B": #Vers la droite
                    yImage = (-self._image.get_size()[1]) + self.taille[1] - self.borduresLargeurs[2]
                elif self.imageAlignement[1] == "J":
                    hImage = (self.taille[1] - (self.borduresLargeurs[1] + self.borduresLargeurs[3]))/self._image.get_size()[1]
            
            if wImage * self._image.get_size()[0] != self._ancienneImageTaille[0] or hImage * self._image.get_size()[1] != self._ancienneImageTaille[1]: #Si modification nécessaire
                self._imageShowed = transform.scale(self._image, (wImage*self._image.get_size()[0], hImage*self._image.get_size()[1]))
            
            surface.blit(self._imageShowed, (xImage, yImage, self.taille[0] - (self.borduresLargeurs[3] + self.borduresLargeurs[1]), self.taille[1] - (self.borduresLargeurs[2] + self.borduresLargeurs[0]))) #Dessiner l'image sur la surface

            self._ancienneImageTaille = self._imageShowed.get_size()  # Actualiser ancienneTaille pour la prochaine itération de la fonction

        surface = super()._renderBeforeHierarchy(surface) #Dessiner la bordure
        
        return surface
    
    def get_imageAlignement(self): #Retourne l'alignement de l'image
        return self.imageAlignement
    
    def get_imageLien(self): #Fonction permettant de retourne le lien de l'image
        return self.imageLien
    
    def set_imageAlignement(self, imageAlignement): #Modifie l'alignement de l'image
        self.imageAlignement = imageAlignement
    
    def set_imageLien(self, imageLien, forcer = False): #Fonction permettant de modifier le lien de l'image
        if imageLien == "":
            self.imageLien = imageLien
            self._image = None
            self._imageShowed = None
        else:
            if imageLien != self.imageLien or forcer:
                self.imageLien = imageLien
                self._image = image.load(self.imageLien)
                self._imageShowed = image.load(self.imageLien)
                self._ancienneImageTaille = (0, 0)