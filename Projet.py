from math import *
from PIL import *
from PIL.Image import *
from PIL.ImageDraw import *
from random import *

def IntToStrBin():
    pass

def binStrToInt(n: str): #Convertir un int binaire dans un str en entier base dix
    resultat = 0
    for i in enumerate(n[::-1]):
        if(i[1] == "1"):
            resultat += 2 ** i[0]
    return resultat

def defi3(imageLien: str, n: int): #Fonction correspondant au défi 3
    image = open(imageLien) #Chargé l'image
    imageTaille = image.size #Obtenir la taille de l'image
    for y in range(floor(imageTaille[1]/n)):
        for x in range(floor(imageTaille[0]/n)): #Parcourir chaque pixel de l'image
            somme = [0, 0, 0] #Somme des valeurs des couleurs de l'image
            nb = 0 #Nombre de pixels traités
            for i in range(n):
                for j in range(n): #Calcul du pixel agrandi
                    couleur = image.getpixel((floor(n * x + j), floor(n * y + i)))
                    somme[0] += couleur[0] #Calcul de la somme
                    somme[1] += couleur[1]
                    somme[2] += couleur[2]
                    nb += 1
            couleurFinal = (round(somme[0] / nb), round(somme[1] / nb), round(somme[2] / nb)) #Calcul de la moyenne
            for i in range(n):
                for j in range(n): #Calcul du pixel agrandi
                    couleur = image.putpixel((floor(n * x + j), floor(n * y + i)), couleurFinal)
    image.show()
                  
def defi5Cacher(imageLien1: str, imageLien2 : str): #Fonction correspondant au défi 5
    image1 = open(imageLien1) #Chargé l'image 1
    image2 = open(imageLien2) #Chargé l'image 2
    imageTaille = image1.size #Obtenir la taille de l'image
    for y in range(imageTaille[1]):
        for x in range(imageTaille[0]): #Parcourir chaque pixel de l'image
            couleur1 = image1.getpixel((x, y))
            couleur2 = image2.getpixel((x, y))
            chiffreAleatoire = randint(0, 1)
            bleu = 0
            rouge = 0
            vert = 0
            if chiffreAleatoire == 1:
                bleu1 = str(bin(couleur1[2]))[2:6]
                bleu2 = str(bin(couleur2[2]))[2:6]
                bleu = int(binStrToInt(bleu1+bleu2))
                rouge1 = str(bin(couleur1[0]))[2:6]
                rouge2 = str(bin(couleur2[0]))[2:6]
                rouge = int(binStrToInt(rouge1+rouge2))
                vert1 = str(bin(couleur1[1]))[2:6]
                vert2 = str(bin(couleur2[1]))[2:6]
                vert = int(binStrToInt(vert1+vert2))
            if chiffreAleatoire == 0:
                bleu1 = str(bin(couleur2[2]))[2:6]
                bleu2 = str(bin(couleur1[2]))[2:6]
                bleu = int(binStrToInt(bleu1+bleu2))
                rouge1 = str(bin(couleur2[0]) )[2:6]
                rouge2 = str(bin(couleur1[0]) )[2:6]
                rouge = int(binStrToInt(rouge1+rouge2))
                vert1 = str(bin(couleur2[1]))[2:6]
                vert2 = str(bin(couleur1[1]))[2:6]
                vert = int(binStrToInt(vert1+vert2))
            #print(couleur1[0], couleur2[0], bin(couleur1[0]), bin(240) and bin(couleur1[0]), bleu1, bleu2, bleu)
            image2.putpixel((x, y), (rouge, vert, bleu))
    image2.show()
            
defi5Cacher("C:/Users/Mattéo Menou/Pictures/coq empire craft.jpg", "C:/Users/Mattéo Menou/Pictures/Donald trump.png")