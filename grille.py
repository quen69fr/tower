# tour.py
# coding: utf-8

__author__ = 'Quentin'

from outils import *

class Grille():

    def __init__(self):

        self.grille=[]
        self.listeTours = []
        self.grille = [[BLOC_INCONNU for j in range(GRILLE_LY)] for i in range(GRILLE_LX)]

        for i in range(GRILLE_LX):
            self.grille[i][0]=BLOC_BORD
            self.grille[i][GRILLE_LY-1]=BLOC_BORD

        for j in range(GRILLE_LY):
            self.grille[0][j]=BLOC_BORD
            self.grille[GRILLE_LX-1][j]=BLOC_BORD

        self.grille[GRILLE_LX-1][GRILLE_PORTE]=BLOC_PORTE
        self.grille[GRILLE_LX-1][GRILLE_PORTE+1]=BLOC_PORTE

        self.grille[0][GRILLE_PORTE]=BLOC_ENTREE
        self.grille[0][GRILLE_PORTE+1]=BLOC_ENTREE

    # ------------------------------------------------
    def reset_distance_grille(self):
        for x in range(0,GRILLE_LX):
            for y in range(0,GRILLE_LY):
                if self.grille[x][y] != BLOC_BORD \
                        and self.grille[x][y] != BLOC_PORTE \
                        and self.grille[x][y] != BLOC_ENTREE \
                        and self.grille[x][y] != BLOC_TOUR:
                    self.grille[x][y] = BLOC_INCONNU

    # ------------------------------------------------
    def nouvelle_tour(self,tour):
        x = tour.x
        y = tour.y

        if self.grille[x][y] > 0 and self.grille[x+1][y] > 0 and self.grille[x][y+1] > 0 and self.grille[x+1][y+1] > 0:
            self.listeTours.append(tour)
            self.grille[x][y]=BLOC_TOUR
            self.grille[x+1][y]=BLOC_TOUR
            self.grille[x][y+1]=BLOC_TOUR
            self.grille[x+1][y+1]=BLOC_TOUR

    # ------------------------------------------------
    def enleve_tour(self,x,y):

        if self.grille[x][y] == BLOC_TOUR and self.grille[x+1][y] == BLOC_TOUR and self.grille[x][y+1] == BLOC_TOUR and self.grille[x+1][y+1] == BLOC_TOUR:
            for t in self.listeTours:
                if t.x == x and t.y == y:
                    self.listeTours.remove(t)
                    self.grille[x][y]=BLOC_INCONNU
                    self.grille[x+1][y]=BLOC_INCONNU
                    self.grille[x][y+1]=BLOC_INCONNU
                    self.grille[x+1][y+1]=BLOC_INCONNU

    # ------------------------------------------------
    def affiche_grille(self):
        # print "------------------"
        for j in range(GRILLE_LY):
            print (j, ':',)
            for i in range(GRILLE_LX):
                print (self.grille[i][j],)
            print ("")

    # ------------------------------------------------
    def dessine_grille(self):
        SCREEN.fill(0)
        for j in range(GRILLE_LY):
            for i in range(GRILLE_LX):
                v=self.grille[i][j]
                # dessiner un rectangle en x,y de couleur v
                c=NOIR
                if v == BLOC_BORD:
                    c=BLEU
                if v == BLOC_PORTE:
                    c=NOIR
                if v == BLOC_ENTREE:
                    c=BLANC
                if v == BLOC_INCONNU:
                    c=ROUGE
                if v > 0:
                    nuance = v*3
                    if nuance>255 :
                        nuance = 255
                    c = (nuance,nuance,nuance)
                (x,y) = conversionCoordCasesVersPixels(i,j)
                pygame.draw.rect(SCREEN, c, (x,y,TAILLE_BLOC,TAILLE_BLOC),0)

        for tour in self.listeTours:
            tour.affiche()

        pygame.display.update()
        #pygame.time.delay(DELAY )

    # ------------------------------------------------
    def calcule_distance(self,x,y):

        # TODO : BUG si case de départ occupée par un bloc

        #print "Calcul ",x,y
        #self.dessine_grille()

        # il faut récupérer les 4 valeurs autour
        vg = self.grille[x-1][y]
        vd = self.grille[x+1][y]
        vh = self.grille[x][y-1]
        vb = self.grille[x][y+1]
        liste_valeur=[]
        if vg >= 0 :
            liste_valeur.append(vg)
        if vd >=0 :
            liste_valeur.append(vd)
        if vh >= 0 :
            liste_valeur.append(vh)
        if vb >=0 :
            liste_valeur.append(vb)
        # la plus petite distance deja trouvvee autour
        mini = min(liste_valeur)

        # donc un de plus pour la case x,y
        v2 = mini + 1
        self.grille[x][y] = v2

        # si on a changé qq chose, on doit recalculer certaines cases autour, il faut donc les ajouter à la liste à traiter
        # celles qui sont positives ou inconnnues
        if vg == BLOC_INCONNU and len(self.listeCasesACalculer) < 1000:
            newCase = [x-1,y]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)
        if vd == BLOC_INCONNU and len(self.listeCasesACalculer) < 1000:
            newCase = [x+1,y]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)
        if vh == BLOC_INCONNU and len(self.listeCasesACalculer) < 1000:
            newCase = [x,y-1]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)
        if vb == BLOC_INCONNU and len(self.listeCasesACalculer) < 1000:
            newCase = [x,y+1]
            if newCase not in self.listeCasesACalculer:
                self.listeCasesACalculer.append(newCase)

    # ------------------------------------------------
    def calcule_distance_grille(self):
        self.reset_distance_grille()
        self.listeCasesACalculer=[]

        self.listeCasesACalculer.append([GRILLE_LX-2,GRILLE_PORTE])
        self.listeCasesACalculer.append([GRILLE_LX-2,GRILLE_PORTE+1])

        for case in self.listeCasesACalculer:
            #print("liste : ",len(self.listeCasesACalculer) ,self.listeCasesACalculer)
            self.calcule_distance(case[0],case[1])
            if len(self.listeCasesACalculer) > 1000:
                break