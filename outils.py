# coding: utf-8

__author__ = 'Quentin'

# imports
import pygame
from pygame.locals import *
import random
import math
import csv

# SCREEN sera une "surface de dessin"
LARGEUR = 1100
HAUTEUR = 650

pygame.init()
SCREEN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Tower by Quentin PALAZON !                                        T O W E R")

FPS = 60                # nombre d'image par seconde

DELAY = 0               # vitesse du jeu

TAILLE_BLOC = 20
MARGE_ECRAN = 40

ARGENT_DEPART = 1000

ETAT_PARTIE_ACCUEIL = 1
ETAT_PARTIE_JEU = 2
ETAT_PARTIE_PERDU = 4
ETAT_PARTIE_GAGNE = 5
ETAT_PARTIE_PAUSE = 6
ETAT_PARTIE_AIDE = 7

# ----------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ IMAGES + POLICE + COULEURS ------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------

# ------------------ Images ------------------
IMAGE_FOND = pygame.image.load("image/Fond2.png")

IMAGE_TOURELLE_NORMAL = pygame.image.load("image/TourelleNormal.png")
IMAGE_TOURELLE_VOLANT = pygame.image.load("image/TourelleVolant.png")
IMAGE_TOURELLE_TOUS = pygame.image.load("image/TourelleTous.png")
IMAGE_TOURELLE_BOUM = pygame.image.load("image/TourelleBoum.png")
IMAGE_TOURELLE_BOUM_VOLANT = pygame.image.load("image/TourelleBoumVolant.png")
IMAGE_TOURELLE_PLUS = pygame.image.load("image/TourellePlus.png")
IMAGE_TOURELLE_AMELIOREE = pygame.image.load("image/TourelleAmelioree.png")

IMAGE_START = pygame.image.load("image/Start.png")
IMAGE_NEXT = pygame.image.load("image/Next.png")
IMAGE_RESTART = pygame.image.load("image/ReStart.png")
IMAGE_BOUTON_PLAY = pygame.image.load("image/BoutonPlay.png")
IMAGE_BOUTON_PAUSE = pygame.image.load("image/BoutonPause.png")
IMAGE_BOUTON_PLUS = pygame.image.load("image/Bouton+.png")
IMAGE_BOUTON_MOINS = pygame.image.load("image/Bouton-.png")
IMAGE_PENCARTE = pygame.image.load("image/Pencarte.png")
IMAGE_BOUTON_FLECHE = pygame.image.load("image/BoutonFleches.png")
IMAGE_AIDE = pygame.image.load("image/Aide.png")
IMAGE_TOUCHE_AMELIORATION = pygame.image.load("image/ToucheAmelioration.png")
IMAGE_TOUCHE_SUPRESSION = pygame.image.load("image/ToucheSupression.png")

IMAGE_EXPLICATION_1 = pygame.image.load("image/Explication.png")
IMAGE_EXPLICATION_2 = pygame.image.load("image/Explication2.png")
IMAGE_EXPLICATION_3 = pygame.image.load("image/Explication3.png")
IMAGE_EXPLICATION_4 = pygame.image.load("image/Explication4.png")
IMAGE_AIDE_EXPLICATION = pygame.image.load("image/AideExplication.png")

IMAGE_TOURELLE_CANON_1 = pygame.image.load("image/TourelleCanon1.png")
IMAGE_TOURELLE_CANON_2 = pygame.image.load("image/TourelleCanon2.png")
IMAGE_TOURELLE_CANON_3 = pygame.image.load("image/TourelleCanon3.png")
IMAGE_TOURELLE_CANON_4 = pygame.image.load("image/TourelleCanon4.png")


# ------------------ Polices ------------------
FONT = pygame.font.Font(None,30)
FONT_2 = pygame.font.Font(None,20)
FONT_3 = pygame.font.Font(None,100)
FONT_4 = pygame.font.Font(None,40)


