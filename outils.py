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
DELAY = 0               # vitesse du jeu

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

FICHIER_DEF_BLOCS = "blocs2.csv"

TAILLE_BLOC = 20
MARGE_ECRAN = 5

# tous les fichiets IMAGES
IMAGE_TOURELLE_VIDE = pygame.image.load("image/TourelleVide.png")
IMAGE_BESTIOLE = pygame.image.load("image/BestioleNormale.png")

AFFICHE_PERIMETRE_TIR = True
AFFICHE_CSV = False

def conversionCoordCasesVersPixels(i,j):
    return (MARGE_ECRAN+i*TAILLE_BLOC,MARGE_ECRAN+j*TAILLE_BLOC)

def conversionCoordPixelsVersCases(x,y):
    return (int((x-MARGE_ECRAN)/TAILLE_BLOC),int((y-MARGE_ECRAN)/TAILLE_BLOC))

def centreCase(i,j):
    '''
    Donne le pixel (px,py) du centre d'une case (i,j)
    :param i: abscisse de la case dans la grille 0 .. N-1
    :param j: ordonnée
    :return: un tupple de coordonnées pixel
    '''
    return (MARGE_ECRAN+(i+0.5) * TAILLE_BLOC, MARGE_ECRAN+(j+0.5) * TAILLE_BLOC)
    pass

def centreTour(i,j):
    ''' une tour occupe 4 cases
    rend le pixel du centre des 4 cases,
    c'est à dire le coin haut-gauche de la case i+1, j+1
    '''
    return conversionCoordCasesVersPixels(i+1,j+1)

def anglesCase(i,j):
    ''' dans l'ordre x1,y1 coin supérieur gauche et x2,y2 coin inférieur droit
    '''
    return [MARGE_ECRAN+i*TAILLE_BLOC, MARGE_ECRAN+j*TAILLE_BLOC,MARGE_ECRAN+(i+1)*TAILLE_BLOC, MARGE_ECRAN+(j+1)*TAILLE_BLOC]


def directionCentreCase(px, py):
    (i, j) = conversionCoordCasesVersPixels(px, py)
    (px2, py2) = centreCase(i, j)
    hypo = math.sqrt((px2-px)**2 + (py2-py)**2)
    return ((px2-px)/hypo, (py2-py)/hypo)

def depasseHaut(x,y,r):
    ''' renvoie True si l'objet x,y rayon r, depasse le haut de sa case'''
    (i,j) = conversionCoordPixelsVersCases(x,y)
    coordAnglesCase = anglesCase(i,j)
    return (y-r<coordAnglesCase[1])

def depasseBas(x,y,r):
    ''' renvoie True si l'objet x,y rayon r, depasse le bas de sa case'''
    (i,j) = conversionCoordPixelsVersCases(x,y)
    coordAnglesCase = anglesCase(i,j)
    return (y+r>coordAnglesCase[3])

def depasseGauche(x,y,r):
    ''' renvoie True si l'objet x,y rayon r, depasse le gauche de sa case'''
    (i,j) = conversionCoordPixelsVersCases(x,y)
    coordAnglesCase = anglesCase(i,j)
    return (x-r<coordAnglesCase[0])

def depasseDroit(x,y,r):
    ''' renvoie True si l'objet x,y rayon r, depasse le droit de sa case'''
    (i,j) = conversionCoordPixelsVersCases(x,y)
    coordAnglesCase = anglesCase(i,j)
    return (x+r>coordAnglesCase[2])


