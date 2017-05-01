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

    def __init__(self, bete, vitesse, force,force_ralentire,compte_a_rebour_ralentire, x = 100, y = 100):
        self.x = x             # pixel abscisse
        self.y = y             # ordonnéee
        self.bete = bete       # cible du tir
        self.vitesse = vitesse
        self.impact = False    # le tir a-t-il atteint sa cible ?
        self.force = force     # force du tir (diminution de vie de la bestiole touchee)
        #print(self.force)

        self.force_ralentire = force_ralentire
        self.compte_a_rebour_ralentire = compte_a_rebour_ralentire

    # ------------------------------------------------
    def affiche(self):
        couleur = BLANC
        if self.vitesse == TABLE_TOUR_VITESSE[0]:
            couleur = BLANC
        elif self.vitesse == TABLE_TOUR_VITESSE[0]+TABLE_TOUR_VITESSE[1]:
            couleur = JAUNE
        elif self.vitesse == TABLE_TOUR_VITESSE[0]+TABLE_TOUR_VITESSE[1]+TABLE_TOUR_VITESSE[2]:
            couleur = ORANGE
        elif self.vitesse == TABLE_TOUR_VITESSE[0]+TABLE_TOUR_VITESSE[1]+TABLE_TOUR_VITESSE[2]+TABLE_TOUR_VITESSE[3]:
            couleur = ROUGE

        tail = 2
        if self.force == TABLE_TOUR_FORCE[0]:
            tail = 1
        elif self.force == TABLE_TOUR_FORCE[0]+TABLE_TOUR_FORCE[1]:
            tail = 2
        elif self.force == TABLE_TOUR_FORCE[0]+TABLE_TOUR_FORCE[1]+TABLE_TOUR_FORCE[2]:
            tail = 3
        elif self.force == TABLE_TOUR_FORCE[0]+TABLE_TOUR_FORCE[1]+TABLE_TOUR_FORCE[2]+TABLE_TOUR_FORCE[3]:
            tail = 4

        pygame.draw.circle(SCREEN, couleur, [int(self.x), int(self.y)], tail, 0)
        pass

    # ------------------------------------------------
    def deplace(self):
        # TODO : prendre le centre de la bestiole et pas le coin pixel haut-gauche
        dirx = self.bete.x - self.x
        diry = self.bete.y - self.y
        distance = math.sqrt(dirx ** 2 + diry **2)

        # impact
        if distance < self.vitesse:
            self.impact = True
            return

        # sinon deplace
        dirx = dirx / distance
        diry = diry / distance

        self.x = int(self.x + dirx * self.vitesse )
        self.y = int(self.y + diry * self.vitesse )

    # ------------------------------------------------
    def traite_impact(self):

        # on diminue la vie de la bestiole selon la force du tir
        if self.bete.vie > self.force:
            self.bete.vie -= self.force

            if self.bete.ralentie(self.compte_a_rebour_ralentire,self.force_ralentire):
                self.bete.vitesse = self.bete.vitesse * self.force_ralentire

        else:
            self.bete.vie=0