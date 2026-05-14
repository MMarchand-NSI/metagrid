"""
2048
----
Fusionne des tuiles pour atteindre 2048.
Chaque valeur est représentée par une couleur distincte (palette classique du jeu).
Les victoires et défaites sont annoncées dans la console.

Refaire avec des images à la place des couleurs serait un bon exercice pour se familiariser avec les fonctions `set_cell_image` et `load_image`.

z : haut   s : bas   q : gauche   d : droite
r : recommencer
"""

import metagrid
from metagrid import AbstractEngine
from random import choice, random


TAILLE      = 4
TAILLE_CASE = 120

# Palette classique du jeu original
COULEURS: dict[int, str] = {
    0:    "#CDC1B4",
    2:    "#EEE4DA",
    4:    "#EDE0C8",
    8:    "#F2B179",
    16:   "#F59563",
    32:   "#F67C5F",
    64:   "#F65E3B",
    128:  "#EDCF72",
    256:  "#EDCC61",
    512:  "#EDC850",
    1024: "#EDC53F",
    2048: "#EDC22E",
}

grille: list[list[int]]
score: int
flag_game_over: bool

jeu: AbstractEngine


def cases_vides() -> list[tuple[int, int]]:
    return [(i, j) for i in range(TAILLE) for j in range(TAILLE) if grille[i][j] == 0]


def ajouter_tuile():
    """Fait apparaître un 2 (90 %) ou un 4 (10 %) dans une case vide aléatoire."""
    vides = cases_vides()
    if vides:
        i, j = choice(vides)
        grille[i][j] = 2 if random() < 0.9 else 4


def glisser_ligne(ligne: list[int]) -> tuple[list[int], int]:
    """Glisse et fusionne une ligne vers la gauche.
    Renvoie (nouvelle_ligne, points_gagnés).
    """
    tuiles = [x for x in ligne if x != 0]
    result: list[int] = []
    points = 0
    i = 0
    while i < len(tuiles):
        if i + 1 < len(tuiles) and tuiles[i] == tuiles[i + 1]:
            valeur = tuiles[i] * 2
            result.append(valeur)
            points += valeur
            i += 2
        else:
            result.append(tuiles[i])
            i += 1
    result += [0] * (TAILLE - len(result))
    return result, points


def appliquer_mouvement(sens: str) -> bool:
    """Applique un mouvement dans le sens donné et renvoie True si la grille a changé."""
    global score
    ancienne = [ligne[:] for ligne in grille]

    if sens in ('gauche', 'droite'):
        for i in range(TAILLE):
            ligne = grille[i] if sens == 'gauche' else grille[i][::-1]
            nouvelle, pts = glisser_ligne(ligne)
            grille[i] = nouvelle if sens == 'gauche' else nouvelle[::-1]
            score += pts
    else:
        for j in range(TAILLE):
            colonne = [grille[i][j] for i in range(TAILLE)]
            if sens == 'bas':
                colonne = colonne[::-1]
            nouvelle, pts = glisser_ligne(colonne)
            if sens == 'bas':
                nouvelle = nouvelle[::-1]
            for i in range(TAILLE):
                grille[i][j] = nouvelle[i]
            score += pts

    return grille != ancienne


def aucun_mouvement_possible() -> bool:
    """Renvoie True si aucun coup n'est jouable (grille pleine sans fusion possible)."""
    if cases_vides():
        return False
    for i in range(TAILLE):
        for j in range(TAILLE):
            if j + 1 < TAILLE and grille[i][j] == grille[i][j + 1]:
                return False
            if i + 1 < TAILLE and grille[i][j] == grille[i + 1][j]:
                return False
    return True


def init():
    global grille, score, flag_game_over
    grille = [[0] * TAILLE for _ in range(TAILLE)]
    score = 0
    flag_game_over = False
    ajouter_tuile()
    ajouter_tuile()


def touche(key: str):
    global flag_game_over
    if key == 'r':
        init()
        return
    if flag_game_over:
        return
    sens = {'z': 'haut', 's': 'bas', 'q': 'gauche', 'd': 'droite'}.get(key)
    if sens is None:
        return
    if not appliquer_mouvement(sens):
        return  # coup sans effet : pas de nouvelle tuile
    if any(grille[i][j] == 2048 for i in range(TAILLE) for j in range(TAILLE)):
        flag_game_over = True
        print(f"Félicitations ! Vous avez atteint 2048 ! Score : {score}")
    elif aucun_mouvement_possible():
        flag_game_over = True
        print(f"Game over ! Score final : {score}")
    else:
        ajouter_tuile()


COULEUR_TEXTE: dict[int, str] = {
    0: "#CDC1B4",   # invisible sur fond vide
    2: "#776E65",
    4: "#776E65",
}
TEXTE_CLAIR = "#F9F6F2"   # pour toutes les tuiles >= 8


def draw():
    for i in range(TAILLE):
        for j in range(TAILLE):
            val = grille[i][j]
            jeu.set_cell_color(i, j, COULEURS.get(val, "#3C3A32"))
            texte = str(val) if val != 0 else ""
            couleur_texte = COULEUR_TEXTE.get(val, TEXTE_CLAIR)
            jeu.set_cell_char(i, j, texte, couleur_texte)


if __name__ == "__main__":
    jeu = metagrid.create(TAILLE, TAILLE, TAILLE_CASE, 8)
    jeu.on_init(init)
    jeu.on_key(touche)

    jeu.on_draw(draw)
    jeu.start()
