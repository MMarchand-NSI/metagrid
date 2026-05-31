"""
Morpion réseau
--------------
Jeu de morpion (tic-tac-toe) à 2 joueurs via le serveur de jeu.

    python morpion_reseau.py

Prérequis : pip install metagrid[network] python-dotenv
Configure .env avec METAGRID_URL et METAGRID_TOKEN.
"""

import metagrid

TAILLE      = 3
TAILLE_CASE = 200

COULEUR_VIDE      = "#DDDDDD"
COULEUR_J1        = "#4A90D9"   # X — bleu
COULEUR_J2        = "#E05050"   # O — rouge
COULEUR_VICTOIRE  = "#4CAF50"   # vert : surligne les 3 cases gagnantes
COULEUR_DECONNEXION = "#FF9800" # orange : l'adversaire a quitté

SYMBOLES = {0: "", 1: "X", 2: "O"}
COULEURS  = {0: COULEUR_VIDE, 1: COULEUR_J1, 2: COULEUR_J2}

plateau:            list[list[int]]
mon_numero:         int | None              # 1 ou 2, connu après on_game_start
mon_tour:           bool
cellules_gagnantes: list[tuple[int, int]]
partie_terminee:    bool
adversaire_a_quitte: bool


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
    global plateau, mon_numero, mon_tour, cellules_gagnantes, partie_terminee, adversaire_a_quitte
    plateau = [[0] * TAILLE for _ in range(TAILLE)]
    mon_numero = None
    mon_tour = False
    cellules_gagnantes = []
    partie_terminee = False
    adversaire_a_quitte = False


def draw():
    gagnantes = set(cellules_gagnantes)
    for i in range(TAILLE):
        for j in range(TAILLE):
            val = plateau[i][j]
            if (i, j) in gagnantes:
                couleur = COULEUR_VICTOIRE
            elif adversaire_a_quitte:
                couleur = COULEUR_DECONNEXION
            else:
                couleur = COULEURS[val]
            jeu.set_cell_color(i, j, couleur)
            jeu.set_cell_char(i, j, SYMBOLES[val], "#FFFFFF")


def debut(je_commence: bool):
    global mon_numero, mon_tour
    mon_numero = 1 if je_commence else 2
    mon_tour = je_commence
    print(f"\n=== Partie commencée ! Tu joues {SYMBOLES[mon_numero]} ===")
    print("C'est ton tour." if mon_tour else "Attends le coup de l'adversaire.")


def coup_adversaire(state: list[list[int]]):
    global plateau, mon_tour, cellules_gagnantes, partie_terminee
    plateau = state
    cellules_gagnantes = trouver_alignement()
    if cellules_gagnantes:
        print("L'adversaire a gagné.")
        partie_terminee = True
        jeu.disconnect()
    elif match_nul():
        print("Match nul !")
        partie_terminee = True
        jeu.disconnect()
    else:
        mon_tour = True
        print("C'est ton tour.")


def adversaire_parti():
    global partie_terminee, adversaire_a_quitte
    print("L'adversaire a quitté la partie.")
    partie_terminee = True
    adversaire_a_quitte = True
    jeu.disconnect()


def cliquer(i: int, j: int, _bouton: str):
    global mon_tour, cellules_gagnantes, partie_terminee
    if partie_terminee or not mon_tour or mon_numero is None or plateau[i][j] != 0:
        return
    plateau[i][j] = mon_numero
    jeu.send_move(plateau)
    mon_tour = False
    cellules_gagnantes = trouver_alignement()
    if cellules_gagnantes:
        print("Tu as gagné !")
        partie_terminee = True
        jeu.disconnect()
    elif match_nul():
        print("Match nul !")
        partie_terminee = True
        jeu.disconnect()
    else:
        print("Coup envoyé. Attends l'adversaire...")


if __name__ == "__main__":
    jeu = metagrid.create_networked(TAILLE, TAILLE, TAILLE_CASE, 10)

    jeu.on_init(init)
    jeu.on_draw(draw)
    jeu.on_game_start(debut)
    jeu.on_opponent_move(coup_adversaire)
    jeu.on_opponent_left(adversaire_parti)
    jeu.on_click(cliquer)

    jeu.start()
