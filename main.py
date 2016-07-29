# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'
# 2016-07-29 11:21

# imports
import pygame
from pygame.locals import *
import random
import math


#outil pour lire un fichier CSV
import csv


# import sys
# sys.setrecursionlimit(10000)


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
GRILLE_PORTE = 13


BLOC_BORD=-2
BLOC_TOUR=-1
BLOC_PORTE=0
BLOC_ENTREE=-3
BLOC_INCONNU=-99

FICHIER_DEF_BLOCS = "blocs1.csv"
TOURELLE_VIDE = pygame.image.load("image/TourelleVide.png")

ETAT_TOUR_CONSTRUIT = 1
ETAT_TOUR_BROUILLON = 0

TAILLE_BLOC = 20
MARGE_ECRAN = 5
# ============================================================

# ============================================================
class Tour():
    """
    Cette classe sert à gérer les tours et canons
    """
    def __init__(self,x,y,etat=ETAT_TOUR_CONSTRUIT):
        self.x = x
        self.y = y
        self.etat = etat

    def affiche(self):
        if self.etat == ETAT_TOUR_BROUILLON:
            recttransparent = pygame.Surface((40,40), pygame.SRCALPHA, 32)
            recttransparent.fill((0,0,255, 50))
            SCREEN.blit(recttransparent, (MARGE_ECRAN+self.x*TAILLE_BLOC,MARGE_ECRAN+self.y*TAILLE_BLOC))

        elif self.etat== ETAT_TOUR_CONSTRUIT:
            #pygame.draw.rect(SCREEN, BLEU, (MARGE_ECRAN+self.x*TAILLE_BLOC,MARGE_ECRAN+self.y*TAILLE_BLOC,TAILLE_BLOC*2,TAILLE_BLOC*2),0)
            SCREEN.blit(TOURELLE_VIDE,(MARGE_ECRAN+self.x*TAILLE_BLOC,MARGE_ECRAN+self.y*TAILLE_BLOC))

