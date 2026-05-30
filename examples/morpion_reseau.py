"""
Morpion réseau
--------------
Jeu de morpion (tic-tac-toe) à 2 joueurs via le serveur de jeu.

Joueur 1 (crée la partie) :
    python morpion_reseau.py
    → note l'identifiant affiché dans la console, transmets-le au joueur 2

Joueur 2 (rejoint la partie) :
    python morpion_reseau.py XXXX12

Prérequis : pip install metagrid[network]
"""

import sys
import metagrid

# ──────────────────────────────────────────────────────────────────────────────
# Remplis ces deux valeurs avec celles fournies par ton enseignant
# ──────────────────────────────────────────────────────────────────────────────
URL   = "wss://game-server-brisk-skylark-1315.fly.dev/ws"     # adresse du serveur
TOKEN = "secret"           # mot de passe d'accès
# ──────────────────────────────────────────────────────────────────────────────

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


def coup_adversaire(state):
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
    if partie_terminee or not mon_tour or plateau[i][j] != 0:
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
    jeu = metagrid.create_networked(TAILLE, TAILLE, TAILLE_CASE, 10, url=URL, token=TOKEN)

    jeu.on_init(init)
    jeu.on_draw(draw)
    jeu.on_game_start(debut)
    jeu.on_opponent_move(coup_adversaire)
    jeu.on_opponent_left(adversaire_parti)
    jeu.on_click(cliquer)

    if len(sys.argv) == 1:
        game_id = jeu.create()
        print(f"\nPartie créée. Transmets cet ID à ton adversaire : {game_id}")
        print("En attente du second joueur...\n")
    else:
        game_id = sys.argv[1].upper()
        print(f"\nRejoindre la partie {game_id}...")
        jeu.join(game_id)

    jeu.start()
