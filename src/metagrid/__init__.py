try:
    from importlib.metadata import version
    __version__ = version("metagrid")
except Exception:
    __version__ = "0.0.0"


from .backends import AbstractEngine
from .CrafterFactory import CrafterFactory

def create(nb_lignes: int, nb_colonnes: int, cell_size: int, margin: int) -> AbstractEngine:
    """
    Returns a metagrid engine.

    Parameters:
    - nb_lignes : Number of lines in the grid
    - nb_colonnes : Number of columns in the grid
    - cell_size : cells are squares. length of the side of the cell in pixels
    - margin: Thickness of the margin to be displayed between each cell
    """
    return CrafterFactory.create("arcade", nb_lignes, nb_colonnes, cell_size, margin)

__all__ = ["create", "AbstractEngine"]
