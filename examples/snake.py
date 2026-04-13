import metagrid
from random import randint
import file  # pyright: ignore[reportImplicitRelativeImport]
from typing import TypeAlias

import logging

logging.basicConfig(level=logging.DEBUG)


#!#####################
#! VARIABLES GLOBALES #
#!#####################

#! CONSTANTES

HEIGHT = 30
WIDTH = 30
VITESSE = 10

#! ETAT DU JEU
Coord: TypeAlias = tuple[int, int]

# L'ensemble de ces variables est à mettre en global dans les fonctions

snake: file.File[Coord]  # Un snake est une file de coordonnées
pomme: Coord             # coordonnées de la pomme
dx: int                  # Déplacement horizontal du snake
dy: int                  # Déplacement vertical du snake
tete: Coord              # Coordonnées de la tete du snake
supprime: Coord | None   # Coordonnées de la dernière queue supprimée
game_over: bool          # flag indiquant si le jeu est terminé

jeu = metagrid.create(HEIGHT, WIDTH, 20, 1)
jeu.play_sound(r"assets/snake/snake.mp3")


#!############
#! CALLBACKS #
#!############

@jeu.init
def init():
    """
    Initialisation des variables globales
    """
    global snake, pomme, dx, dy, tete, supprime, game_over
    snake = file.creer()
    tete = (WIDTH//2, HEIGHT//2)
    supprime = None
    file.enfiler(tete, snake)
    (dx, dy) = (0, 0)
    spawn_pomme()
    game_over = False


@jeu.callback_key
def touche(car: str):
    """
    Callback de gestion des évènements clavier (déplacement du snake).
    """
    global snake, pomme, dx, dy, tete, supprime, game_over
    if car == "r":
        init()
        return
    if car == "d" and (dx, dy) != (0, -1):
        (dx, dy) = (0, 1)
    elif car == "z" and (dx, dy) != (1, 0):
        (dx, dy) = (-1, 0)
    elif car == "q" and (dx, dy) != (0, 1):
        (dx, dy) = (0, -1)
    elif car == "s" and (dx, dy) != (-1, 0):
        (dx, dy) = (1, 0)


@jeu.update
def update():
    global snake, pomme, dx, dy, tete, supprime, game_over

    if game_over:
        return

    if jeu.frame_no % VITESSE != 0:
        return

    tete = ( (tete[0]+dx) % WIDTH,  (tete[1]+dy) % HEIGHT )

    if tete in snake and (dx, dy) != (0,0):
        game_over = True
        jeu.play_sound(r"assets/sounds/gameover.mp3")

    if tete == pomme:
        spawn_pomme()
        jeu.play_sound(r"assets/snake/tasty.mp3")
    else:
        supprime = file.defiler(snake)

    file.enfiler(tete, snake)


@jeu.draw
def draw():
    global snake, tete, supprime, game_over
    if game_over:
        return
    if supprime:
        jeu.set_cell_color(supprime[0], supprime[1], "#FFFFFF")
    jeu.set_cell_color(tete[0], tete[1], "#00FF00")
    jeu.set_cell_color(pomme[0], pomme[1], "#FF0000")


#####################
# FONCTIONS DU JEU  #
#####################

def spawn_pomme():
    """
    On profite pour introduire légèrement à la récursivité
    """
    global snake, pomme, dx, dy, tete, supprime, game_over
    pomme = (randint(0, HEIGHT-1), randint(0, WIDTH-1))
    if pomme in snake:
        spawn_pomme()


jeu.start()
