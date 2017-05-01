# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'


from grille import *
from tour import *
from bestiole import *
from tir import *
from outils import *
from bandeauActions import *

# TODO BUG : le perimetre  de tir des tours a disparu quand on construit ; Phil - 26aout
# TODO BUG : on aperçoit les bestioles avant la porte
# TODO BUG : on ne peut pas lancer plusieurs vagues rapidement (il faut attendre la fin de sortie de la vague précédente)

# TODO : plusieurs sortes de Tours ou d'upgrade
# TODO : améliorer les graphiques (taille, contraste)
# TODO : on ne peut pas constuire avant de faire start (et envoi des bestioles)
# TODO : eloigner les bestioles (trop superposées)
# TODO : les sons
# TODO : une classe MenuBoutons (qui affiche, vérifie ce qui est cliqué, etc.)
# TODO : sortie les TABLE_VAGUE et TABLE_BESTIOLES dans un format json
# TODO :  afficher le copyright et noms des développeurs

if __name__=="__main__":

    vague = 0
    vague_compteur= 0 # nombre de betes deja envoyees dans la vague en cours
    vague_attente = 0 # attente entre deux vagues
    etat_partie = None
    argent = 0
    nombre_vie = 0
    grille = None
    listeBestioles = []
    listeTirs = []
    tourBrouillon = None
    bestiole_selectionnee = None
    bandeauAction = None
    premiere_vague = True
    tour_type = None


    while True:

        # On initialise la partie si pas de partie en cours
        if etat_partie==None:
            vague = 0
            vague_compteur= 0 # nombre de betes deja envoyees dans la vague en cours
            vague_attente = 0 # attente entre deux vagues
            etat_partie = ETAT_PARTIE_ACCUEIL
            argent = ARGENT_DEPART
            nombre_vie = NOMBRE_BESTIOLES_SORTIE_MAX
            grille = Grille()
            listeBestioles = []
            listeTirs = []
            grille.charge_csv()
            grille.calcule_distance_grille()
            grille.dessine_grille()
            tourBrouillon = None
            bestiole_selectionnee = None
            bandeauAction = BandeauAction()
            premiere_vague = True
            tour_type = None


        bandeauAction.mise_jour_etat(etat_partie,grille.tour_selectionnee,bestiole_selectionnee,argent)
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
                    if grille.enleve_tour_selectionnee():
                        argent += int(PRIX_TOUR/2)
                    grille.calcule_distance_grille()

                if grille.tour_selectionnee!=None:
                    t = grille.tour_selectionnee
                    # F
                    if event.key==102:
                        if t.niveau_force<len(TABLE_TOUR_FORCE)-1:
                            prix = TABLE_TOUR_FORCE_PRIX[t.niveau_force] + prixSuplementaire(t)
                            if argent>=prix:
                                if t.ameliore(TOUR_AMELIORATION_FORCE):
                                    argent-=prix
                    # D
                    if event.key==100:
                        if t.niveau_distance<len(TABLE_TOUR_DISTANCE)-1:
                            prix = TABLE_TOUR_DISTANCE_PRIX[t.niveau_distance] + prixSuplementaire(t)
                            if argent>=prix:
                                if t.ameliore(TOUR_AMELIORATION_DISTANCE):
                                    argent-=prix
                    # R
                    if event.key==114:
                        if t.niveau_rapidite<len(TABLE_TOUR_RAPIDITE)-1:
                            prix = TABLE_TOUR_RAPIDITE_PRIX[t.niveau_rapidite] + prixSuplementaire(t)
                            if argent>=prix:
                                if t.ameliore(TOUR_AMELIORATION_RAPIDITE):
                                    argent-=prix
                    # V
                    if event.key==118:
                        if t.niveau_vitesse<len(TABLE_TOUR_VITESSE)-1:
                            prix = TABLE_TOUR_VITESSE_PRIX[t.niveau_vitesse] + prixSuplementaire(t)
                            if argent>=prix:
                                if t.ameliore(TOUR_AMELIORATION_VITESSE):
                                    argent-=prix

                    # L
                    if event.key==108:
                        if t.niveau_ralentire<len(TABLE_TOUR_RALENTI_DUREE)-1:
                            prix = TABLE_TOUR_RALENTI_PRIX[t.niveau_ralentire] + prixSuplementaire(t)
                            if argent>=prix:
                                if t.ameliore(TOUR_AMELIORATION_RALENTI):
                                    argent-=prix


                # N
                if event.key==110:
                    if vague_compteur < TABLE_VAGUE[vague]['quantite']:
                        pass
                    else:
                        vague += 1
                        vague_compteur = 0
                        vague_attente = 0
                        delay_entre_vague = DELAI_ENTRE_VAGUE
                        premiere_vague = False

                # P
                if event.key==112:
                    if etat_partie == ETAT_PARTIE_PAUSE:
                        etat_partie = ETAT_PARTIE_JEU
                    elif etat_partie == ETAT_PARTIE_JEU:
                        etat_partie = ETAT_PARTIE_PAUSE
                    else:
                        pass

            #===========================================================
            # Click sur le bouton gauche
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                ev_clicgauche = True
                continue

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                ev_clic_droit = True
                continue

        SCREEN.fill(0)
        grille.dessine_grille()
        grille.affiche_score(argent, premiere_vague, nombre_vie, int((DELAI_ENTRE_VAGUE - vague_attente)/20))
        grille.dessine_portes()
        bandeauAction.affiche()
        for bete in listeBestioles:
            bete.affiche()
        for tir in listeTirs:
            tir.affiche()

        # -----------------------------
        if etat_partie == ETAT_PARTIE_ACCUEIL:
            if ev_clicgauche:
                if bandeauAction.clic(x_souris,y_souris)==BOUTON_START_NEXT:
                    etat_partie = ETAT_PARTIE_JEU
            continue

        # -----------------------------
        if etat_partie == ETAT_PARTIE_PERDU or etat_partie == ETAT_PARTIE_GAGNE:

            if etat_partie == ETAT_PARTIE_PERDU:
                texte="Perdu"
                surface = FONT_3.render(texte, True, ROUGE)
                rect = surface.get_rect(topleft=(MARGE_ECRAN+200, 260))
                SCREEN.blit(surface, rect)

            if etat_partie == ETAT_PARTIE_GAGNE:
                texte="Gagné"
                surface = FONT_3.render(texte, True, VERT)
                rect = surface.get_rect(topleft=(MARGE_ECRAN+200, 260))
                SCREEN.blit(surface, rect)

            if ev_clicgauche:
                if bandeauAction.clic(x_souris,y_souris)==BOUTON_START_NEXT:
                    etat_partie = None
            continue

        # -----------------------------
        if etat_partie == ETAT_PARTIE_PAUSE:

            # Click gauche : on regarde si on doit enlever la pause
            #==============================================================
            if ev_clicgauche:

                if bandeauAction.clic(x_souris,y_souris)==BOUTON_PAUSE:
                    etat_partie = ETAT_PARTIE_JEU

            texte="Pause"
            surface = FONT_3.render(texte, True, ROUGE)
            rect = surface.get_rect(topleft=(MARGE_ECRAN+200, 260))
            SCREEN.blit(surface, rect)

            continue
        # -----------------------------
        # etat_partie_JEU
        # -----------------------------

        # Algo d'envoi des bestioles et vagues
        # une vague à la fois , on tire au hasard l'entrée de chaque bete de la vague
        # quand la vague est complete, on attend un peu
        # et on passe à la vague d'apres s'il en reste

        # print ('Vague {} ; compteur {} ; attente {}'.format(vague,vague_compteur, vague_attente))

        # vague en cours finie ?
        if vague == len(TABLE_VAGUE)-1:
            etat_partie = ETAT_PARTIE_GAGNE
            continue

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
            if premiere_vague == True:
                delay_entre_vague = 1000000000000000

            if vague_attente < delay_entre_vague:
                # oui
                vague_attente += 1
            else:
                # non, je change de vague s'il y a encore des vagues à envoyer
                if vague < len(TABLE_VAGUE)-1:
                    vague += 1
                    vague_compteur = 0
                    vague_attente = 0
                    delay_entre_vague = DELAI_ENTRE_VAGUE
                    premiere_vague = False

        # clic-gauche - handle MOUSEBUTTONUP
        if ev_clicgauche:

            bestiole_selectionnee=None
            grille.tour_selectionnee=None

            if bandeauAction.clic(x_souris,y_souris)==BOUTON_PLUS:
                if FPS != 1560:
                    FPS = FPS + 500

            if bandeauAction.clic(x_souris,y_souris)==BOUTON_MOINS:
                if FPS != 60:
                    FPS = FPS - 500

            # Gestion du bouton pause
            if bandeauAction.clic(x_souris,y_souris)==BOUTON_PAUSE:
                etat_partie = ETAT_PARTIE_PAUSE
                continue

            # Gestion du bouton next
            if bandeauAction.clic(x_souris,y_souris)==BOUTON_START_NEXT:
                # TODO : gerer la dernière vague
                if vague_compteur >= TABLE_VAGUE[vague]['quantite']:
                    vague += 1
                    vague_compteur = 0
                    vague_attente = 0
                    delay_entre_vague = DELAI_ENTRE_VAGUE
                    premiere_vague = False

                tourBrouillon=None
                continue

            # Gestion du bouton tourelle
            if bandeauAction.clic(x_souris,y_souris)==BOUTON_TOURELLE_NORMAL:
                tour_type = TOUR_NORMAL
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif bandeauAction.clic(x_souris,y_souris)==BOUTON_TOURELLE_VOLANT:
                tour_type = TOUR_VOLANT
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif bandeauAction.clic(x_souris,y_souris)==BOUTON_TOURELLE_TOUS:
                tour_type = TOUR_TOUS
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif bandeauAction.clic(x_souris,y_souris)==BOUTON_TOURELLE_BOUM:
                tour_type = TOUR_BOUM
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif bandeauAction.clic(x_souris,y_souris)==BOUTON_TOURELLE_BOUM_VOLANT:
                tour_type = TOUR_BOUM_VOLANT
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif bandeauAction.clic(x_souris,y_souris)==BOUTON_TOURELLE_PLUS:
                tour_type = TOUR_PLUS
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue



            # Gestion du clic sur une bestiole
            for bete in listeBestioles:
                if bete.clic(x_souris,y_souris):
                    bestiole_selectionnee = bete
                    tourBrouillon=None
                    continue

            # Gestion du clic sur une tour existante
            (i, j) = conversionCoordPixelsVersCases(x_souris, y_souris)
            tour = grille.quelle_tour_dans_case(i,j)
            if tour:
                grille.tour_selectionnee=tour
                tourBrouillon = None
                continue

            # Gestion de la construction d'une nouvelle tour
            if tourBrouillon and grille.caseVide4(i,j):
                if argent >= PRIX_TOUR:
                    if grille.nouvelle_tour_complet(i,j,listeBestioles,tour_type):
                        argent -= PRIX_TOUR
                else:
                    tourBrouillon = None


        # les bestioles
        for bete in listeBestioles:
            bete.deplace(grille)
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
                if bestiole_selectionnee == bete:
                    bestiole_selectionnee=None
                #bestiole.affiche_vie(TABLE_BESTIOLE[bete.type]['gain']*TABLE_VAGUE[vague]['difficultee'])
                continue

        # gestion des tours
        for tour in grille.listeTours:
            tour.gere_construction()
            tour.gere_deconstruction()
            t=tour.cree_tir(listeBestioles)
            if t is not None :
                listeTirs.extend(t)

        # les tirs
        for tir in listeTirs:
            tir.deplace()
            if tir.impact == True:
                tir.traite_impact()
                listeTirs.remove(tir)

        # le curseur / tour en construction
        if tourBrouillon:
            (i, j) = conversionCoordPixelsVersCases(x_souris, y_souris)
            tourBrouillon.x = i
            tourBrouillon.y = j
            if grille.estDansGrille(i,j):
                if grille.caseVide4(i,j):
                    tourBrouillon.etat=tourBrouillon._ETAT_TOUR_BROUILLON
                else:
                    tourBrouillon.etat=tourBrouillon._ETAT_TOUR_BROUILLON_IMPOSSIBLE
                tourBrouillon.affiche()