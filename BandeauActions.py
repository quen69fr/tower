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
    def affiche(self):
        self.afficheCadreHaut()
        self.afficheCadreInfo()

    # ------------------------------------------------
    def afficheCadreHaut(self):
        if self.etat_partie == ETAT_PARTIE_ACCUEIL:
            SCREEN.blit(IMAGE_START,(X_START_NEXT,Y_START_NEXT))

        elif self.etat_partie == ETAT_PARTIE_PERDU or self.etat_partie == ETAT_PARTIE_GAGNE:
            SCREEN.blit(IMAGE_RESTART,(X_START_NEXT,Y_START_NEXT))

        elif self.etat_partie == ETAT_PARTIE_JEU:
            SCREEN.blit(IMAGE_NEXT,(X_START_NEXT,Y_START_NEXT))

            SCREEN.blit(IMAGE_TOURELLE_TOUS,(X_TOURELLE,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_NORMAL,(X_TOURELLE+60,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_BOUM,(X_TOURELLE+120,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_VOLANT,(X_TOURELLE+180,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_BOUM_VOLANT,(X_TOURELLE+240,Y_TOURELLE))
            SCREEN.blit(IMAGE_TOURELLE_PLUS,(X_TOURELLE+300,Y_TOURELLE))

            SCREEN.blit(IMAGE_BOUTON_PAUSE,(X_BOUTON_PLAY_PAUSE,Y_BOUTON_PLAY_PAUSE))

            SCREEN.blit(IMAGE_BOUTON_PLUS,(900,Y_BOUTON_PLAY_PAUSE))
            SCREEN.blit(IMAGE_BOUTON_MOINS,(948,Y_BOUTON_PLAY_PAUSE))

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
    def afficheCadreInfo(self):

        if self.tour_select != None:
            tour = self.tour_select
            SCREEN.blit(IMAGE_PENCARTE,(680,150))

            if tour.type == TOUR_PLUS:
                self.afficheTourPLUS(tour)

            else:
                self.afficheTourForce(tour)
                self.afficheTourDistance(tour)
                self.afficheTourRapidité(tour)
                self.afficheTourVitesse(tour)
                self.afficheTourRalentir(tour)
                self.afficheTourCoeff(tour)
                self.afficheTourSuprimee(tour)


        elif self.bestiole_select != None:

            bestiole =self.bestiole_select
            SCREEN.blit(IMAGE_PENCARTE,(680,150))

            img = TABLE_BESTIOLE[bestiole.type]["image_d"]
            SCREEN.blit(img,(800,250))

            texte="Vie : {}".format(bestiole.vie)
            surface = FONT_4.render(texte, True, ROUGE)
            rect = surface.get_rect(topleft=(700, 300))
            SCREEN.blit(surface, rect)

            texte="Argent : {}".format(TABLE_BESTIOLE[bestiole.type]['gain']*TABLE_VAGUE[bestiole.vague]['difficultee'])
            surface = FONT_4.render(texte, True, JAUNE)
            rect = surface.get_rect(topleft=(700, 350))
            SCREEN.blit(surface, rect)

            texte="Vitesse : {}".format(bestiole.vitesse)
            surface = FONT_4.render(texte, True, BLEU)
            rect = surface.get_rect(topleft=(700, 400))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourForce(self,tour):

        texte="F-Force : {}".format(tour.force_tir)
        surface = FONT_4.render(texte, True, ROUGE)
        rect = surface.get_rect(topleft=(700, 250))
        SCREEN.blit(surface, rect)

        if tour.niveau_force<len(TABLE_NORMALE_TOUR_FORCE)-1:
            texte="+ {}".format(TABLE_NORMALE_TOUR_FORCE[tour.niveau_force + 1])
            surface = FONT_4.render(texte, True, ROUGE)
            rect = surface.get_rect(topleft=(940, 250))
            SCREEN.blit(surface, rect)

            texte="{} €".format(TABLE_NORMALE_TOUR_FORCE_PRIX[tour.niveau_force] + prixSuplementaire(tour))
            if self.argent >= TABLE_NORMALE_TOUR_FORCE_PRIX[tour.niveau_force] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 250))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourDistance(self,tour):

        texte="D-Distance : {}".format(tour.distance_tir)
        surface = FONT_4.render(texte, True, VERT)
        rect = surface.get_rect(topleft=(700, 300))
        SCREEN.blit(surface, rect)

        if tour.niveau_distance<len(TABLE_NORMALE_TOUR_DISTANCE)-1:
            texte="+ {}".format(TABLE_NORMALE_TOUR_DISTANCE[tour.niveau_distance + 1])
            surface = FONT_4.render(texte, True, VERT)
            rect = surface.get_rect(topleft=(940, 300))
            SCREEN.blit(surface, rect)

            texte="{} €".format(TABLE_NORMALE_TOUR_DISTANCE_PRIX[tour.niveau_distance] + prixSuplementaire(tour))
            if self.argent >= TABLE_NORMALE_TOUR_DISTANCE_PRIX[tour.niveau_distance] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 300))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourRapidité(self,tour):

        texte="R-Rapidité : {}".format(tour.rapidite_tir)
        surface = FONT_4.render(texte, True, BLEU)
        rect = surface.get_rect(topleft=(700, 350))
        SCREEN.blit(surface, rect)

        if tour.niveau_rapidite<len(TABLE_NORMALE_TOUR_RAPIDITE)-1:
            texte="+ {}".format(TABLE_NORMALE_TOUR_RAPIDITE[tour.niveau_rapidite + 1])
            surface = FONT_4.render(texte, True, BLEU)
            rect = surface.get_rect(topleft=(940, 350))
            SCREEN.blit(surface, rect)

            texte="{} €".format(TABLE_NORMALE_TOUR_RAPIDITE_PRIX[tour.niveau_rapidite] + prixSuplementaire(tour))
            if self.argent >= TABLE_NORMALE_TOUR_RAPIDITE_PRIX[tour.niveau_rapidite] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 350))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourVitesse(self,tour):

        texte="V-Vitesse : {}".format(tour.vitesse_tir)
        surface = FONT_4.render(texte, True, GRIS)
        rect = surface.get_rect(topleft=(700, 400))
        SCREEN.blit(surface, rect)

        if tour.niveau_vitesse<len(TABLE_NORMALE_TOUR_VITESSE)-1:
            texte="+ {}".format(TABLE_NORMALE_TOUR_VITESSE[tour.niveau_vitesse + 1])
            surface = FONT_4.render(texte, True, GRIS)
            rect = surface.get_rect(topleft=(940, 400))
            SCREEN.blit(surface, rect)

            texte="{} €".format(TABLE_NORMALE_TOUR_VITESSE_PRIX[tour.niveau_vitesse] + prixSuplementaire(tour))
            if self.argent >= TABLE_NORMALE_TOUR_VITESSE_PRIX[tour.niveau_vitesse] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 400))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourRalentir(self,tour):

        texte="L-Ralentire : {}".format(tour.compte_a_rebour_ralentire)
        surface = FONT_4.render(texte, True, ORANGE)
        rect = surface.get_rect(topleft=(700, 450))
        SCREEN.blit(surface, rect)

        if tour.niveau_ralentire<len(TABLE_NORMALE_TOUR_RALENTI_DUREE)-1:
            texte="+ {}".format(TABLE_NORMALE_TOUR_RALENTI_DUREE[tour.niveau_ralentire + 1])
            surface = FONT_4.render(texte, True, ORANGE)
            rect = surface.get_rect(topleft=(940, 450))
            SCREEN.blit(surface, rect)

            texte="{} €".format(TABLE_NORMALE_TOUR_RALENTI_PRIX[tour.niveau_ralentire] + prixSuplementaire(tour))
            if self.argent >= TABLE_NORMALE_TOUR_RALENTI_PRIX[tour.niveau_ralentire] + prixSuplementaire(tour):
                surface = FONT_4.render(texte, True, JAUNE)
            else:
                surface = FONT_4.render(texte, True, JAUNE2)
            rect = surface.get_rect(topleft=(1020, 450))
            SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourCoeff(self,tour):

        texte="Coeff : {}".format(round(tour.coeffPlus,2))
        surface = FONT_4.render(texte, True, JAUNE)
        rect = surface.get_rect(topleft=(700, 200))
        SCREEN.blit(surface, rect)

    # ------------------------------------------------
    def afficheTourSuprimee(self,tour):

        texte="S-Supression"
        surface = FONT_4.render(texte, True, ROUGE)
        rect = surface.get_rect(topleft=(700, 500))
        SCREEN.blit(surface, rect)

        texte="+ {} €".format(int(tour.argent_depense/2))
        surface = FONT_4.render(texte, True, JAUNE)
        rect = surface.get_rect(topleft=(1020, 500))
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
            if self.etat_partie == ETAT_PARTIE_JEU:
                return BOUTON_TOURELLE_TOUS

        elif X_TOURELLE+60 < x_souris < (X_TOURELLE+40+60) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            if self.etat_partie == ETAT_PARTIE_JEU:
                return BOUTON_TOURELLE_NORMAL

        elif X_TOURELLE+120 < x_souris < (X_TOURELLE+40+120) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            if self.etat_partie == ETAT_PARTIE_JEU:
                return BOUTON_TOURELLE_BOUM

        elif X_TOURELLE+180 < x_souris < (X_TOURELLE+40+180) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            if self.etat_partie == ETAT_PARTIE_JEU:
                return BOUTON_TOURELLE_VOLANT

        elif X_TOURELLE+240 < x_souris < (X_TOURELLE+40+240) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            if self.etat_partie == ETAT_PARTIE_JEU:
                return BOUTON_TOURELLE_BOUM_VOLANT

        elif X_TOURELLE+300 < x_souris < (X_TOURELLE+40+300) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
            if self.etat_partie == ETAT_PARTIE_JEU:
                return BOUTON_TOURELLE_PLUS

        elif math.sqrt((x_souris - (900+RAYON_BOUTON_PAUSE))**2 + (y_souris - (Y_BOUTON_PLAY_PAUSE+RAYON_BOUTON_PAUSE))**2 ) <= RAYON_BOUTON_PAUSE:
            if self.etat_partie == ETAT_PARTIE_JEU:
                return BOUTON_PLUS

        elif math.sqrt((x_souris - (948+RAYON_BOUTON_PAUSE))**2 + (y_souris - (Y_BOUTON_PLAY_PAUSE+RAYON_BOUTON_PAUSE))**2 ) <= RAYON_BOUTON_PAUSE:
            if self.etat_partie == ETAT_PARTIE_JEU:
                return BOUTON_MOINS

        else:
            return None