# coding: utf-8

__author__ = 'Quentin'

from outils import *


class Evenement():

    def __init__(self,x,y,texte='test',couleur=VERT,duree=50,police=FONT_2):

        self.x=x
        self.y=y
        self.texte = texte
        self.police = police
        self.couleur = couleur
        self.duree = duree

    # -------------------------------------------------
    def affiche(self):
        surface = self.police.render(self.texte, True, self.couleur)
        rect = surface.get_rect(topleft=(self.x, self.y))
        SCREEN.blit(surface, rect)