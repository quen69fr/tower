# tour.py
# coding: utf-8

__author__ = 'Quentin'

from outils import *
from tir import Tir

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
        self.a_tire = False
        self.distance_tir = 100  # en pixels

    # ------------------------------------------------
    def affiche(self):
        if self.etat == Tour._ETAT_TOUR_BROUILLON:
            recttransparent = pygame.Surface((40,40), pygame.SRCALPHA, 32)
            recttransparent.fill((0,0,255, 50))
            SCREEN.blit(recttransparent, conversionCoordCasesVersPixels(self.x,self.y))

        elif self.etat== Tour._ETAT_TOUR_CONSTRUIT:
            SCREEN.blit(IMAGE_TOURELLE_VIDE,conversionCoordCasesVersPixels(self.x,self.y))
            (cx,cy)=centreCase(self.x,self.y)
            pygame.draw.circle(SCREEN,VERT, (int(cx),int(cy)) ,self.distance_tir, 1)

    def gere_construction(self):
        ''' si necessaire, fait avancer la construction d'une tour'''
        # TODO gere construction tour
        pass


    def gere_deconstruction(self):
        ''' si necessaire, fait avancer la DE-construction d'une tour'''
        # TODO gere_deconstruction tour
        pass


    def cree_tir(self,listeBestioles):
        '''
        determine s'il faut tirer, et si oui, crée un tir, trouve la cible ...
        retourne un tir si un tir a été créé, sinon rend NULL
        '''
        # TODO : frequence de tir, presence cible, viser cible
        if self.a_tire is False:
            # Frequence ?
            # todo
            # Présence cible en vue ?
            # ...
            for b in listeBestioles:
                # distance entre : self.centreCase() et (b.x, b.y)
                (cx,cy) = centreCase(self.x,self.y)
                dist = math.sqrt ( (cx-b.x)**2 + (cy-b.y)**2 )
                if dist <= self.distance_tir:
                    # Si oui, calculer direction
                    self.a_tire = True
                    c = centreCase(self.x, self.y)
                    return Tir(c[0], c[1])

        # sinon pas de tir
        return