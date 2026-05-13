# Debian/Ubuntu :
# sudo apt install libgl1 libxrender1 libx11-6

import metagrid
from metagrid import AbstractEngine
from random import randint

HAUTEUR = 10
LARGEUR = 10
NB_MINES = 10


#? ETAT DU JEU

class Cellule:
    est_mine: bool
    nb_voisins: int
    revelee: bool
    drapeau: bool

    def __init__(self):
        self.est_mine = False
        self.nb_voisins = 0
        self.revelee = False
        self.drapeau = False

grille: list[list[Cellule]]
game_over: bool
game: AbstractEngine


def init():
    global grille, game_over
    game_over = False
    grille = [[Cellule() for _ in range(LARGEUR)] for _ in range(HAUTEUR)]

    compteur = 0
    while compteur < NB_MINES:
        i = randint(0, HAUTEUR-1)
        j = randint(0, LARGEUR-1)
        if not grille[i][j].est_mine:
            grille[i][j].est_mine = True
            compteur += 1

    for i in range(HAUTEUR):
        for j in range(LARGEUR):
            grille[i][j].nb_voisins = get_mines_voisines(i, j)


def get_mines_voisines(i: int, j: int) -> int:
    res = 0
    for vi in range(max(0, i-1), min(HAUTEUR, i+2)):
        for vj in range(max(0, j-1), min(LARGEUR, j+2)):
            if not (vi == i and vj == j):
                res += grille[vi][vj].est_mine
    return res


def reveler_toutes_mines():
    for i in range(HAUTEUR):
        for j in range(LARGEUR):
            if grille[i][j].est_mine:
                grille[i][j].revelee = True


def est_gagne() -> bool:
    return all(
        grille[i][j].revelee
        for i in range(HAUTEUR)
        for j in range(LARGEUR)
        if not grille[i][j].est_mine
    )


def decouvre(i: int, j: int):
    cell = grille[i][j]
    cell.revelee = True
    if cell.nb_voisins == 0:
        for vi in range(max(0, i-1), min(HAUTEUR, i+2)):
            for vj in range(max(0, j-1), min(LARGEUR, j+2)):
                if not grille[vi][vj].revelee and not grille[vi][vj].est_mine:
                    decouvre(vi, vj)


def click(i: int, j: int, button: str):
    global game_over
    if game_over:
        return
    case = grille[i][j]
    if button == "left" and not case.drapeau and not case.revelee:
        if case.est_mine:
            game_over = True
            reveler_toutes_mines()
            print("Game over !")
        else:
            decouvre(i, j)
            if est_gagne():
                game_over = True
                print("Gagné !")
    elif button == "right" and not case.revelee:
        case.drapeau = not case.drapeau


def draw():
    for i in range(HAUTEUR):
        for j in range(LARGEUR):
            case = grille[i][j]
            if case.drapeau:
                game.set_cell_color(i, j, "#555555")
                game.set_cell_char(i, j, "F", "#FF0000")
            elif not case.revelee:
                game.set_cell_color(i, j, "#555555")
                game.set_cell_char(i, j, "", "#000000")
            elif case.est_mine:
                game.set_cell_color(i, j, "#FF4444")
                game.set_cell_char(i, j, "X", "#FFFFFF")
            elif case.nb_voisins > 0:
                game.set_cell_color(i, j, "#FFFFFF")
                game.set_cell_char(i, j, str(case.nb_voisins), "#3418D4")
            else:
                game.set_cell_color(i, j, "#FFFFFF")
                game.set_cell_char(i, j, "", "#000000")


if __name__ == "__main__":
    game = metagrid.create(HAUTEUR, LARGEUR, 50, 1)
    game.on_init(init)
    game.on_click(click)
    game.on_draw(draw)
    game.start()
