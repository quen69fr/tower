# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'


from grille import *
from tour import *
from bestiole import *
from tir import *
from outils import *



# TODO général
# - corriger les bugs
#     bug cases devant porte de sortie ne se déconstruit pas
#     bug obstruction totale de la porte d'entrée par 2 tours
# - dessiner la vie restante au dessus de chaque bestiole
# - eloigner les bestioles (trop superposées)
# - plusieurs sortes de Tours
# - les upgrades (améliorations) de Tours
# - l'orientation des bestioles (rotations)
# - les sons


if __name__=="__main__":

    vague = 0
    vague_compteur= 0 # nombre de betes deja envoyees dans la vague en cours
    vague_attente = 0 # attente entre deux vagues

    etat_partie = ETAT_PARTIE_ACCUEIL
    argent = 100

    nombre_vie = NOMBRE_BESTIOLES_SORTIE_MAX

    grille = Grille()
    listeBestioles = []
    listeTirs = []

    grille.charge_csv()
    grille.calcule_distance_grille()
    grille.dessine_grille()

    tourBrouillon = None

    while True:

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
                #print(event.key)
                # Q
                if event.key==97:
                    pygame.quit()
                    exit(0)

                # S
                if event.key==115:
                    grille.enleve_tour_selectionnee()
                    grille.calcule_distance_grille()
                    argent += int(PRIX_TOUR/2)


                # U
                if event.key==117:
                    pass

                # N
                if event.key==110:
                    if vague_compteur < TABLE_VAGUE[vague]['quantite']:
                        pass
                    else:
                        vague += 1
                        vague_compteur = 0
                        vague_attente = 0

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
            afficheAccueil(etat_partie)

            if event.type==pygame.MOUSEBUTTONUP:
                if X_START_NEXT < x_souris < (X_START_NEXT+155) and Y_START_NEXT < y_souris < (Y_START_NEXT+53):
                    etat_partie = ETAT_PARTIE_JEU
            continue
        # -----------------------------
        if etat_partie == ETAT_PARTIE_PERDU:
            grille.dessine_grille()
            grille.dessine_portes()
            afficheAccueil(etat_partie)

            for bete in listeBestioles:
                bete.affiche()
            for tir in listeTirs:
                tir.affiche()
            texte="Perdu"
            surface = FONT_3.render(texte, True, ROUGE)
            rect = surface.get_rect(topleft=(MARGE_ECRAN+200, 200))
            SCREEN.blit(surface, rect)

            '''if event.type==pygame.MOUSEBUTTONUP:
                if X_START_NEXT < x_souris < (X_START_NEXT+155) and Y_START_NEXT < y_souris < (Y_START_NEXT+53):
                    etat_partie = ETAT_PARTIE_JEU
                    TODO il faut tout remêtre à 0.'''


            continue
        # -----------------------------
        # etat_partie_JEU
        # -----------------------------

        grille.dessine_grille()
        grille.affiche_score(argent, nombre_vie, int((DELAI_ENTRE_VAGUE - vague_attente)/20))

        # Algo d'envoi des bestioles et vagues
        # une vague à la fois , on tire au hasard l'entrée de chaque bete de la vague
        # quand la vague est complete, on attend un peu
        # et on passe à la vague d'apres s'il en reste

        # print ('Vague {} ; compteur {} ; attente {}'.format(vague,vague_compteur, vague_attente))

        # vague en cours finie ?
        if vague_compteur < TABLE_VAGUE[vague]['quantite']:
            # non, il faut envoyer une nouvelle bestiole de la vague en cours
            if TABLE_VAGUE[vague]['type'] == 'groupe' or TABLE_VAGUE[vague]['type'] == 'boss_groupe':
                    t=TABLE_VAGUE[vague]['type']
                    bestiole = Bestiole(vague,type=t)
                    listeBestioles.append(bestiole)
                    vague_compteur += 1

            else:
                if random.randint(0,INTERVALLE_BESTIOLE) == 1:
                    t=TABLE_VAGUE[vague]['type']
                    bestiole = Bestiole(vague,type=t)
                    listeBestioles.append(bestiole)
                    vague_compteur += 1
        else:
            # oui la vague est finie,
            # j'attends ?
            if vague_attente < DELAI_ENTRE_VAGUE:
                # oui
                vague_attente += 1
            else:
                # non, je change de vague s'il y a encore des vagues à envoyer
                if vague < len(TABLE_VAGUE)-1:
                    vague += 1
                    vague_compteur = 0
                    vague_attente = 0

        # clic-gauche - handle MOUSEBUTTONUP
        if ev_clicgauche:

            (i, j) = conversionCoordPixelsVersCases(x_souris, y_souris)
            # chercher sur quoi on a cliqué : bouton, tour, case vide, bestiole
            CIBLE_CLIC, CIBLE_OBJET = grille.cherche_cible_clic(i,j,listeBestioles)
            #print ("CIBLE_CLIC = ",CIBLE_CLIC)

            # construction sur case vide 4 ?
            if tourBrouillon:
                if CIBLE_CLIC == 'vide4':
                     if argent >= PRIX_TOUR:
                        if grille.nouvelle_tour_complet(i,j):
                            argent -= PRIX_TOUR
                else:
                    tourBrouillon = None

            # selection d'un bouton Tour
            # TODO : gerer les differents boutons
            if CIBLE_CLIC == 'menu':
                if X_START_NEXT < x_souris < (X_START_NEXT+155) and Y_START_NEXT < y_souris < (Y_START_NEXT+53):
                    if vague_compteur < TABLE_VAGUE[vague]['quantite']:
                        pass
                    else:
                        vague += 1
                        vague_compteur = 0
                        vague_attente = 0

                if X_TOURELLE < x_souris < (X_TOURELLE+40) and Y_TOURELLE < y_souris < (Y_TOURELLE+40):
                    tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
        # si clic-sur menu / bouton de tour, tour Brouillon :
        #

        if ev_clic_droit:
            pass


        # les bestioles
        for bete in listeBestioles:
            bete.deplace(grille)
            bete.affiche()
            (i,j)=conversionCoordPixelsVersCases(bete.x,bete.y)
            if i == GRILLE_LX-1:
                # une besstiole est sortie
                listeBestioles.remove(bete)
                nombre_vie -= 1
                if nombre_vie == 0:
                    etat_partie = ETAT_PARTIE_PERDU
                continue
            if bete.vie <= 0:
                argent += TABLE_BESTIOLE[bete.type]['gain']*TABLE_VAGUE[vague]['difficultee']
                listeBestioles.remove(bete)
                #bestiole.affiche_vie(TABLE_BESTIOLE[bete.type]['gain']*TABLE_VAGUE[vague]['difficultee'])
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
            (i, j) = conversionCoordPixelsVersCases(x_souris, y_souris)
            tourBrouillon.x = i
            tourBrouillon.y = j
            tourBrouillon.affiche()

        grille.dessine_portes()
        afficheAccueil(etat_partie)