# ============================================================
class Grille():

    # ------------------------------------------------
    def __init__(self):

        self.grille=[]
        self.listeTours = []
        self.grille = [[BLOC_INCONNU for j in range(GRILLE_LY)] for i in range(GRILLE_LX)]

        for i in range(GRILLE_LX):
            self.grille[i][0]=BLOC_BORD
            self.grille[i][GRILLE_LY-1]=BLOC_BORD

        for j in range(GRILLE_LY):
            self.grille[0][j]=BLOC_BORD
            self.grille[GRILLE_LX-1][j]=BLOC_BORD

        self.grille[GRILLE_LX-1][GRILLE_PORTE]=BLOC_PORTE
        self.grille[GRILLE_LX-1][GRILLE_PORTE+1]=BLOC_PORTE

        self.grille[0][GRILLE_PORTE]=BLOC_ENTREE
        self.grille[0][GRILLE_PORTE+1]=BLOC_ENTREE

    # ------------------------------------------------
    def reset_distance_grille(self):
        for x in range(0,GRILLE_LX):
            for y in range(0,GRILLE_LY):
                if self.grille[x][y] != BLOC_BORD \
                        and self.grille[x][y] != BLOC_PORTE \
                        and self.grille[x][y] != BLOC_ENTREE \
                        and self.grille[x][y] != BLOC_TOUR:
                    self.grille[x][y] = BLOC_INCONNU

    # ------------------------------------------------
    def nouvelle_tour(self,tour):
        x = tour.x
        y = tour.y

        if self.grille[x][y] > 0 and self.grille[x+1][y] > 0 and self.grille[x][y+1] > 0 and self.grille[x+1][y+1] > 0:
            self.listeTours.append(tour)
            self.grille[x][y]=BLOC_TOUR
            self.grille[x+1][y]=BLOC_TOUR
            self.grille[x][y+1]=BLOC_TOUR
            self.grille[x+1][y+1]=BLOC_TOUR

    # ------------------------------------------------
    def enleve_tour(self,x,y):

        if self.grille[x][y] == BLOC_TOUR and self.grille[x+1][y] == BLOC_TOUR and self.grille[x][y+1] == BLOC_TOUR and self.grille[x+1][y+1] == BLOC_TOUR:
            for t in self.listeTours:
                if t.x == x and t.y == y:
                    self.listeTours.remove(t)
                    self.grille[x][y]=BLOC_INCONNU
                    self.grille[x+1][y]=BLOC_INCONNU
                    self.grille[x][y+1]=BLOC_INCONNU
                    self.grille[x+1][y+1]=BLOC_INCONNU

    # ------------------------------------------------
    def affiche_grille(self):
        # print "------------------"
        for j in range(GRILLE_LY):
            print (j, ':',)
            for i in range(GRILLE_LX):
                print (self.grille[i][j],)
            print ("")

    # ------------------------------------------------
    def dessine_grille(self,x=0,y=0):
        SCREEN.fill(0)
        for j in range(GRILLE_LY):
            for i in range(GRILLE_LX):
                v=self.grille[i][j]
                # dessiner un rectangle en x,y de couleur v
                c=NOIR
                if v == BLOC_BORD:
                    c=BLEU
                if v == BLOC_PORTE:
                    c=NOIR
                if v == BLOC_ENTREE:
                    c=BLANC
                if v > 0:
                    nuance = v*3
                    if nuance>255 :
                        nuance = 255
                    c = (nuance,nuance,nuance)
                pygame.draw.rect(SCREEN, c, (5+i*20,5+j*20,20,20),0)
        if x != 0 or y !=0:
                pygame.draw.rect(SCREEN, JAUNE, (5+x*20,5+ y*20,19,19),1)

        for tour in self.listeTours:
            tour.affiche()

        pygame.display.update()
        #pygame.time.delay(DELAY )

    # ------------------------------------------------
    def calcule_distance(self,x,y):

        # TODO : BUG si case de départ occupée par un bloc

        #print "Calcul ",x,y
        #self.dessine_grille(x,y)

        # il faut récupérer les 4 valeurs autour
        vg = self.grille[x-1][y]
        vd = self.grille[x+1][y]
        vh = self.grille[x][y-1]
        vb = self.grille[x][y+1]
        liste_valeur=[]
        if vg >= 0 :
            liste_valeur.append(vg)
        if vd >=0 :
            liste_valeur.append(vd)
        if vh >= 0 :
            liste_valeur.append(vh)
        if vb >=0 :
            liste_valeur.append(vb)
        # la plus petite distance deja trouvvee autour
        mini = min(liste_valeur)

        # donc un de plus pour la case x,y
        v2 = mini + 1
        self.grille[x][y] = v2

        # si on a changé qq chose, on doit recalculer certaines cases autour, il faut donc les ajouter à la liste à traiter
        # celles qui sont positives ou inconnnues
        if vg == BLOC_INCONNU and len(self.listeCasesACalculer) < 1000:
            newCase = [x-1,y]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)
        if vd == BLOC_INCONNU and len(self.listeCasesACalculer) < 1000:
            newCase = [x+1,y]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)
        if vh == BLOC_INCONNU and len(self.listeCasesACalculer) < 1000:
            newCase = [x,y-1]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)
        if vb == BLOC_INCONNU and len(self.listeCasesACalculer) < 1000:
            newCase = [x,y+1]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)

    # ------------------------------------------------
    def calcule_distance_grille(self):
        self.reset_distance_grille()
        self.listeCasesACalculer=[]

        self.listeCasesACalculer.append([GRILLE_LX-2,GRILLE_PORTE])
        self.listeCasesACalculer.append([GRILLE_LX-2,GRILLE_PORTE+1])

        for case in self.listeCasesACalculer:
            #print("liste : ",len(self.listeCasesACalculer) ,self.listeCasesACalculer)
            self.calcule_distance(case[0],case[1])
            if len(self.listeCasesACalculer) > 1000:
                break

# ============================================================
# ============================================================

if __name__=="__main__":

    grille = Grille()
    grille.calcule_distance_grille()
    grille.dessine_grille()

    while True:

        for event in pygame.event.get():
            #print (event)

            # un clic sur le X de fermeture de fenetre ?
            if event.type==pygame.QUIT:
                    pygame.quit()
                    exit(0)

            if event.type==pygame.KEYDOWN:
                #print(event.key)

                # Q
                if event.key==97:
                    pygame.quit()
                    exit(0)

            souris = pygame.mouse.get_pos()
            #print(souris)
            x_souris = souris[0]
            y_souris = souris[1]

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                grille.nouvelle_tour(Tour(int(x_souris/20),int(y_souris/20)))
                grille.calcule_distance_grille()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                grille.enleve_tour(int(x_souris/20),int(y_souris/20))
                grille.calcule_distance_grille()

            else:
                tourBrouillon = Tour(int(x_souris/20),int(y_souris/20),ETAT_TOUR_BROUILLON)

        grille.dessine_grille()
        if tourBrouillon:
            tourBrouillon.affiche()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


