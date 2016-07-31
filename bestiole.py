# tour.py
# coding: utf-8

__author__ = 'Quentin'

from grille import *
from outils import *

class Bestiole():

    def __init__(self,x=-1,y=-1):
        self.vitesse = 0.5
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
        (case_x,case_y) = conversionCoordPixelsVersCases(self.x,self.y)

        # (prochaine_case_x,prochaine_case_y) = grille.prochaineCase(case_x,case_y)
        (prochaine_case_x, prochaine_case_y) = grille.prochaineCase2(case_x, case_y)

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
        (direction_x,direction_y) = (prochaine_case_x-case_x,prochaine_case_y-case_y)

        #print("dirx : ",direction_x,"diry : ",direction_y)
        self.x+=direction_x*self.vitesse
        self.y+=direction_y*self.vitesse