# ------------------ Couleur ------------------
NOIR =   (0,0,0)
GRIS =   (100,100,100)
BLANC =  (255,255,255)
BLEU =   (0,0,255)
VERT =   (52,175,0)
ROUGE =  (255,0,0)
ORANGE = (255,100,0)
JAUNE =  (255,255,0)
JAUNE2 =  (100,100,0)

# -----------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------- BOUTONS ----------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


RAYON_BOUTON_PAUSE = int(IMAGE_BOUTON_PAUSE.get_height()/2)

BOUTON_START_NEXT = "BOUTON_START_NEXT"
BOUTON_PAUSE = "BOUTON_PAUSE"
BOUTON_TOURELLE_NORMAL = "BOUTON_TOURELLE_NORMAL"
BOUTON_TOURELLE_VOLANT = "BOUTON_TOURELLE_VOLANT"
BOUTON_TOURELLE_TOUS = "BOUTON_TOURELLE_TOUS"
BOUTON_TOURELLE_BOUM = "BOUTON_TOURELLE_BOUM"
BOUTON_TOURELLE_BOUM_VOLANT = "BOUTON_TOURELLE_BOUM_VOLANT"
BOUTON_TOURELLE_PLUS = "BOUTON_TOURELLE_PLUS"
BOUTON_PLUS = "BOUTON_PLUS"
BOUTON_MOINS = "BOUTON_MOINS"
BOUTON_AIDE = "BOUTON_AIDE"
BOUTON_FLECHE_DROITE = "BOUTON_FLECHE -->"
BOUTON_FLECHE_GAUCHE = "BOUTON_FLECHE <--"
TOUCHE_F = "TOUCHE_F"
TOUCHE_D = "TOUCHE_D"
TOUCHE_C = "TOUCHE_C"
TOUCHE_V = "TOUCHE_V"
TOUCHE_R = "TOUCHE_R"
TOUCHE_S = "TOUCHE_S"


X_START_NEXT = 700
Y_START_NEXT = 20
X_BOUTON_PLAY_PAUSE = 1030
Y_BOUTON_PLAY_PAUSE = 21
X_BOUTON_AIDE = 960
Y_BOUTON_AIDE = 155
X_BOUTON_FLECHE = 480
Y_BOUTON_FLECHE = 548
X_TOUCHE = 690
Y_TOUCHE_F = 245
Y_TOUCHE_D = 295
Y_TOUCHE_C = 345
Y_TOUCHE_V = 395
Y_TOUCHE_R = 445
Y_TOUCHE_S = 495

X_TOURELLE = 700
Y_TOURELLE = 100

# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------- BESTIOLES + VAGUES ---------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

TABLE_BESTIOLE = {}

# pour faire des tests de rotation !
TABLE_BESTIOLE['départ']         = {'image':"image/BestioleNormale.png"     , 'vie':10   , 'gain': 1  , 'vitesse':0.2}

TABLE_BESTIOLE['normale']      = {'image':"image/BestioleNormale.png"     , 'vie':10   , 'gain': 1  , 'vitesse':1.0}
TABLE_BESTIOLE['boss_normale'] = {'image':"image/BestioleNormaleBoss.png" , 'vie':150  , 'gain': 40 , 'vitesse':1.0}

TABLE_BESTIOLE['rapide']       = {'image':"image/BestioleRapide.png"      , 'vie':10   , 'gain': 1  , 'vitesse':1.5}
TABLE_BESTIOLE['boss_rapide']  = {'image':"image/BestioleRapideBoss.png"  , 'vie':200  , 'gain': 45 , 'vitesse':1.5}

TABLE_BESTIOLE['groupe']       = {'image':"image/BestioleGroupe.png"      , 'vie':10   , 'gain': 1  , 'vitesse':1.0}
TABLE_BESTIOLE['boss_groupe']  = {'image':"image/BestioleGroupeBoss.png"  , 'vie':80   , 'gain': 17 , 'vitesse':1.0}

