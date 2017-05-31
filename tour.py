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

        self.prix_tour = PRIX_TOUR_NORMALE
        self.table_tour_force = TABLE_NORMALE_TOUR_FORCE
        self.table_tour_force_prix = TABLE_NORMALE_TOUR_FORCE_PRIX
        self.table_tour_distance = TABLE_NORMALE_TOUR_DISTANCE
        self.table_tour_distance_prix = TABLE_NORMALE_TOUR_DISTANCE_PRIX
        self.table_tour_vitesse = TABLE_NORMALE_TOUR_VITESSE
        self.table_tour_vitesse_prix = TABLE_NORMALE_TOUR_VITESSE_PRIX
        self.table_tour_cadence = TABLE_NORMALE_TOUR_CADENCE
        self.table_tour_cadence_prix = TABLE_NORMALE_TOUR_CADENCE_PRIX
        self.table_tour_ralenti_force = TABLE_NORMALE_TOUR_RALENTI_FORCE
        self.table_tour_ralenti_duree = TABLE_NORMALE_TOUR_RALENTI_DUREE
        self.table_tour_ralenti_prix = TABLE_NORMALE_TOUR_RALENTI_PRIX

        if type == TOUR_NORMAL:
            pass

        elif type == TOUR_TOUS:
            self.image = IMAGE_TOURELLE_TOUS

            self.prix_tour = PRIX_TOUR_TOUS
            self.table_tour_force = TABLE_TOUS_TOUR_FORCE
            self.table_tour_force_prix = TABLE_TOUS_TOUR_FORCE_PRIX
            self.table_tour_distance = TABLE_TOUS_TOUR_DISTANCE
            self.table_tour_distance_prix = TABLE_TOUS_TOUR_DISTANCE_PRIX
            self.table_tour_vitesse = TABLE_TOUS_TOUR_VITESSE
            self.table_tour_vitesse_prix = TABLE_TOUS_TOUR_VITESSE_PRIX
            self.table_tour_cadence = TABLE_TOUS_TOUR_CADENCE
            self.table_tour_cadence_prix = TABLE_TOUS_TOUR_CADENCE_PRIX
            self.table_tour_ralenti_force = TABLE_TOUS_TOUR_RALENTI_FORCE
            self.table_tour_ralenti_duree = TABLE_TOUS_TOUR_RALENTI_DUREE
            self.table_tour_ralenti_prix = TABLE_TOUS_TOUR_RALENTI_PRIX

        elif type == TOUR_BOUM:
            self.image = IMAGE_TOURELLE_BOUM

            self.prix_tour = PRIX_TOUR_BOUM
            self.table_tour_force = TABLE_BOUM_TOUR_FORCE
            self.table_tour_force_prix = TABLE_BOUM_TOUR_FORCE_PRIX
            self.table_tour_distance = TABLE_BOUM_TOUR_DISTANCE
            self.table_tour_distance_prix = TABLE_BOUM_TOUR_DISTANCE_PRIX
            self.table_tour_vitesse = TABLE_BOUM_TOUR_VITESSE
            self.table_tour_vitesse_prix = TABLE_BOUM_TOUR_VITESSE_PRIX
            self.table_tour_cadence = TABLE_BOUM_TOUR_CADENCE
            self.table_tour_cadence_prix = TABLE_BOUM_TOUR_CADENCE_PRIX
            self.table_tour_ralenti_force = TABLE_BOUM_TOUR_RALENTI_FORCE
            self.table_tour_ralenti_duree = TABLE_BOUM_TOUR_RALENTI_DUREE
            self.table_tour_ralenti_prix = TABLE_BOUM_TOUR_RALENTI_PRIX

        elif type == TOUR_VOLANT:
            self.image = IMAGE_TOURELLE_VOLANT

            self.prix_tour = PRIX_TOUR_VOLANT
            self.table_tour_force = TABLE_VOLANT_TOUR_FORCE
            self.table_tour_force_prix = TABLE_VOLANT_TOUR_FORCE_PRIX
            self.table_tour_distance = TABLE_VOLANT_TOUR_DISTANCE
            self.table_tour_distance_prix = TABLE_VOLANT_TOUR_DISTANCE_PRIX
            self.table_tour_vitesse = TABLE_VOLANT_TOUR_VITESSE
            self.table_tour_vitesse_prix = TABLE_VOLANT_TOUR_VITESSE_PRIX
            self.table_tour_cadence = TABLE_VOLANT_TOUR_CADENCE
            self.table_tour_cadence_prix = TABLE_VOLANT_TOUR_CADENCE_PRIX
            self.table_tour_ralenti_force = TABLE_VOLANT_TOUR_RALENTI_FORCE
            self.table_tour_ralenti_duree = TABLE_VOLANT_TOUR_RALENTI_DUREE
            self.table_tour_ralenti_prix = TABLE_VOLANT_TOUR_RALENTI_PRIX

        elif type == TOUR_BOUM_VOLANT:
            self.image = IMAGE_TOURELLE_BOUM_VOLANT

            self.prix_tour = PRIX_TOUR_BOUM_VOLANT
            self.table_tour_force = TABLE_BOUM_VOLANT_TOUR_FORCE
            self.table_tour_force_prix = TABLE_BOUM_VOLANT_TOUR_FORCE_PRIX
            self.table_tour_distance = TABLE_BOUM_VOLANT_TOUR_DISTANCE
            self.table_tour_distance_prix = TABLE_BOUM_VOLANT_TOUR_DISTANCE_PRIX
            self.table_tour_vitesse = TABLE_BOUM_VOLANT_TOUR_VITESSE
            self.table_tour_vitesse_prix = TABLE_BOUM_VOLANT_TOUR_VITESSE_PRIX
            self.table_tour_cadence = TABLE_BOUM_VOLANT_TOUR_CADENCE
            self.table_tour_cadence_prix = TABLE_BOUM_VOLANT_TOUR_CADENCE_PRIX
            self.table_tour_ralenti_force = TABLE_BOUM_VOLANT_TOUR_RALENTI_FORCE
            self.table_tour_ralenti_duree = TABLE_BOUM_VOLANT_TOUR_RALENTI_DUREE
            self.table_tour_ralenti_prix = TABLE_BOUM_VOLANT_TOUR_RALENTI_PRIX

        elif type == TOUR_PLUS:
            self.image = IMAGE_TOURELLE_PLUS

        self.x = x
        self.y = y
        self.etat = 1

        self.coeffPlus = 1

        self.niveau_force=0
        self.niveau_distance=0
        self.niveau_cadence = 0
        self.niveau_vitesse = 0
        self.niveau_ralentire = 0

        self.force_tir = self.table_tour_force[0]

        self.distance_tir = self.table_tour_distance[0]

        self.vitesse_tir = self.table_tour_vitesse[0]

        self.cadence_tir = self.table_tour_cadence[0]
        self.delai_tir = 0

        self.delai = 0

        self.force_ralentire = self.table_tour_ralenti_force[0]
        self.compte_a_rebour_ralentire = self.table_tour_ralenti_duree[0]

        self.cible_bete = None
        self.image_canon = IMAGE_TOURELLE_CANON_1
        self.image_tourelle_canon = self.image_canon

        self.argent_depense = self.prix_tour

    # ------------------------------------------------
    def affiche(self,tour_selectionnee = False ):

        if self.etat == Tour._ETAT_TOUR_BROUILLON or self.etat == Tour._ETAT_TOUR_BROUILLON_IMPOSSIBLE:
            recttransparent = pygame.Surface((40,40), pygame.SRCALPHA, 32)
            if self.etat==Tour._ETAT_TOUR_BROUILLON:
                recttransparent.fill((52,175,0, 50))
            else:
                recttransparent.fill((255,0,0, 50))
            SCREEN.blit(recttransparent, conversionCoordCasesVersPixels(self.x,self.y))
            if AFFICHE_DISTANCE_TIR_BROUILLON:
                pygame.draw.circle(SCREEN, VERT, centreTour(self.x, self.y), self.distance_tir, 1)

        elif self.etat== Tour._ETAT_TOUR_CONSTRUIT:

            if tour_selectionnee == False:
                SCREEN.blit(self.image,conversionCoordCasesVersPixels(self.x,self.y))
                self.orinenteCanon()
                (x,y) = conversionCoordCasesVersPixels(self.x, self.y)
                if self.type != TOUR_BOUM and self.type != TOUR_PLUS and self.type != TOUR_BOUM_VOLANT:
                    SCREEN.blit(self.image_tourelle_canon,(x,y))

                if self.coeffPlus != 1:
                    SCREEN.blit(IMAGE_TOURELLE_AMELIOREE, conversionCoordCasesVersPixels(self.x,self.y))



            elif tour_selectionnee == True:
                SCREEN.blit(self.image,conversionCoordCasesVersPixels(self.x,self.y))
                self.orinenteCanon()
                (x,y) = conversionCoordCasesVersPixels(self.x, self.y)
                if self.type != TOUR_BOUM and self.type != TOUR_PLUS and self.type != TOUR_BOUM_VOLANT:
                    SCREEN.blit(self.image_tourelle_canon,(x,y))


                recttransparent = pygame.Surface((40,40), pygame.SRCALPHA, 32)
                recttransparent.fill((255,255,255, 150))
                SCREEN.blit(recttransparent, conversionCoordCasesVersPixels(self.x,self.y))

                if self.type != TOUR_PLUS:
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

        self.delai_tir = 70 - (15*(self.cadence_tir-1))

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
                        return [Tir(b,self.vitesse_tir,self.force_tir,force_tir_plus_coeff*2,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1])]

        elif self.type == TOUR_VOLANT:
            for b in listeBestioles:
                if b.type == 'volant' or b.type == 'boss_volant':
                    c = self.touve_bestiole_cible(b)
                    if c != False:
                        #return Tir(b,self.vitesse_tir,force_tir_plus_coeff,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1])
                        return [Tir(b,self.vitesse_tir,self.force_tir,force_tir_plus_coeff*2,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1])]

        elif self.type == TOUR_TOUS:
            for b in listeBestioles:
                c = self.touve_bestiole_cible(b)
                if c != False:
                    return [Tir(b,self.vitesse_tir,self.force_tir,force_tir_plus_coeff,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1])]

        elif self.type == TOUR_BOUM:
            listeTirsBoum = []
            for b in listeBestioles:
                if b.type != 'volant' and b.type != 'boss_volant':
                    c = self.touve_bestiole_cible(b)
                    if c != False:
                        listeTirsBoum.append(Tir(b,self.vitesse_tir,self.force_tir,force_tir_plus_coeff,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1]))
            return listeTirsBoum

        elif self.type == TOUR_BOUM_VOLANT:
            listeTirsBoum = []
            for b in listeBestioles:
                if b.type == 'volant' or b.type == 'boss_volant':
                    c = self.touve_bestiole_cible(b)
                    if c != False:
                        listeTirsBoum.append(Tir(b,self.vitesse_tir,self.force_tir,force_tir_plus_coeff,self.force_ralentire,self.compte_a_rebour_ralentire, c[0], c[1]))
            return listeTirsBoum

        return

    # ------------------------------------------------
    def ameliore(self,type,argent):

        if self.type == TOUR_PLUS:
            return 0

        if type == TOUR_AMELIORATION_FORCE:
            if self.niveau_force<len(self.table_tour_force)-1:
                prix = self.table_tour_force_prix[self.niveau_force]+prixSuplementaire(self)
                if argent>=prix:
                    self.niveau_force += 1
                    self.force_tir += self.table_tour_force[self.niveau_force]
                    self.argent_depense += prix
                    return prix
            return 0

        elif type == TOUR_AMELIORATION_DISTANCE:
            if self.niveau_distance<len(self.table_tour_distance)-1:
                prix = self.table_tour_distance_prix[self.niveau_distance]+prixSuplementaire(self)
                if argent>=prix:
                    self.niveau_distance += 1
                    self.distance_tir += self.table_tour_distance[self.niveau_distance]
                    self.argent_depense += prix

                    if self.niveau_distance == 0:
                        self.image_canon = IMAGE_TOURELLE_CANON_1
                    elif self.niveau_distance == 1:
                        self.image_canon = IMAGE_TOURELLE_CANON_2
                    elif self.niveau_distance == 2:
                        self.image_canon = IMAGE_TOURELLE_CANON_3
                    elif self.niveau_distance == 3:
                        self.image_canon = IMAGE_TOURELLE_CANON_4

                    return prix
            return 0

        elif type == TOUR_AMELIORATION_CADENCE:
            if self.niveau_cadence<len(self.table_tour_cadence)-1:
                prix = self.table_tour_cadence_prix[self.niveau_cadence]+prixSuplementaire(self)
                if argent>=prix:
                    self.niveau_cadence += 1
                    self.cadence_tir += self.table_tour_cadence[self.niveau_cadence]
                    self.argent_depense += prix
                    return prix
            return 0

        elif type == TOUR_AMELIORATION_VITESSE:
            if self.niveau_vitesse<len(self.table_tour_vitesse)-1:
                prix = self.table_tour_vitesse_prix[self.niveau_vitesse]+prixSuplementaire(self)
                if argent>=prix:
                    self.niveau_vitesse += 1
                    self.vitesse_tir += self.table_tour_vitesse[self.niveau_vitesse]
                    self.argent_depense += prix
                    return prix
            return 0

        elif type == TOUR_AMELIORATION_RALENTI:
            if self.niveau_ralentire<len(self.table_tour_ralenti_duree)-1:
                prix = self.table_tour_ralenti_prix[self.niveau_ralentire]+prixSuplementaire(self)
                if argent>=prix:
                    self.niveau_ralentire += 1
                    self.force_ralentire += self.table_tour_ralenti_force[self.niveau_ralentire]
                    self.compte_a_rebour_ralentire += self.table_tour_ralenti_duree[self.niveau_ralentire]
                    self.argent_depense += prix
                    return prix
            return 0

        else:
            return 0

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