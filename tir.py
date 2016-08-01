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

    def __init__(self, bete, x = 100 ,y=100):
        self.x = x             # pixel abscisse
        self.y = y             # ordonnéee
        self.bete = bete       # cible du tir
        self.vitesse = VITESSE_TIR
        self.impact = False    # le tir a-t-il atteint sa cible ?
        self.force = 3         # force du tir (diminution de vie de la bestiole touchee)

    def affiche(self):
        # SCREEN.blit(self.rot_center(IMAGE_BESTIOLE,45),(self.x-self.rayon,self.y-self.rayon))
        pygame.draw.circle(SCREEN, BLEU, [int(self.x), int(self.y)], 6, 0)
        pass

    def deplace(self, grille):
        # print (type(self.x), type(self.dirx))
        # TODO : prendre le centre de la bestiole et pas le coin pixel haut-gauche
        dirx = self.bete.x - self.x
        diry = self.bete.y - self.y
        distance = math.sqrt(dirx ** 2 + diry **2)

        # impact
        if distance < 5:
            self.impact = True
            return

        # sinon deplace
        dirx = dirx / distance
        diry = diry / distance

        self.x = int(self.x + dirx * self.vitesse )
        self.y = int(self.y + diry * self.vitesse )

    def traite_impact(self):
        # on diminue la vie de la bestiole selon la force du tir
        self.bete.vie -= self.force


