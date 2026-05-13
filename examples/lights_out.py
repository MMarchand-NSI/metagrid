"""
Lights Out
----------
Toutes les cellules sont allumées ou éteintes.
Cliquer une cellule inverse son état et celui de ses 4 voisines.
But : éteindre toutes les lumières.

Touche r : recommencer.
"""

import metagrid
from metagrid import AbstractEngine
from random import randint


NB_LIGNES   = 5
NB_COLONNES = 5
TAILLE_CASE = 100

COULEUR_ALLUMEE  = "#FFDD00"
COULEUR_ETEINTE  = "#222222"
COULEUR_VICTOIRE = "#44FF88"

grille: list[list[bool]]  # True = allumée, False = éteinte
flag_game_over: bool

jeu: AbstractEngine


def toggle(i: int, j: int):
    """Inverse la cellule (i, j) et ses 4 voisines (haut, bas, gauche, droite)."""
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di == 0 or dj == 0:   # croix : on exclut les diagonales
                ni, nj = i + di, j + dj
                if 0 <= ni < NB_LIGNES and 0 <= nj < NB_COLONNES:
                    grille[ni][nj] = not grille[ni][nj]


def gagne() -> bool:
    """Renvoie True si toutes les cellules sont éteintes."""
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            if grille[i][j]:
                return False
    return True


def init():
    """Génère un nouveau puzzle garanti soluble.

    Principe : on part d'une grille entièrement éteinte,
    puis on lui applique 20 toggles aléatoires.
    """
    global grille, flag_game_over
    grille = [[False] * NB_COLONNES for _ in range(NB_LIGNES)]
    for _ in range(20):
        toggle(randint(0, NB_LIGNES - 1), randint(0, NB_COLONNES - 1))
    flag_game_over = False


def cliquer(i: int, j: int, _button: str):
    """Joue un coup sur la cellule (i, j) et vérifie la victoire."""
    global flag_game_over
    if flag_game_over:
        return
    toggle(i, j)
    if gagne():
        flag_game_over = True


def touche(key: str):
    """Gère les touches clavier : r pour recommencer."""
    if key == 'r':
        init()


def draw():
    """Colorie chaque cellule selon son état : allumée, éteinte, ou victoire."""
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            if flag_game_over:
                jeu.set_cell_color(i, j, COULEUR_VICTOIRE)
            elif grille[i][j]:
                jeu.set_cell_color(i, j, COULEUR_ALLUMEE)
            else:
                jeu.set_cell_color(i, j, COULEUR_ETEINTE)


if __name__ == "__main__":
    jeu = metagrid.create(NB_LIGNES, NB_COLONNES, TAILLE_CASE, 4)
    jeu.init(init)
    jeu.callback_click(cliquer)
    jeu.callback_key(touche)
    jeu.draw(draw)
    jeu.start()
