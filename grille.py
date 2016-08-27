# tour.py
# coding: utf-8

__author__ = 'Quentin'

from tour import *
from outils import *
from bestiole import *

class Grille():

    def __init__(self):

        self.grille=[]
        self.listeTours = []
        self.grille = [[BLOC_INCONNU for j in range(GRILLE_LY)] for i in range(GRILLE_LX)]
        self.tour_selectionnee = None

        for i in range(GRILLE_LX):
            self.grille[i][0]=BLOC_BORD
            self.grille[i][GRILLE_LY-1]=BLOC_BORD

        for j in range(GRILLE_LY):
            self.grille[1][j]=BLOC_BORD
            self.grille[GRILLE_LX-2][j]=BLOC_BORD

        for j in range(GRILLE_LY):
            self.grille[0][j]=BLOC_BORD_NOIR
            self.grille[GRILLE_LX-1][j]=BLOC_BORD_NOIR

        for k in range(0,TAILLE_PORTE):
            self.grille[0][Y_PORTE+k]=BLOC_ENTREE
            self.grille[GRILLE_LX-1][Y_PORTE+k]=BLOC_PORTE

            self.grille[1][Y_PORTE+k]=BLOC_INCONNU
            self.grille[GRILLE_LX-2][Y_PORTE+k]=BLOC_INCONNU

    # ------------------------------------------------
    def cherche_cible_clic(self, i,j, listeBestioles):
        '''
        Cherche et renvoie l'objet cliqué à la souris dans le jeu
        :param i,j:  case cliquée
        :param listeBestioles:
        :return: cible_clic (vide, vide4, inconnu, menu, bete, tour) et cible_objet (objet cliqué, bete, tour)
        '''
        self.listeBestioles = listeBestioles
        cible_clic = 0
        cible_objet = None
        self.tour_selectionnee = None

        if i >= 1 and i < GRILLE_LX - 1 and j >= 1 and j < GRILLE_LY - 1:
            # une bestiole ? (en premier, donc permet d'éviter aussi de construire une tour sur une case avec bete)
            for bete in listeBestioles:
                if bete.verifie_bestiole_dans_case(i,j):
                    cible_clic='bete'

                    cible_objet = bete
                    #print("BETE CLIQUEE", cible_objet)
                    return cible_clic, cible_objet
            # sinon une tour ?
            if self.grille[i][j] == BLOC_TOUR:
                cible_clic = 'tour'
                cible_objet = self.quelle_tour_dans_case(i,j)

                #print("cible tour : ",cible_objet)

                self.tour_selectionnee = cible_objet

                return cible_clic, cible_objet

            # sinon une case vide
            elif self.grille[i][j]>=0:
                # vide sur les 4 ?
                if self.grille[i+1][j]>0 and self.grille[i+1][j+1]>0 and self.grille[i][j+1]>0:
                    cible_clic = 'vide4'
                else:
                    cible_clic = 'vide'
                return cible_clic, cible_objet
            else:
                cible_clic = 'inconnu'
        else:
            cible_clic = 'menu'
            # CIBLE_BOUTON = .......Menu.verifie_clic()
            # cible_clic='autre'
        return cible_clic, cible_objet

    # ------------------------------------------------
    def reset_distance_grille(self):
        for x in range(0,GRILLE_LX):
            for y in range(0,GRILLE_LY):
                if self.grille[x][y] != BLOC_BORD \
                        and self.grille[x][y] != BLOC_PORTE \
                        and self.grille[x][y] != BLOC_ENTREE \
                        and self.grille[x][y] != BLOC_BORD_NOIR \
                        and self.grille[x][y] != BLOC_TOUR:
                    self.grille[x][y] = BLOC_INCONNU

    # ------------------------------------------------
    def nouvelle_tour_complet(self,i,j):
        '''
        :return: True / False selon réussite
        '''
        t=Tour(i,j)

        self.listeTours.append(t)
        self.grille[i][j]=BLOC_TOUR
        self.grille[i+1][j]=BLOC_TOUR
        self.grille[i][j+1]=BLOC_TOUR
        self.grille[i+1][j+1]=BLOC_TOUR

        self.calcule_distance_grille()
        # verifie s'il y a des cases non calculées ?

        for k in range(GRILLE_LX):
            for l in range (GRILLE_LY):
                if self.grille[k][l]==BLOC_INCONNU:
                    for bete in self.listeBestioles:
                        if bete.verifie_bestiole_dans_case(k,l,False):
                            self.enleve_tour(i,j)
                            self.calcule_distance_grille()
                            return False

        for k in range(0,TAILLE_PORTE):
            if self.grille[1][Y_PORTE+k] == BLOC_INCONNU or self.grille[GRILLE_LX-2][Y_PORTE+k] == BLOC_INCONNU:
                self.enleve_tour(i,j)
                self.calcule_distance_grille()
                return False


        return True

    # ------------------------------------------------
    def enleve_tour_selectionnee(self):

        if self.tour_selectionnee == None:
            pass

        else:
            t=self.tour_selectionnee

            self.listeTours.remove(t)
            self.grille[t.x][t.y]=BLOC_INCONNU
            self.grille[t.x+1][t.y]=BLOC_INCONNU
            self.grille[t.x][t.y+1]=BLOC_INCONNU
            self.grille[t.x+1][t.y+1]=BLOC_INCONNU


    # ------------------------------------------------
    def enleve_tour(self,x,y):
        for t in self.listeTours:
            if t.x == x and t.y == y:
                self.listeTours.remove(t)
                self.grille[x][y]=BLOC_INCONNU
                self.grille[x+1][y]=BLOC_INCONNU
                self.grille[x][y+1]=BLOC_INCONNU
                self.grille[x+1][y+1]=BLOC_INCONNU
                break

    # ------------------------------------------------
    def affiche_grille(self):
        # log "------------------"
        for j in range(GRILLE_LY):
            print (j, ':',)
            for i in range(GRILLE_LX):
                print(self.grille[i][j],)
            print ("")

    # ------------------------------------------------
    def affiche_score(self,argent,nombre_vie,vague_compteur):

        texte="Argent : {} €".format(argent)
        surface = FONT.render(texte, True, JAUNE)
        rect = surface.get_rect(topleft=(MARGE_ECRAN+425, 10))
        SCREEN.blit(surface, rect)

        texte="Nombre de vies : {}".format(nombre_vie)
        surface = FONT.render(texte, True, BLANC)
        rect = surface.get_rect(topleft=(MARGE_ECRAN+20, 10))
        SCREEN.blit(surface, rect)

        texte="Vagues : {:02d}".format(vague_compteur)
        surface = FONT.render(texte, True, BLEU)
        rect = surface.get_rect(topleft=(MARGE_ECRAN+260, 10))
        SCREEN.blit(surface, rect)
        pass

    # ------------------------------------------------
    def dessine_grille(self):
        # SCREEN.fill(0)

        # les cases distances
        for j in range(GRILLE_LY):
            for i in range(GRILLE_LX):
                v=self.grille[i][j]
                # dessiner un rectangle en x,y de couleur v
                c=NOIR

                if v == BLOC_BORD:
                    c=BLEU

                if v == BLOC_BORD_NOIR:
                    c=NOIR

                #if v == BLOC_ENTREE:
                #    c=BLANC
                if v == BLOC_INCONNU:
                    c=ROUGE

                if v > 0:
                    nuance = v*3
                    if nuance > 255:
                        nuance = 255
                    c = (nuance,nuance,nuance)
                (x,y) = conversionCoordCasesVersPixels(i,j)
                # pygame.draw.rect(SCREEN, c, (x,y,TAILLE_BLOC,TAILLE_BLOC),0)
                pygame.draw.rect(SCREEN, c, (x, y, TAILLE_BLOC, TAILLE_BLOC), 0)

        # les tours
        for tour in self.listeTours:
            #tour.affiche()
            if tour == self.tour_selectionnee:
                tourSelectionnee = True
                tour.affiche(tourSelectionnee)
            else:
                tourSelectionnee = False
                tour.affiche(tourSelectionnee)

    # ------------------------------------------------
    def dessine_portes(self):

        for j in range(GRILLE_LY):

            if self.grille[GRILLE_LX-1][j] == BLOC_PORTE:
                (x, y) = conversionCoordCasesVersPixels(GRILLE_LX-1, j)
                pygame.draw.rect(SCREEN, NOIR, (x, y, TAILLE_BLOC, TAILLE_BLOC), 0)

            if self.grille[0][j] == BLOC_ENTREE:
                (x, y) = conversionCoordCasesVersPixels(0, j)
                pygame.draw.rect(SCREEN, NOIR, (x, y, TAILLE_BLOC, TAILLE_BLOC), 0)

    # ------------------------------------------------
    def calcule_distance(self,x,y):

        # TODO BUG si case de départ occupée par un bloc

        #log "Calcul ",x,y
        #self.dessine_grille()

        # il faut récupérer les 4 valeurs autour
        vg = self.grille[x-1][y]
        vd = self.grille[x+1][y]
        vh = self.grille[x][y-1]
        vb = self.grille[x][y+1]
        vhg = self.grille[x-1][y-1]
        vhd = self.grille[x+1][y-1]
        vbg = self.grille[x-1][y+1]
        vbd = self.grille[x+1][y+1]
        liste_valeur=[]
        if vg >= 0 :
            liste_valeur.append(vg)
        if vd >=0 :
            liste_valeur.append(vd)
        if vh >= 0 :
            liste_valeur.append(vh)
        if vb >=0 :
            liste_valeur.append(vb)
        # if vhg >= 0:
        #     liste_valeur.append(vhg)
        # if vhd >= 0:
        #     liste_valeur.append(vhd)
        # if vbg >= 0:
        #     liste_valeur.append(vbg)
        # if vbd >= 0:
        #     liste_valeur.append(vbd)
        # la plus petite distance deja trouvvee autour
        mini = min(liste_valeur)

        # donc un de plus pour la case x,y
        v2 = mini + 1
        self.grille[x][y] = v2

        # si on a changé qq chose, on doit recalculer certaines cases autour, il faut donc les ajouter à la liste à traiter
        # celles qui sont positives ou inconnnues
        if vg == BLOC_INCONNU:
            newCase = [x-1,y]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)
        if vd == BLOC_INCONNU:
            newCase = [x+1,y]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)
        if vh == BLOC_INCONNU:
            newCase = [x,y-1]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)
        if vb == BLOC_INCONNU:
            newCase = [x,y+1]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)

    # ------------------------------------------------
    def calcule_distance_grille(self):
        self.reset_distance_grille()
        self.listeCasesACalculer=[]

        self.listeCasesACalculer.append([GRILLE_LX-2,Y_PORTE])
        self.listeCasesACalculer.append([GRILLE_LX-2,Y_PORTE+1])
        self.listeCasesACalculer.append([GRILLE_LX-2,Y_PORTE+2])
        self.listeCasesACalculer.append([GRILLE_LX-2,Y_PORTE+3])

        for case in self.listeCasesACalculer:
            #print("liste : ",len(self.listeCasesACalculer) ,self.listeCasesACalculer)
            self.calcule_distance(case[0],case[1])
            if len(self.listeCasesACalculer) > 1000:
                break

    # ------------------------------------------------
    def prochaineCase(self, x, y):

        # 1 - Trouver lesquelles des 8 cases adjacentes sont eligibles
        # 2 - selectionner celle / l'une de celle qui a la distance mini
        # Une autre fonction  vérifiera la trajectoire pixel optimale

        # portes d'entrée
        # if x == 0:
        #     return ('vd',x + 1, y)

        if x == 0 or type == 'volant':   # porte d'entrée
            v = self.grille[x][y]
            vg = 9999
            vd = self.grille[x + 1][y]
            vh = self.grille[x][y - 1]
            vb = self.grille[x][y + 1]
            vhg = 9999
            vhd = self.grille[x + 1][y - 1]
            vbg = 9999
            vbd = self.grille[x + 1][y + 1]
        elif x == GRILLE_LX - 1:  # porte de sortie
            return ('vd', x+1, y)
        else :
        # une case nondiagonale est accessible si libre
        # une case diagonale est accessible si non entourrée de 2 cases nondiag

            v = self.grille[x][y]
            vg = self.grille[x - 1][y]
            vd = self.grille[x + 1][y]
            vh = self.grille[x][y - 1]
            vb = self.grille[x][y + 1]
            vhg = self.grille[x - 1][y - 1]
            vhd = self.grille[x + 1][y - 1]
            vbg = self.grille[x - 1][y + 1]
            vbd = self.grille[x + 1][y + 1]

        dico = {}

        if vg >= 0:
            dico['vg']=vg
        if vd >= 0:
            dico['vd']=vd
        if vh >= 0:
            dico['vh']=vh
        if vb >= 0:
            dico['vb'] = vb
        # diag
        if vhg >= 0 and (vh >= 0 or vg >= 0):
            dico['vhg']=vhg+0.414
        if vhd >= 0 and (vh >= 0 or vd >= 0):
            dico['vhd']=vhd+0.414
        if vbg >= 0 and (vb >= 0 or vg >= 0):
            dico['vbg']=vbg+0.414
        if vbd >= 0 and ( vb >= 0 or vd >= 0):
            dico['vbd']=vbd+0.414

        #print ("ProchaineCase2 - dico:",dico)
        best = min(dico, key=dico.get)
        #print ("ProchaineCase2 - x,y, best, vbest, v :", x,y,best, dico[best], v)

        if best == 'vg':
            return (best, x-1,y)
        if best == 'vd':
            return (best, x+1,y)
        if best == 'vh':
            return (best, x,y-1)
        if best == 'vb':
            return (best, x,y+1)
        if best == 'vhg':
            return (best, x-1,y-1)
        if best == 'vhd':
            return (best, x+1,y-1)
        if best == 'vbg':
            return (best, x-1,y+1)
        if best == 'vbd':
            return (best, x+1,y+1)

    # -------------------------------------------------
    def est_libre(self, i,j):
        ''' renvoie True/False selon que la case i,j est libre (pas de tour)'''
        if self.grille[i][j] >= 0:
            return True
        else:
            return False

    # -------------------------------------------------
    def quelle_tour_dans_case(self,i,j):
        # TODO : à améliorer (performance) : maintenir une table plutot que d'examiner toutes les tours.
        for t in self.listeTours:
            if t.x == i and t.y == j or\
            t.x+1 == i and t.y == j or\
            t.x == i and t.y+1 == j or\
            t.x+1 == i and t.y+1 == j:
                return t
        return None

    # -------------------------------------------------
    def charge_csv(self):
        if AFFICHE_CSV:
            fichierDefBlocs = csv.reader(open(FICHIER_DEF_BLOCS,"r"),delimiter=';')
            numLigne = 0
            for ligne in fichierDefBlocs:
                for i in range(0,len(ligne)):
                    valeur = int(ligne[i])
                    if valeur == 1:
                        self.nouvelle_tour(Tour(i+1,numLigne+1))
                numLigne += 1