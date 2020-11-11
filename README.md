# sim-feu-foret

Simulation d'un feu de forêt en Python 3.7

## Installation et lancement

## Configuration de la simulation

Il est possible de changer les métadonnées de la simulation via le fichier `config-sim.yml` à la racine du projet. Ci-dessous sont décrites les fonctions de chaque paramètre du fichier de configuration qu'il est possible de modifier.

### Paramètres de la simulation

**Paramètres principaux**

Paramètre | Type/Contraintes | Description
--- | --- | ---
`largeur_foret` | *Nombre entier positif* | Largeur de la forêt en nombre d'arbres (chaque arbre étant représenté par une case)
`hauteur_foret` | *Nombre entier positif* | Hauteur de la forêt en nombre d'arbres (chaque arbre étant représenté par une case)
`probabilite_propagation` | *Nombre décimal compris entre 0 et 1* | Probabilité qu'une case feu se propage à une case adjacente représentant un arbre

**Feux à l'état initial**

On définit les coordonnées des feux de départ dans la liste `feux_depart`. On marche chaque entrée d'un trait d'union et on lui donne les paramètres suivants :

Paramètre | Type/Contraintes | Description
--- | --- | ---
`ligne` | *Nombre entier positif strictement inférieur à `hauteur_foret`* | Coordonnée ligne de la case feu désignée dans la forêt
`colonne` | *Nombre entier positif strictement inférieur à `largeur_foret`* | Coordonnée colonne de la case feu désignée dans la forêt

### Paramètres d'affichage

**Paramètres principaux**

Paramètre | Type/Contraintes | Description
--- | --- | ---
`activer_logs_console` | *Booléen* | A définir sur `true` si l'on souhaite voir l'avancement du calcul de la simulation en console, `false` sinon (fait légèrement gagner en performance)
`play_animation` | *Booléen* | A définir sur `true` si l'on souhaite visualiser la totalité de la simulation sous forme d'animation, `false` si l'on souhaite simplement visualiser l'état initial et l'état final consécutivement
`fps_max_animation` | *Nombre entier positif* | Nombre maximum d'images par secondes que l'on souhaite afficher pour la simulation animée

**Couleurs de la simulation**

Sous le paramètre objet `couleurs` : 

Paramètre | Type/Contraintes | Description
--- | --- | ---
`couleur_arbre_hex` | *Code couleur hexadécimal (dans une chaîne de caractères)* | Couleur des cases représentant des arbres normaux
`couleur_feu_hex` | *Code couleur hexadécimal (dans une chaîne de caractères)* | Couleur des cases représentant des arbres en feu
`couleur_cendre_hex` | *Code couleur hexadécimal (dans une chaîne de caractères)* | Couleur des cases représentant des cendres

Un code couleur hexadécimal s'écrit sous la forme `#xxxxxx`, avec `x` un chiffre hexadécimal. Il s'agit en réalité de trois nombres hexadécimaux de longueur 2 concaténés, chacun représentant respectivement une valeur de rouge, vert et bleu allant de 0 à 255.

**Paramètres de la fenêtre de visualisation**

Sous le paramètre objet `plot_window` : 

Paramètre | Type/Contraintes | Description
--- | --- | ---
`window_extend` | *Booléen* | A définir sur `true` si l'on souhaite voir la simulation en plein écran (fenêtre maximisée), `false` si l'on préfère une fenêtre de taille plus réduite (fait légèrement gagner en performance)
`window_largeur` | *Nombre entier positif* | Largeur de la fenêtre de visualisation en pixels lorsque `window_extend` est défini sur `false`
`window_hauteur` | *Nombre entier positif* | Hauteur de la fenêtre de visualisation en pixels lorsque `window_extend` est défini sur `false`