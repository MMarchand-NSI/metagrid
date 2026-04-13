import metagrid

grille: list[list[int]] = [
    [0, 1, 0, 0, 0],
    [0, 0, 2, 1, 0],
    [2, 0, 0, 0, 3],
    [0, 1, 0, 0, 3],
    [0, 0, 0, 0, 1],
]

game = metagrid.create(5, 5, 50, 1)

@game.init
def init():
    print("Jeu initialisé")


@game.callback_click
def clique(i: int, j: int):
    print(f"Case ({i}, {j}) cliquée")


@game.callback_key
def touche(key: str):
    print(f"Touche {key} enfoncée")


@game.update
def update():
    if game.frame_no % 120 == 0:
        print("Update quand le numéro de frame est un multiple de 120")


@game.draw
def draw():
    for i in range(5):
        for j in range(5):
            val = grille[i][j]
            if val == 1:
                game.set_cell_color(i, j, "#135683")
            elif val == 2:
                game.set_cell_char(i, j, "X", "#000000")


game.start()
