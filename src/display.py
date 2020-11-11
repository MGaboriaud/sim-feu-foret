import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize
from matplotlib.animation import FuncAnimation


class DisplaySimulation:
    """
    Classe prenant en charge l'affichage graphique de la simulation
    # Attributs publics:
    - fig : objet figure de Pyplot, représente la figure liée à notre simulation
    - simulation_states_forets : liste d'objets Foret représentant chaque état de la simulation
    - couleur_arbre : tuple ou liste de longueur 3 représentant la couleur d'une case arbre sous forme de valeurs RVB
        allant de 0 à 1
    - couleur_feu : tuple ou liste de longueur 3 analogue à couleur_arbre pour la couleur du feu cette fois
    - couleur_cendre : tuple ou liste de longueur 3 analogue à couleur_arbre pour la couleur de la cendre cette fois
    """

    def __init__(self, simulation_states, couleur_metadata, window_metadata):
        """
        Construit un objet DisplaySimulation
        :param simulation_states: liste d'objets Foret qui sera affectée à l'attribut simulation_states_forets
        :param couleur_metadata: dictionnaire des valeurs à affecter aux 3 attributs couleur sous la forme suivante :
            { "COULEUR_ARBRE": couleur_arbre, "COULEUR_FEU": couleur_feu, "COULEUR_CENDRE": couleur_cendre }
        :param window_metadata: dictionnaire des valeurs définissant l'affichage de la fenêtre de visualisation sous la
            forme suivante :
            { "WINDOW_EXTEND": window_extend, "WINDOW_WIDTH": window_width, "WINDOW_HEIGHT": window_height }
            window_extend est un booléen indiquant si l'on souhaite maximiser la fenêtre ou non
            window_width est la largeur que l'on souhaite donner à la fenêtre en pixels (si window_extend = false)
            window_height est la hauteur que l'on souhaite donner à la fenêtre en pixels (si window_extend = false)
        """
        self.fig = plt.figure()
        plt.axis('off')

        self.simulation_states_forets = simulation_states

        self.couleur_arbre = couleur_metadata["COULEUR_ARBRE"]
        self.couleur_feu = couleur_metadata["COULEUR_FEU"]
        self.couleur_cendre = couleur_metadata["COULEUR_CENDRE"]
        self.__cmap = LinearSegmentedColormap.from_list('etat_arbre', [self.couleur_arbre, self.couleur_feu, self.couleur_cendre], N=3)

        # Initialisation de la légende du graphe avec les comptes de chaque type de case
        self.__patch_arbres = mpatches.Patch(color=self.couleur_arbre)
        self.__patch_feu = mpatches.Patch(color=self.couleur_feu)
        self.__patch_cendre = mpatches.Patch(color=self.couleur_cendre)

        # Initialisation des attributs utiles à la méthode prepare_window()
        self.__window_extend = window_metadata["WINDOW_EXTEND"]
        self.__window_width = window_metadata["WINDOW_WIDTH"]
        self.__window_height = window_metadata["WINDOW_HEIGHT"]

    def prepare_window(self):
        """
        Permet d'appliquer les paramètres d'affichage de la fenêtre de visualisation (plein écran / windowed)
        A invoquer avant plt.show()
        """
        mng = plt.get_current_fig_manager()
        if self.__window_extend:
            # En mode plein écran, on maximise la taille de la fenêtre
            mng.resize(*mng.window.maxsize())
        else:
            mng.resize(self.__window_width, self.__window_height)
            # En mode windowed, on centre la fenêtre de visualisation sur l'écran après sa redimension
            mng.window.wm_geometry(
                "+" + str((mng.window.wm_maxsize()[0] - self.__window_width) // 2)
                + "+" + str((mng.window.wm_maxsize()[1] - self.__window_height) // 2)
            )

    def plot_simulation_step(self, i):
        """
        Entre dans le graphe de visualisation les données de la forêt d'indice i dans simulation__states_forets
        A la suite de l'appel de cette méthode, il est nécessaire d'invoquer plt.show() pour visualiser le graphe
        :param i: indice entre 0 et len(simulation_states_forets)-1 désignant l'état de la simulation à afficher
        """
        foret = self.simulation_states_forets[i]

        # On efface la figure précédente pour gagner en performance
        self.fig.clf()

        # Mise à jour de la légende
        self.__patch_arbres.set_label(foret.get_nb_arbres())
        self.__patch_feu.set_label(foret.get_nb_feux())
        self.__patch_cendre.set_label(foret.get_nb_cendres())
        legend_handles = [self.__patch_arbres, self.__patch_feu, self.__patch_cendre]

        # Entrée des données dans le graphe
        plt.imshow(foret.grille_arbres, cmap=self.__cmap, interpolation="nearest", norm=Normalize(0.0, 2.0))
        plt.legend(handles=legend_handles, bbox_to_anchor=(1.05, 1), loc='upper left',
                   borderaxespad=0.)

    def show_simulation_start_and_final(self):
        """
        Affiche dans deux fenêtres de graphe consécutives l'état initial puis l'état final de la simulation
        """

        # Affichage de l'état de départ de la forêt
        self.prepare_window()
        self.plot_simulation_step(0)
        plt.show()

        # Réinitialisation de la figure pour le bon affichage de la figure suivante
        self.fig = plt.figure()

        # Affichage de l'état d'arrivée de la forêt
        self.prepare_window()
        self.plot_simulation_step(-1)
        plt.show()

    def show_simulation_animation(self, intervalle):
        """
        Affiche dans une fenêtre de graphe la totalité de la simulation sous forme d'animation à une vitesse définie
            par le paramètre intervalle
        :param intervalle: délai en millisecondes entre l'affichage de 2 états consécutifs de la simulation
        """

        self.prepare_window()

        # Cette fonction sera appelée à chaque image d'indice i de l'animation
        def animation_frame(i):
            self.plot_simulation_step(i)

        # Lancement et affichage de l'animation sur exactement le nombre d'images donné par simulation_states_forets
        nb_frames = len(self.simulation_states_forets)
        animation = FuncAnimation(self.fig, func=animation_frame, frames=nb_frames, interval=intervalle, repeat=False)
        plt.show()