"""
Exemple complet d'utilisation du module metagrid.
=================================================

metagrid est un moteur de jeu en grille 2D. Il affiche une fenêtre contenant
une grille de cellules, et permet de réagir aux événements (clics, touches,
passage du temps) via des fonctions que l'on enregistre.

Structure d'un programme metagrid
----------------------------------
Un programme metagrid suit toujours le même schéma en cinq étapes :

    1. Définir les variables d'état du jeu (globales).
    2. Écrire les fonctions callbacks (on_init, on_update, on_draw, on_click, on_key).
    3. Dans le bloc if __name__ == "__main__" :
        a. Créer le moteur avec metagrid.create().
        b. Enregistrer chaque callback.
        c. Lancer la boucle de jeu avec game.start().

La boucle de jeu (gérée automatiquement par metagrid)
------------------------------------------------------
Une fois game.start() appelé, le moteur tourne en boucle à 60 images/seconde.
À chaque image (frame), il exécute dans l'ordre :
    1. update()  ← mettre à jour l'état du jeu
    2. draw()    ← redessiner la grille
Les callbacks de clic et de touche sont déclenchés dès qu'un événement arrive,
entre deux frames.
"""

import metagrid
from metagrid import AbstractEngine


# ---------------------------------------------------------------------------
# État du jeu
# ---------------------------------------------------------------------------
# La grille est une liste de listes d'entiers.
# Chaque entier représente ici le "type" de la cellule :
#   0 → cellule vide (fond blanc par défaut)
#   1 → cellule bleue
#   2 → cellule avec le caractère "X"
#   3 → cellule non traitée dans draw() : reste à la couleur par défaut
grille: list[list[int]] = [
    [0, 1, 0, 0, 0],
    [0, 0, 2, 1, 0],
    [2, 0, 0, 0, 3],
    [0, 1, 0, 0, 3],
    [0, 0, 0, 0, 1],
]

# `game` est l'objet moteur. Il est créé dans le bloc __main__ ci-dessous.
# On l'annote ici pour que l'éditeur connaisse son type et propose
# l'autocomplétion, sans lui assigner de valeur pour l'instant.
game: AbstractEngine


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------
# Les callbacks sont des fonctions ordinaires que l'on passe au moteur.
# metagrid les appelle automatiquement au bon moment.

def init():
    """
    Appelée une seule fois au démarrage, avant la première frame.

    C'est ici que l'on initialise toutes les variables d'état du jeu
    (positions de départ, score à zéro, grille vide, etc.).
    Dans cet exemple minimal, on se contente d'un message.
    """
    print("Jeu initialisé")


def clique(i: int, j: int, button: str):
    """
    Appelée chaque fois que l'utilisateur clique sur une cellule de la grille.

    Paramètres
    ----------
    i : int
        Indice de ligne de la cellule cliquée (0 = ligne du haut).
    j : int
        Indice de colonne de la cellule cliquée (0 = colonne de gauche).
    button : str
        Bouton utilisé : "left", "right" ou "middle".
    """
    print(f"Case ({i}, {j}) cliquée avec le bouton {button}")


def touche(key: str):
    """
    Appelée chaque fois que l'utilisateur appuie sur une touche du clavier.

    Paramètre
    ---------
    key : str
        Caractère correspondant à la touche pressée (ex. 'a', 'z', ' ').
        Les touches spéciales (flèches, Échap, Entrée…) sont transmises
        sous forme de chaîne décrivant la touche.
    """
    print(f"Touche {key} enfoncée")


def update():
    """
    Appelée à chaque frame, avant draw().

    C'est ici que l'on met à jour l'état du jeu : déplacer les personnages,
    vérifier les collisions, incrémenter les scores, etc.

    `game.frame_no` contient le numéro de la frame courante (commence à 0
    et s'incrémente de 1 à chaque image). Cela permet de déclencher des
    actions périodiques sans recourir à un timer externe.
    """
    # Exemple : afficher un message toutes les 2 secondes (120 frames à 60 fps)
    if game.frame_no % 120 == 0:
        print("Update quand le numéro de frame est un multiple de 120")


def draw():
    """
    Appelée à chaque frame, après update().

    C'est ici que l'on dessine l'état courant du jeu dans la grille.
    On parcourt toutes les cellules et on leur applique une couleur,
    une image ou un caractère selon leur valeur dans `grille`.

    Fonctions de dessin disponibles sur `game` :
        game.set_cell_color(i, j, "#RRGGBB")
            → colorie le fond de la cellule (i, j)
        game.set_cell_char(i, j, "X", "#RRGGBB")
            → affiche un caractère par-dessus le fond
        game.set_cell_image(i, j, "nom_image")
            → affiche une image chargée avec game.load_image()
    """
    for i in range(5):
        for j in range(5):
            val = grille[i][j]
            if val == 1:
                # Fond bleu foncé pour les cellules de type 1
                game.set_cell_color(i, j, "#135683")
            elif val == 2:
                # Lettre "X" noire pour les cellules de type 2
                # (le fond reste celui par défaut, ici blanc)
                game.set_cell_char(i, j, "X", "#000000")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------
# Le bloc if __name__ == "__main__" s'exécute uniquement quand on lance ce
# fichier directement (python full_example.py). Il ne s'exécute PAS si ce
# fichier est importé par un autre module, ce qui évite des effets de bord.

if __name__ == "__main__":
    # Créer le moteur : grille de 5 lignes × 5 colonnes,
    # cellules de 50 pixels, marges de 1 pixel entre les cellules.
    game = metagrid.create(5, 5, 50, 1)

    # Enregistrer les callbacks : on passe simplement la fonction (sans l'appeler).
    # metagrid se chargera de l'appeler au bon moment.
    game.on_init(init)             # appelée une fois au démarrage
    game.on_click(clique) # appelée à chaque clic sur la grille
    game.on_key(touche)   # appelée à chaque touche du clavier
    game.on_update(update)         # appelée à chaque frame, avant draw
    game.on_draw(draw)             # appelée à chaque frame, après update

    # Lancer la boucle de jeu. Cette ligne est bloquante :
    # le programme reste ici jusqu'à ce que l'utilisateur ferme la fenêtre.
    game.start()
