# sim-feu-foret

Simulation d'un feu de forêt en Python 3.7

## Installation et lancement

## Configuration de la simulation

Il est possible de changer les métadonnées de la simulation via le fichier `config-sim.yml` à la racine du projet. Ci-dessous sont décrites les fonctions de chaque paramètre du fichier de configuration qu'il est possible de modifier.

### Paramètres de la simulation

**Paramètres scalaires**

Paramètre | Type/Contraintes | Description
--- | --- | ---
`largeur_foret` | *Nombre entier positif* | Largeur de la forêt en nombre d'arbres (chaque arbre étant représenté par une case)
`hauteur_foret` | *Nombre entier positif* | Hauteur de la forêt en nombre d'arbres (chaque arbre étant représenté par une case)
`probabilite_propagation` | *Nombre décimal compris entre 0 et 1* | Probabilité qu'une case feu se propage à une case adjacente représentant un arbre

**Feux à l'état initial

On définit les coordonnées des feux de départ dans la liste `feux_depart`. On marche chaque entrée d'un trait d'union et on lui donne les paramètres suivants :

Paramètre | Type/Contraintes | Description
--- | --- | ---
`ligne` | *Nombre entier positif strictement inférieur à `hauteur_foret`* | Coordonnée ligne de la case feu désignée dans la forêt
`colonne` | *Nombre entier positif strictement inférieur à `largeur_foret`* | Coordonnée colonne de la case feu désignée dans la forêt

### Paramètres d'affichage
- 
