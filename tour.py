# tour.py
# coding: utf-8

__author__ = 'Quentin'

from outils import *
from tir import Tir

# ============================================================
class Tour():

    _ETAT_TOUR_CONSTRUIT = 1
    _ETAT_TOUR_BROUILLON = 0
    _ETAT_TOUR_BROUILLON_IMPOSSIBLE = -1

    # ------------------------------------------------
    def __init__(self,x,y,type,etat=_ETAT_TOUR_CONSTRUIT):

        self.type = type

        self.image = IMAGE_TOURELLE_NORMAL
        if type == TOUR_TOUS:
            self.image = IMAGE_TOURELLE_TOUS
        elif type == TOUR_NORMAL:
            self.image = IMAGE_TOURELLE_NORMAL
        elif type == TOUR_BOUM:
            self.image = IMAGE_TOURELLE_BOUM
        elif type == TOUR_VOLANT:
            self.image = IMAGE_TOURELLE_VOLANT
        elif type == TOUR_BOUM_VOLANT:
            self.image = IMAGE_TOURELLE_BOUM_VOLANT
        elif type == TOUR_PLUS:
            self.image = IMAGE_TOURELLE_PLUS

        self.x = x
        self.y = y
        self.etat = 1

        self.coeffPlus = 1

        self.niveau_force=0
        self.niveau_distance=0
        self.niveau_rapidite = 0
        self.niveau_vitesse = 0
        self.niveau_ralentire = 0

        self.force_tir = TABLE_TOUR_FORCE[0]

        self.distance_tir = TABLE_TOUR_DISTANCE[0]

        self.vitesse_tir = TABLE_TOUR_VITESSE[0]

        self.rapidite_tir = TABLE_TOUR_RAPIDITE[0]
        self.delai_tir = 0

        self.delai = 0

        self.force_ralentire = TABLE_TOUR_RALENTI_FORCE[0]
        self.compte_a_rebour_ralentire = TABLE_TOUR_RALENTI_DUREE[0]

        self.cible_bete = None
        self.image_canon = IMAGE_TOURELLE_CANON_1
        self.image_tourelle_canon = self.image_canon

    # ------------------------------------------------
    def affiche(self,tour_selectionnee = False ):

        if self.etat == Tour._ETAT_TOUR_BROUILLON or self.etat == Tour._ETAT_TOUR_BROUILLON_IMPOSSIBLE:
            recttransparent = pygame.Surface((40,40), pygame.SRCALPHA, 32)
            if self.etat==Tour._ETAT_TOUR_BROUILLON:
                recttransparent.fill((52,175,0, 50))
            else:
                recttransparent.fill((255,0,0, 50))
            SCREEN.blit(recttransparent, conversionCoordCasesVersPixels(self.x,self.y))
            if AFFICHE_PERIMETRE_TIR:
                pygame.draw.circle(SCREEN, VERT, centreTour(self.x, self.y), self.distance_tir, 1)

        elif self.etat== Tour._ETAT_TOUR_CONSTRUIT:

            if tour_selectionnee == False:
                SCREEN.blit(self.image,conversionCoordCasesVersPixels(self.x,self.y))
                self.orinenteCanon()
                (x,y) = conversionCoordCasesVersPixels(self.x, self.y)
                if self.type != TOUR_BOUM and self.type != TOUR_PLUS and self.type != TOUR_BOUM_VOLANT:
                    SCREEN.blit(self.image_tourelle_canon,(x,y))

            elif tour_selectionnee == True:
                SCREEN.blit(self.image,conversionCoordCasesVersPixels(self.x,self.y))
                self.orinenteCanon()
                (x,y) = conversionCoordCasesVersPixels(self.x, self.y)
                if self.type != TOUR_BOUM and self.type != TOUR_PLUS and self.type != TOUR_BOUM_VOLANT:
                    SCREEN.blit(self.image_tourelle_canon,(x,y))

                recttransparent = pygame.Surface((40,40), pygame.SRCALPHA, 32)
                recttransparent.fill((255,255,255, 150))
                SCREEN.blit(recttransparent, conversionCoordCasesVersPixels(self.x,self.y))

                pygame.draw.circle(SCREEN, VERT, centreTour(self.x, self.y), self.distance_tir, 1)

    # ------------------------------------------------
    def gere_construction(self):
        ''' si necessaire, fait avancer la construction d'une tour'''
        # TODO gere construction tour
        pass

    # ------------------------------------------------
    def gere_deconstruction(self):
        ''' si necessaire, fait avancer la DE-construction d'une tour'''
        # TODO gere_deconstruction tour
        pass

    # ------------------------------------------------
    def touve_bestiole_cible(self,b):
        # distance entre : self.centreCase() et (b.x, b.y)
        (cx,cy) = centreCase(self.x,self.y)
        dist = math.sqrt ( (cx-b.x)**2 + (cy-b.y)**2 )
        if dist <= self.distance_tir:
            # Si oui, calculer direction
            self.delai = self.delai_tir
            c = centreTour(self.x, self.y)

            self.cible_bete = b

            return c
        return False

    # ------------------------------------------------
    def cree_tir(self,listeBestioles):
        '''
        determine s'il faut tirer, et si oui, crée un tir, trouve la cible ...
        retourne un tir si un tir a été créé, sinon rend NULL
        '''

        force_tir_plus_coeff = self.force_tir*self.coeffPlus

        self.delai_tir = 70 - (15*(self.rapidite_tir-1))

        if TIR_ACTIF is False:
            return

        # delai de tir OK ? (autre stratégie : nombre de tirs simultanés maxi)
        if self.delai != 0:
            self.delai -= 1
            return

        # Recherche cible ?
        # La premiere de la liste qui est à bonne distance

        if self.type == TOUR_NORMAL:
            for b in listeBestioles:
                if b.type != 'volant' and b.type != 'boss_volant':
                    c = self.touve_bestiole_cible(b)
                    if c != False:
                        # return Tir(b,self.vitesse_tir,force_tir_plus_coeff,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1])
                        return [Tir(b,self.vitesse_tir,force_tir_plus_coeff*2,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1])]

        elif self.type == TOUR_VOLANT:
            for b in listeBestioles:
                if b.type == 'volant' or b.type == 'boss_volant':
                    c = self.touve_bestiole_cible(b)
                    if c != False:
                        #return Tir(b,self.vitesse_tir,force_tir_plus_coeff,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1])
                        return [Tir(b,self.vitesse_tir,force_tir_plus_coeff*2,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1])]

        elif self.type == TOUR_TOUS:
            for b in listeBestioles:
                c = self.touve_bestiole_cible(b)
                if c != False:
                    return [Tir(b,self.vitesse_tir,force_tir_plus_coeff,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1])]

        elif self.type == TOUR_BOUM:
            listeTirsBoum = []
            for b in listeBestioles:
                if b.type != 'volant' and b.type != 'boss_volant':
                    c = self.touve_bestiole_cible(b)
                    if c != False:
                        listeTirsBoum.append(Tir(b,self.vitesse_tir,force_tir_plus_coeff,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1]))
            return listeTirsBoum

        elif self.type == TOUR_BOUM_VOLANT:
            listeTirsBoum = []
            for b in listeBestioles:
                if b.type == 'volant' or b.type == 'boss_volant':
                    c = self.touve_bestiole_cible(b)
                    if c != False:
                        listeTirsBoum.append(Tir(b,self.vitesse_tir,force_tir_plus_coeff,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1]))
            return listeTirsBoum

        return

    # ------------------------------------------------
    def ameliore(self,type):

        if type == TOUR_AMELIORATION_FORCE:
            if self.niveau_force<len(TABLE_TOUR_FORCE)-1:
                self.niveau_force += 1
                self.force_tir += TABLE_TOUR_FORCE[self.niveau_force]
                return True
            else:
                return False

        elif type == TOUR_AMELIORATION_DISTANCE:
            if self.niveau_distance<len(TABLE_TOUR_DISTANCE)-1:
                self.niveau_distance += 1
                self.distance_tir += TABLE_TOUR_DISTANCE[self.niveau_distance]

                if self.niveau_distance == 0:
                    self.image_canon = IMAGE_TOURELLE_CANON_1
                elif self.niveau_distance == 1:
                    self.image_canon = IMAGE_TOURELLE_CANON_2
                elif self.niveau_distance == 2:
                    self.image_canon = IMAGE_TOURELLE_CANON_3
                elif self.niveau_distance == 3:
                    self.image_canon = IMAGE_TOURELLE_CANON_4

                return True
            else:
                return False

        elif type == TOUR_AMELIORATION_RAPIDITE:
            if self.niveau_rapidite<len(TABLE_TOUR_RAPIDITE)-1:
                self.niveau_rapidite += 1
                self.rapidite_tir += TABLE_TOUR_RAPIDITE[self.niveau_rapidite]
                return True
            else:
                return False

        elif type == TOUR_AMELIORATION_VITESSE:
            if self.niveau_vitesse<len(TABLE_TOUR_VITESSE)-1:
                self.niveau_vitesse += 1
                self.vitesse_tir += TABLE_TOUR_VITESSE[self.niveau_vitesse]
                return True
            else:
                return False

        elif type == TOUR_AMELIORATION_RALENTI:
            if self.niveau_ralentire<len(TABLE_TOUR_RALENTI_DUREE)-1:
                self.niveau_ralentire += 1
                self.force_ralentire = TABLE_TOUR_RALENTI_FORCE[self.niveau_ralentire]
                self.compte_a_rebour_ralentire = TABLE_TOUR_RALENTI_DUREE[self.niveau_ralentire]
                return True
            else:
                return False

        else:
            return False

    # ------------------------------------------------
    def orinenteCanon(self):
        if self.cible_bete != None :
            (x,y) = conversionCoordCasesVersPixels(self.x,self.y)
            bx = self.cible_bete.x
            by = self.cible_bete.y

            dist = math.sqrt ( (x-bx)**2 + (y-by)**2 )
            cosinus = (bx-x)/dist

            angle = math.acos(cosinus)
            angle = math.degrees(angle)

            if ((y-by)<0):
                angle = -angle

            self.image_tourelle_canon = rot_centre(self.image_canon,angle)

    # ------------------------------------------------
    def plusAmeliore(self):
        self.coeffPlus = self.coeffPlus * COEFF_TOUR_PLUS

    # ------------------------------------------------
    def plusDeameliore(self):
        self.coeffPlus = self.coeffPlus/COEFF_TOUR_PLUS