# Metagrid

*[Version française](https://github.com/MMarchand-NSI/metagrid/blob/main/README.fr.md)*

## Description

Metagrid is a Python library for creating simple 2D grid games.
Each cell in the grid can display:

- a solid color
- an image
- a character

## Installation

```shell
pip install metagrid
```

---

## Tutorial

### Program structure

Every metagrid program follows the same three-step pattern:

1. Declare the game state variables (globals).
2. Write the *callback* functions (`on_init`, `on_update`, `on_draw`, `on_click`, `on_key`).
3. In the `if __name__ == "__main__"` block: create the engine, register the callbacks, then start the loop with `game.start()`.

---

### 1. Create the engine

```python
import metagrid

game = metagrid.create(rows, cols, cell_size, margin)
```

| Parameter   | Role                                        |
|-------------|---------------------------------------------|
| `rows`      | Number of rows in the grid                  |
| `cols`      | Number of columns in the grid               |
| `cell_size` | Size in pixels of each cell                 |
| `margin`    | Thickness in pixels of the border between cells |

---

### 2. Callbacks

Callbacks are plain functions passed to the engine. Metagrid calls them automatically at the right time.

#### `on_init` — initialization

Called **once** at startup, before the first frame. Reset all game state here.

```python
def init():
    print("Game initialized")

game.on_init(init)
```

#### `on_update` — game logic

Called **every frame**, before drawing. Advance the game state here.

`game.frame_no` holds the current frame number (starts at 0, increments by 1 per frame). Useful for triggering periodic actions without an external timer.

```python
def update():
    if game.frame_no % 120 == 0:   # every 2 seconds at 60 fps
        print("tick")

game.on_update(update)
```

#### `on_draw` — drawing

Called **every frame**, after `update`. Translate the game state into colors / images / characters here.

```python
def draw():
    for i in range(5):
        for j in range(5):
            val = grid[i][j]
            if val == 1:
                game.set_cell_color(i, j, "#135683")
            elif val == 2:
                game.set_cell_char(i, j, "X", "#000000")

game.on_draw(draw)
```

#### `on_click` — mouse click

Called when the user clicks on a cell.

```python
def click(i: int, j: int, button: str):
    # i, j   : coordinates of the clicked cell
    # button : "left", "right" or "middle"
    print(f"Cell ({i}, {j}) clicked with {button}")

game.on_click(click)
```

#### `on_key` — keyboard

Called when the user presses a key.

```python
def key(k: str):
    # k : character ('a', 'z', ' ', …) or special key name
    print(f"Key {k} pressed")

game.on_key(key)
```

---

### 3. Drawing in cells

Three functions change the appearance of cell `(i, j)` (row `i`, column `j`, both starting at 0 from the top-left):

#### Solid color

```python
game.set_cell_color(i, j, "#RRGGBB")
```

#### Character

```python
game.set_cell_char(i, j, "A", "#RRGGBB")
```

One character per cell, centered on top of the background.

#### Image

Load an image once (before `game.start()`), then display it:

```python
game.load_image("image_name", "path/to/image.png")
# …
game.set_cell_image(i, j, "image_name")
```

---

### 4. Start the loop

```python
game.start()   # blocks until the window is closed
```

---

### Full example

```python
import metagrid
from metagrid import AbstractEngine

grid: list[list[int]] = [
    [0, 1, 0, 0, 0],
    [0, 0, 2, 1, 0],
    [2, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1],
]

game: AbstractEngine


def init():
    print("Game initialized")


def click(i: int, j: int, button: str):
    print(f"Cell ({i}, {j}) clicked with {button}")


def key(k: str):
    print(f"Key {k} pressed")


def update():
    if game.frame_no % 120 == 0:
        print("Update every 2 seconds")


def draw():
    for i in range(5):
        for j in range(5):
            val = grid[i][j]
            if val == 1:
                game.set_cell_color(i, j, "#135683")
            elif val == 2:
                game.set_cell_char(i, j, "X", "#000000")


if __name__ == "__main__":
    game = metagrid.create(5, 5, 50, 1)

    game.on_init(init)
    game.on_click(click)
    game.on_key(key)
    game.on_update(update)
    game.on_draw(draw)

    game.start()
```

The full source is available in [`examples/full_example.py`](examples/full_example.py).

---

---

## Networked turn-based games

Metagrid supports 2-player networked games over WebSocket. Each player runs the same script; the server matches them and relays moves.

### For teachers — hosting the server

Teachers can self-host the game server using the open-source repository [MMarchand-NSI/game-server](https://github.com/MMarchand-NSI/game-server). Once deployed, share the server URL and access token with your students so they can fill in their `.env` file.

### Configuration

Create a `.env` file at the root of your project (fill in the values provided by your teacher):

```
METAGRID_URL=wss://...
METAGRID_TOKEN=your_token
```

The credentials are loaded automatically — you never write them in the Python file.

### Create the engine

```python
import metagrid

game = metagrid.create_networked(rows, cols, cell_size, margin)
```

### Extra callbacks

#### `on_game_start` — both players connected

```python
def start(i_go_first: bool):
    # i_go_first is True for the player who created the game
    pass

game.on_game_start(start)
```

#### `on_opponent_move` — opponent sent a move

```python
def opponent_move(state):
    # state is whatever was passed to game.send_move() by the opponent
    pass

game.on_opponent_move(opponent_move)
```

#### `on_opponent_left` — opponent disconnected

```python
def opponent_left():
    pass

game.on_opponent_left(opponent_left)
```

### Extra methods

| Method | Description |
|---|---|
| `game.send_move(state)` | Send the current game state to the opponent (any JSON-serialisable value) |
| `game.disconnect()` | Close the connection (call when the game is over) |

### Program structure

`game.start()` automatically asks whether to create or join a game before launching the loop.

```python
if __name__ == "__main__":
    game = metagrid.create_networked(rows, cols, cell_size, margin)

    game.on_init(init)
    game.on_draw(draw)
    game.on_game_start(start)
    game.on_opponent_move(opponent_move)
    game.on_opponent_left(opponent_left)
    game.on_click(click)

    game.start()
```
