"""
Morpion local
-------------
Jeu de morpion (tic-tac-toe) à 2 joueurs sur le même poste.

Les deux joueurs cliquent à tour de rôle dans la même fenêtre.

Pour passer à la version réseau, voir morpion_reseau.py.
Différences avec cette version :
  - metagrid.create_networked() au lieu de create()
  - mon_numero devient fixe (1 ou 2 selon qui crée/rejoint)
  - la logique de fin de tour passe par send_move() et on_opponent_move
"""

import metagrid

TAILLE      = 3
TAILLE_CASE = 200

COULEUR_VIDE     = "#DDDDDD"
COULEUR_J1       = "#4A90D9"   # X — bleu
COULEUR_J2       = "#E05050"   # O — rouge
COULEUR_VICTOIRE = "#4CAF50"   # vert : surligne les 3 cases gagnantes

SYMBOLES = {0: "", 1: "X", 2: "O"}
COULEURS  = {0: COULEUR_VIDE, 1: COULEUR_J1, 2: COULEUR_J2}

plateau:            list[list[int]]
mon_numero:         int                    # joueur courant : 1 ou 2
cellules_gagnantes: list[tuple[int, int]]
partie_terminee:    bool


def trouver_alignement() -> list[tuple[int, int]]:
    """Renvoie les 3 cases gagnantes, ou [] si aucune victoire."""
    for joueur in (1, 2):
        for i in range(TAILLE):
            if all(plateau[i][j] == joueur for j in range(TAILLE)):
                return [(i, j) for j in range(TAILLE)]
        for j in range(TAILLE):
            if all(plateau[i][j] == joueur for i in range(TAILLE)):
                return [(i, j) for i in range(TAILLE)]
        if all(plateau[i][i] == joueur for i in range(TAILLE)):
            return [(i, i) for i in range(TAILLE)]
        if all(plateau[i][TAILLE - 1 - i] == joueur for i in range(TAILLE)):
            return [(i, TAILLE - 1 - i) for i in range(TAILLE)]
    return []


def match_nul() -> bool:
    return all(plateau[i][j] != 0 for i in range(TAILLE) for j in range(TAILLE))


def init():
    global plateau, mon_numero, cellules_gagnantes, partie_terminee
    plateau = [[0] * TAILLE for _ in range(TAILLE)]
    mon_numero = 1
    cellules_gagnantes = []
    partie_terminee = False
    print(f"\n=== Joueur 1 (X) commence. ===")


def draw():
    gagnantes = set(cellules_gagnantes)
    for i in range(TAILLE):
        for j in range(TAILLE):
            val = plateau[i][j]
            couleur = COULEUR_VICTOIRE if (i, j) in gagnantes else COULEURS[val]
            jeu.set_cell_char(i, j, SYMBOLES[val], "#FFFFFF")
            jeu.set_cell_color(i, j, couleur)


def cliquer(i: int, j: int, _bouton: str):
    global mon_numero, cellules_gagnantes, partie_terminee
    if partie_terminee or plateau[i][j] != 0:
        return
    plateau[i][j] = mon_numero
    cellules_gagnantes = trouver_alignement()
    if cellules_gagnantes:
        print(f"Joueur {mon_numero} ({SYMBOLES[mon_numero]}) a gagné !")
        partie_terminee = True
    elif match_nul():
        print("Match nul !")
        partie_terminee = True
    else:
        mon_numero = 2 if mon_numero == 1 else 1
        print(f"Tour du joueur {mon_numero} ({SYMBOLES[mon_numero]}).")


if __name__ == "__main__":
    jeu = metagrid.create(TAILLE, TAILLE, TAILLE_CASE, 10)
    jeu.on_init(init)
    jeu.on_draw(draw)
    jeu.on_click(cliquer)
    jeu.start()
