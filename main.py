# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'
# 2016-07-29 11:21

from grille import *
from tour import *
from bestiole import *
from outils import *


if __name__=="__main__":

    grille = Grille()
    grille.calcule_distance_grille()
    grille.dessine_grille()

    while True:

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
                grille.nouvelle_tour(Tour(int(x_souris/20),int(y_souris/20)))
                grille.calcule_distance_grille()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                grille.enleve_tour(int(x_souris/20),int(y_souris/20))
                grille.calcule_distance_grille()

            else:
                tourBrouillon = Tour(int(x_souris/20),int(y_souris/20),Tour._ETAT_TOUR_BROUILLON)

        grille.dessine_grille()
        if tourBrouillon:
            tourBrouillon.affiche()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