TABLE_BESTIOLE['imune']        = {'image':"image/BestioleImune.png"      , 'vie':10   , 'gain': 1  , 'vitesse':1.0}
TABLE_BESTIOLE['boss_imune']   = {'image':"image/BestioleImuneBoss.png"  , 'vie':300  , 'gain': 55 , 'vitesse':1.0}

TABLE_BESTIOLE['fort']         = {'image':"image/BestioleFort.png"        , 'vie':13   , 'gain': 1  , 'vitesse':0.5}
TABLE_BESTIOLE['boss_fort']    = {'image':"image/BestioleFortBoss.png"    , 'vie':350  , 'gain': 60 , 'vitesse':0.5}

TABLE_BESTIOLE['volant']       = {'image':"image/BestioleVolant.png"      , 'vie':7    , 'gain': 1  , 'vitesse':1.0}
TABLE_BESTIOLE['boss_volant']  = {'image':"image/BestioleVolantBoss.png"  , 'vie':200  , 'gain': 65 , 'vitesse':1.0}

TABLE_BESTIOLE['boss_final']   = {'image':"image/BestioleBossFinal.png"   , 'vie':1000 , 'gain':100 , 'vitesse':1.0}


for bestiole in TABLE_BESTIOLE:
    img = pygame.image.load( TABLE_BESTIOLE[bestiole]['image'] )
    TABLE_BESTIOLE[bestiole]['image_d']=img
    TABLE_BESTIOLE[bestiole]['image_hd']=pygame.transform.rotate(img, 45)
    TABLE_BESTIOLE[bestiole]['image_h']=pygame.transform.rotate(img, 90)
    TABLE_BESTIOLE[bestiole]['image_hg']=pygame.transform.rotate(img, 135)
    TABLE_BESTIOLE[bestiole]['image_g']=pygame.transform.rotate(img, 180)
    TABLE_BESTIOLE[bestiole]['image_bg']=pygame.transform.rotate(img, 225)
    TABLE_BESTIOLE[bestiole]['image_b']=pygame.transform.rotate(img, 270)
    TABLE_BESTIOLE[bestiole]['image_bd']=pygame.transform.rotate(img, 315)
# variante plus jolie : dessiner chacune des images à l'avance et faire une boucle de chargement
# for ...
#   nom=TABLE_BESTIOLE[bestiole]['image']   # image/BestioleNormale
#   TABLE_BESTIOLE[bestiole]['image_h']=pygame.image.load("nom"+"_h.png")
#   ...


NOMBRE_BESTIOLES_SORTIE_MAX = 20  # avant perte de partie
INTERVALLE_BESTIOLE = 20 # (random 1 sur / intervalle)
DELAI_ENTRE_VAGUE = 500  # délai en secondes entre deux vagues ; constant pour toute la partie

X_BARRE_DE_VIE = 10
Y_BARRE_DE_VIE = 2
HAUTEUR_BARRE_DE_VIE = 5

