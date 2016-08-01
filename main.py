# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'

from grille import *
from tour import *
from bestiole import *
from outils import *
from tir import *


# TODO général
# - DONE - les Tirs
# - DONE mort des bestioles
# - corriger les bugs
#     affichage tour construction hors grille (TODO => Quentin)
#     case fermée
#     ne pas créer une case sur une bestiole
#     DONE - porte de sortie
#     DONE - fermeture porte d'entrée
#     DONE - clic hors grille
# - gestion de partie : debut, séries de bestioles
# - score / vies

# - eloigner les bestioles (trop superposées)
# - faire tourner les yeux des bestioles
# - gestion de l'argent
# - plusieurs sortes de Bestioles
# - plusieurs sortes de Tours
# - les upgrades (améliorations) de Tours
# - l'orientation des bestioles (rotations)
# - les sons


if __name__=="__main__":

    grille = Grille()
    listeBestioles = []
    listeTirs = []

    # TODO : mettre le chargement csv, dans une methode de grille()  [ou outil à voir]
    if AFFICHE_CSV:
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

    for i in range(NOMBRE_BESTIOLE):
        bestiole = Bestiole()
        listeBestioles.append(bestiole)


    while True:

        #print ("Tours : {} ; Betes : {} ;  Tirs : {}".format(len(grille.listeTours), len(listeBestioles), len(listeTirs)))

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
                (i,j)=conversionCoordPixelsVersCases(x_souris,y_souris)
                if i >= 1 and i < GRILLE_LX-1 and j >= 1 and j < GRILLE_LY-1:
                    grille.nouvelle_tour(Tour(i,j))
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
        for bete in listeBestioles:
            bete.deplace(grille)
            bete.affiche()
            (i,j)=conversionCoordPixelsVersCases(bete.x,bete.y)
            if i == GRILLE_LX-1:
                listeBestioles.remove(bete)
                next
            if bete.vie <= 0:
                listeBestioles.remove(bete)
                next
        # gestion des tours
        for tour in grille.listeTours:
            tour.gere_construction()
            tour.gere_deconstruction()
            t=tour.cree_tir(listeBestioles)
            if t is not None :
                listeTirs.append(t)

        # les tirs
        for tir in listeTirs:
            tir.deplace(grille)
            if tir.impact == True:
                tir.traite_impact()
                listeTirs.remove(tir)
                next
            tir.affiche()

        # le curseur / tour en construction
        if tourBrouillon:
            tourBrouillon.affiche()

        grille.dessine_portes()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        # pygame.time.delay(DELAY )




