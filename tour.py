# tour.py
# coding: utf-8

__author__ = 'Quentin'

from outils import *

# ============================================================
# ============================================================
class Tour():

    _ETAT_TOUR_CONSTRUIT = 1
    _ETAT_TOUR_BROUILLON = 0

    # ------------------------------------------------
    def __init__(self,x,y,etat=_ETAT_TOUR_CONSTRUIT):
        self.x = x
        self.y = y
        self.etat = etat

    # ------------------------------------------------
    def affiche(self):
        if self.etat == Tour._ETAT_TOUR_BROUILLON:
            recttransparent = pygame.Surface((40,40), pygame.SRCALPHA, 32)
            recttransparent.fill((0,0,255, 50))
            SCREEN.blit(recttransparent, conversionCoordCasesVersPixels(self.x,self.y))

        elif self.etat== Tour._ETAT_TOUR_CONSTRUIT:
            SCREEN.blit(IMAGE_TOURELLE_VIDE,conversionCoordCasesVersPixels(self.x,self.y))