TABLE_VAGUE =  ({'type':'départ','quantite':0, 'difficultee':1},

                {'type':'normale', 'quantite':10, 'difficultee':1},
                {'type':'rapide','quantite':10, 'difficultee':1},
                {'type':'groupe','quantite':10, 'difficultee':1},
                {'type':'imune','quantite':10, 'difficultee':1},
                {'type':'fort','quantite':10, 'difficultee':1},
                {'type':'volant','quantite':10, 'difficultee':1},

                {'type':'boss_normale','quantite':1, 'difficultee':1},

                {'type':'normale', 'quantite':10, 'difficultee':2},
                {'type':'rapide','quantite':10, 'difficultee':2},
                {'type':'groupe','quantite':10, 'difficultee':2},
                {'type':'imune','quantite':10, 'difficultee':2},
                {'type':'fort','quantite':10, 'difficultee':2},
                {'type':'volant','quantite':10, 'difficultee':2},

                {'type':'boss_rapide','quantite':1, 'difficultee':2},

                {'type':'normale', 'quantite':10, 'difficultee':3},
                {'type':'rapide','quantite':10, 'difficultee':3},
                {'type':'groupe','quantite':10, 'difficultee':3},
                {'type':'imune','quantite':10, 'difficultee':3},
                {'type':'fort','quantite':10, 'difficultee':3},
                {'type':'volant','quantite':10, 'difficultee':3},

                {'type':'boss_groupe','quantite':3, 'difficultee':3},

                {'type':'normale', 'quantite':10, 'difficultee':4},
                {'type':'rapide','quantite':10, 'difficultee':4},
                {'type':'groupe','quantite':10, 'difficultee':4},
                {'type':'imune','quantite':10, 'difficultee':4},
                {'type':'fort','quantite':10, 'difficultee':4},
                {'type':'volant','quantite':10, 'difficultee':4},

                {'type':'boss_imune','quantite':1, 'difficultee':4},

                {'type':'normale', 'quantite':10, 'difficultee':5},
                {'type':'rapide','quantite':10, 'difficultee':5},
                {'type':'groupe','quantite':10, 'difficultee':5},
                {'type':'imune','quantite':10, 'difficultee':5},
                {'type':'fort','quantite':10, 'difficultee':5},
                {'type':'volant','quantite':10, 'difficultee':5},

                {'type':'boss_fort','quantite':1, 'difficultee':5},

                {'type':'normale', 'quantite':10, 'difficultee':6},
                {'type':'rapide','quantite':10, 'difficultee':6},
                {'type':'groupe','quantite':10, 'difficultee':6},
                {'type':'imune','quantite':10, 'difficultee':6},
                {'type':'fort','quantite':10, 'difficultee':6},
                {'type':'volant','quantite':10, 'difficultee':6},

                {'type':'boss_volant','quantite':1, 'difficultee':6},

                {'type':'normale', 'quantite':10, 'difficultee':7},
                {'type':'rapide','quantite':10, 'difficultee':7},
                {'type':'groupe','quantite':10, 'difficultee':7},
                {'type':'imune','quantite':10, 'difficultee':7},
                {'type':'fort','quantite':10, 'difficultee':7},
                {'type':'volant','quantite':10, 'difficultee':7},

                {'type':'boss_normale','quantite':1, 'difficultee':7},

                {'type':'normale', 'quantite':10, 'difficultee':8},
                {'type':'rapide','quantite':10, 'difficultee':8},
                {'type':'groupe','quantite':10, 'difficultee':8},
                {'type':'imune','quantite':10, 'difficultee':8},
                {'type':'fort','quantite':10, 'difficultee':8},
                {'type':'volant','quantite':10, 'difficultee':8},

                {'type':'boss_rapide','quantite':1, 'difficultee':8},

                {'type':'normale', 'quantite':10, 'difficultee':9},
                {'type':'rapide','quantite':10, 'difficultee':9},
                {'type':'groupe','quantite':10, 'difficultee':9},
                {'type':'imune','quantite':10, 'difficultee':9},
                {'type':'fort','quantite':10, 'difficultee':9},
                {'type':'volant','quantite':10, 'difficultee':9},

                {'type':'boss_groupe','quantite':3, 'difficultee':9},

                {'type':'normale', 'quantite':10, 'difficultee':10},
                {'type':'rapide','quantite':10, 'difficultee':10},
                {'type':'groupe','quantite':10, 'difficultee':10},
                {'type':'imune','quantite':10, 'difficultee':10},
                {'type':'fort','quantite':10, 'difficultee':10},
                {'type':'volant','quantite':10, 'difficultee':10},

                {'type':'boss_imune','quantite':1, 'difficultee':10},

                {'type':'normale', 'quantite':10, 'difficultee':11},
                {'type':'rapide','quantite':10, 'difficultee':11},
                {'type':'groupe','quantite':10, 'difficultee':11},
                {'type':'imune','quantite':10, 'difficultee':11},
                {'type':'fort','quantite':10, 'difficultee':11},
                {'type':'volant','quantite':10, 'difficultee':11},

                {'type':'boss_fort','quantite':1, 'difficultee':11},

                {'type':'normale', 'quantite':10, 'difficultee':12},
                {'type':'rapide','quantite':10, 'difficultee':12},
                {'type':'groupe','quantite':10, 'difficultee':12},
                {'type':'imune','quantite':10, 'difficultee':12},
                {'type':'fort','quantite':10, 'difficultee':12},
                {'type':'volant','quantite':10, 'difficultee':12},

                {'type':'boss_volant','quantite':1, 'difficultee':12},
                {'type':'boss_final','quantite':1, 'difficultee':13})

