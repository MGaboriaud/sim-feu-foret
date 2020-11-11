class SimulationLogger:
    """
    Classe dont les instances permettent d'émettre des messages en console relatifs à la simulation
    # Attributs publics :
    - foret : objet Foret sur lequel sont effectués les calculs de la simulation (permet d'en déduire un avancement
        global du calcul)
    - display_logs : booléen indiquant si le logger doit effectivement afficher ses messages en console ou non
    # Constantes :
    - BAR_SIZE : taille de la barre de chargement dans la console (en caractères)
    """

    BAR_SIZE = 50

    def __init__(self, foret, display_logs):
        """
        Construit un objet SimulationLogger
        :param foret: objet Foret assigné à l'attribut foret
        :param display_logs: booléen assigné à display_logs
        """
        self.foret = foret
        self.__taille_foret = self.foret.get_largeur() * self.foret.get_hauteur()

        self.display_logs = display_logs

    def log_simulation_computing_start(self):
        """
        Affiche un simple message indiquant le début du calcul de la simulation
        Affichage activé uniquement si display_logs = True
        """
        if self.display_logs:
            print("--------------------")
            print("Calcul de la simulation en cours...")

    def update_loading_bar(self):
        """
        Affiche une barre de chargement et un pourcentage indiquant l'avancement du calcul de la simulation.
        Cette méthode invoquée une deuxième fois sans nouvelle ligne dans la console met à jour la barre de chargement
        Affichage activé uniquement si display_logs = True
        """
        if self.display_logs:
            avancement = self.foret.get_nb_cendres()
            progress_bar = avancement / self.__taille_foret
            print(
                "Avancement estimé : " + "%.2f" % (progress_bar * 100) + "%"
                + " | [" + '#' * int(progress_bar * self.BAR_SIZE) + ' ' * int((1.0 - progress_bar) * self.BAR_SIZE) + "]",
                end='\r',
                flush=True
            )

    def end_loading_bar(self):
        """
        Affiche les indications d'avancement à 100%.
        Méthode à invoquer après avoir fini le calcul de la simulation
        Affichage activé uniquement si display_logs = True
        """
        if self.display_logs:
            print("Avancement estimé : 100.00% | [" + '#' * int(self.BAR_SIZE) + "]")

    def log_simulation_report(self, elapsed_time_seconds):
        """
        Affiche un rapport de simulation (temps écoulé, pourcentage d'arbres brûlés...)
        Affichage activé uniquement si display_logs = True
        :param elapsed_time_seconds: temps de simulation écoulé calculé par le contrôleur
        """
        if self.display_logs:
            pourcentage_foret_brulee = self.foret.get_nb_cendres() * 100 / self.__taille_foret
            print("--------------------")
            print("Ecriture de la simulation terminée. (" + "%.3f" % (elapsed_time_seconds) + "s)")
            print("Arbres brûlés : " + str(self.foret.get_nb_cendres()) + " sur " + str(self.__taille_foret)
                  + " (" + "%.2f" % pourcentage_foret_brulee + "%)")

    def log_simulation_display_start(self):
        """
        Affiche un simple message indiquant le lancement de la visualisation de la simulation
        Affichage activé uniquement si display_logs = True
        """
        if self.display_logs:
            print("--------------------")
            print("Lancement de l'affichage graphique...")

    def log_end_of_program(self):
        """
        Affiche un simple message de fin de simulation, à invoquer juste avant l'arrêt du programme
        Affichage activé uniquement si display_logs = True
        """
        if self.display_logs:
            print("--------------------")
            print("Simulation terminée.")
            print("Arrêt du programme...")
            print("")