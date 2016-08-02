# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'

from grille import *
from tour import *
from bestiole import *
from outils import *
from tir import *


# TODO général
# - corriger les bugs
#     ne pas créer une case sur une bestiole ?
#     cases devant porte de sortie porte de sortie
# - vies  : calculer (DONE) , afficher (QUENTIN)
# - argent : calculer, afficher

# - dessiner la vie restante au dessus de chaque bestiole
# - eloigner les bestioles (trop superposées)
# - plusieurs sortes de Bestioles
# - plusieurs sortes de Tours
# - les upgrades (améliorations) de Tours
# - l'orientation des bestioles (rotations)
# - les sons

ETAT_PARTIE_ACCUEIL = 1   # on construit, pas de betes, on quitte quand on clic sur DEMARRER
ETAT_PARTIE_JEU = 2       # les betes arrivent, on construit
ETAT_PARTIE_PERDU = 4     # on fige le jeu ; on affiche la grille, les betes, et des boutons "ENCORE / QUITTER"
ETAT_PARTIE_GAGNE = 5     # on fige le jeu ; on affiche la grille, les betes, et des boutons "ENCORE / QUITTER"

if __name__=="__main__":

    etat_partie = ETAT_PARTIE_ACCUEIL
    argent = 100

    nombre_bestioles_sorties = 0

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




    while True:

        #print(argent)
        #print(len(grille.listeTours))
        #print ("etat_partie={} ; nombre_pertes={} argent={}".format(etat_partie, nombre_bestioles_sorties, argent))
        #print ("Tours : {} ; Betes : {} ;  Tirs : {}".format(len(grille.listeTours), len(listeBestioles), len(listeTirs)))

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        # pygame.time.delay(DELAY )

        souris = pygame.mouse.get_pos()
        #print(souris)
        x_souris = souris[0]
        y_souris = souris[1]
        ev_clicgauche=False
        ev_clic_droit=False

        # Les événements clavier / souris
        for event in pygame.event.get():
            #print (event)

            # un clic sur le X de fermeture de fenetre ?
            if event.type==pygame.QUIT:
                    pygame.quit()
                    exit(0)

            if event.type==pygame.KEYDOWN:
                # print(event.key)
                # Q
                if event.key==97:
                    pygame.quit()
                    exit(0)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                ev_clicgauche = True
                continue

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                ev_clic_droit = True
                continue

        SCREEN.fill(0)

        # -----------------------------
        if etat_partie == ETAT_PARTIE_ACCUEIL:
            grille.dessine_grille()
            grille.dessine_portes()
            if event.type==pygame.KEYDOWN:
                # S (start):  if event.key==115:
                etat_partie = ETAT_PARTIE_JEU
            continue

        # -----------------------------
        if etat_partie == ETAT_PARTIE_PERDU:
            grille.dessine_grille()
            grille.dessine_portes()
            for bete in listeBestioles:
                bete.affiche()
            for tir in listeTirs:
                tir.affiche()
            continue
        # -----------------------------
        # etat_partie_JEU

        grille.dessine_grille()

        # ajout de bestiole ?
        # (todo : une par une, par vague, de differentes sortes ... ; faire une methode )
        if random.randint(0,FREQUENCE_BESTIOLE) == 1:
            bestiole = Bestiole()
            listeBestioles.append(bestiole)

        # handle MOUSEBUTTONUP
        if ev_clicgauche:
            # print ("event mousebuttonup and button 1")
            (i, j) = conversionCoordPixelsVersCases(x_souris, y_souris)
            if i >= 1 and i < GRILLE_LX - 1 and j >= 1 and j < GRILLE_LY - 1:
                # assez d'argent ?
                if argent >= PRIX_TOUR:
                    # emplacement autorisé ?
                    grille2 = copy.deepcopy(grille)
                    grille2.nouvelle_tour(Tour(i, j))
                    grille2.calcule_distance_grille()
                    # verifie s'il y a des cases non calculées ?
                    grille2_ok = True
                    for i in range(GRILLE_LX):
                        for j in range (GRILLE_LY):
                            if grille2.grille[i][j]==BLOC_INCONNU:
                                grille2_ok = False
                                break
                        if grille2_ok == False:
                            break
                    if grille2_ok == True:
                        argent -= PRIX_TOUR
                        # print(argent)
                        grille=copy.deepcopy(grille2)
                        pygame.event.clear()

        if ev_clic_droit:
            (a, b) = conversionCoordPixelsVersCases(x_souris, y_souris)
            grille.enleve_tour(a, b)
            grille.calcule_distance_grille()

        else:
            (a, b) = conversionCoordPixelsVersCases(x_souris, y_souris)
            if a >= 1 and a <= GRILLE_LX-3 and b >=1 and b <= GRILLE_LY - 3:
                tourBrouillon = Tour(a, b, Tour._ETAT_TOUR_BROUILLON)
            else:
                tourBrouillon = None

        # les bestioles
        for bete in listeBestioles:
            bete.deplace(grille)
            bete.affiche()
            (i,j)=conversionCoordPixelsVersCases(bete.x,bete.y)
            if i == GRILLE_LX-1:
                # une besstiole est sortie
                listeBestioles.remove(bete)
                nombre_bestioles_sorties += 1
                if nombre_bestioles_sorties >= NOMBRE_BESTIOLES_SORTIE_MAX:
                    etat_partie = ETAT_PARTIE_PERDU
                continue
            if bete.vie <= 0:
                listeBestioles.remove(bete)
                continue

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