TABLE_VAGUE_SANS_VOLANT =  ({'type':'départ','quantite':0, 'difficultee':1},

                {'type':'normale', 'quantite':10, 'difficultee':1},
                {'type':'rapide','quantite':10, 'difficultee':1},
                {'type':'groupe','quantite':10, 'difficultee':1},
                {'type':'imune','quantite':10, 'difficultee':1},
                {'type':'fort','quantite':10, 'difficultee':1},

                {'type':'boss_normale','quantite':1, 'difficultee':1},

                {'type':'normale', 'quantite':10, 'difficultee':2},
                {'type':'rapide','quantite':10, 'difficultee':2},
                {'type':'groupe','quantite':10, 'difficultee':2},
                {'type':'imune','quantite':10, 'difficultee':2},
                {'type':'fort','quantite':10, 'difficultee':2},

                {'type':'boss_rapide','quantite':1, 'difficultee':2},

                {'type':'normale', 'quantite':10, 'difficultee':3},
                {'type':'rapide','quantite':10, 'difficultee':3},
                {'type':'groupe','quantite':10, 'difficultee':3},
                {'type':'imune','quantite':10, 'difficultee':3},
                {'type':'fort','quantite':10, 'difficultee':3},

                {'type':'boss_groupe','quantite':3, 'difficultee':3},

                {'type':'normale', 'quantite':10, 'difficultee':4},
                {'type':'rapide','quantite':10, 'difficultee':4},
                {'type':'groupe','quantite':10, 'difficultee':4},
                {'type':'imune','quantite':10, 'difficultee':4},
                {'type':'fort','quantite':10, 'difficultee':4},

                {'type':'boss_imune','quantite':1, 'difficultee':4},

                {'type':'normale', 'quantite':10, 'difficultee':5},
                {'type':'rapide','quantite':10, 'difficultee':5},
                {'type':'groupe','quantite':10, 'difficultee':5},
                {'type':'imune','quantite':10, 'difficultee':5},
                {'type':'fort','quantite':10, 'difficultee':5},

                {'type':'boss_fort','quantite':1, 'difficultee':5},

                {'type':'normale', 'quantite':10, 'difficultee':6},
                {'type':'rapide','quantite':10, 'difficultee':6},
                {'type':'groupe','quantite':10, 'difficultee':6},
                {'type':'imune','quantite':10, 'difficultee':6},
                {'type':'fort','quantite':10, 'difficultee':6},

                {'type':'normale', 'quantite':10, 'difficultee':7},
                {'type':'rapide','quantite':10, 'difficultee':7},
                {'type':'groupe','quantite':10, 'difficultee':7},
                {'type':'imune','quantite':10, 'difficultee':7},
                {'type':'fort','quantite':10, 'difficultee':7},

                {'type':'boss_normale','quantite':1, 'difficultee':7},

                {'type':'normale', 'quantite':10, 'difficultee':8},
                {'type':'rapide','quantite':10, 'difficultee':8},
                {'type':'groupe','quantite':10, 'difficultee':8},
                {'type':'imune','quantite':10, 'difficultee':8},
                {'type':'fort','quantite':10, 'difficultee':8},

                {'type':'boss_rapide','quantite':1, 'difficultee':8},

                {'type':'normale', 'quantite':10, 'difficultee':9},
                {'type':'rapide','quantite':10, 'difficultee':9},
                {'type':'groupe','quantite':10, 'difficultee':9},
                {'type':'imune','quantite':10, 'difficultee':9},
                {'type':'fort','quantite':10, 'difficultee':9},

                {'type':'boss_groupe','quantite':3, 'difficultee':9},

                {'type':'normale', 'quantite':10, 'difficultee':10},
                {'type':'rapide','quantite':10, 'difficultee':10},
                {'type':'groupe','quantite':10, 'difficultee':10},
                {'type':'imune','quantite':10, 'difficultee':10},
                {'type':'fort','quantite':10, 'difficultee':10},

                {'type':'boss_imune','quantite':1, 'difficultee':10},

                {'type':'normale', 'quantite':10, 'difficultee':11},
                {'type':'rapide','quantite':10, 'difficultee':11},
                {'type':'groupe','quantite':10, 'difficultee':11},
                {'type':'imune','quantite':10, 'difficultee':11},
                {'type':'fort','quantite':10, 'difficultee':11},

                {'type':'boss_fort','quantite':1, 'difficultee':11},

                {'type':'normale', 'quantite':10, 'difficultee':12},
                {'type':'rapide','quantite':10, 'difficultee':12},
                {'type':'groupe','quantite':10, 'difficultee':12},
                {'type':'imune','quantite':10, 'difficultee':12},
                {'type':'fort','quantite':10, 'difficultee':12},

                {'type':'boss_final','quantite':1, 'difficultee':13})    # Sans volant


