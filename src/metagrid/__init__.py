try:
    from importlib.metadata import version
    __version__ = version("metagrid")
except Exception:
    __version__ = "0.0.0"


from .backends import AbstractEngine
from .crafter_factory import CrafterFactory

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


def create_networked(nrows: int, ncols: int, cell_size: int, margin: int, url: str | None = None, token: str | None = None):
    """
    Returns a networked metagrid engine for 2-player remote games.

    Parameters:
    - nrows, ncols, cell_size, margin : same as create()
    - url   : WebSocket URL of the game server (provided by your teacher)
    - token : access token (provided by your teacher)

    Requires: pip install metagrid[network]

    Extra callbacks:
        @game.on_game_start    → fn(je_commence: bool)
        @game.on_opponent_move → fn(state)
        @game.on_opponent_left → fn()

    Extra methods:
        game_id = game.create()   # create a game and get the ID to share
        game.join(game_id)        # join an existing game
        game.send_move(state)     # send your game state to the opponent
    """
    try:
        from .networked import NetworkedEngine
    except ImportError:
        raise ImportError(
            "Le jeu en réseau nécessite le paquet 'websockets'.\n"
            "Installe-le avec : pip install metagrid[network]"
        )
    engine = CrafterFactory.create("arcade", nrows, ncols, cell_size, margin)
    return NetworkedEngine(engine, url, token)


__all__ = ["create", "create_networked", "AbstractEngine"]
