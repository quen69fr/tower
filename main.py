# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'


from grille import *
from tour import *
from bestiole import *
from tir import *
from outils import *



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

    vague=0
    vague_compteur=0  # nombre de betes deja envoyees dans la vague en cours
    vague_attente = 0 # attente entre deux vagues

    etat_partie = ETAT_PARTIE_ACCUEIL
    argent = 100

    nombre_vie = NOMBRE_BESTIOLES_SORTIE_MAX

    grille = Grille()
    listeBestioles = []
    listeTirs = []

    # TODO : mettre le chargement csv, dans une methode de grille()
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
            texte="Une touche pour commencer ..."
            surface = FONT.render(texte, True, BLANC)
            rect = surface.get_rect(topleft=(180, 220))
            SCREEN.blit(surface, rect)
            if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONUP:
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
        grille.affiche_score(argent, nombre_vie, vague)

        # Algo d'envoi des bestioles et vagues
        # une vague à la fois , on tire au hasard l'entrée de chaque bete de la vague
        # quand la vague est complete, on attend un peu
        # et on passe à la vague d'apres s'il en reste

        # print ('Vague {} ; compteur {} ; attente {}'.format(vague,vague_compteur, vague_attente))

        # vague en cours finie ?
        if vague_compteur < TABLE_VAGUE[vague]['quantite']:
            # non, il faut envoyer une nouvelle bestiole de la vague en cours
            if random.randint(0,INTERVALLE_BESTIOLE) == 1:
                t=TABLE_VAGUE[vague]['type']
                bestiole = Bestiole(type=t) # TODO : mettre ici les caractéristiques de la bete à créer
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



        # handle MOUSEBUTTONUP
        if ev_clicgauche:
            # chercher sur quoi on a cliqué : bouton, tour, case vide, bestiole
            CIBLE_CLIC = 0
            CIBLE_TOUR = None
            CIBLE_BETE = None
            CIBLE_BOUTON = None
            (i, j) = conversionCoordPixelsVersCases(x_souris, y_souris)
            if i >= 1 and i < GRILLE_LX - 1 and j >= 1 and j < GRILLE_LY - 1:
                # une bestiole ?
                for bete in listeBestioles:
                    if bete.verifie_bestiole_dans_case(i,j):
                        CIBLE_CLIC='bete'
                        CIBLE_BETE = bete
                        print("BETE CLIQUEE")
                        break
                if CIBLE_CLIC == 0:
                    # sinon une tour ?
                    if grille.grille[i][j] == BLOC_TOUR:
                        CIBLE_CLIC = 'tour'
                        CIBLE_TOUR = grille.quelle_tour_dans_case(i,j)
                        print("cible tour : ",CIBLE_TOUR)
                    # sinon une case vide
                    elif grille.grille[i][j]>=0:
                        CIBLE_CLIC = 'grille_vide'
                    else:
                        CIBLE_CLIC = 'autre'
            else:
                # CIBLE_CLIC = 'menu'
                # CIBLE_BOUTON = .......Menu.verifie_clic()
                CIBLE_CLIC='autre'

            print ("CIBLE_CLIC = ",CIBLE_CLIC)





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

        else:
            (a, b) = conversionCoordPixelsVersCases(x_souris, y_souris)
            if a >= 1 and a <= GRILLE_LX-3 and b >=1 and b <= GRILLE_LY - 3:
                tourBrouillon = Tour(a, b, Tour._ETAT_TOUR_BROUILLON)
            else:
                tourBrouillon = None

        if ev_clic_droit:
            (a, b) = conversionCoordPixelsVersCases(x_souris, y_souris)
            if grille.grille[a][b] == BLOC_TOUR and grille.grille[a+1][b] == BLOC_TOUR and grille.grille[a][b+1] == BLOC_TOUR and grille.grille[a+1][b+1] == BLOC_TOUR:
                grille.enleve_tour(a, b)
                grille.calcule_distance_grille()
                argent += int(PRIX_TOUR/2)

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
                argent += TABLE_BESTIOLE[bete.type]['gain']
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