# ---------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ TOURS(GRILLE) ------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------
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

# ------------------ Tours ------------------
AFFICHE_CSV = False
FICHIER_DEF_BLOCS = "blocs2.csv"

TIR_ACTIF = True
AFFICHE_DISTANCE_TIR_BROUILLON = True

COEFF_TOUR_PLUS = 1.1

# Définition des améliorations possibles des tours
TOUR_NORMAL = "TOUR_NORMAL"
TOUR_VOLANT = "TOUR_VOLANT"
TOUR_TOUS = "TOUR_TOUS"
TOUR_BOUM = "TOUR_BOUM"
TOUR_BOUM_VOLANT = "TOUR_BOUM_VOLANT"
TOUR_PLUS = "TOUR_PLUS"


# prix de départ d'une tour
PRIX_TOUR_NORMALE = 20
PRIX_TOUR_VOLANT = 20
PRIX_TOUR_TOUS = 5
PRIX_TOUR_BOUM = 20
PRIX_TOUR_BOUM_VOLANT = 20
PRIX_TOUR_PLUS = 75


TOUR_AMELIORATION_FORCE = "TOUR_AMELIORATION_FORCE"
TABLE_NORMALE_TOUR_FORCE = [10, 20, 40, 60]
TABLE_VOLANT_TOUR_FORCE = [10, 20, 40, 60]
TABLE_TOUS_TOUR_FORCE = [3, 5, 10, 20]
TABLE_BOUM_TOUR_FORCE = [10, 20, 40, 60]
TABLE_BOUM_VOLANT_TOUR_FORCE = [10, 20, 40, 60]

TABLE_NORMALE_TOUR_FORCE_PRIX = [15, 40, 80]
TABLE_VOLANT_TOUR_FORCE_PRIX = [15, 40, 80]
TABLE_TOUS_TOUR_FORCE_PRIX = [8, 20, 50]
TABLE_BOUM_TOUR_FORCE_PRIX = [15, 40, 80]
TABLE_BOUM_VOLANT_TOUR_FORCE_PRIX = [8, 25, 60]


TOUR_AMELIORATION_DISTANCE = "TOUR_AMELIORATION_DISTANCE"
TABLE_NORMALE_TOUR_DISTANCE = [40, 50, 58, 70]
TABLE_VOLANT_TOUR_DISTANCE = [40, 50, 58, 70]
TABLE_TOUS_TOUR_DISTANCE = [40, 10, 12, 14]
TABLE_BOUM_TOUR_DISTANCE = [40, 12, 14, 18]
TABLE_BOUM_VOLANT_TOUR_DISTANCE = [40, 12, 14, 18]

