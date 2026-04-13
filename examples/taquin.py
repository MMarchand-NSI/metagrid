import metagrid
from random import choice, randint


NB_LIGNES = 4
NB_COLONNES = NB_LIGNES
TAILLE_CASE = 128

grille: list[list[int]] # grille comportant le numero des tiles
itrou: int              # indice ligne du trou
jtrou: int              # indice colonne du trou

jeu = metagrid.create(NB_LIGNES, NB_COLONNES, TAILLE_CASE, 0)

# Chargement de toutes les images dans le moteur
for i in range(16):
    jeu.load_image(f"tile{i}", f"assets/taquin/tile_{i}.png")


def melanger(n: int):
    """
    Répète n fois:
    - faire bouger aléatoirement en haut, en bas, à gauche, ou à droite.
    """
    global grille, itrou, jtrou
    for _ in range(n):
        if randint(0,1):
            bouge(itrou, jtrou+choice((-1,1)))
        else:
            bouge(itrou+choice((-1,1)), jtrou)


def gagne() -> bool:
    """
    si toutes les cases sont ordonnées, on a gagné
    """
    global grille
    return all(grille[i][j] == i * NB_COLONNES + j for i in range(NB_LIGNES) for j in range(NB_COLONNES))


def bouge(i: int, j: int):
    """
    Bouge la case (i,j) dans le trou
    Si le trou est bien autour de i et de j: le trou et (i, j) sont intervertis
    """
    global grille, itrou, jtrou
    if not ( 0<=i<NB_LIGNES and 0<=j<NB_COLONNES):
        return
    if ((itrou==i) and jtrou in (j-1, j+1)) or ((jtrou==j) and itrou in (i-1, i+1)):
        trou = grille[itrou][jtrou]
        grille[itrou][jtrou] = grille[i][j]
        grille[i][j] = trou
        itrou, jtrou = i, j

    if gagne():
        print("GAGNE")
        # Afficher écran de fin


@jeu.init
def init():
    """
    Initialisation des variables du jeu.
    Il suffit d'appeler cette procédure pour réinitialiser le jeu.
    """
    global grille, itrou, jtrou
    (itrou, jtrou) = (0, 3) # Dans l'exemple, le trou est à (0, 3). Exemple de déconstruction de tuple
    grille = [[i * NB_COLONNES + j for j in range(NB_COLONNES)] for i in range(NB_LIGNES)]
    melanger(100)


@jeu.callback_click
def cliquer(i: int, j: int):
    bouge(i, j)


@jeu.draw
def affiche_grille():
    """
    Méthode d'affichage du jeu
    """
    global grille, itrou, jtrou
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            if grille[i][j] != grille[itrou][jtrou]:
                jeu.set_cell_image(i, j, f"tile{grille[i][j]}")
            else:
                jeu.set_cell_color(i, j, "#FFFFFF")


@jeu.update
def update():
    pass


jeu.start()
