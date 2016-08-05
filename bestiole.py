# tour.py
# coding: utf-8

__author__ = 'Quentin'

from grille import *
from outils import *


class Bestiole():

    def __init__(self,x=-1,y=-1, type='normale'):
        ''' x et y en pixels'''

        self.type = type
        self.vitesse = TABLE_BESTIOLE[type]['vitesse']
        self.vie = TABLE_BESTIOLE[type]['vie']
        self.rayon = TABLE_BESTIOLE[type]['image'].get_width()/2
        self.image = TABLE_BESTIOLE[type]['image']

        if x!=-1 and y!=-1:
            self.x=x
            self.y=y
        else:
            random.random()
            positionDansPorte = random.randint(1,TAILLE_PORTE-2)
            y=Y_PORTE+positionDansPorte
            (self.x,self.y)=conversionCoordCasesVersPixels(0,y)
            x_pixel = random.randint(0,TAILLE_BLOC)
            self.x += x_pixel
            y_pixel = random.randint(0,TAILLE_BLOC)
            self.y+=y_pixel

            self.y+= -5

    # -------------------------------------------------
    def verifie_bestiole_dans_case(self,i,j):
        '''
        Verifie si la bete est dans la case i,j
        :param i: abscisse case
        :param j: ordonnée case
        :return:  True/False si cette bete est dans la case i,j
        '''
        (i2,j2)=conversionCoordPixelsVersCases(self.x, self.y)
        if i == i2 and j == j2:
            return True
        else:
            return False

    # -------------------------------------------------
    def affiche(self):
        SCREEN.blit(self.image,(self.x-self.rayon,self.y-self.rayon))
        # print(self.vie)

    # -------------------------------------------------
    def deplace(self,grille):

        # TODO : bestiole volante

        if type == 'volant':
            pass

        else:
            # on regarde dans quelle case on est
            (cx,cy) = conversionCoordPixelsVersCases(self.x,self.y)

            # (prochaine_case_x,prochaine_case_y) = grille.prochaineCase(case_x,case_y)
            (best, pcx, pcy) = grille.prochaineCase(cx, cy)

            #print ("cx:{},cy:{}, x:{} ,y:{}, best:{}, pcx:{}, pcy:{}". format(cx,cy,self.x,self.y,best, pcx,pcy))
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
                    # hd et bd sont libres
                    direction = (1,0)
                else :
                    if depasseHaut(self.x,self.y,self.rayon):
                        if grille.est_libre(cx+1,cy-1):
                            # hd est libre
                            direction = (1,0)
                        else:
                            direction = (0,1)
                    elif depasseBas(self.x,self.y, self.rayon):
                        if grille.est_libre(cx+1,cy+1):
                            # bd est libre
                            direction = (1,0)
                        else:
                            direction = (0,-1)
                    else:
                        direction = (1,0)
            elif best == 'vb':
                if grille.est_libre(cx+1, cy+1) and grille.est_libre(cx-1,cy+1):
                    # bd et bg sont libres
                    direction = (0,1)
                else :
                    if depasseDroit(self.x,self.y,self.rayon):
                        if grille.est_libre(cx+1,cy+1):
                            # bd est libre
                            direction = (0,1)
                        else:
                            direction = (-1,0)
                    elif depasseGauche(self.x,self.y, self.rayon):
                        if grille.est_libre(cx-1,cy+1):
                            # bg est libre
                            direction = (0,1)
                        else:
                            direction = (1,0)
                    else:
                        direction = (0,1)
            elif best == 'vg':
                if grille.est_libre(cx-1, cy-1) and grille.est_libre(cx-1,cy+1):
                    # hg et bg sont libres
                    direction = (-1,0)
                else :
                    if depasseHaut(self.x,self.y,self.rayon):
                        if grille.est_libre(cx-1,cy-1):
                            # hg est libre
                            direction = (-1,0)
                        else:
                            direction = (0,1)
                    elif depasseBas(self.x,self.y, self.rayon):
                        if grille.est_libre(cx-1,cy+1):
                            # bg est libre
                            direction = (-1,0)
                        else:
                            direction = (0,-1)
                    else:
                        direction = (-1,0)
            elif best == 'vh':
                if grille.est_libre(cx - 1, cy - 1) and grille.est_libre(cx + 1, cy - 1):
                    # hg et hd sont libres
                    direction = (0, -1)
                else:
                    if depasseGauche(self.x,self.y,self.rayon):
                        if grille.est_libre(cx-1,cy-1):
                            # hg est libre
                            direction = (0,-1)
                        else:
                            direction = (1,0)
                    elif depasseDroit(self.x,self.y, self.rayon):
                        if grille.est_libre(cx-1,cy+1):
                            # hd est libre
                            direction = (0,-1)
                        else:
                            direction = (-1,0)
                    else:
                        direction = (0,-1)
            else:
                #print("***********DIAG**********")
                if not (depasseHaut(self.x,self.y,self.rayon) or depasseDroit(self.x,self.y,self.rayon) or depasseGauche(self.x,self.y,self.rayon) or depasseBas(self.x,self.y,self.rayon)):
                    # on ne dépasse pas, on fonce !
                    direction = ( pcx - cx, pcy - cy)
                else:
                    if best == 'vhd':
                        if depasseHaut(self.x, self.y,self.rayon) and not grille.est_libre(cx,cy-1):
                            direction = (1,0)
                        elif depasseDroit(self.x, self.y,self.rayon) and not grille.est_libre(cx+1,cy):
                            direction = (0,-1)
                        else:
                            direction = (1,-1)
                    elif best == 'vhg':
                        if depasseHaut(self.x, self.y,self.rayon) and not grille.est_libre(cx,cy-1):
                            direction = (-1,0)
                        elif depasseGauche(self.x, self.y,self.rayon) and not grille.est_libre(cx-1,cy):
                            direction = (0,-1)
                        else:
                            direction = (-1,-1)
                    elif best == 'vbg':
                        if depasseBas(self.x, self.y,self.rayon) and not grille.est_libre(cx,cy+1):
                            direction = (-1,0)
                        elif depasseGauche(self.x, self.y,self.rayon) and not grille.est_libre(cx-1,cy):
                            direction = (0,1)
                        else:
                            direction = (-1,1)
                    elif best == 'vbd':
                        if depasseBas(self.x, self.y,self.rayon) and not grille.est_libre(cx,cy+1):
                            direction = (1,0)
                        elif depasseDroit(self.x, self.y,self.rayon) and not grille.est_libre(cx+1,cy):
                            direction = (0,1)
                        else:
                            direction = (1,1)
                    else :
                        direction = ( pcx - cx, pcy - cy)

            #print("direction :", direction)

            dx = direction[0]
            dy = direction[1]
            #print("dirx : ",direction_x,"diry : ",direction_y)
            self.x+=dx*self.vitesse
            self.y+=dy*self.vitesse

