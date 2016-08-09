# tour.py
# coding: utf-8

__author__ = 'Quentin'

from outils import *
from tir import Tir

# ============================================================
class Tour():

    _ETAT_TOUR_CONSTRUIT = 1
    _ETAT_TOUR_BROUILLON = 0

    # ------------------------------------------------
    def __init__(self,x,y,etat=_ETAT_TOUR_CONSTRUIT):
        self.x = x
        self.y = y
        self.etat = etat
        self.distance_tir = DISTANCE_TIR  # en pixels
        self.delai_initial = DELAI_TIR
        self.delai = 0

    # ------------------------------------------------
    def affiche(self,tour_selectionnee = False ):
        if self.etat == Tour._ETAT_TOUR_BROUILLON:
            recttransparent = pygame.Surface((40,40), pygame.SRCALPHA, 32)
            recttransparent.fill((0,0,255, 50))
            SCREEN.blit(recttransparent, conversionCoordCasesVersPixels(self.x,self.y))
            if AFFICHE_PERIMETRE_TIR:
                pygame.draw.circle(SCREEN, VERT, centreTour(self.x, self.y), self.distance_tir, 1)

        elif self.etat== Tour._ETAT_TOUR_CONSTRUIT:

            if tour_selectionnee == False:
                SCREEN.blit(IMAGE_TOURELLE_VIDE,conversionCoordCasesVersPixels(self.x,self.y))

            elif tour_selectionnee == True:

                SCREEN.blit(IMAGE_TOURELLE_VIDE,conversionCoordCasesVersPixels(self.x,self.y))

                recttransparent = pygame.Surface((40,40), pygame.SRCALPHA, 32)
                recttransparent.fill((0,255,0, 100))
                SCREEN.blit(recttransparent, conversionCoordCasesVersPixels(self.x,self.y))

                pygame.draw.circle(SCREEN, VERT, centreTour(self.x, self.y), self.distance_tir, 1)

    # ------------------------------------------------
    def gere_construction(self):
        ''' si necessaire, fait avancer la construction d'une tour'''
        # TODO gere construction tour
        pass

    # ------------------------------------------------
    def gere_deconstruction(self):
        ''' si necessaire, fait avancer la DE-construction d'une tour'''
        # TODO gere_deconstruction tour
        pass

    # ------------------------------------------------
    def cree_tir(self,listeBestioles):
        '''
        determine s'il faut tirer, et si oui, crée un tir, trouve la cible ...
        retourne un tir si un tir a été créé, sinon rend NULL
        '''

        if TIR_ACTIF is False:
            return

        # delai de tir OK ? (autre stratégie : nombre de tirs simultanés maxi)
        if self.delai != 0:
            self.delai -= 1
            return

        # Recherche cible ?
        # La premiere de la liste qui est à bonne distance
        # TODO : autre stratégie : la plus proche de la sortie, la plus proche de la tour, ...
        for b in listeBestioles:
            # distance entre : self.centreCase() et (b.x, b.y)
            (cx,cy) = centreCase(self.x,self.y)
            dist = math.sqrt ( (cx-b.x)**2 + (cy-b.y)**2 )
            if dist <= self.distance_tir:
                # Si oui, calculer direction
                self.delai = self.delai_initial
                c = centreTour(self.x, self.y)
                return Tir(b, c[0], c[1])

        # print(self.delai)
        # sinon pas de tir
        return