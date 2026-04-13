from typing import Callable
from abc import ABCMeta, abstractmethod

class AbstractEngine(metaclass = ABCMeta):
    """
    Abstracting the functionalities independently of its implementation
    """

    def __init__(self, nb_lignes: int, nb_colonnes: int, cell_size: int, margin: int) -> None:
        """
        Initialisation du jeu.
        """
        self.margin: int = margin        # grid line with (px)
        self.nrows: int = nb_lignes      # Number of rows
        self.ncols: int = nb_colonnes    # Number of columns
        self.cell_size: int = cell_size  # Cell size
        self.fps: int = 60               # FPS, defaults to 60
        self.frame_no: int = 0           # Holds the number of frame since start

        self._init_fn: Callable[[], None] | None = None
        self.fn_click: Callable[[int, int], None] | None = None
        self.fn_key: Callable[[str], None] | None = None
        self.fn_draw: Callable[[], None] | None = None
        self.fn_update: Callable[[], None] | None = None


    def init(self, fn: Callable[[], None]) -> Callable[[], None]:
        """Decorator. Register the initialisation function."""
        self._init_fn = fn
        return fn

    def callback_click(self, fn: Callable[[int, int], None]) -> Callable[[int, int], None]:
        """Decorator. Register the function called when a cell is clicked.
        The function receives (i, j) — the grid coordinates of the clicked cell.
        """
        self.fn_click = fn
        return fn

    def callback_key(self, fn: Callable[[str], None]) -> Callable[[str], None]:
        """Decorator. Register the function called when a key is pressed.
        The function receives the pressed character as a string.
        """
        self.fn_key = fn
        return fn

    def draw(self, fn: Callable[[], None]) -> Callable[[], None]:
        """Decorator. Register the draw function, called every frame to render the grid."""
        self.fn_draw = fn
        return fn

    def update(self, fn: Callable[[], None]) -> Callable[[], None]:
        """Decorator. Register the update function, called every frame before draw."""
        self.fn_update = fn
        return fn


    @abstractmethod
    def start(self) -> None:
        """Start the game loop. Register all callbacks with decorators before calling this."""
        assert self._init_fn is not None, "An init function must be registered with @game.init"
        assert self.fn_draw is not None, "A draw function must be registered with @game.draw"
        assert self.fn_update is not None, "An update function must be registered with @game.update"
        self._init_fn()
        ...


    @abstractmethod
    def exit(self) -> None:
        """Exit the application"""
        ...

    @abstractmethod
    def set_cell_color(self, i: int, j: int, couleur: str) -> None:
        """Set the background color of cell (i, j). Clears any image previously set on that cell.
        Any character set via set_cell_char is drawn on top and is unaffected.

        Color format: "#RRGGBB" or "#RRGGBBAA"
        """
        ...

    @abstractmethod
    def set_cell_image(self, i: int, j: int, image: str) -> None:
        """Display an image in cell (i, j), replacing any color previously set on that cell.
        Any character set via set_cell_char is drawn on top and is unaffected.

        `image` must be a name previously registered with load_image().
        Raises KeyError if the image name is not found in the cache.
        """
        ...

    @abstractmethod
    def set_cell_char(self, i: int, j: int, char: str, color: str) -> None:
        """Draw a single character on top of cell (i, j), over any color or image.
        Pass an empty string to clear the character.

        Color format: "#RRGGBB" or "#RRGGBBAA"
        """
        assert len(char) < 2
        ...


    @abstractmethod
    def load_image(self, name: str, path: str) -> None:
        """
        Loads the image stored at `path` under the `name` key in the engine's textures cache
        You have to load all the images at startup, giving them a name that you will use in the function `set_cell_image`.

        Example use:
        >>> images = ["angel", "demon", "key", "door"]
        >>> for nom in images:
        ...     engine.load_image(nom, f"assets/wordle/{nom}.png")

        """
        ...


    @abstractmethod
    def play_sound(self, path: str) -> None:
        """
        Plays a sound file immediately when called, given its path.
        """
        ...
