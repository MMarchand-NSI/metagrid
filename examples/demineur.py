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
    """
    Représente une case de la grille du démineur.

    Attributs
    ---------
    est_mine : bool
        True si cette case cache une mine.
    nb_voisins : int
        Nombre de mines dans les 8 cases adjacentes (calculé une fois à l'init).
    revelee : bool
        True si la case a été découverte par le joueur.
    drapeau : bool
        True si le joueur a posé un drapeau sur cette case (clic droit).
    """
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
    """
    Initialise une nouvelle partie.

    Crée une grille vierge, place NB_MINES mines à des positions aléatoires
    (sans doublons), puis calcule pour chaque case le nombre de mines voisines.
    Cette fonction est appelée automatiquement par metagrid au démarrage.
    """
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
    """
    Compte le nombre de mines dans le voisinage de la case (i, j).

    On parcourt le carré 3×3 centré sur (i, j), en restant dans les bornes
    de la grille grâce à max/min, et en excluant la case elle-même.
    Le résultat (0 à 8) est stocké dans cellule.nb_voisins à l'initialisation.

    Paramètres
    ----------
    i : int
        Indice de ligne de la case.
    j : int
        Indice de colonne de la case.
    """
    res = 0
    for vi in range(max(0, i-1), min(HAUTEUR, i+2)):
        for vj in range(max(0, j-1), min(LARGEUR, j+2)):
            if not (vi == i and vj == j):
                res += grille[vi][vj].est_mine
    return res


def reveler_toutes_mines():
    """
    Marque toutes les mines de la grille comme révélées.

    Appelée lors d'un game over pour que draw() puisse les afficher.
    """
    for i in range(HAUTEUR):
        for j in range(LARGEUR):
            if grille[i][j].est_mine:
                grille[i][j].revelee = True


def est_gagne() -> bool:
    """
    Vérifie si le joueur a gagné la partie.

    La condition de victoire au démineur est : toutes les cases qui ne sont
    pas des mines ont été révélées. Les mines restent cachées (avec ou sans
    drapeau), seules les cases sûres doivent l'être toutes.

    Retourne True si la partie est gagnée, False sinon.
    """
    return all(
        grille[i][j].revelee
        for i in range(HAUTEUR)
        for j in range(LARGEUR)
        if not grille[i][j].est_mine
    )


def decouvre(i: int, j: int):
    """
    Révèle la case (i, j) et propage récursivement si elle n'a aucun voisin miné.

    C'est l'algorithme de « flood fill » (remplissage par diffusion) du démineur :
    - On révèle la case courante.
    - Si elle a au moins un voisin miné (nb_voisins > 0), on s'arrête là :
      le chiffre affiché suffit à guider le joueur.
    - Si elle n'a aucun voisin miné (nb_voisins == 0), on appelle récursivement
      decouvre() sur chacun de ses voisins non encore révélés et non minés.

    Cette récursion s'arrête naturellement car chaque case ne peut être révélée
    qu'une seule fois (on vérifie `not grille[vi][vj].revelee` avant de recurser).

    Paramètres
    ----------
    i : int
        Indice de ligne de la case à révéler.
    j : int
        Indice de colonne de la case à révéler.
    """
    cell = grille[i][j]
    cell.revelee = True
    if cell.nb_voisins == 0:
        for vi in range(max(0, i-1), min(HAUTEUR, i+2)):
            for vj in range(max(0, j-1), min(LARGEUR, j+2)):
                if not grille[vi][vj].revelee and not grille[vi][vj].est_mine:
                    decouvre(vi, vj)


def click(i: int, j: int, button: str):
    """
    Gère un clic sur la case (i, j).

    Clic gauche sur une case non révélée et sans drapeau :
      - Si c'est une mine → game over : on révèle toutes les mines.
      - Sinon → on découvre la case (avec propagation si nécessaire),
        puis on vérifie si la partie est gagnée.

    Clic droit sur une case non révélée :
      - Pose ou retire un drapeau. Le drapeau est un marqueur visuel que
        le joueur pose pour signaler une mine supposée ; il empêche un clic
        gauche accidentel sur cette case.

    Si la partie est terminée (game_over), tous les clics sont ignorés.

    Paramètres
    ----------
    i : int
        Indice de ligne de la case cliquée.
    j : int
        Indice de colonne de la case cliquée.
    button : str
        Bouton de la souris : "left" ou "right".
    """
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
    """
    Dessine l'état courant de la grille, case par case.

    Chaque case est affichée selon son état, par ordre de priorité :
      - Drapeau        → fond gris, lettre F rouge
      - Non révélée    → fond gris, pas de caractère
      - Mine révélée   → fond rouge, croix blanche (game over)
      - Chiffre        → fond blanc, nombre bleu (nb de mines voisines)
      - Case vide      → fond blanc, pas de caractère

    Cette fonction est appelée automatiquement par metagrid à chaque frame.
    """
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