TABLE_NORMALE_TOUR_DISTANCE_PRIX = [10, 35, 75]
TABLE_VOLANT_TOUR_DISTANCE_PRIX = [10, 35, 75]
TABLE_TOUS_TOUR_DISTANCE_PRIX = [10, 20, 50]
TABLE_BOUM_TOUR_DISTANCE_PRIX = [10, 20, 50]
TABLE_BOUM_VOLANT_TOUR_DISTANCE_PRIX = [10, 20, 50]


TOUR_AMELIORATION_VITESSE = "TOUR_AMELIORATION_VITESSE"
TABLE_NORMALE_TOUR_VITESSE = [5, 6, 7, 9]
TABLE_VOLANT_TOUR_VITESSE = [5, 6, 7, 9]
TABLE_TOUS_TOUR_VITESSE = [5, 6, 7, 9]
TABLE_BOUM_TOUR_VITESSE = [5, 6, 7, 9]
TABLE_BOUM_VOLANT_TOUR_VITESSE = [5, 6, 7, 9]

TABLE_NORMALE_TOUR_VITESSE_PRIX = [5, 10, 20]
TABLE_VOLANT_TOUR_VITESSE_PRIX = [5, 10, 20]
TABLE_TOUS_TOUR_VITESSE_PRIX = [5, 10, 20]
TABLE_BOUM_TOUR_VITESSE_PRIX = [5, 10, 20]
TABLE_BOUM_VOLANT_TOUR_VITESSE_PRIX = [5, 10, 20]


TOUR_AMELIORATION_CADENCE = "TOUR_AMELIORATION_CADENCE"
TABLE_NORMALE_TOUR_CADENCE = [1, 1, 1, 1]
TABLE_VOLANT_TOUR_CADENCE = [1, 1, 1, 1]
TABLE_TOUS_TOUR_CADENCE = [1, 1, 1, 1]
TABLE_BOUM_TOUR_CADENCE = [1, 1, 1, 1]
TABLE_BOUM_VOLANT_TOUR_CADENCE = [1, 1, 1, 1]

TABLE_NORMALE_TOUR_CADENCE_PRIX = [20,25,30]
TABLE_VOLANT_TOUR_CADENCE_PRIX = [20,25,30]
TABLE_TOUS_TOUR_CADENCE_PRIX = [20,25,30]
TABLE_BOUM_TOUR_CADENCE_PRIX = [20,25,30]
TABLE_BOUM_VOLANT_TOUR_CADENCE_PRIX = [20,25,30]


TOUR_AMELIORATION_RALENTI = "TOUR_AMELIORATION_RALENTI"
TABLE_NORMALE_TOUR_RALENTI_FORCE = [1, (-0.1), (-0.15), (-0.20)]
TABLE_VOLANT_TOUR_RALENTI_FORCE = [1, (-0.1), (-0.15), (-0.20)]
TABLE_TOUS_TOUR_RALENTI_FORCE = [1, (-0.1), (-0.15), (-0.20)]
TABLE_BOUM_TOUR_RALENTI_FORCE = [1, (-0.1), (-0.15), (-0.20)]
TABLE_BOUM_VOLANT_TOUR_RALENTI_FORCE = [1, (-0.1), (-0.15), (-0.20)]

TABLE_NORMALE_TOUR_RALENTI_DUREE = [1, 5, 20, 50]
TABLE_VOLANT_TOUR_RALENTI_DUREE = [1, 5, 20, 50]
TABLE_TOUS_TOUR_RALENTI_DUREE = [1, 5, 20, 50]
TABLE_BOUM_TOUR_RALENTI_DUREE = [1, 8, 30, 80]
TABLE_BOUM_VOLANT_TOUR_RALENTI_DUREE = [1, 6, 25, 60]

