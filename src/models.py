import numpy as np
import random


class Feu:
    """
    Classe représentant un arbre enflammé
    # Attributs publics :
    - position_i : coordonnée ligne de la case où se trouve le feu
    - position_j : coordonnée colonne de la case où se trouve le feu
    """

    def __init__(self, i0, j0):
        """
        Construit un objet Feu
        :param i0: entier positif inférieur à la hauteur de la forêt, sera affecté à l'attribut position_i
        :param j0: entier positif inférieur à la largeur de la forêt, sera affecté à l'attribut position_j
        """
        self.position_i = i0
        self.position_j = j0

    def cibler_propagation(self, p, l, h):
        """
        Retourne un dictionnaire de cases adjacentes que le feu va cibler pour se propager
            (sélectionnées selon une probabilité p)
        :param p: probabilité qu'une case adjacente soit ciblée
        :param l: longueur de la forêt (pour la gestion des effets de bords)
        :param h: hauteur de la forêt (pour la gestion des effets de bords)
        :return: dictionnaire de cases ciblées par le feu qui s'embraseront à l'étape suivante si elles désignent des
            arbres. Les cases sont désignées par des clés représentant les points cardinaux, par exemple la clé 'N'
            désigne le voisin Nord.
        """
        # Alias des coordonnées pour une meilleure lisibilité
        i = self.position_i
        j = self.position_j

        # Construction du dictionnaire de voisins en fonction de la probabilité de propagation
        voisins = {}
        voisins_keys = ['N', 'S', 'W', 'E']
        voisins_values = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        for k, v in zip(voisins_keys, voisins_values):
            if random.random() < p:
                voisins[k] = v

        # On enlève les voisins qui n'existent pas dans le cas où le feu est adjacent à un ou deux bords
        if i == 0:
            voisins.pop('N', '') # Le second argument (default) permet de gérer l'exception si la case n'existe pas
        elif i == h-1:
            voisins.pop('S', '')
        if j == 0:
            voisins.pop('W', '')
        elif j == l-1:
            voisins.pop('E', '')

        return voisins

class Foret:
    """
    Classe représentant la forêt sous forme de matrice.
    # Attributs publics :
    - grille_arbres : objet de type numpy.array() de dimension h*l. Les cases de cette matrice peuvent prendre les
    valeurs des constantes "VALEUR" uniquement
    - incendie : tableau d'objets Feu représentant les arbres enflammés à l'instant courant de la simulation et
        permettant de modéliser le comportement de propagation de l'incendie
    - proba_propagation : probabilité d'un arbre enflammé de propager son feu à un arbre adjacent
    # Constantes :
    - VALEUR_ARBRE : valeur d'une case désignant un arbre normal
    - VALEUR_FEU : valeur d'une case désignant un arbre enflammé depuis lequel le feu peut se propager,
    - VALEUR_CENDRE : valeur d'une case désignant un tas de cendres (qui ne peut donc pas brûler)
    """
    VALEUR_ARBRE = 0
    VALEUR_FEU = 1
    VALEUR_CENDRE = 2

    def __init__(self, l, h, foyers, p):
        """
        Construit un objet Foret
        :param l: largeur de la forêt en nombre de cases
        :param h: hauteur de la forêt en nombre de cases
        :param foyers: tableau de coordonnées ligne-colonne (i, j) représentant les tous premiers arbres en feu
        :param p : probabilité de propagation du feu à partir d'un arbre enflammé
        """
        self.grille_arbres = np.full((h, l), self.VALEUR_ARBRE, dtype=int)

        self.incendie = []
        for coordonnees_feu in foyers:
            i = coordonnees_feu[0]
            j = coordonnees_feu[1]
            self.incendie.append(Feu(i, j))
            self.grille_arbres[i][j] = self.VALEUR_FEU

        self.proba_propagation = p

        self.__nb_feux = len(self.incendie)
        self.__nb_arbres = l*h-self.__nb_feux
        self.__nb_cendres = 0

    def get_largeur(self):
        """
        Renvoie la largeur de la forêt
        :return: nombre de colonnes de grille_arbres
        """
        if self.grille_arbres.size == 0:
            return 0
        else:
            return len(self.grille_arbres[0])

    def get_hauteur(self):
        """
        Renvoie la hauteur de la forêt
        :return: nombre de lignes de grille_arbres
        """
        return len(self.grille_arbres)

    def get_nb_arbres(self):
        """
        Retourne le nombre de cases représentant un arbre dans la forêt
        :return: nombre de cases représentant un arbre
        """
        return self.__nb_arbres

    def get_nb_feux(self):
        """
        Retourne le nombre de cases représentant un arbre en feu
        :return: nombre de cases représentant un feu
        """
        return self.__nb_feux

    def get_nb_cendres(self):
        """
        Retourne le nombre de cases représentant un arbre réduit en cendres
        :return: nombre de cases représentant un tas de cendres
        """
        return self.__nb_cendres

    def copier(self):
        """
        Retourne une copie de l'objet Foret courant
        :return: un objet Foret identique à self
        """
        coordonnees_feu = [(feu.position_i, feu.position_j) for feu in self.incendie]

        copie_foret = Foret(self.get_largeur(), self.get_hauteur(), coordonnees_feu, self.proba_propagation)
        copie_foret.grille_arbres = np.copy(self.grille_arbres)
        copie_foret.__nb_arbres = self.__nb_arbres
        copie_foret.__nb_feux = self.__nb_feux
        copie_foret.__nb_cendres = self.__nb_cendres

        return copie_foret

    def bruler_arbre(self, coordonnees):
        """
        Fait passer une case d'état arbre normal à arbre en feu,
        Précondition : la case désignée doit représenter un arbre
        :param coordonnees: un tuple ligne-colonne (i, j) désignant la case ciblée par la méthode
        :return: un objet Feu initialisé avec les coordonnées données en argument
        """
        i = coordonnees[0]
        j = coordonnees[1]
        # Gestion du cas où la case désignée n'est pas un arbre
        if not self.grille_arbres[i][j] == self.VALEUR_ARBRE:
            raise Exception("ERREUR : la case désignée pour être brûlée ne représente pas un arbre. "
                            "   Arrêt de la simulation...")
        else:
            self.grille_arbres[i][j] = self.VALEUR_FEU
            self.__nb_feux += 1
            self.__nb_arbres -= 1
            return Feu(i, j)

    def finir_combustion(self, feu):
        """
        Finit la combustion d'un objet Feu en faisant passer sa représentation dans la forêt à l'état de cendre
        :param feu: l'objet Feu qui désigne la case à réduire en cendres
        """
        self.grille_arbres[feu.position_i, feu.position_j] = self.VALEUR_CENDRE
        self.__nb_cendres += 1
        self.__nb_feux -= 1

    def propager_incendie(self):
        """
        Simule une étape de propagation du feu au sein de la forêt
        """
        feux_futurs_arbres_brules = []

        # Pour chaque feu de l'incendie à l'étape courante
        for feu in self.incendie:
            # On récupère les cases sur lesquelles le feu cherche à se propager et on les brûle s'il s'agit d'arbres
            cases_ciblees = feu.cibler_propagation(self.proba_propagation, self.get_largeur(), self.get_hauteur())
            for case in cases_ciblees.values():
                if self.grille_arbres[case[0], case[1]] == self.VALEUR_ARBRE:
                    feux_futurs_arbres_brules.append(self.bruler_arbre(case))
            # Enfin on réduit en cendres l'arbre qui vient de finir de brûler
            self.finir_combustion(feu)

        # On initialise les feux de l'étape suivante
        self.incendie = [feu for feu in feux_futurs_arbres_brules]
