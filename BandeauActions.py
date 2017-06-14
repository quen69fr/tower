# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'

from outils import *
from tour import *
from bestiole import *


class BandeauAction():

    def __init__(self):
        pass

    # ------------------------------------------------
    def mise_jour_etat(self,etat_partie, tour_select, bestiole_select, argent):
        self.etat_partie=etat_partie
        self.tour_select = tour_select
        self.bestiole_select = bestiole_select
        self.argent = argent

    # ------------------------------------------------
    def affiche(self,premiere_vague,boutonInfoGrille):
        self.afficheCadreHaut(boutonInfoGrille)
        self.afficheCadreInfo(premiere_vague)

    # ------------------------------------------------
    def afficheCadreHaut(self,boutonInfoGrille):
        if self.etat_partie == ETAT_PARTIE_ACCUEIL:
            SCREEN.blit(IMAGE_START,(X_START_NEXT,Y_START_NEXT))

        elif self.etat_partie == ETAT_PARTIE_PERDU or self.etat_partie == ETAT_PARTIE_GAGNE:
            SCREEN.blit(IMAGE_RESTART,(X_START_NEXT,Y_START_NEXT))

        elif self.etat_partie == ETAT_PARTIE_JEU:
            SCREEN.blit(IMAGE_NEXT,(X_START_NEXT,Y_START_NEXT))

            SCREEN.blit(IMAGE_TOURELLE_TOUS,(X_TOURELLE,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_CANON_1,(X_TOURELLE,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_NORMAL,(X_TOURELLE+60,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_CANON_1,(X_TOURELLE+60,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_BOUM,(X_TOURELLE+120,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_VOLANT,(X_TOURELLE+180,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_CANON_1,(X_TOURELLE+180,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_BOUM_VOLANT,(X_TOURELLE+240,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_PLUS,(X_TOURELLE+300,Y_TOURELLE))

            SCREEN.blit(IMAGE_BOUTON_PAUSE,(X_BOUTON_PLAY_PAUSE,Y_BOUTON_PLAY_PAUSE))
            SCREEN.blit(IMAGE_BOUTON_PLUS,(900,Y_BOUTON_PLAY_PAUSE))
            SCREEN.blit(IMAGE_BOUTON_MOINS,(948,Y_BOUTON_PLAY_PAUSE))
            if boutonInfoGrille:
                SCREEN.blit(IMAGE_BOUTON_INFO_GRILLE2,(X_BOUTON_INFO_GRILLE,Y_BOUTON_INFO_GRILLE))
            else:
                SCREEN.blit(IMAGE_BOUTON_INFO_GRILLE,(X_BOUTON_INFO_GRILLE,Y_BOUTON_INFO_GRILLE))

            SCREEN.blit(IMAGE_AIDE, (X_BOUTON_AIDE,Y_BOUTON_AIDE))


        elif self.etat_partie == ETAT_PARTIE_PAUSE:
            SCREEN.blit(IMAGE_NEXT,(X_START_NEXT,Y_START_NEXT))

            SCREEN.blit(IMAGE_TOURELLE_TOUS,(X_TOURELLE,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_NORMAL,(X_TOURELLE+60,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_BOUM,(X_TOURELLE+120,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_VOLANT,(X_TOURELLE+180,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_BOUM_VOLANT,(X_TOURELLE+240,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_PLUS,(X_TOURELLE+300,Y_TOURELLE))

            SCREEN.blit(IMAGE_BOUTON_PLAY,(X_BOUTON_PLAY_PAUSE,Y_BOUTON_PLAY_PAUSE))

    # ------------------------------------------------
    def afficheCadreInfo(self,premiere_vague):

        if self.tour_select != None:
            tour = self.tour_select
            SCREEN.blit(IMAGE_PENCARTE,(680,150))

            if tour.type == TOUR_PLUS:
                self.afficheTourPLUS(tour)

            else:
                self.afficheTourForce(tour)
                self.afficheTourDistance(tour)
                self.afficheTourCadence(tour)
                self.afficheTourVitesse(tour)
                self.afficheTourRalentir(tour)
                self.afficheTourCoeff(tour)
                self.afficheTourSuprimee(tour,premiere_vague)

        elif self.bestiole_select != None:

            bestiole =self.bestiole_select
            SCREEN.blit(IMAGE_PENCARTE,(680,150))

            img = TABLE_BESTIOLE[bestiole.type]["image_d"]
            SCREEN.blit(img,(800,250))

            texte="Vie : {}".format(int(bestiole.vie))
            surface = FONT_4.render(texte, True, ROUGE)
            rect = surface.get_rect(topleft=(700, 300))
            SCREEN.blit(surface, rect)

            texte="Argent : {}".format(bestiole.gain)
            surface = FONT_4.render(texte, True, JAUNE)
            rect = surface.get_rect(topleft=(700, 350))
            SCREEN.blit(surface, rect)

            texte="Vitesse : {}".format(bestiole.vitesse)
            surface = FONT_4.render(texte, True, BLEU)
            rect = surface.get_rect(topleft=(700, 400))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheExplication(self,pageAide):
        if pageAide == 0:
            SCREEN.blit(IMAGE_EXPLICATION_1,(120,60))
        elif pageAide == 1:
            SCREEN.blit(IMAGE_EXPLICATION_2,(120,60))
        elif pageAide == 2:
            SCREEN.blit(IMAGE_EXPLICATION_3,(120,60))
        elif pageAide == 3:
            SCREEN.blit(IMAGE_EXPLICATION_4,(120,60))

        SCREEN.blit(IMAGE_AIDE_EXPLICATION,(90,30))
        SCREEN.blit(IMAGE_BOUTON_FLECHE,(X_BOUTON_FLECHE,Y_BOUTON_FLECHE))

    # ------------------------------------------------
    def afficheTourForce(self,tour):

        SCREEN.blit(IMAGE_TOUCHE_AMELIORATION,(X_TOUCHE,Y_TOUCHE_F))

        texte="F Force : {}".format(tour.force_tir)
        surface = FONT_4.render(texte, True, VERT)
        rect = surface.get_rect(topleft=(700, 250))
        SCREEN.blit(surface, rect)

        if tour.niveau_force<len(tour.table_tour_force)-1:
            texte="+ {}".format(tour.table_tour_force[tour.niveau_force + 1])
            surface = FONT_4.render(texte, True, VERT)
            rect = surface.get_rect(topleft=(940, 250))
            SCREEN.blit(surface, rect)

            texte="{} €".format(tour.table_tour_force_prix[tour.niveau_force] + prixSuplementaire(tour))
            if self.argent >= tour.table_tour_force_prix[tour.niveau_force] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 250))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourDistance(self,tour):

        SCREEN.blit(IMAGE_TOUCHE_AMELIORATION,(X_TOUCHE,Y_TOUCHE_D))

        texte="D Distance : {}".format(tour.distance_tir)
        surface = FONT_4.render(texte, True, VERT)
        rect = surface.get_rect(topleft=(700, 300))
        SCREEN.blit(surface, rect)

        if tour.niveau_distance<len(tour.table_tour_distance)-1:
            texte="+ {}".format(tour.table_tour_distance[tour.niveau_distance + 1])
            surface = FONT_4.render(texte, True, VERT)
            rect = surface.get_rect(topleft=(940, 300))
            SCREEN.blit(surface, rect)

            texte="{} €".format(tour.table_tour_distance_prix[tour.niveau_distance] + prixSuplementaire(tour))
            if self.argent >= tour.table_tour_distance_prix[tour.niveau_distance] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 300))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourCadence(self,tour):

        SCREEN.blit(IMAGE_TOUCHE_AMELIORATION,(X_TOUCHE,Y_TOUCHE_C))

        texte="C Cadence : {}".format(tour.cadence_tir)
        surface = FONT_4.render(texte, True, VERT)
        rect = surface.get_rect(topleft=(700, 350))
        SCREEN.blit(surface, rect)

        if tour.niveau_cadence<len(tour.table_tour_cadence)-1:
            texte="+ {}".format(tour.table_tour_cadence[tour.niveau_cadence + 1])
            surface = FONT_4.render(texte, True, VERT)
            rect = surface.get_rect(topleft=(940, 350))
            SCREEN.blit(surface, rect)

            texte="{} €".format(tour.table_tour_cadence_prix[tour.niveau_cadence] + prixSuplementaire(tour))
            if self.argent >= tour.table_tour_cadence_prix[tour.niveau_cadence] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 350))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourVitesse(self,tour):

        SCREEN.blit(IMAGE_TOUCHE_AMELIORATION,(X_TOUCHE,Y_TOUCHE_V))

        texte="V Vitesse : {}".format(tour.vitesse_tir)
        surface = FONT_4.render(texte, True, VERT)
        rect = surface.get_rect(topleft=(700, 400))
        SCREEN.blit(surface, rect)

        if tour.niveau_vitesse<len(tour.table_tour_vitesse)-1:
            texte="+ {}".format(tour.table_tour_vitesse[tour.niveau_vitesse + 1])
            surface = FONT_4.render(texte, True, VERT)
            rect = surface.get_rect(topleft=(940, 400))
            SCREEN.blit(surface, rect)

            texte="{} €".format(tour.table_tour_vitesse_prix[tour.niveau_vitesse] + prixSuplementaire(tour))
            if self.argent >= tour.table_tour_vitesse_prix[tour.niveau_vitesse] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 400))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourRalentir(self,tour):

        SCREEN.blit(IMAGE_TOUCHE_AMELIORATION,(X_TOUCHE,Y_TOUCHE_R))

        texte="R Ralentir : {}".format(tour.compte_a_rebour_ralentire)
        surface = FONT_4.render(texte, True, VERT)
        rect = surface.get_rect(topleft=(700, 450))
        SCREEN.blit(surface, rect)

        if tour.niveau_ralentire<len(tour.table_tour_ralenti_duree)-1:
            texte="+ {}".format(tour.table_tour_ralenti_duree[tour.niveau_ralentire + 1])
            surface = FONT_4.render(texte, True, VERT)
            rect = surface.get_rect(topleft=(940, 450))
            SCREEN.blit(surface, rect)

            texte="{} €".format(tour.table_tour_ralenti_prix[tour.niveau_ralentire] + prixSuplementaire(tour))
            if self.argent >= tour.table_tour_ralenti_prix[tour.niveau_ralentire] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 450))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourCoeff(self,tour):

        texte="Coeff : {} %".format(round((tour.coeffPlus-1)*100,2))
        surface = FONT_4.render(texte, True, JAUNE)
        rect = surface.get_rect(topleft=(700, 170))
        SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourSuprimee(self,tour,premiere_vague):

        SCREEN.blit(IMAGE_TOUCHE_SUPRESSION,(X_TOUCHE,Y_TOUCHE_S))

        texte="S Supression"
        surface = FONT_4.render(texte, True, ROUGE)
        rect = surface.get_rect(topleft=(700, 500))
        SCREEN.blit(surface, rect)

        if premiere_vague:
            texte="+ {} €".format(int(tour.argent_depense))
        else:
            texte="+ {} €".format(int(tour.argent_depense/2))
        surface = FONT_4.render(texte, True, JAUNE)
        rect = surface.get_rect(topleft=(1000, 500))
        SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourPLUS(self,tour):
        pass

    # ------------------------------------------------
    def clic(self,x_souris,y_souris):

        if X_START_NEXT < x_souris < (X_START_NEXT+155) and Y_START_NEXT < y_souris < (Y_START_NEXT+53):
            return BOUTON_START_NEXT

        elif math.sqrt((x_souris - (X_BOUTON_PLAY_PAUSE+RAYON_BOUTON_PAUSE))**2 + (y_souris - (Y_BOUTON_PLAY_PAUSE+RAYON_BOUTON_PAUSE))**2 ) <= RAYON_BOUTON_PAUSE:
            return BOUTON_PAUSE

        elif X_TOURELLE < x_souris < (X_TOURELLE+40) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            return BOUTON_TOURELLE_TOUS

        elif X_TOURELLE+60 < x_souris < (X_TOURELLE+40+60) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            return BOUTON_TOURELLE_NORMAL

        elif X_TOURELLE+120 < x_souris < (X_TOURELLE+40+120) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            return BOUTON_TOURELLE_BOUM

        elif X_TOURELLE+180 < x_souris < (X_TOURELLE+40+180) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            return BOUTON_TOURELLE_VOLANT

        elif X_TOURELLE+240 < x_souris < (X_TOURELLE+40+240) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            return BOUTON_TOURELLE_BOUM_VOLANT

        elif X_TOURELLE+300 < x_souris < (X_TOURELLE+40+300) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            return BOUTON_TOURELLE_PLUS

        elif math.sqrt((x_souris - (900+RAYON_BOUTON_PAUSE))**2 + (y_souris - (Y_BOUTON_PLAY_PAUSE+RAYON_BOUTON_PAUSE))**2 ) <= RAYON_BOUTON_PAUSE:
            return BOUTON_PLUS

        elif math.sqrt((x_souris - (948+RAYON_BOUTON_PAUSE))**2 + (y_souris - (Y_BOUTON_PLAY_PAUSE+RAYON_BOUTON_PAUSE))**2 ) <= RAYON_BOUTON_PAUSE:
            return BOUTON_MOINS

        elif X_BOUTON_AIDE < x_souris < (X_BOUTON_AIDE+80) and Y_BOUTON_AIDE < y_souris < (Y_BOUTON_AIDE+81):
            return BOUTON_AIDE

        elif X_BOUTON_FLECHE < x_souris < (X_BOUTON_FLECHE+48) and Y_BOUTON_FLECHE < y_souris < (Y_BOUTON_FLECHE+48):
            return BOUTON_FLECHE_GAUCHE

        elif X_BOUTON_FLECHE+64 < x_souris < (X_BOUTON_FLECHE+64+48) and Y_BOUTON_FLECHE < y_souris < (Y_BOUTON_FLECHE+48):
            return BOUTON_FLECHE_DROITE

        elif X_TOUCHE < x_souris < (X_TOUCHE+35) and Y_TOUCHE_F < y_souris < (Y_TOUCHE_F+35):
            return TOUCHE_F

        elif X_TOUCHE < x_souris < (X_TOUCHE+35) and Y_TOUCHE_D < y_souris < (Y_TOUCHE_D+35):
            return TOUCHE_D

        elif X_TOUCHE < x_souris < (X_TOUCHE+35) and Y_TOUCHE_C < y_souris < (Y_TOUCHE_C+35):
            return TOUCHE_C

        elif X_TOUCHE < x_souris < (X_TOUCHE+35) and Y_TOUCHE_V < y_souris < (Y_TOUCHE_V+35):
            return TOUCHE_V

        elif X_TOUCHE < x_souris < (X_TOUCHE+35) and Y_TOUCHE_R < y_souris < (Y_TOUCHE_R+35):
            return TOUCHE_R

        elif X_TOUCHE < x_souris < (X_TOUCHE+35) and Y_TOUCHE_S < y_souris < (Y_TOUCHE_S+35):
            return TOUCHE_S

        elif X_BOUTON_INFO_GRILLE < x_souris < (X_BOUTON_INFO_GRILLE+100) and Y_BOUTON_INFO_GRILLE < y_souris < (Y_BOUTON_INFO_GRILLE+50):
            return BOUTON_INFO_GRILLE

        else:
            return None

    # ------------------------------------------------
    def affiche_vagues(self,vague):

        for i in range(1,6):
            image = IMAGE_VAGUE_N
            if vague+i>len(TABLE_VAGUE)-1:
                continue
            if TABLE_VAGUE[vague+i]['type']=='rapide':
                image = IMAGE_VAGUE_R
            if TABLE_VAGUE[vague+i]['type']=='groupe':
                image = IMAGE_VAGUE_G
            if TABLE_VAGUE[vague+i]['type']=='imune':
                image = IMAGE_VAGUE_I
            if TABLE_VAGUE[vague+i]['type']=='fort':
                image = IMAGE_VAGUE_L
            if TABLE_VAGUE[vague+i]['type']=='volant':
                image = IMAGE_VAGUE_V

            if TABLE_VAGUE[vague+i]['type']=='boss_normale':
                image = IMAGE_VAGUE_BN
            if TABLE_VAGUE[vague+i]['type']=='boss_rapide':
                image = IMAGE_VAGUE_BR
            if TABLE_VAGUE[vague+i]['type']=='boss_groupe':
                image = IMAGE_VAGUE_BG
            if TABLE_VAGUE[vague+i]['type']=='boss_imune':
                image = IMAGE_VAGUE_BI
            if TABLE_VAGUE[vague+i]['type']=='boss_fort':
                image = IMAGE_VAGUE_BL
            if TABLE_VAGUE[vague+i]['type']=='boss_volant':
                image = IMAGE_VAGUE_BV

            SCREEN.blit(image,(75+(100*i),550))
