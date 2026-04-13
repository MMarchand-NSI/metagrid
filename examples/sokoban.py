import metagrid
from sokoban_maps import maps, tiles  # pyright: ignore[reportImplicitRelativeImport]
import sys


grille: list[list[int]] # map du sokoban
ikeeper: int            # indice ligne du gardien
jkeeper: int            # indice colonne du gardien
flag_game_over: bool    # True si le jeu est terminé

niveau = int(sys.argv[1])
if not (0 <= niveau < len(maps)):
    raise ValueError(f"Le niveau doit être compris entre 0 et {len(maps)-1}")

jeu = metagrid.create(len(maps[niveau]), len(maps[niveau][0]), 32, 0)

# Chargement des tiles
for nom in tiles.values():
    jeu.load_image(nom, f"assets/sokoban/{nom}.png")

jeu.play_sound(r"assets/sounds/sokoban_intro.mp3")


def get_nb_colonnes():
    return len(grille[0])

def get_nb_lignes() -> int:
    return len(grille)

def find_keeper() -> tuple[int, int]:
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if tiles[grille[i][j]] in ('keeper', 'keeper_on_target'):
                return (i, j)
    raise ValueError(f"Pas de gardien sur la map {niveau}")

def gagne() -> bool:
    """
    On a gagné s'il n'y a plus de 4 dans la grille
    """
    return not any(e==4 for ligne in grille for e in ligne)


@jeu.init
def init():
    global ikeeper, jkeeper, grille, flag_game_over
    grille = [[e for e in ligne] for ligne in maps[niveau]]
    ikeeper, jkeeper = find_keeper()
    flag_game_over = False


@jeu.callback_key
def touche(c: str):
    """
    D'après le déplacement voulu, on s'intéresse à la prochaine case,
    et si c'est un cargo, à la suivante pour vérifier qu'on peut l'y déplacer
    """
    global grille, ikeeper, jkeeper, flag_game_over

    if c == 'r':
        init()
        return

    if flag_game_over:
        return

    di, dj = (0, 0)
    match c:
        case 'z':   # haut
            di, dj = (-1, 0)
        case 'd':   # droite
            di, dj = (0, 1)
        case 's':   # bas
            di, dj = (1, 0)
        case 'q':   # gauche
            di, dj = (0, -1)
        case _:
            pass

    next = grille[ikeeper+di][jkeeper+dj]
    # Est-ce que la prochaine case est le sol ou une cible?
    if tiles[next] in ('floor', 'target'):
        # deplacer le keeper
        grille[ikeeper+di][jkeeper+dj] += 4 # keeper ou keeper_target laisse sa place à floor ou target
        grille[ikeeper][jkeeper] -= 4  # floor ou target recoivent keeper ou keeper_target
        # maj des indices keeper
        ikeeper = ikeeper+di
        jkeeper = jkeeper+dj
    # Sinon si c'est un cargo
    elif tiles[next] in ('cargo', 'cargo_on_target'):
        next2 = grille[ikeeper+2*di][jkeeper+2*dj]
        # qu'y-a-til apres le cargo?
        if tiles[next2] in ('floor', 'target'):
            # déplacer le cargo et le keeper
            grille[ikeeper][jkeeper] -= 4  # keeper ou keeper_target laisse sa place à floor ou target
            grille[ikeeper+di][jkeeper+dj] += 2  # cargo ou cargo_target laisse sa place à keeper ou keeper_target
            grille[ikeeper+2*di][jkeeper+2*dj] += 2  # cargo ou cargo_target arrive sur floor ou target
            # maj indices keeper
            ikeeper = ikeeper+di
            jkeeper = jkeeper+dj

    if gagne():
        flag_game_over = True
        jeu.play_sound(r"assets/sounds/victory.mp3")


@jeu.draw
def dessiner():
    for i in range(get_nb_lignes()):
        for j in range(get_nb_colonnes()):
            jeu.set_cell_image(i, j, tiles[grille[i][j]])


@jeu.update
def update():
    pass


jeu.start()
