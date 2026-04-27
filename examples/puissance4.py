"""
Puissance 4
-----------
Deux joueurs s'affrontent en tour par tour.
Cliquer une colonne (n'importe quelle ligne) pour y faire tomber un jeton.
On peut aussi utiliser les touches 1 à 7.
Premier à aligner 4 jetons (horizontalement, verticalement ou en diagonale) gagne.

Joueur 1 : rouge   Joueur 2 : jaune
Touche r : recommencer.
"""

import metagrid
from metagrid import AbstractEngine


NB_LIGNES   = 6
NB_COLONNES = 7
TAILLE_CASE = 80

COULEUR_FOND    = "#1133AA"  # bleu foncé : le plateau
COULEUR_J1      = "#EE2222"  # rouge : joueur 1
COULEUR_J2      = "#FFDD00"  # jaune : joueur 2
COULEUR_VICTOIRE = "#0CDB1E" # vert : surligne les 4 jetons gagnants

grille: list[list[int]]           # 0 = vide, 1 = joueur 1, 2 = joueur 2
joueur_courant: int               # 1 ou 2
cellules_gagnantes: list[tuple[int, int]]
flag_game_over: bool

jeu: AbstractEngine


def trouver_alignement(i: int, j: int) -> list[tuple[int, int]]:
    """
    Après qu'un jeton vient d'être posé en (i, j), cherche un alignement de 4.
    Renvoie la liste des cellules alignées, ou [] si personne n'a gagné.
    """
    joueur = grille[i][j]
    for di, dj in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        cellules = [(i, j)]
        for sens in (1, -1):
            ni, nj = i + sens * di, j + sens * dj
            while 0 <= ni < NB_LIGNES and 0 <= nj < NB_COLONNES and grille[ni][nj] == joueur:
                cellules.append((ni, nj))
                ni += sens * di
                nj += sens * dj
        if len(cellules) >= 4:
            return cellules
    return []


def placer_jeton(col: int) -> int | None:
    """Place le jeton du joueur courant dans la colonne `col`.
    Renvoie l'indice de ligne où il atterrit, ou None si la colonne est pleine.
    """
    for i in range(NB_LIGNES - 1, -1, -1):
        if grille[i][col] == 0:
            grille[i][col] = joueur_courant
            return i
    return None


def apres_coup(i: int, col: int):
    """Détecte la victoire et passe au joueur suivant après un jeton posé en (i, col)."""
    global joueur_courant, cellules_gagnantes, flag_game_over
    cellules_gagnantes = trouver_alignement(i, col)
    if cellules_gagnantes:
        flag_game_over = True
        nom = "Rouge" if joueur_courant == 1 else "Jaune"
        print(f"Joueur {joueur_courant} ({nom}) a gagné !")
    else:
        joueur_courant = 2 if joueur_courant == 1 else 1


def jouer_dans_colonne(col: int):
    """Orchestre un coup : vérifie les gardes, place le jeton, traite le résultat."""
    if flag_game_over or not (0 <= col < NB_COLONNES):
        return
    i = placer_jeton(col)
    if i is not None:
        apres_coup(i, col)


def init():
    global grille, joueur_courant, cellules_gagnantes, flag_game_over
    grille = [[0] * NB_COLONNES for _ in range(NB_LIGNES)]
    joueur_courant = 1
    cellules_gagnantes = []
    flag_game_over = False


def cliquer(i: int, j: int):
    # On ignore la ligne cliquée : seule la colonne compte (gravité)
    jouer_dans_colonne(j)


def touche(key: str):
    if key == 'r':
        init()
    elif '1' <= key <= '7':
        jouer_dans_colonne(int(key) - 1)


def draw():
    couleurs = {0: COULEUR_FOND, 1: COULEUR_J1, 2: COULEUR_J2}
    gagnantes = set(cellules_gagnantes)
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            if (i, j) in gagnantes:
                jeu.set_cell_color(i, j, COULEUR_VICTOIRE)
            else:
                jeu.set_cell_color(i, j, couleurs[grille[i][j]])


if __name__ == "__main__":
    jeu = metagrid.create(NB_LIGNES, NB_COLONNES, TAILLE_CASE, 4)
    jeu.init(init)
    jeu.callback_click(cliquer)
    jeu.callback_key(touche)

    jeu.draw(draw)
    jeu.start()
