# Debian/Ubuntu :
# sudo apt install libgl1 libxrender1 libx11-6

import metagrid
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


def init():
    """
    Initialisation aléatoire d'une grille
    """
    global grille
    grille = [[Cellule() for _ in range(LARGEUR)] for _ in range(HAUTEUR)]

    # Poser les NB_MINES mines aléatoirement
    compteur  = 0
    while compteur<NB_MINES:
        i = randint(0, HAUTEUR-1)
        j = randint(0, LARGEUR-1)
        if not grille[i][j].est_mine :
            grille[i][j].est_mine = True
            compteur+=1

    # Calculer le nombre de mines voisines
    for i in range(0, HAUTEUR):
        for j in range(0, LARGEUR):
            grille[i][j].nb_voisins = get_mines_voisines(i, j)


def get_mines_voisines(i: int, j: int) -> int:
    res = 0
    for vi in range(max(0, i-1), min(HAUTEUR, i+2)):
        for vj in range(max(0, j-1), min(LARGEUR, j+2)):
            if not (vi==i and vj==j):
                res += grille[vi][vj].est_mine
    return res


def click(i: int, j: int, button: str):
    case = grille[i][j]
    if button == "left" and not case.drapeau:
        if case.est_mine:
            print("game over")
        else:
            decouvre(i,j)
    elif button == "right":
        case.drapeau = not case.drapeau


def decouvre(i: int, j: int):
    cell = grille[i][j]
    if cell.nb_voisins > 0:
        cell.revelee = True
    else:
        cell.revelee = True
        for vi in range(max(0, i-1), min(HAUTEUR, i+2)):
            for vj in range(max(0, j-1), min(LARGEUR, j+2)):
                if not grille[vi][vj].revelee:
                    decouvre(vi, vj)


def draw():
    for i in range(0, HAUTEUR):
        for j in range(0, LARGEUR):
            case = grille[i][j]
            
            if case.drapeau:
                game.set_cell_char(i,j,"F","#FF0000")
                continue
            if not case.revelee:
                game.set_cell_color(i,j,"#555555")
                continue
            else:
                game.set_cell_color(i,j,"#FFFFFF")

            if case.est_mine:
                game.set_cell_char(i,j,"X","#A72929")
            elif grille[i][j].nb_voisins>0:
                game.set_cell_char(i,j,str(case.nb_voisins), "#3418D4")


if __name__ == "__main__":
    game = metagrid.create(LARGEUR, HAUTEUR, 50, 1)
    game.init(init)
    game.callback_click(click)
    game.draw(draw)
    game.start()
