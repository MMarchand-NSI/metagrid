try:
    from importlib.metadata import version
    __version__ = version("metagrid")
except Exception:
    __version__ = "0.0.0"


from .backends import AbstractEngine
from .CrafterFactory import CrafterFactory

def create(nrows: int, ncols: int, cell_size: int, margin: int) -> AbstractEngine:
    """
    Returns a metagrid engine.

    Parameters:
    - nrows : Number of rows in the grid
    - ncols : Number of columns in the grid
    - cell_size : cells are squares. length of the side of the cell in pixels
    - margin: Thickness of the margin to be displayed between each cell
    """
    return CrafterFactory.create("arcade", nrows, ncols, cell_size, margin)

__all__ = ["create", "AbstractEngine"]
