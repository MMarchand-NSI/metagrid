from pathlib import Path
from arcade.sound import Sound
from arcade.application import View
from arcade.application import Window
from arcade.sprite.colored import SpriteSolidColor
from arcade.texture.texture import Texture
from typing_extensions import override

import pyglet.image

from arcade.types import Color, RGBOrA255
from .abstract import AbstractEngine
from typing import Callable
from PIL import Image
import arcade
import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _hex_to_rgb(hex_color: str) -> RGBOrA255:
    assert bool(re.fullmatch(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})", hex_color)), f"Bad color format for #RRGGBB/#RRGGBBAA: {hex_color}"

    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        return tuple[int, int, int](int(hex_color[i:i+2], 16) for i in (0, 2, 4)) #type: ignore
    elif len(hex_color) == 8:
        return tuple[int, int, int, int](int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6)) #type: ignore
    else:
        raise ValueError("Invalid hex color format")



class ArcadeEngine(AbstractEngine):
    def __init__(self, nb_lignes: int, nb_colonnes: int, cell_size: int, margin: int) -> None:
        super().__init__(nb_lignes, nb_colonnes, cell_size, margin)
        WINDOW_WIDTH = (self.cell_size + self.margin) * self.ncols + self.margin
        WINDOW_HEIGHT = (self.cell_size + self.margin) * self.nrows + self.margin
        WINDOW_TITLE = ""

        self.window: Window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        
        # Charger l'icône depuis assets/
        self._load_icon()
        
        self.view: GameView = GameView(self)
        self.frame_no: int = 0
    
    def _load_icon(self) -> None:
        """Load window icon from package assets directory."""
        try:
            icon_path = Path(__file__).parent.parent / "assets" / "grille_icon_256.png"
            
            if icon_path.exists():
                # Charger l'image
                icon = pyglet.image.load(str(icon_path))
                # Convertir en ImageData
                self.window.set_icon(icon.get_image_data())
        except Exception:
            pass
        
    @override
    def start(self) -> None:
        super().start()
        self.window.show_view(self.view)
        arcade.run()


    @override
    def exit(self) -> None:
        self.window.close()

    @override
    def set_cell_color(self, i: int, j: int, couleur: str) -> None:
        """permet de colorier une case de la grille"""
        if i >= self.nrows or j >= self.ncols:
            raise IndexError("Index of of bound")
        i = self.nrows - 1 - i

        # TODO improve by not recreating each time
        empty_image = Image.new("RGBA", (self.cell_size, self.cell_size), (255, 255, 255, 255))
        empty_texture = arcade.Texture(name="vide", image=empty_image)

        self.view.grid_sprites[i][j].texture = empty_texture
        self.view.grid_sprites[i][j].color = _hex_to_rgb(couleur)

    @override
    def set_cell_image(self, i: int, j: int, image: str) -> None:
        """Color cell i,j with image in cache"""
        if i >= self.nrows or j >= self.ncols:
            return
        if image not in self.view.textures:
            raise KeyError(f"Image '{image}' not loaded. Call load_image('{image}', path) first.")
        i = self.nrows - 1 - i
        self.view.grid_sprites[i][j].color = _hex_to_rgb("#FFFFFFFF")
        self.view.grid_sprites[i][j].texture = self.view.textures[image]

    @override
    def set_cell_char(self, i: int, j: int, char: str, color: str) -> None:
        super().set_cell_char(i, j, char, color)
        if 0 <= i < self.nrows and 0 <= j < self.ncols:
            i_flipped = self.nrows - 1 - i
            sprite = self.view.grid_sprites[i_flipped][j]

            if char:
                # Create or update the Text
                if self.view.grid_chars[i][j] is None:
                    self.view.grid_chars[i][j] = arcade.Text(
                        text=char,
                        x=sprite.center_x,
                        y=sprite.center_y,
                        color=_hex_to_rgb(color),
                        font_size=self.cell_size*0.75,  # Rough approximation for now
                        anchor_x="center",
                        anchor_y="center"
                    )
                elif self.view.grid_chars[i][j].text != char: #type: ignore  # pyright: ignore[reportOptionalMemberAccess]
                    self.view.grid_chars[i][j].text = char #type: ignore  # pyright: ignore[reportOptionalMemberAccess]
            else:
                # Clear the character
                self.view.grid_chars[i][j] = None

    @override
    def load_image(self, name: str, path: str) -> None:
        self.view.textures[name] = arcade.load_texture(path)
        self.view.textures[name].width = self.cell_size
        self.view.textures[name].height = self.cell_size

    @override
    def play_sound(self, path: str) -> None:
        son: Sound = arcade.load_sound(path)
        _ = son.play()



class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self, crafter: ArcadeEngine) -> None:
        """
        Set up the application.
        """
        super().__init__()
        self.crafter: ArcadeEngine = crafter
        # Set the background color of the window
        self.background_color: Color = arcade.color.BLACK

        self.textures: dict[str, arcade.Texture] = dict[str, Texture]()
        # 1d list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        # 2d grid hat holds references to the spritelist
        self.grid_sprites: list[list[arcade.Sprite]] = []

        # 2d grid that holds Texts to be drawn on top of sprites
        self.grid_chars: list[list[arcade.Text|None]] = [[None for _ in range(crafter.ncols)] for _ in range(crafter.nrows)]

        # Create a list of solidcolor sprites to represent each cell
        for row in range(self.crafter.nrows):
            self.grid_sprites.append([])
            for column in range(self.crafter.ncols):
                x = column * (self.crafter.cell_size + self.crafter.margin) + (self.crafter.cell_size / 2 + self.crafter.margin)
                y = row * (self.crafter.cell_size + self.crafter.margin) + (self.crafter.cell_size / 2 + self.crafter.margin)
                sprite: SpriteSolidColor = arcade.SpriteSolidColor(self.crafter.cell_size, self.crafter.cell_size, color=arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    @override
    def on_update(self, delta_time: float) -> bool | None:
        logger.debug(f"on_update({delta_time})")
        self.crafter.frame_no += 1 #! Incrémentation du frame_no
        #print("test")
        _ = super().on_update(delta_time)
        if self.crafter.fn_update:
            self.crafter.fn_update()

    @override
    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        logger.debug(f"on_key_press({symbol}, {modifiers})")
        _ = super().on_key_press(symbol, modifiers)
        #print(symbol, chr(symbol), modifiers)
        if self.crafter.fn_key:
            self.crafter.fn_key(chr(symbol))
#            self.immediate_update()

    @override
    def on_draw(self) -> None:
        """
        Render the screen.
        """
        if self.crafter.fn_draw:
            self.crafter.fn_draw()
        self.clear()
        self.grid_sprite_list.draw()
        #print(self.grid_chars)
        for i in range(self.crafter.nrows):
            for j in range(self.crafter.ncols):
                text_obj = self.grid_chars[i][j]
                if text_obj:
                    text_obj.draw()

    @override
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """
        Called when the user presses a mouse button.
        """
        logger.debug(f"on_mouse_press({x},{y},{button},{modifiers})")
        column = int(x // (self.crafter.cell_size + self.crafter.margin))
        row = self.crafter.nrows - 1 - int(y // (self.crafter.cell_size + self.crafter.margin))
        logger.debug(f"Grid coordinates: ({row}, {column})")
        if self.crafter.fn_click:
            self.crafter.fn_click(row, column)
            #self.immediate_update()

"""
    def immediate_update(self):
        self.on_update(0)
        self.window.set_update_rate(0)
        self.on_draw()
        self.window.flip()
        self.window.set_update_rate(1/self.crafter.fps)
"""