TABLE_NORMALE_TOUR_RALENTI_PRIX = [8, 15, 20]
TABLE_VOLANT_TOUR_RALENTI_PRIX = [8, 15, 20]
TABLE_TOUS_TOUR_RALENTI_PRIX = [20, 25, 30]
TABLE_BOUM_TOUR_RALENTI_PRIX = [20, 30, 40]
TABLE_BOUM_VOLANT_TOUR_RALENTI_PRIX = [20, 30, 40]

# ----------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------- FONCTIONS --------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------

def conversionCoordCasesVersPixels(i,j):
    return (MARGE_ECRAN+i*TAILLE_BLOC,MARGE_ECRAN+j*TAILLE_BLOC)

# ------------------------------------------------
def conversionCoordPixelsVersCases(x,y):
    return (int((x-MARGE_ECRAN)/TAILLE_BLOC),int((y-MARGE_ECRAN)/TAILLE_BLOC))

# ------------------------------------------------
def centreCase(i,j):
    '''
    Donne le pixel (px,py) du centre d'une case (i,j)
    :param i: abscisse de la case dans la grille 0 .. N-1
    :param j: ordonnée
    :return: un tupple de coordonnées pixel
    '''
    return (MARGE_ECRAN+(i+0.5) * TAILLE_BLOC, MARGE_ECRAN+(j+0.5) * TAILLE_BLOC)
    pass

# ------------------------------------------------
def centreTour(i,j):
    ''' une tour occupe 4 cases
    rend le pixel du centre des 4 cases,
    c'est à dire le coin haut-gauche de la case i+1, j+1
    '''
    return conversionCoordCasesVersPixels(i+1,j+1)

# ------------------------------------------------
def anglesCase(i,j):
    ''' dans l'ordre x1,y1 coin supérieur gauche et x2,y2 coin inférieur droit
    '''
    return [MARGE_ECRAN+i*TAILLE_BLOC, MARGE_ECRAN+j*TAILLE_BLOC,MARGE_ECRAN+(i+1)*TAILLE_BLOC, MARGE_ECRAN+(j+1)*TAILLE_BLOC]

# ------------------------------------------------
def directionCentreCase(px, py):
    (i, j) = conversionCoordCasesVersPixels(px, py)
    (px2, py2) = centreCase(i, j)
    hypo = math.sqrt((px2-px)**2 + (py2-py)**2)
    return ((px2-px)/hypo, (py2-py)/hypo)

# ------------------------------------------------
def depasseHaut(x,y,r):
    ''' renvoie True si l'objet x,y rayon r, depasse le haut de sa case'''
    (i,j) = conversionCoordPixelsVersCases(x,y)
    coordAnglesCase = anglesCase(i,j)
    return (y-r<coordAnglesCase[1])

# ------------------------------------------------
def depasseBas(x,y,r):
    ''' renvoie True si l'objet x,y rayon r, depasse le bas de sa case'''
    (i,j) = conversionCoordPixelsVersCases(x,y)
    coordAnglesCase = anglesCase(i,j)
    return (y+r>coordAnglesCase[3])

# ------------------------------------------------
def depasseGauche(x,y,r):
    ''' renvoie True si l'objet x,y rayon r, depasse le gauche de sa case'''
    (i,j) = conversionCoordPixelsVersCases(x,y)
    coordAnglesCase = anglesCase(i,j)
    return (x-r<coordAnglesCase[0])

# ------------------------------------------------
def depasseDroit(x,y,r):
    ''' renvoie True si l'objet x,y rayon r, depasse le droit de sa case'''
    (i,j) = conversionCoordPixelsVersCases(x,y)
    coordAnglesCase = anglesCase(i,j)
    return (x+r>coordAnglesCase[2])

# ------------------------------------------------
def prixSuplementaire(t):
    suplement = (t.niveau_distance + t.niveau_force + t.niveau_ralentire + t.niveau_cadence + t.niveau_vitesse)
    suplement = int(suplement * suplement)
    return suplement

# ------------------------------------------------
def rot_centre(image, angle):

    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image