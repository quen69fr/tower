# coding: utf-8

__author__ = 'Quentin'

# imports
import pygame
from pygame.locals import *
import random
import math
import csv



# SCREEN sera une "surface de dessin"
LARGEUR = 1000
HAUTEUR = 650

pygame.init()
SCREEN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("tower !")
FPS = 60                # nombre d'image par seconde
DELAY = 0               # vitesse du jeu

NOIR =  (0,0,0)
BLANC = (255,255,255)
BLEU =  (0,0,255)
VERT =  (52,175,0)
ROUGE = (255,0,0)
ORANGE = (255,127,0)
JAUNE = (255,255,0)

BLOC_BORD_NOIR = -3
BLOC_BORD = -2
BLOC_TOUR = -1
BLOC_PORTE = 0
BLOC_ENTREE = 9999
BLOC_INCONNU = -99

GRILLE_LX = 30
GRILLE_LY = 24
TAILLE_PORTE = 6
Y_PORTE = 9 # ordonnée plus haute case de porte


X_BARRE_DE_VIE = 10
Y_BARRE_DE_VIE = 2
HAUTEUR_BARRE_DE_VIE = 5

TAILLE_BLOC = 20
MARGE_ECRAN = 40

ARGENT = 100
#ARGENT_BESTIOLE = 2
PRIX_TOUR = 5

# tous les fichiets IMAGES
IMAGE_TOURELLE_VIDE = pygame.image.load("image/TourelleVide.png")

IMAGE_START = pygame.image.load("image/Start.png")
IMAGE_NEXT = pygame.image.load("image/Next.png")
IMAGE_RESTART = pygame.image.load("image/ReStart.png")
IMAGE_BOUTON_PLAY = pygame.image.load("image/BoutonPlay.png")
IMAGE_BOUTON_PAUSE = pygame.image.load("image/BoutonPause.png")
IMAGE_PENCARTE = pygame.image.load("image/Pencarte.png")


NOMBRE_BESTIOLES_SORTIE_MAX = 20  # avant perte de partie

TIR_ACTIF = True
AFFICHE_PERIMETRE_TIR = True
VITESSE_TIR = 5
DISTANCE_TIR = 50
DELAI_TIR = 30

X_START_NEXT = 700
Y_START_NEXT = 20
X_BOUTON_PLAY_PAUSE = 900
Y_BOUTON_PLAY_PAUSE = 21

X_TOURELLE = 700
Y_TOURELLE = 100

FONT = pygame.font.Font(None,30)
FONT_2 = pygame.font.Font(None,20)
FONT_3 = pygame.font.Font(None,100)
FONT_4 = pygame.font.Font(None,40)

AFFICHE_CSV = False
FICHIER_DEF_BLOCS = "blocs2.csv"



ETAT_PARTIE_ACCUEIL = 1   # on construit, pas de betes, on quitte quand on clic sur DEMARRER
ETAT_PARTIE_JEU = 2       # les betes arrivent, on construit
ETAT_PARTIE_PERDU = 4     # on fige le jeu ; on affiche la grille, les betes, et des boutons "ENCORE / QUITTER"
ETAT_PARTIE_GAGNE = 5     # on fige le jeu ; on affiche la grille, les betes, et des boutons "ENCORE / QUITTER"
ETAT_PARTIE_PAUSE = 6


# Les types et caractéristiques des différentes bestioles

TABLE_BESTIOLE = {}
TABLE_BESTIOLE['normale']       = {'image':pygame.image.load("image/BestioleNormale.png")   , 'vie':10     , 'gain': 1,   'vitesse':1.0}
TABLE_BESTIOLE['boss_normale']  = {'image':pygame.image.load("image/BestioleNormaleBoss.png")   , 'vie':100    , 'gain': 50,  'vitesse':1.0}

TABLE_BESTIOLE['rapide']        = {'image':pygame.image.load("image/BestioleRapide.png")    , 'vie':10     , 'gain': 1,   'vitesse':1.5}
TABLE_BESTIOLE['boss_rapide']   = {'image':pygame.image.load("image/BestioleRapideBoss.png")    , 'vie':100    , 'gain': 50,   'vitesse':1.5}

TABLE_BESTIOLE['groupe']       = {'image':pygame.image.load("image/BestioleGroupe.png")   , 'vie':10     , 'gain': 1,   'vitesse':1.0}
TABLE_BESTIOLE['boss_groupe']  = {'image':pygame.image.load("image/BestioleGroupeBoss.png")   , 'vie':50    , 'gain': 50,  'vitesse':1.0}

TABLE_BESTIOLE['fort']        = {'image':pygame.image.load("image/BestioleFort.png")    , 'vie':20     , 'gain': 1,   'vitesse':0.5}
TABLE_BESTIOLE['boss_fort']   = {'image':pygame.image.load("image/BestioleFortBoss.png")    , 'vie':200    , 'gain': 50,   'vitesse':0.5}

