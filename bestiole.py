# tour.py
# coding: utf-8

__author__ = 'Quentin'

from grille import *
from outils import *

class Bestiole():

    def __init__(self,x=-1,y=-1):
        self.vitesse = 0.5
        self.rayon = 10
        if x!=-1 and y!=-1:
            self.x=x
            self.y=y
        else:
            random.random()
            positionDansPorte = random.randint(0,TAILLE_PORTE-1)
            y=GRILLE_PORTE+positionDansPorte
            (self.x,self.y)=conversionCoordCasesVersPixels(0,y)

    def affiche(self):
        SCREEN.blit(IMAGE_BESTIOLE,(self.x-10,self.y-10))

    def deplace(self,grille):

        # on regarde dans quelle case on est
        (cx,cy) = conversionCoordPixelsVersCases(self.x,self.y)

        # (prochaine_case_x,prochaine_case_y) = grille.prochaineCase(case_x,case_y)
        (best, pcx, pcy) = grille.prochaineCase2(cx, cy)

        print ("cx:{},cy:{}, x:{} ,y:{}, best:{}, pcx:{}, pcy:{}". format(cx,cy,self.x,self.y,best, pcx,pcy))
        # TOODO / à améliorer
        # si on va dans une case orthogonale (ex. : d ) :
        #   - si les deux cases autour sont vides (ex. hd, bd) : direction simple (ex. d)
        #   - si  une ou deux autour sont occupées, vérifier si ca passe en largeur
        #           - si oui : direction simple (d)
        #           - si non : direction centre de la case actuelle (à améliorer)
        # si on va dans une case diagonale (ex. bd)
        #   - si les deux cases autour sont vides (b,d), direction centre de la case diagonale
        #   - si une des deux cases autour est vide (ex.b) : direction ortho (ex. b) : A AMELIORER (b + 45degré)
        #   - si deux cases autour occupées, pas possible, déjà éliminé par ProchaineCase2()

        direction = (0,0)
        if best == 'vd':
            # 2 cas : autour est libre, ou pas
            if grille.est_libre(cx+1, cy-1) and grille.est_libre(cx+1,cy+1):
                direction = (1,0)
            else :
                if depasseHaut(self.x,self.y,self.rayon):
                    if grille.est_libre(cx+1,cy-1):
                        direction = (1,0)
                    else:
                        direction = (0,1)
                elif depasseBas(self.x,self.y, self.rayon):
                    if grille.est_libre(cx+1,cy+1):
                        direction = (1,0)
                    else:
                        direction = (0,-1)
                else:
                    direction = (1,0)
                # direction centre case dans un premier temps
                # direction = directionCentreCase(self.x, self.y)
        elif best == 'vb':
            if grille.est_libre(cx+1, cy+1) and grille.est_libre(cx-1,cy+1):
                direction = (0,1)
            else :
                # direction centre case dans un premier temps
                direction = directionCentreCase(self.x, self.y)
        elif best == 'vg':
            if grille.est_libre(cx-1, cy+1) and grille.est_libre(cx-1,cy+1):
                direction = (-1,0)
            else :
                # direction centre case dans un premier temps
                direction = directionCentreCase(self.x, self.y)
        elif best == 'vh':
            if grille.est_libre(cx - 1, cy - 1) and grille.est_libre(cx + 1, cy - 1):
                direction = (0, -1)
            else:
                # direction centre case dans un premier temps
                direction = directionCentreCase(self.x, self.y)
        else:
            direction = ( pcx - cx, pcy - cy)

        print("direction :", direction)

        dx = direction[0]
        dy = direction[1]
        #print("dirx : ",direction_x,"diry : ",direction_y)
        self.x+=dx*self.vitesse
        self.y+=dy*self.vitesse