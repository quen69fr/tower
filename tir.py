# -*- coding: utf-8 -*-
# Tower / tirs

__author__ = 'Quentin'

from grille import *
from outils import *


# Algo
# chaque tour gère son rythme de tir
# une tour qui tire :
# - cherche sa cible (la plus proche, la plus proche de la sortie, ...)
# - cree un tir, l'ajoute à la liste des tirs à suivre.

class Tir():

    def __init__(self,x = 100 ,y=100):
        self.x = x
        self.y = y
        self.dirx = 2
        self.diry = 1


    def affiche(self):
        # SCREEN.blit(self.rot_center(IMAGE_BESTIOLE,45),(self.x-self.rayon,self.y-self.rayon))
        pygame.draw.circle(SCREEN, BLEU, [int(self.x), int(self.y)], 6, 0)
        pass

    def deplace(self, grille):
        # print (type(self.x), type(self.dirx))
        self.x = self.x + self.dirx
        self.y += self.diry

    def verifie_impact(self):
        pass

