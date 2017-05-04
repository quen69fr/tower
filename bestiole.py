# tour.py
# coding: utf-8

__author__ = 'Quentin'

from grille import *   # pas tres propre
from outils import *


class Bestiole():

    def __init__(self,vague,x=-1,y=-1, type='normale'):
        ''' x et y en pixels'''

        self.type = type
        self.vitesse = TABLE_BESTIOLE[type]['vitesse']
        self.vie = TABLE_BESTIOLE[type]['vie']
        self.vague = vague
        self.gain = TABLE_BESTIOLE[self.type]['gain']

        self.rayon = TABLE_BESTIOLE[type]['image_d'].get_width()/2
        # inutile : on ira chercher la/les images dans la TABLE
        # self.image = TABLE_BESTIOLE[type]['image']
        # la direction permet de faire tourner les betes lors des deplacements
        # et de choisir la bonne image à afficher
        # 8 valeurs : _d , _hd , _h , _hg ,  _g , _bg , _b , _bd
        self.direction = '_d'  # direction à droite par défaut au début
        self.difficultee = TABLE_VAGUE[vague]['difficultee']

        self.selectionne = False

        self.vie = int(self.vie * self.difficultee * self.difficultee * self.difficultee*0.5)
        self.gain = int(self.gain*self.difficultee)
        self.vie_max = self.vie

        if x!=-1 and y!=-1:
            self.x=x
            self.y=y

        else:
            if self.type == 'groupe' or self.type == 'boss_groupe':
                y=Y_PORTE+TAILLE_PORTE/2
                (self.x,self.y)=conversionCoordCasesVersPixels(0,y)
                x_pixel = random.randint(0,TAILLE_BLOC/2)
                self.x += x_pixel
                y_pixel = random.randint(0,TAILLE_BLOC/2)
                self.y+=y_pixel

                self.y+= -5

            else:
                random.random()
                positionDansPorte = random.randint(1,TAILLE_PORTE-2)
                y=Y_PORTE+positionDansPorte
                (self.x,self.y)=conversionCoordCasesVersPixels(0,y)
                x_pixel = TAILLE_BLOC
                self.x += x_pixel
                y_pixel = random.randint(0,TAILLE_BLOC)
                self.y+=y_pixel

                self.y+= -5

        self.force_ralentie = 0
        self.compte_a_rebour_ralentie = -15

    # -------------------------------------------------
    def verifie_bestiole_dans_case(self,i,j,selectionne=True):
        '''
        Verifie si la bete est dans la case i,j
        :param i: abscisse case
        :param j: ordonnée case
        :return:  True/False si cette bete est dans la case i,j
        '''
        (i2,j2)=conversionCoordPixelsVersCases(self.x, self.y)
        if i == i2 and j == j2:
            if selectionne == True:
                self.selectionne = True
            return True
        else:
            if selectionne == True:
                self.selectionne = False
            return False

    # -------------------------------------------------
    def affiche(self):

        img=TABLE_BESTIOLE[self.type]["image"+self.direction]
        SCREEN.blit(img,(self.x-self.rayon,self.y-self.rayon))
        # SCREEN.blit(self.image,(self.x-self.rayon,self.y-self.rayon))

        self.affiche_vie()

        # print(self.vie)

    # -------------------------------------------------
    def affiche_vie(self):
        ratio = self.vie/self.vie_max

        largeur1 = int(X_BARRE_DE_VIE*ratio)

        x_vie = self.x-X_BARRE_DE_VIE/2
        y_vie = self.y-Y_BARRE_DE_VIE/2-self.rayon-HAUTEUR_BARRE_DE_VIE

        if ratio>0:
            pygame.draw.rect(SCREEN, VERT, (x_vie, y_vie, largeur1, Y_BARRE_DE_VIE), 0)
        if ratio<1:
            pygame.draw.rect(SCREEN, ROUGE, (x_vie+largeur1, y_vie, X_BARRE_DE_VIE-largeur1, Y_BARRE_DE_VIE), 0)

    # -------------------------------------------------
    def affiche_gain(self,gain):
        texte="+ {}".format(gain)
        surface = FONT_2.render(texte, True, JAUNE)
        rect = surface.get_rect(topleft=(MARGE_ECRAN+410, 10))
        SCREEN.blit(surface, rect)

    # -------------------------------------------------
    def clic(self,x_souris,y_souris):
        return math.sqrt((x_souris - self.x)**2 + (y_souris - self.y)**2 ) <= self.rayon+5

    # -------------------------------------------------
    def deplace(self,grille):

        self.reaccelerer()
        # on regarde dans quelle case on est
        (ci, cj) = conversionCoordPixelsVersCases(self.x, self.y)

        # bestiole volante
        if self.type == 'volant' or self.type == 'boss_volant':

            # prochaine case : à droite
            direction = (1,0)
            direction2 = '_d'
            best="vd"
            pci = ci + 1
            pcj = cj

        else:

            # on cherche la prochaine case
            (best, pci, pcj) = grille.prochaineCase(ci, cj)

            # print ("cx:{},cy:{}, x:{} ,y:{}, best:{}, pcx:{}, pcy:{}". format(cx,cy,self.x,self.y,best, pcx,pcy))

            # et on ajuste la trajectoire en pixel, selon les diagonales, angles et rayons des bestioles
            # Algo :
            # si on va dans une case orthogonale (ex. : d ) :
            #   - si les deux cases autour sont vides (ex. hd, bd) : direction simple (ex. d)
            #   - si  une ou deux autour sont occupées, vérifier si ca passe en largeur
            #           - si oui : direction simple (d)
            #           - si non : direction centre de la case actuelle (à améliorer)
            # si on va dans une case diagonale (ex. bd)
            #   - si les deux cases autour sont vides (b,d), direction centre de la case diagonale
            #   - si une des deux cases autour est vide (ex.b) : direction ortho (ex. b) : A AMELIORER (b + 45degré)
            #   - si deux cases autour occupées, pas possible, déjà éliminé par ProchaineCase()

            direction = (1,0)
            if best == 'vd':
                # 2 cas : autour est libre, ou pas
                if grille.caseVide(ci+1, cj-1) and grille.caseVide(ci+1,cj+1):
                    # hd et bd sont libres
                    direction = (1,0)
                else:
                    if depasseHaut(self.x,self.y,self.rayon):
                        if grille.caseVide(ci+1,cj-1):
                            # hd est libre
                            direction = (1,0)
                        else:
                            direction = (0,1)
                    elif depasseBas(self.x,self.y, self.rayon):
                        if grille.caseVide(ci+1,cj+1):
                            # bd est libre
                            direction = (1,0)
                        else:
                            direction = (0,-1)
                    else:
                        direction = (1,0)
            elif best == 'vb':
                if grille.caseVide(ci+1, cj+1) and grille.caseVide(ci-1,cj+1):
                    # bd et bg sont libres
                    direction = (0,1)
                else :
                    if depasseDroit(self.x,self.y,self.rayon):
                        if grille.caseVide(ci+1,cj+1):
                            # bd est libre
                            direction = (0,1)
                        else:
                            direction = (-1,0)
                    elif depasseGauche(self.x,self.y, self.rayon):
                        if grille.caseVide(ci-1,cj+1):
                            # bg est libre
                            direction = (0,1)
                        else:
                            direction = (1,0)
                    else:
                        direction = (0,1)
            elif best == 'vg':
                if grille.caseVide(ci-1, cj-1) and grille.caseVide(ci-1,cj+1):
                    # hg et bg sont libres
                    direction = (-1,0)
                else :
                    if depasseHaut(self.x,self.y,self.rayon):
                        if grille.caseVide(ci-1,cj-1):
                            # hg est libre
                            direction = (-1,0)
                        else:
                            direction = (0,1)
                    elif depasseBas(self.x,self.y, self.rayon):
                        if grille.caseVide(ci-1,cj+1):
                            # bg est libre
                            direction = (-1,0)
                        else:
                            direction = (0,-1)
                    else:
                        direction = (-1,0)
            elif best == 'vh':
                if grille.caseVide(ci - 1, cj - 1) and grille.caseVide(ci + 1, cj - 1):
                    # hg et hd sont libres
                    direction = (0, -1)
                else:
                    if depasseGauche(self.x,self.y,self.rayon):
                        if grille.caseVide(ci-1,cj-1):
                            # hg est libre
                            direction = (0,-1)
                        else:
                            direction = (1,0)
                    elif depasseDroit(self.x,self.y, self.rayon):
                        if grille.caseVide(ci-1,cj+1):
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
                    direction = ( pci - ci, pcj - cj)
                else:
                    if best == 'vhd':
                        if depasseHaut(self.x, self.y,self.rayon) and not grille.caseVide(ci,cj-1):
                            direction = (1,0)
                        elif depasseDroit(self.x, self.y,self.rayon) and not grille.caseVide(ci+1,cj):
                            direction = (0,-1)
                        else:
                            direction = (1,-1)
                    elif best == 'vhg':
                        if depasseHaut(self.x, self.y,self.rayon) and not grille.caseVide(ci,cj-1):
                            direction = (-1,0)
                        elif depasseGauche(self.x, self.y,self.rayon) and not grille.caseVide(ci-1,cj):
                            direction = (0,-1)
                        else:
                            direction = (-1,-1)
                    elif best == 'vbg':
                        if depasseBas(self.x, self.y,self.rayon) and not grille.caseVide(ci,cj+1):
                            direction = (-1,0)
                        elif depasseGauche(self.x, self.y,self.rayon) and not grille.caseVide(ci-1,cj):
                            direction = (0,1)
                        else:
                            direction = (-1,1)
                    elif best == 'vbd':
                        if depasseBas(self.x, self.y,self.rayon) and not grille.caseVide(ci,cj+1):
                            direction = (1,0)
                        elif depasseDroit(self.x, self.y,self.rayon) and not grille.caseVide(ci+1,cj):
                            direction = (0,1)
                        else:
                            direction = (1,1)
                    else :
                        direction = ( pci - ci, pcj - cj)

        # Fin des cas selon type de bestioles et directions : maintenant on déplace !

        dx = direction[0]
        dy = direction[1]

        table_direction2 = [
                            ['?','_b','_h'],  # dx = 0
                            ['_d', '_bd', '_hd'],  # dx = 1
                            ['_g', '_bg', '_hg']  # dx = -1
                            ]
        direction2 = table_direction2[dx][dy]
        # print("direction :", direction, "direction2 : ",direction2, "best : ",best, "dx : ",dx,"dy : ",dy)

        # si self.direction != direction2 , on tourne
        # (directement vers l'orientation finale ) (amélioration : on tourne cran par cran)
        if self.direction != direction2:
            self.direction = direction2
        else:
            # sinon on deplace
            self.x+=dx*self.vitesse
            self.y+=dy*self.vitesse

            # et on  fait un petit ajustement de trajectoire éventuel en direction
            # du centre de la prochaine case pour éviter les décalages au dernier moment
            # Phil - 28 aout
            (pcx, pcy) = centreCase(pci, pcj)
            if (direction2 == '_d' or direction2 == '_g') and (best =='vd' or best == 'vg'):
                if self.y > pcy+2:
                    self.y -= 0.05
                if self.y < pcy-2:
                    self.y += 0.05
            if (direction2 == '_h' or direction2 == '_b') and (best == 'vh' or best =='vb'):
                if self.x > pcx + 2:
                    self.x -= 0.05
                if self.x < pcx - 2:
                    self.x += 0.05
    
    # -------------------------------------------------
    def ralentie(self,temps,force):

        if self.type == 'imune' or self.type == 'boss_imune':
            pass

        else:
            if self.compte_a_rebour_ralentie == -15:

                self.compte_a_rebour_ralentie = temps
                self.force_ralentie = force

                return True

            else:
                return False

    # -------------------------------------------------
    def reaccelerer(self):
        if self.compte_a_rebour_ralentie == -15:
            self.compte_a_rebour_ralentie = -15

        elif self.compte_a_rebour_ralentie == 1:
            self.vitesse = TABLE_BESTIOLE[self.type]['vitesse']
            self.compte_a_rebour_ralentie = 0

        else:
            self.compte_a_rebour_ralentie -= 1