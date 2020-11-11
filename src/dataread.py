import yaml
from webcolors import hex_to_rgb

class SimulationDataLoader:
    """
    Classe dont l'instance permet de lire le fichier de configuration de la simulation
    # Attributs publics :
    - sim_parametres : dictionnaire des paramètres directement lus depuis le fichier de configuration
    """

    def __init__(self, filepath):
        """
        Construit un objet SimulationDataLoader
        :param filepath: Chemin vers le fichier de configuration depuis le dossier racine du projet
        """
        try:
            config_file_r = open(filepath)
            self.sim_parametres = yaml.load(config_file_r, Loader=yaml.FullLoader)
        except:
            raise Exception("Le fichier de configuration n'a pas été atteint ou n'a pas pu être lu. Veuillez vérifier "
                            "qu'il n'y ait aucune erreur de syntaxe.")

    def get_metadonnee_foret(self, key, is_integer):
        """
        Renvoie un paramètre décrit par le fichier de configuration en gérant les erreurs de type et de syntaxe
        :param key: nom du paramètre dans le fichier de configuration
        :param is_integer: booléen, indique si le paramètre est un entier lorsque True (pour la gestion des exceptions)
        :return: valeur du paramètre désigné par key dans le fichier de configuration
        """
        # Gestion de l'absence éventuelle du paramètre dans le fichier de configuration
        try:
            valeur_parametre = self.sim_parametres["parametres"]["simulation"]["metadonnees_foret"][key]
        except:
            raise Exception("Le paramètre " + key + " est manquant.")

        # Gestion du type du paramètre (int si on a indiqué que c'était un entier, float sinon)
        if is_integer:
            try:
                valeur_parametre = int(abs(valeur_parametre))
            except:
                raise Exception("Le paramètre " + key + " n'a pas pu être lu en tant que nombre entier positif.")
        elif type(valeur_parametre) != float:
            raise Exception("Le paramètre " + key + " doit être un nombre.")

        return valeur_parametre

    def get_feux_depart(self):
        """
        Renvoie la liste des feux de départ de la simulation
        :return: liste de coordonnées ligne-colonne (i, j) désignant les cases en feu au début de la simulation
        """
        # Gestion de l'absence éventuelle du paramètre dans le fichier de configuration
        try:
            parametre_feux = self.sim_parametres["parametres"]["simulation"]["feux_depart"]
        except:
            raise Exception("Le paramètre feux_depart est manquant.")

        # Gestion du cas où les feux ne sont pas spécifiés sous forme de liste
        try:
            len(parametre_feux)
        except:
            raise Exception("La liste de feux doit être un tableau, même s'il n'y a qu'un seul feu de départ.")

        # Gestion des erreurs liées à la lecture des coordonnées
        try:
            feux = []
            largeur_foret = self.sim_parametres["parametres"]["simulation"]["metadonnees_foret"]["largeur_foret"]
            hauteur_foret = self.sim_parametres["parametres"]["simulation"]["metadonnees_foret"]["hauteur_foret"]
            # Gestion des coordonnées supérieures à la taille de la forêt
            for param_feu in parametre_feux:
                if int(abs(param_feu["ligne"])) >= hauteur_foret or int(abs(param_feu["colonne"])) >= largeur_foret:
                    raise Exception()
                else:
                    feux.append(( int(abs(param_feu["ligne"])), int(abs(param_feu["colonne"])) ))
            return feux
        except:
            raise Exception("Erreur dans la lecture des coordonnées des feux. Veuillez vérifier qu'il n'y ait aucune "
                            "erreur de syntaxe, qu'il ne manque pas un paramètre et que les coordonnées des feux sont "
                            "bien strictement inférieures aux dimensions de la forêt.")

    def get_display_bool_metadata(self, key):
        """
        Retourne un paramètre booléen de la catégorie display dans le fichier de configuration (méthode spécifique aux
            booléens pour la gestion des exceptions)
        :param key: nom du paramètre dans le fichier de configuration
        :return: valeur du paramètre désigné par key dans le fichier de configuration
        """
        # Gestion de l'absence éventuelle du paramètre dans le fichier de configuration
        try:
            valeur_parametre = self.sim_parametres["parametres"]["display"][key]
        except:
            raise Exception("Le paramètre " + key + " est manquant.")

        # Gestion du type
        if type(valeur_parametre) != bool:
            raise Exception("Le paramètre " + key + " ne peut avoir pour valeur que true ou false")
        else:
            return valeur_parametre

    def get_intervalle_animation(self):
        """
        Retourne la valeur de l'intervalle entre deux images de la simulation animée en fonction du paramètre
            fps_max_animation qui désigne la fréquence d'image dans le fichier de configuration
        :return: nombre entier positif désignant l'intervalle en millisecondes entre deux images de l'animation de la
            simulation
        """
        # Gestion de l'absence éventuelle du paramètre dans le fichier de configuration
        try:
            fps = self.sim_parametres["parametres"]["display"]["fps_max_animation"]
        except:
            raise Exception("Le paramètre fps_max_animation est manquant.")

        # Gestion du type de paramètre (une fraction ne marche pas si le dénominateur n'est pas un nombre
        try:
            intervalle = int(abs(1000/fps))
            return intervalle
        except:
            raise Exception("Erreur dans la lecture du paramètre fps_max_animation. Veuillez vérifier qu'il s'agit "
                            "bien d'un nombre positif.")

    def get_couleur_metadata_dictionary(self):
        """
        Retourne le dictionnaire des couleurs de la simulation, chacune étant un tableau de longueur 3 désignant
            respectivement le pourcentage de rouge, de vert et de bleu désignant la couleur.
        :return: dictionnaire des couleurs de la simulation, désignées par les clés COULEUR_ARBRE, COULEUR_FEU et
            COULEUR_CENDRE (chaque clé correspond dans le fichier de configuration au paramètre de même nom en lettres
            minuscules)
        """
        # Gestion de l'absence éventuelle du paramètre dans le fichier de configuration
        try:
            param_couleurs = self.sim_parametres["parametres"]["display"]["couleurs"]
        except:
            raise Exception("Le paramètre couleurs est manquant.")

        # Gestion de la bonne définition des couleurs
        try:
            couleur_metadata = {
                "COULEUR_ARBRE": [i / 255 for i in hex_to_rgb(param_couleurs["couleur_arbre_hex"])],
                "COULEUR_FEU": [i / 255 for i in hex_to_rgb(param_couleurs["couleur_feu_hex"])],
                "COULEUR_CENDRE": [i / 255 for i in hex_to_rgb(param_couleurs["couleur_cendre_hex"])],
            }
            return couleur_metadata
        except:
            raise Exception("Les couleurs n'ont pas été définies convenablement. Veuillez vérifier que tous les "
                            "paramètres sont présents (couleur_arbre_hex, couleur_feu_hex, couleur_cendre_hex) et "
                            "qu'ils ont pour valeur un code couleur hexadécimal de la forme #xxxxxx (x étant un "
                            "chiffre en hexadécimal).")

    def get_window_metadata_dictionary(self):
        """
        Retourne un dictionnaire contenant les valeurs des paramètres de configuration de la fenêtre d'affichage du
            graphe de simulation.
        :return: dictionnaire des paramètres de fenêtre de simulation, désignés par les clés WINDOW_EXTEND,
            WINDOW_WIDTH et WINDOW_HEIGHT (chaque clé correspond dans le fichier de configuration au paramètre de même
            nom en lettres minuscules)
        """
        # Gestion de l'absence éventuelle du paramètre dans le fichier de configuration
        try:
            param_window = self.sim_parametres["parametres"]["display"]["plot_window"]
        except:
            raise Exception("Le paramètre plot_window est manquant.")

        # Gestion de l'absence éventuelle d'un sous-paramètre
        try:
            window_extend = param_window["window_extend"]
            window_largeur = param_window["window_largeur"]
            window_hauteur = param_window["window_hauteur"]
        except:
            raise Exception("Un sous-paramètre de plot window semble manquant. Veuillez vérifier que les 3 paramètres "
                            "window_extend, window_largeur et window_hauteur sont bien présents.")

        # Gestion des types de ces paramètres

        window_metadata = {}

        if type(window_extend) == bool:
            window_metadata["WINDOW_EXTEND"] = window_extend
        else:
            raise Exception("Le paramètre window_extend doit être de type booléen (valeur true ou false uniquement).")

        try:
            window_largeur = int(abs(window_largeur))
            window_hauteur = int(abs(window_hauteur))

            window_metadata["WINDOW_WIDTH"] = window_largeur
            window_metadata["WINDOW_HEIGHT"] = window_hauteur

            return window_metadata
        except:
            raise Exception("Les dimensions de la fenêtre d'affichage (window_largeur et window_hauteur) n'ont pas pu "
                            "être lues en tant que nombres entiers positifs.")