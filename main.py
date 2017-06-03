# -*- coding: utf-8 -*-
__author__ = 'Quentin , Manu et Philippe'


from grille import *
from tour import *
from bestiole import *
from tir import *
from outils import *
from bandeauActions import *
from evenement import *

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
    listeEvenements = []
    pageAide = 0


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
            #grille.dessine_grille()
            tourBrouillon = None
            bestiole_selectionnee = None
            bandeauAction = BandeauAction()
            premiere_vague = True
            tour_type = None
            listeEvenements = []
            pageAide = 0

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
                print(event.key)
                # Q
                if event.key==97:
                    pygame.quit()
                    exit(0)

                if grille.tour_selectionnee!=None:
                    t = grille.tour_selectionnee
                    # F
                    if event.key==102:
                        argent-=t.ameliore(TOUR_AMELIORATION_FORCE,argent)
                    # D
                    if event.key==100:
                        argent-=t.ameliore(TOUR_AMELIORATION_DISTANCE,argent)
                    # C
                    if event.key==99:
                        argent-=t.ameliore(TOUR_AMELIORATION_CADENCE,argent)
                    # V
                    if event.key==118:
                        argent-=t.ameliore(TOUR_AMELIORATION_VITESSE,argent)
                    # R
                    if event.key==114:
                        argent-=t.ameliore(TOUR_AMELIORATION_RALENTI,argent)
                    # S
                    if event.key==115:
                        argent += grille.enleve_tour_selectionnee(premiere_vague)
                        grille.calcule_distance_grille()


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

        SCREEN.blit(IMAGE_FOND, (0, 0))
        grille.affiche_score(argent, premiere_vague, nombre_vie, int((DELAI_ENTRE_VAGUE - vague_attente)/20))
        bandeauAction.affiche(premiere_vague)

        # -----------------------------
        if etat_partie == ETAT_PARTIE_ACCUEIL:
            if ev_clicgauche:
                if bandeauAction.clic(x_souris,y_souris)==BOUTON_START_NEXT:
                    etat_partie = ETAT_PARTIE_JEU
            continue

        grille.dessine_grille()
        grille.dessine_portes()
        for bete in listeBestioles:
            bete.affiche()
        for tir in listeTirs:
            tir.affiche()


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
        if etat_partie == ETAT_PARTIE_AIDE:
            if ev_clicgauche:
                if bandeauAction.clic(x_souris,y_souris)==BOUTON_FLECHE_DROITE:
                    pageAide = pageAide + 1
                    #print("toto")

                if bandeauAction.clic(x_souris,y_souris)==BOUTON_FLECHE_GAUCHE:
                    pageAide = pageAide - 1

            if pageAide >= 4:
                etat_partie = ETAT_PARTIE_JEU
            elif pageAide < 0:
                etat_partie = ETAT_PARTIE_JEU

            bandeauAction.afficheExplication(pageAide)

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
                delay_entre_vague = 10000000000000000000000000000000000000000000000000

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

            ResultatBandeauActionClic = bandeauAction.clic(x_souris,y_souris)

            # Gestion des ameliorations (et supression) de la tour selctionnee
            if grille.tour_selectionnee!=None:
                t = grille.tour_selectionnee
                if ResultatBandeauActionClic==TOUCHE_F:
                    argent-=t.ameliore(TOUR_AMELIORATION_FORCE,argent)
                    continue
                elif ResultatBandeauActionClic==TOUCHE_D:
                    argent-=t.ameliore(TOUR_AMELIORATION_DISTANCE,argent)
                    continue
                elif ResultatBandeauActionClic==TOUCHE_C:
                    argent-=t.ameliore(TOUR_AMELIORATION_CADENCE,argent)
                    continue
                elif ResultatBandeauActionClic==TOUCHE_V:
                    argent-=t.ameliore(TOUR_AMELIORATION_VITESSE,argent)
                    continue
                elif ResultatBandeauActionClic==TOUCHE_R:
                    argent-=t.ameliore(TOUR_AMELIORATION_RALENTI,argent)
                    continue
                elif ResultatBandeauActionClic==TOUCHE_S:
                    argent += grille.enleve_tour_selectionnee(premiere_vague)
                    grille.calcule_distance_grille()
                    continue
                else :
                    grille.tour_selectionnee=None
                    bestiole_selectionnee=None

            # Gestion de la vitesse du jeu
            elif ResultatBandeauActionClic==BOUTON_PLUS:
                if FPS != 1560:
                    FPS = FPS + 500
            elif ResultatBandeauActionClic==BOUTON_MOINS:
                if FPS != 60:
                    FPS = FPS - 500

            # Gestion du bouton pause
            elif ResultatBandeauActionClic==BOUTON_PAUSE:
                etat_partie = ETAT_PARTIE_PAUSE
                continue

            # Gestion du bouton next
            if ResultatBandeauActionClic==BOUTON_START_NEXT:
                # TODO : gerer la dernière vague
                if vague_compteur >= TABLE_VAGUE[vague]['quantite']:
                    vague += 1
                    vague_compteur = 0
                    vague_attente = 0
                    delay_entre_vague = DELAI_ENTRE_VAGUE
                    premiere_vague = False

                tourBrouillon=None
                continue


            elif ResultatBandeauActionClic==BOUTON_AIDE:
                etat_partie = ETAT_PARTIE_AIDE
                pageAide = 0
                continue

            # Gestion du bouton tourelle
            elif ResultatBandeauActionClic==BOUTON_TOURELLE_NORMAL:
                tour_type = TOUR_NORMAL
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif ResultatBandeauActionClic==BOUTON_TOURELLE_VOLANT:
                tour_type = TOUR_VOLANT
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif ResultatBandeauActionClic==BOUTON_TOURELLE_TOUS:
                tour_type = TOUR_TOUS
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif ResultatBandeauActionClic==BOUTON_TOURELLE_BOUM:
                tour_type = TOUR_BOUM
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif ResultatBandeauActionClic==BOUTON_TOURELLE_BOUM_VOLANT:
                tour_type = TOUR_BOUM_VOLANT
                tourBrouillon = Tour(2,2, Tour._ETAT_TOUR_BROUILLON)
                continue

            elif ResultatBandeauActionClic==BOUTON_TOURELLE_PLUS:
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
                argent = argent - int(grille.nouvelle_tour_complet(i,j,listeBestioles,tour_type,argent))

        # les bestioles
        for bete in listeBestioles:
            bete.deplace(grille)
            (i,j)=conversionCoordPixelsVersCases(bete.x,bete.y)
            if i == GRILLE_LX-1:
                # une besstiole est sortie
                listeBestioles.remove(bete)
                nombre_vie -= 1
                listeEvenements.append(Evenement(bete.x-5,bete.y-5,"- 1",ROUGE))
                if nombre_vie == 0:
                    etat_partie = ETAT_PARTIE_PERDU
                continue
            if bete.vie <= 0:
                argent += TABLE_BESTIOLE[bete.type]['gain']*TABLE_VAGUE[vague]['difficultee']
                listeBestioles.remove(bete)
                if bestiole_selectionnee == bete:
                    bestiole_selectionnee=None
                #bestiole.affiche_vie(TABLE_BESTIOLE[bete.type]['gain']*TABLE_VAGUE[vague]['difficultee'])
                listeEvenements.append(Evenement(bete.x-5,bete.y-5,"+ "+str(bete.gain)))
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

        # affichage des événements
        for evenement in listeEvenements:
            if evenement.duree >0:
                evenement.affiche()
                evenement.duree = evenement.duree-1
            else:
                listeEvenements.remove(evenement)
