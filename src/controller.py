import time

from src.models import Foret
from src.display import DisplaySimulation
from src.logger import SimulationLogger
from src.dataread import SimulationDataLoader


CONFIG_FILE_PATH_FROM_ROOT = "config-sim.yml"

# Initialisation des constantes de la simulation à l'aide d'un objet DataRead
config_reader = SimulationDataLoader(CONFIG_FILE_PATH_FROM_ROOT)

LARGEUR_FORET = config_reader.get_metadonnee_foret("largeur_foret", is_integer=True)
HAUTEUR_FORET = config_reader.get_metadonnee_foret("hauteur_foret", is_integer=True)
PROBABILITE_PROPAGATION = config_reader.get_metadonnee_foret("probabilite_propagation", is_integer=False)
FEUX_DEPART = config_reader.get_feux_depart()

ACTIVER_LOGS_CONSOLE = config_reader.get_display_bool_metadata("activer_logs_console")
PLAY_ANIMATION = config_reader.get_display_bool_metadata("play_animation")
INTERVALLE_ANIMATION = config_reader.get_intervalle_animation()

COULEUR_METADATA = config_reader.get_couleur_metadata_dictionary()

WINDOW_METADATA = config_reader.get_window_metadata_dictionary()

def launch_simulation():
    """
    Lance la simulation en tenant compte des paramètres définis par config-sim.yml
    """

    # Initialisation de la liste des états de la simulation représentés par des objets Foret
    simulation_states_forets = []
    foret = Foret(LARGEUR_FORET, HAUTEUR_FORET, FEUX_DEPART, PROBABILITE_PROPAGATION)
    simulation_states_forets.append(foret.copier())

    # Création du logger pour l'affichage console
    logger = SimulationLogger(foret, ACTIVER_LOGS_CONSOLE)

    # Calcul et stockage de tous les états de la simulation
    logger.log_simulation_computing_start()
    start_time = time.time()
    while foret.get_nb_feux() > 0:
        foret.propager_incendie()
        simulation_states_forets.append(foret.copier())
        logger.update_loading_bar()
    logger.end_loading_bar()

    # Affichage console des informations complémentaires calculées au cours de la simulation
    logger.log_simulation_report(time.time() - start_time)

    # Lancement de l'affichage de la simulation (choix de la méthode si on a choisi ou non d'afficher l'animation)
    logger.log_simulation_display_start()
    display = DisplaySimulation(simulation_states_forets, COULEUR_METADATA, WINDOW_METADATA)
    if PLAY_ANIMATION:
        display.show_simulation_animation(INTERVALLE_ANIMATION)
    else:
        display.show_simulation_start_and_final()

    # Indication de la fin du programme en console
    logger.log_end_of_program()
