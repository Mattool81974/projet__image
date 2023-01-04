from math import *
from PIL import *
from PIL.Image import *
from PIL.ImageDraw import *
from random import *

def IntToStrBin(n: int, taille = 8):
    resultat = str(bin(n)).split("b")[1]
    if len(resultat) < taille:
        for i in range(taille - len(resultat)):
            resultat = "0" + resultat
    return resultat

def binStrToInt(n: str): #Convertir un int binaire dans un str en entier base dix
    resultat = 0
    for i in enumerate(n[::-1]):
        if(i[1] == "1"):
            resultat += 2 ** i[0]
    return resultat

def defi3(imageLien: str, nw: int, nh: int = None): #Fonction correspondant au défi 3
    if nh is None:
        nh = nw
    image = open(imageLien) #Chargé l'image
    imageTaille = image.size #Obtenir la taille de l'image
    imagePixeliseTaille = (imageTaille[0]//nw, imageTaille[1]//nh) #Obtenir la taille de l'image en pixel de n de large
    imageTailleErreurY = imageTaille[1]%nh #Nombre de pixels d'erreurs à la hauteur
    IMAGETAILLEERREURY = imageTaille[1]%nh #Pareil que ImageTailleErreurY mais constant
    imageTailleErreurYErreur = IMAGETAILLEERREURY%imagePixeliseTaille[1] #Nombre de pixel d'erreurs pour le calcul du nombre de pixels d'erreurs à la hauteur
    offsetY = 0 #Taux de décalage de y pour éviter des erreurs et des zones non pixellés
    multiplieurHauteur = 1 #Variable permettant de compter ou non la hauteur à retirer
    if imageTailleErreurY == 0: #Si il n'y aura aps de pixels non pixellisés
        multiplieurHauteur = 0 #Ignorer la hauteur à retirer
    for y in range(0, imageTaille[1] - nh * multiplieurHauteur, nh): #Parcourir chaque pixel de l'image
        imageTailleErreurX = imageTaille[0]%nw #Nombre de pixels d'erreurs à la largeur
        IMAGETAILLEERREURX = imageTaille[0] % nw  # Pareil que ImageTailleErreurY mais constant
        imageTailleErreurXErreur = IMAGETAILLEERREURX%imagePixeliseTaille[0] ##Nombre de pixel d'erreurs pour le calcul du nombre de pixels d'erreurs à la largeur
        y += offsetY #Décaler y selon le taux de décalage à appliquer
        offsetErreurY = 0 #Décalage à appliquer pour que le pixel qui va être pixellisé soit adapté
        if imageTailleErreurY > 0: #Si un décalage doit être appliqué
            offsetErreurY = floor(IMAGETAILLEERREURY/imagePixeliseTaille[1]) #Générer le décalage à appliquer pour que le pixel qui va être pixellisé soit adapté
            if imageTailleErreurYErreur > 0: #Si le nombre de pixels d'erreurs à la hauteur à une erreur
                offsetErreurY += 1 #Décaler encore le décalage de y pour éviter cette erreur
                imageTailleErreurYErreur -= 1 #Modification du décalage totale en prenant en compte que celui ci est fait
            imageTailleErreurY -= offsetErreurY #Modification du décalage totale en prenant en compte que celui ci est fait
        offsetX = 0 #Taux de décalage de x pour éviter des erreurs et des zones non pixellés
        multiplieurLargeur = 1  # Variable permettant de compter ou non la largeur à retirer
        if imageTailleErreurX == 0:  # Si il n'y aura pas de pixels non pixellisés
            multiplieurLargeur = 0  # Ignorer la  largeur à retirer
        for x in range(0, imageTaille[0] - nw * multiplieurLargeur, nw):
            x += offsetX
            offsetErreurX = 0
            if imageTailleErreurX > 0:
                offsetErreurX = floor(IMAGETAILLEERREURX/imagePixeliseTaille[0])
                if imageTailleErreurXErreur > 0:  # Si le nombre de pixels d'erreurs à la largeur à une erreur
                    offsetErreurX += 1  # Décaler encore le décalage de y pour éviter cette erreur
                    imageTailleErreurXErreur -= 1  # Modification du décalage totale en prenant en compte que celui ci est fait
                imageTailleErreurX -= offsetErreurX
            somme = [0, 0, 0] #Somme des valeurs des couleurs de l'image
            nb = 0 #Nombre de pixels traités
            for i in range(nh + offsetErreurY):
                for j in range(nw + offsetErreurX): #Calcul du pixel agrandi
                    #print(y, i, y+i, x, j, x+j, (x + j, y + i), image.size)
                    couleur = image.getpixel((x + j, y + i))
                    somme[0] += couleur[0] #Calcul de la somme
                    somme[1] += couleur[1]
                    somme[2] += couleur[2]
                    nb += 1
            couleurFinal = (round(somme[0] / nb), round(somme[1] / nb), round(somme[2] / nb)) #Calcul de la moyenne
            for i in range(nh + offsetErreurY):
                for j in range(nw + offsetErreurX): #Calcul du pixel agrandi
                    couleur = image.putpixel((x + j, y + i), couleurFinal)
            offsetX += offsetErreurX
        offsetY += offsetErreurY
    image.show()
                  
def defi5Cacher(imageLien1: str, imageLien2 : str): #Fonction correspondant au défi 5
    image1 = open(imageLien1) #Chargé l'image 1
    image2 = open(imageLien2) #Chargé l'image 2
    imageTaille = image1.size #Obtenir la taille de l'image
    for y in range(imageTaille[1]):
        for x in range(imageTaille[0]): #Parcourir chaque pixel de l'image
            couleur1 = image1.getpixel((x, y))
            couleur2 = image2.getpixel((x, y))
            if type(couleur1) == int: #Dans le cas ou l'image est grise
                couleur1 = (couleur1, couleur1, couleur1)
            bleu = 0
            rouge = 0
            vert = 0
            bleu1 = IntToStrBin(couleur2[2])[0:4] #Calcul des différentes couleurs
            bleu2 = IntToStrBin(couleur1[2])[0:4]
            bleu = int(binStrToInt(bleu1+bleu2))
            rouge1 = IntToStrBin(couleur2[0])[0:4]
            rouge2 = IntToStrBin(couleur1[0])[0:4]
            rouge = int(binStrToInt(rouge1+rouge2))
            vert1 = IntToStrBin(couleur2[1])[0:4]
            vert2 = IntToStrBin(couleur1[1])[0:4]
            vert = int(binStrToInt(vert1+vert2))
            #print((x, y), (rouge, vert, bleu), rouge2, (rouge, vert, bleu))
            image2.putpixel((x, y), (rouge, vert, bleu))
    image2.save("C:/Users/Matt_o/Pictures/A SUPPRIMER/resultat.png")
    image2.show()

def defi5Trouver(imageLien: str):
    image = open(imageLien)
    imageTaille = image.size  # Obtenir la taille de l'image
    for y in range(imageTaille[1]):
        for x in range(imageTaille[0]): #Parcourir chaque pixel de l'image
            couleur = image.getpixel((x, y))
            #print(couleur)
            rouge = binStrToInt(IntToStrBin(int(couleur[0]))[4:9] + "0000")
            bleu = binStrToInt(IntToStrBin(int(couleur[2]))[4:9] + "0000")
            vert = binStrToInt(IntToStrBin(int(couleur[1]))[4:9] + "0000")
            #print((x, y), (rouge, vert, bleu), IntToStrBin(int(couleur[0]))[4:9])
            image.putpixel((x, y), (rouge, vert, bleu))
    image.save("C:/Users/Matt_o/Pictures/A SUPPRIMER/resultat2.png")
    image.show()

defi3("C:/Users/Matt_o/Pictures/bubsy 3d.png", 57)
#defi5Cacher("C:/Users/Matt_o/Pictures/A SUPPRIMER/test1.png", "C:/Users/Matt_o/Pictures/A SUPPRIMER/test2.png")
#print("---------------")
#defi5Trouver("C:/Users/Matt_o/Pictures/A SUPPRIMER/resultat.png")
#defi5Cacher("C:/Users/Matt_o/Pictures/A SUPPRIMER/noel.jpg", "C:/Users/Matt_o/Pictures/A SUPPRIMER/ecureuil.jpg")
#defi5Trouver("C:/Users/Matt_o/Pictures/A SUPPRIMER/resultat.png")