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

def defi3(imageLien: str, n: int): #Fonction correspondant au défi 3
    image = open(imageLien) #Chargé l'image
    imageTaille = image.size #Obtenir la taille de l'image
    imageTailleErreurY = imageTaille[1]%n
    offsetX = 0
    offsetY = 0
    for y in range(0, imageTaille[1] - n, n):
        imageTailleErreurX = imageTaille[0]%n
        y += offsetY
        offsetErreurY = 0
        if imageTailleErreurY > 0:
            offsetErreurY = 1
            imageTailleErreurY -= offsetErreurY
        for x in range(0, imageTaille[0] - n, n): #Parcourir chaque pixel de l'image
            x += offsetX
            offsetErreurX = 0
            if imageTailleErreurX > 0:
                offsetErreurX = 1
                imageTailleErreurX -= offsetErreurX
            somme = [0, 0, 0] #Somme des valeurs des couleurs de l'image
            nb = 0 #Nombre de pixels traités
            for i in range(n + offsetErreurY):
                for j in range(n + offsetErreurX): #Calcul du pixel agrandi
                    if y > 99 and i > 98: print(y, i, y+i, x, j, x+j, (x + j, y + i), image.size)
                    couleur = image.getpixel((x + j, y + i))
                    somme[0] += couleur[0] #Calcul de la somme
                    somme[1] += couleur[1]
                    somme[2] += couleur[2]
                    nb += 1
            couleurFinal = (round(somme[0] / nb), round(somme[1] / nb), round(somme[2] / nb)) #Calcul de la moyenne
            for i in range(n + offsetErreurY):
                for j in range(n + offsetErreurX): #Calcul du pixel agrandi
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

defi3("C:/Users/Mattéo Menou/Pictures/Donald trump.png", 99)
#defi5Cacher("C:/Users/Matt_o/Pictures/A SUPPRIMER/test1.png", "C:/Users/Matt_o/Pictures/A SUPPRIMER/test2.png")
#print("---------------")
#defi5Trouver("C:/Users/Matt_o/Pictures/A SUPPRIMER/resultat.png")
#defi5Cacher("C:/Users/Matt_o/Pictures/A SUPPRIMER/noel.jpg", "C:/Users/Matt_o/Pictures/A SUPPRIMER/ecureuil.jpg")
#defi5Trouver("C:/Users/Matt_o/Pictures/A SUPPRIMER/resultat.png")