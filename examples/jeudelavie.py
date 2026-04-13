import metagrid
from random import randint


# VARIABLES GLOBALES
WIDTH = 20
HEIGHT = 20

grille: list[list[int]]
running: bool

jeu = metagrid.create(HEIGHT, WIDTH, 20, 0)


@jeu.init
def init():
    global grille, running
    grille = [ [0]*WIDTH for _ in range(HEIGHT) ]
    running = False


@jeu.callback_click
def cliquer(i: int, j: int):
    """
    Callback de l'évènement click. i et j sont les coordonnées de la grille cliquées
    """
    global running, grille
    grille[i][j] = 1 - grille[i][j]
    draw()


@jeu.callback_key
def touche(car: str):
    """
    Callback de l'évènement touche appuyée.
    car est le caractère du clavier qui a été enfoncé
    """
    global running, grille
    if car == 's':
        running = not running
    elif car == 'a':
        grille = [ [randint(0,1) for _ in range(WIDTH)] for _ in range(HEIGHT) ]
        draw()


@jeu.update
def update():
    """
    Cette fonction sert à mettre à jour la grille à chaque fps si le flag running est True
    """
    global running, grille
    if running:
        grille = prochaine_grille(grille)


@jeu.draw
def draw():
    """
    Cette fonction sert à dessiner l'état courant de la grille
    """
    global running, grille
    for j in range(WIDTH):
        for i in range(HEIGHT):
            jeu.set_cell_color(i, j, "#000000" if grille[i][j] else "#FFFFFF")


#! FONCTIONS DU JEU

def nb_voisins(row: int, col: int, g: list[list[int]]) -> int:
    """Renvoie le nombre de voisins de la cellule de coordonnée (row, col) dans la grille g torique"""
    return sum(g[i%HEIGHT][j%WIDTH] for j in range(col-1, col+2) for i in range(row-1, row+2) if i!=row or j!=col)


def prochain_etat(row: int, col: int, g: list[list[int]]) -> int:
    """Renvoie le prochain etat d'une cellule en appliquant les règles du jeu de la vie"""
    return int(g[row][col] * (nb_voisins(row, col, g) in (2, 3)) or nb_voisins(row, col, g) == 3)


def prochaine_grille(g: list[list[int]]) -> list[list[int]]:
    """Renvoie la prochainne grille en appliquant les règles à toutes les cellules de la grille g"""
    return [[prochain_etat(i,j,g) for j in range(WIDTH)] for i in range(HEIGHT)]


jeu.start()
