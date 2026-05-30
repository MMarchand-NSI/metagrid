# Metagrid

*[English version](https://github.com/MMarchand-NSI/metagrid/blob/main/README.md)*

## Description

Metagrid est une bibliothèque Python pour créer des jeux en grille 2D.
Une cellule de la grille peut afficher :

- une couleur unie
- une image
- un caractère

## Installation

```shell
pip install metagrid
```

---

## Tutoriel

### Structure d'un programme

Un programme metagrid suit toujours le même schéma en trois étapes :

1. Déclarer les variables d'état du jeu (globales).
2. Écrire les fonctions *callbacks* (`on_init`, `on_update`, `on_draw`, `on_click`, `on_key`).
3. Dans le bloc `if __name__ == "__main__"` : créer le moteur, enregistrer les callbacks, puis lancer la boucle avec `game.start()`.

---

### 1. Créer le moteur

```python
import metagrid

game = metagrid.create(nb_lignes, nb_colonnes, taille_case, marge)
```

| Paramètre     | Rôle                                           |
|---------------|------------------------------------------------|
| `nb_lignes`   | Nombre de lignes de la grille                  |
| `nb_colonnes` | Nombre de colonnes de la grille                |
| `taille_case` | Taille en pixels de chaque cellule             |
| `marge`       | Épaisseur en pixels de la bordure entre cases  |

---

### 2. Les callbacks

Les callbacks sont des fonctions ordinaires passées au moteur. Metagrid les appelle automatiquement au bon moment.

#### `on_init` — initialisation

Appelée **une seule fois** au démarrage, avant la première frame. C'est ici qu'on remet les variables d'état à zéro.

```python
def init():
    print("Jeu initialisé")

game.on_init(init)
```

#### `on_update` — logique de jeu

Appelée **à chaque frame**, avant le dessin. C'est ici qu'on fait avancer l'état du jeu.

`game.frame_no` contient le numéro de la frame courante (commence à 0, s'incrémente de 1 par frame). Utile pour déclencher des actions périodiques sans timer externe.

```python
def update():
    if game.frame_no % 120 == 0:   # toutes les 2 secondes à 60 fps
        print("tic")

game.on_update(update)
```

#### `on_draw` — dessin

Appelée **à chaque frame**, après `update`. C'est ici qu'on traduit l'état du jeu en couleurs / images / caractères.

```python
def draw():
    for i in range(5):
        for j in range(5):
            val = grille[i][j]
            if val == 1:
                game.set_cell_color(i, j, "#135683")
            elif val == 2:
                game.set_cell_char(i, j, "X", "#000000")

game.on_draw(draw)
```

#### `on_click` — clic souris

Appelée quand l'utilisateur clique sur une cellule.

```python
def clique(i: int, j: int, button: str):
    # i, j   : coordonnées de la cellule cliquée
    # button : "left", "right" ou "middle"
    print(f"Case ({i}, {j}) cliquée avec {button}")

game.on_click(clique)
```

#### `on_key` — touche clavier

Appelée quand l'utilisateur appuie sur une touche.

```python
def touche(key: str):
    # key : caractère ('a', 'z', ' ', …) ou nom de touche spéciale
    print(f"Touche {key} enfoncée")

game.on_key(touche)
```

---

### 3. Dessiner dans les cellules

Trois fonctions permettent de modifier l'apparence d'une cellule `(i, j)` (ligne `i`, colonne `j`, toutes deux à partir de 0 depuis le haut gauche) :

#### Couleur unie

```python
game.set_cell_color(i, j, "#RRGGBB")
```

#### Caractère

```python
game.set_cell_char(i, j, "A", "#RRGGBB")
```

Un seul caractère est affiché par cellule, centré, par-dessus le fond.

#### Image

Charger une image une seule fois (avant `game.start()`), puis l'afficher :

```python
game.load_image("nom_image", "chemin/vers/image.png")
# …
game.set_cell_image(i, j, "nom_image")
```

---

### 4. Lancer la boucle

```python
game.start()   # bloquant jusqu'à la fermeture de la fenêtre
```

---

### Exemple complet

```python
import metagrid
from metagrid import AbstractEngine

grille: list[list[int]] = [
    [0, 1, 0, 0, 0],
    [0, 0, 2, 1, 0],
    [2, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1],
]

game: AbstractEngine


def init():
    print("Jeu initialisé")


def clique(i: int, j: int, button: str):
    print(f"Case ({i}, {j}) cliquée avec le bouton {button}")


def touche(key: str):
    print(f"Touche {key} enfoncée")


def update():
    if game.frame_no % 120 == 0:
        print("Update toutes les 2 secondes")


def draw():
    for i in range(5):
        for j in range(5):
            val = grille[i][j]
            if val == 1:
                game.set_cell_color(i, j, "#135683")
            elif val == 2:
                game.set_cell_char(i, j, "X", "#000000")


if __name__ == "__main__":
    game = metagrid.create(5, 5, 50, 1)

    game.on_init(init)
    game.on_click(clique)
    game.on_key(touche)
    game.on_update(update)
    game.on_draw(draw)

    game.start()
```

Ce code est disponible en intégralité dans [`examples/full_example.py`](examples/full_example.py).

---

## Exemples inclus

| Fichier                              | Jeu          |
|--------------------------------------|--------------|
| [`examples/snake.py`](examples/snake.py) | Snake |
| [`examples/jeudelavie.py`](examples/jeudelavie.py) | Jeu de la vie |
| [`examples/jeu2048.py`](examples/jeu2048.py) | 2048 |
| [`examples/puissance4.py`](examples/puissance4.py) | Puissance 4 |
| [`examples/memory.py`](examples/memory.py) | Memory |
| [`examples/lights_out.py`](examples/lights_out.py) | Lights Out |
| [`examples/sokoban.py`](examples/sokoban.py) | Sokoban |
| [`examples/taquin.py`](examples/taquin.py) | Taquin |
| [`examples/wordle.py`](examples/wordle.py) | Wordle |
