# pyright: reportImportCycles=false
from typing import Literal
from . import backends

BackendName = Literal["arcade"]

class CrafterFactory:

    @staticmethod
    def create(backend: BackendName, nrows: int,
            ncols: int, cell_size: int, margin: int) -> backends.AbstractEngine:
        """
        Crée une instance de moteur de grille selon le backend choisi.

        Retourne une instance du crafter choisi (ArcadeCrafter est le seul backend supporté pour l'instant).
        """
        if backend == "arcade":
            from .backends.arcade_impl import ArcadeEngine
            return ArcadeEngine(nrows, ncols, cell_size, margin)
        else:
            raise ValueError(f"Backend inconnu : {backend!r}")  # pyright: ignore[reportUnreachable]
