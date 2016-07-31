# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'

from grille import *
from tour import *
from bestiole import *
from outils import *


if __name__=="__main__":

    grille = Grille()

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

    listeBestioles = []
    for i in range(10):
            bestiole = Bestiole()
            listeBestioles.append(bestiole)

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

        grille.dessine_grille()
        for i in range(len(listeBestioles)):
            listeBestioles[i].deplace(grille)
            listeBestioles[i].affiche()

        if tourBrouillon:
            tourBrouillon.affiche()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


