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
            SCREEN.blit(recttransparent, (MARGE_ECRAN+self.x*TAILLE_BLOC,MARGE_ECRAN+self.y*TAILLE_BLOC))

        elif self.etat== Tour._ETAT_TOUR_CONSTRUIT:
            #pygame.draw.rect(SCREEN, BLEU, (MARGE_ECRAN+self.x*TAILLE_BLOC,MARGE_ECRAN+self.y*TAILLE_BLOC,TAILLE_BLOC*2,TAILLE_BLOC*2),0)
            SCREEN.blit(IMAGE_TOURELLE_VIDE,(MARGE_ECRAN+self.x*TAILLE_BLOC,MARGE_ECRAN+self.y*TAILLE_BLOC))