TABLE_BESTIOLE['volant']        = {'image':pygame.image.load("image/BestioleVolant.png")    , 'vie':10     , 'gain': 1,   'vitesse':1.0}
TABLE_BESTIOLE['boss_volant']   = {'image':pygame.image.load("image/BestioleVolantBoss.png")    , 'vie':100    , 'gain': 50,   'vitesse':1.0}

TABLE_BESTIOLE['boss_final']    = {'image':pygame.image.load("image/BestioleBossFinal.png")   , 'vie':500, 'gain':100 ,  'vitesse':1.0}

# TABLE_BESTIOLE['normale']['vie'] => la vie de la bestiole normale
#
# La composition des vagues de bestioles
# type de bestiole
# quantité
# idées : coef multi de gain, de vie, etalement de l'arrivée

INTERVALLE_BESTIOLE = 15 # (random 1 sur / intervalle)
DELAI_ENTRE_VAGUE = 500  # délai en secondes entre deux vagues ; constant pour toute la partie

TABLE_VAGUE = ( {'type':'boss_final','quantite':0, 'difficultee':1},

                {'type':'normale', 'quantite':10, 'difficultee':1},
                {'type':'rapide','quantite':10, 'difficultee':1},
                {'type':'groupe','quantite':10, 'difficultee':1},
                {'type':'fort','quantite':10, 'difficultee':1},
                {'type':'volant','quantite':10, 'difficultee':1},

                {'type':'boss_normale','quantite':1, 'difficultee':1},

                {'type':'normale', 'quantite':10, 'difficultee':2},
                {'type':'rapide','quantite':10, 'difficultee':2},
                {'type':'groupe','quantite':10, 'difficultee':2},
                {'type':'fort','quantite':10, 'difficultee':2},
                {'type':'volant','quantite':10, 'difficultee':2},

                {'type':'boss_rapide','quantite':1, 'difficultee':2},

                {'type':'normale', 'quantite':10, 'difficultee':3},
                {'type':'rapide','quantite':10, 'difficultee':3},
                {'type':'groupe','quantite':10, 'difficultee':3},
                {'type':'fort','quantite':10, 'difficultee':3},
                {'type':'volant','quantite':10, 'difficultee':3},

                {'type':'boss_groupe','quantite':3, 'difficultee':3},

                {'type':'normale', 'quantite':10, 'difficultee':4},
                {'type':'rapide','quantite':10, 'difficultee':4},
                {'type':'groupe','quantite':10, 'difficultee':4},
                {'type':'fort','quantite':10, 'difficultee':4},
                {'type':'volant','quantite':10, 'difficultee':4},

                {'type':'boss_fort','quantite':1, 'difficultee':4},

                {'type':'normale', 'quantite':10, 'difficultee':5},
                {'type':'rapide','quantite':10, 'difficultee':5},
                {'type':'groupe','quantite':10, 'difficultee':5},
                {'type':'fort','quantite':10, 'difficultee':5},
                {'type':'volant','quantite':10, 'difficultee':5},

                {'type':'boss_volant','quantite':1, 'difficultee':5},

                {'type':'boss_final','quantite':1, 'difficultee':6})



# TODO  :dico de famille de tours, contenant une liste de tours, contenant une liste d'attributs
# TABLE_TOUR = {} ? avec les différentes tour


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

def afficheAccueil(etat_partie):
    if etat_partie == ETAT_PARTIE_ACCUEIL:
        SCREEN.blit(IMAGE_START,(X_START_NEXT,Y_START_NEXT))

    elif etat_partie == ETAT_PARTIE_PERDU or etat_partie == ETAT_PARTIE_GAGNE:
        SCREEN.blit(IMAGE_RESTART,(X_START_NEXT,Y_START_NEXT))

    elif etat_partie == ETAT_PARTIE_JEU:
        SCREEN.blit(IMAGE_NEXT,(X_START_NEXT,Y_START_NEXT))
        SCREEN.blit(IMAGE_TOURELLE_VIDE,(X_TOURELLE,Y_TOURELLE))
        SCREEN.blit(IMAGE_BOUTON_PAUSE,(X_BOUTON_PLAY_PAUSE,Y_BOUTON_PLAY_PAUSE))

    elif etat_partie == ETAT_PARTIE_PAUSE:
        SCREEN.blit(IMAGE_NEXT,(X_START_NEXT,Y_START_NEXT))
        SCREEN.blit(IMAGE_TOURELLE_VIDE,(X_TOURELLE,Y_TOURELLE))
        SCREEN.blit(IMAGE_BOUTON_PLAY,(X_BOUTON_PLAY_PAUSE,Y_BOUTON_PLAY_PAUSE))

    else:
        pass

