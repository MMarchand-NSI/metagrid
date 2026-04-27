"""
Memory
------
Retrouvez toutes les paires de lettres identiques.
Cliquez sur deux cartes pour les retourner.
Si elles sont identiques, elles restent visibles.
Sinon, elles se retournent après un court délai.

Touche r : recommencer.
"""

import metagrid
from metagrid import AbstractEngine
from random import shuffle


NB_LIGNES        = 4
NB_COLONNES      = 4
TAILLE_CASE      = 110
DUREE_AFFICHAGE  = 90   # frames avant de retourner les cartes non appariées (~1.5s à 60fps)

COULEUR_DOS      = "#3D405B"  # carte face cachée
COULEUR_RETOURNEE = "#F2CC8F" # carte temporairement visible
COULEUR_TROUVEE  = "#81B29A"  # paire définitivement trouvée
COULEUR_TEXTE    = "#FFFFFF"

# 8 paires de lettres pour remplir la grille 4×4
LETTRES = [c for c in "ABCDEFGH" for _ in range(2)]

grille: list[list[str]]           # lettre de chaque carte
retournees: list[tuple[int, int]] # cartes actuellement face visible (0, 1 ou 2)
trouvees: list[tuple[int, int]]   # coordonnées des paires définitivement trouvées
delai: int                        # compte à rebours avant de rerourner les cartes non appariées
flag_game_over: bool

jeu: AbstractEngine


def init():
    """Mélange les cartes et remet tous les compteurs à zéro."""
    global grille, retournees, trouvees, delai, flag_game_over
    lettres = LETTRES[:]
    shuffle(lettres)
    grille = [[lettres[i * NB_COLONNES + j] for j in range(NB_COLONNES)] for i in range(NB_LIGNES)]
    retournees = []
    trouvees = []
    delai = 0
    flag_game_over = False


def cliquer(i: int, j: int):
    """Retourne la carte cliquée et vérifie si une paire est formée."""
    global delai, flag_game_over
    # Ignorer le clic si le délai est actif, si la carte est déjà trouvée ou déjà retournée
    if flag_game_over or delai > 0:
        return
    if (i, j) in trouvees or (i, j) in retournees:
        return

    retournees.append((i, j))

    if len(retournees) == 2:
        (i1, j1), (i2, j2) = retournees
        if grille[i1][j1] == grille[i2][j2]:
            # Paire trouvée : on la marque définitivement
            trouvees.extend(retournees)
            retournees.clear()
            if len(trouvees) == NB_LIGNES * NB_COLONNES:
                flag_game_over = True
                print("Bravo ! Toutes les paires trouvées !")
        else:
            # Pas une paire : démarrer le compte à rebours avant de retourner
            delai = DUREE_AFFICHAGE


def touche(key: str):
    """Gère les touches clavier : r pour recommencer."""
    if key == 'r':
        init()


def update():
    """Décrémente le délai et retourne les cartes non appariées quand il expire."""
    global delai
    if delai > 0:
        delai -= 1
        if delai == 0:
            retournees.clear()


def draw():
    """Affiche chaque carte selon son état : cachée, retournée ou trouvée."""
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            if (i, j) in trouvees:
                jeu.set_cell_color(i, j, COULEUR_TROUVEE)
                jeu.set_cell_char(i, j, grille[i][j], COULEUR_TEXTE)
            elif (i, j) in retournees:
                jeu.set_cell_color(i, j, COULEUR_RETOURNEE)
                jeu.set_cell_char(i, j, grille[i][j], COULEUR_TEXTE)
            else:
                jeu.set_cell_color(i, j, COULEUR_DOS)
                jeu.set_cell_char(i, j, '', COULEUR_TEXTE)


if __name__ == "__main__":
    jeu = metagrid.create(NB_LIGNES, NB_COLONNES, TAILLE_CASE, 6)
    jeu.init(init)
    jeu.callback_click(cliquer)
    jeu.callback_key(touche)
    jeu.update(update)
    jeu.draw(draw)
    jeu.start()
