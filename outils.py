# coding: utf-8

__author__ = 'Quentin'

# imports
import pygame
from pygame.locals import *
import random
import math
import csv

# SCREEN sera une "surface de dessin"
LARGEUR = 800
HAUTEUR = 600

pygame.init()
SCREEN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("tower !")
FPS = 60                 # nombre d'image par seconde
DELAY = 1               # vitesse du jeu

NOIR =  (  0,   0,   0)
BLANC = (255, 255, 255)
BLEU =  (  0,   0, 255)
VERT =  (  0, 255,   0)
ROUGE = (255,   0,   0)
JAUNE = (255, 255,   0)

GRILLE_LX = 28
GRILLE_LY = 28
TAILLE_PORTE=4
GRILLE_PORTE = int((GRILLE_LY-TAILLE_PORTE)/2)


BLOC_BORD=-2
BLOC_TOUR=-1
BLOC_PORTE=0
BLOC_ENTREE=-3
BLOC_INCONNU=-99

FICHIER_DEF_BLOCS = "blocs1.csv"

TAILLE_BLOC = 20
MARGE_ECRAN = 5

# tous les fichiets IMAGES
IMAGE_TOURELLE_VIDE = pygame.image.load("image/TourelleVide.png")
IMAGE_BESTIOLE = pygame.image.load("image/BestioleNormale.png")


def conversionCoordCasesVersPixels(i,j):
    return (MARGE_ECRAN+i*TAILLE_BLOC,MARGE_ECRAN+j*TAILLE_BLOC)

def conversionCoordPixelsVersCases(x,y):
    return (int((x-MARGE_ECRAN)/TAILLE_BLOC),int((y-MARGE_ECRAN)/TAILLE_BLOC))
