# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'

from grille import *
from tour import *
from bestiole import *
from outils import *
from tir import *


# TODO général
# - plusieurs sortes de Tours
# - plusieurs sortes de Bestioles
# - les Tirs
# - les upgrades (améliorations) de Tours
# - corriger les bugs de case qui plantent (porte, hors grille, labyrinthe fermé, ...)
# - gestion de l'argent
# - gestion de partie : debut, séries de bestioles
# - score / vies
# - l'orientation des bestioles (rotations)
# - les sons


if __name__=="__main__":

    grille = Grille()
    listeBestioles = []
    listeTirs = []

    csv = 0
    # TODO : mettre le chargement csv, dans une methode de grille()  [ou outil à voir]
    if csv == 1:
        fichierDefBlocs = csv.reader(open(FICHIER_DEF_BLOCS,"r"),delimiter=';')
        numLigne = 0
        for ligne in fichierDefBlocs:
            for i in range(0,len(ligne)):
                valeur = int(ligne[i])
                if valeur == 1:
                    grille.nouvelle_tour(Tour(i+1,numLigne+1))
            numLigne += 1

    grille.calcule_distance_grille()
    grille.dessine_grille()

    for i in range(5):
        bestiole = Bestiole()
        listeBestioles.append(bestiole)
        #bestiole = Bestiole()
        listeBestioles.append(bestiole)

    #listeTirs = []
    # listeTirs.append(Tir(x=300,y=100))
    # from outils

    while True:

        # Les événements clavier / souris
        for event in pygame.event.get():
            #print (event)

            # un clic sur le X de fermeture de fenetre ?
            if event.type==pygame.QUIT:
                    pygame.quit()
                    exit(0)

            if event.type==pygame.KEYDOWN:
                #print(event.key)
                # Q
                if event.key==97:
                    pygame.quit()
                    exit(0)

            souris = pygame.mouse.get_pos()
            #print(souris)
            x_souris = souris[0]
            y_souris = souris[1]

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                (a,b)=conversionCoordPixelsVersCases(x_souris,y_souris)
                grille.nouvelle_tour(Tour(a,b))
                grille.calcule_distance_grille()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                (a,b)=conversionCoordPixelsVersCases(x_souris,y_souris)
                grille.enleve_tour(a,b)
                grille.calcule_distance_grille()

            else:
                (a,b)=conversionCoordPixelsVersCases(x_souris,y_souris)
                tourBrouillon = Tour(a,b,Tour._ETAT_TOUR_BROUILLON)

        SCREEN.fill(0)

        grille.dessine_grille()

        # les bestioles
        for i in range(len(listeBestioles)):
            listeBestioles[i].deplace(grille)
            listeBestioles[i].affiche()

        # gestion des tours
        for i in range(len(grille.listeTours)):
            grille.listeTours[i].gere_construction()
            grille.listeTours[i].gere_deconstruction()
            t=grille.listeTours[i].cree_tir(listeBestioles)
            if t is not None :
                listeTirs.append(t)

        # les tirs
        for i in range(len(listeTirs)):
            listeTirs[i].deplace(grille)
            listeTirs[i].verifie_impact()
            listeTirs[i].affiche()

        # le curseur / tour en construction
        if tourBrouillon:
            tourBrouillon.affiche()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        # pygame.time.delay(DELAY )




