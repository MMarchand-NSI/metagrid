from typing import Callable
from abc import ABCMeta, abstractmethod

class AbstractEngine(metaclass = ABCMeta):
    """
    Abstracting the functionalities independently of its implementation
    """

    def __init__(self, nrows: int, ncols: int, cell_size: int, margin: int) -> None:
        self.margin: int = margin
        self.nrows: int = nrows
        self.ncols: int = ncols
        self.cell_size: int = cell_size
        self.fps: int = 60
        self.frame_no: int = 0

        self.on_init_fn: Callable[[], None] | None = None
        self.on_click_fn: Callable[[int, int, str], None] | None = None
        self.on_key_fn: Callable[[str], None] | None = None
        self.on_draw_fn: Callable[[], None] | None = None
        self.on_update_fn: Callable[[], None] | None = None


    def on_init(self, fn: Callable[[], None]) -> Callable[[], None]:
        """Decorator. Register the initialisation function."""
        self.on_init_fn = fn
        return fn

    def on_click(self, fn: Callable[[int, int, str], None]) -> Callable[[int, int, str], None]:
        """Decorator. Register the function called when a cell is clicked.
        The function receives (i, j, button) — grid coordinates and the button: "left", "right", or "middle".
        """
        self.on_click_fn = fn
        return fn

    def on_key(self, fn: Callable[[str], None]) -> Callable[[str], None]:
        """Decorator. Register the function called when a key is pressed.
        The function receives the pressed character as a string.
        """
        self.on_key_fn = fn
        return fn

    def on_draw(self, fn: Callable[[], None]) -> Callable[[], None]:
        """Decorator. Register the draw function, called every frame to render the grid."""
        self.on_draw_fn = fn
        return fn

    def on_update(self, fn: Callable[[], None]) -> Callable[[], None]:
        """Decorator. Register the update function, called every frame before draw."""
        self.on_update_fn = fn
        return fn


    @abstractmethod
    def start(self) -> None:
        """Start the game loop. Register all callbacks before calling this.

        Required: on_init, on_draw.
        Optional: on_update, on_click, on_key.
        """
        assert self.on_init_fn is not None, "An init function must be registered with @game.on_init"
        assert self.on_draw_fn is not None, "A draw function must be registered with @game.on_draw"
        self.on_init_fn()
        ...


    @abstractmethod
    def exit(self) -> None:
        """Exit the application"""
        ...

    @abstractmethod
    def set_cell_color(self, i: int, j: int, color: str) -> None:
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
        if len(char) > 1:
            raise ValueError(f"char must be a single character or empty string, got {char!r}")
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
