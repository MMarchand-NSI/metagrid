import atexit
import queue
from collections.abc import Callable
from typing import Any
from .backends import AbstractEngine


class NetworkedEngine:
    """
    Wraps an AbstractEngine with a WebSocket network layer.

    Network events arrive from a background thread and are injected into
    the arcade loop via a thread-safe queue, drained every frame in on_update.

    Extra callbacks:
        @game.on_game_start    -> fn(i_go_first: bool)
        @game.on_opponent_move -> fn(state)
        @game.on_opponent_left -> fn()   (optional)

    Extra method:
        game.send_move(state)  # send the game state to the opponent
    """

    def __init__(self, engine: AbstractEngine, url: str | None = None, token: str | None = None) -> None:
        from .game_client import GameClient

        self._engine = engine
        self._queue: queue.Queue[tuple[Any, ...]] = queue.Queue()
        self._user_update_fn: Callable[[], None] | None = None
        self._on_game_start_fn: Callable[[bool], None] | None = None
        self._on_opponent_move_fn: Callable[[Any], None] | None = None
        self._on_opponent_left_fn: Callable[[], None] | None = None
        self._game_started = False
        self._network_ended = False
        self._i_created: bool = False

        self._client = GameClient(
            url=url,
            token=token,
            on_start=lambda c: self._queue.put(("start", self._i_created)),
            on_update=lambda c, state: self._queue.put(("update", state)),
            on_opponent_left=lambda c: self._queue.put(("left",)),
        )

    # ------------------------------------------------------------------
    # Network callbacks
    # ------------------------------------------------------------------

    def on_game_start(self, fn: Callable[[bool], None]) -> Callable[[bool], None]:
        """Decorator. Called when both players are connected.
        Receives i_go_first (bool): True if this client created the game.
        """
        self._on_game_start_fn = fn
        return fn

    def on_opponent_move(self, fn: Callable[[Any], None]) -> Callable[[Any], None]:
        """Decorator. Called when the opponent sends a game state.
        Receives state: the JSON value sent by the opponent.
        """
        self._on_opponent_move_fn = fn
        return fn

    def on_opponent_left(self, fn: Callable[[], None]) -> Callable[[], None]:
        """Decorator. Called when the opponent leaves the game."""
        self._on_opponent_left_fn = fn
        return fn

    # ------------------------------------------------------------------
    # Network actions
    # ------------------------------------------------------------------

    def send_move(self, state: Any) -> None:
        """Send the current game state to the opponent."""
        self._client.move(state)

    def disconnect(self) -> None:
        """Close the network connection (call when the game is over)."""
        self._client.stop()

    # ------------------------------------------------------------------
    # on_update: intercepted to drain the network queue every frame
    # ------------------------------------------------------------------

    def on_update(self, fn: Callable[[], None]) -> Callable[[], None]:
        """Decorator. Register the function called every frame (before draw)."""
        self._user_update_fn = fn
        return fn

    def start(self) -> None:
        atexit.register(self._shutdown)
        try:
            self._create_or_join()
            user_update = self._user_update_fn

            def combined_update() -> None:
                if user_update:
                    user_update()
                self._drain_queue()

            self._engine.on_update_fn = combined_update
            self._engine.start()
        finally:
            self._shutdown()

    def _shutdown(self) -> None:
        """Close the WebSocket connection cleanly. Idempotent."""
        atexit.unregister(self._shutdown)
        self._client.stop()
        self._client.wait(timeout=1.0)

    # ------------------------------------------------------------------
    # Delegation to the underlying engine
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        return getattr(self._engine, name)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _create(self) -> str:
        self._i_created = True
        return self._client.create()

    def _join(self, game_id: str) -> None:
        self._client.join(game_id)

    def _create_or_join(self) -> None:
        choice = ""
        while choice not in ("c", "j"):
            try:
                choice = input("Créer une partie (c) ou rejoindre une partie (j) ? ").strip().lower()
            except EOFError:
                raise RuntimeError(
                    "Impossible de lire la saisie (stdin fermé). "
                    "Lance le script dans un terminal interactif."
                )
            if choice not in ("c", "j"):
                print("Réponds par 'c' ou 'j'.")

        if choice == "c":
            game_id = self._create()
            print(f"\nPartie créée. Transmets cet ID à ton adversaire : {game_id}")
            print("En attente du second joueur...\n")
        else:
            game_id = ""
            while not game_id:
                try:
                    game_id = input("Entre l'identifiant de la partie : ").strip().upper()
                except EOFError:
                    raise RuntimeError(
                        "Impossible de lire la saisie (stdin fermé). "
                        "Lance le script dans un terminal interactif."
                    )
                if not game_id:
                    print("L'identifiant ne peut pas être vide.")
            print(f"\nRejoindre la partie {game_id}...")
            self._join(game_id)

    def _drain_queue(self) -> None:
        if self._network_ended:
            return
        while True:
            try:
                event = self._queue.get_nowait()
            except queue.Empty:
                break
            kind = event[0]
            if kind == "start":
                self._game_started = True
                if self._on_game_start_fn:
                    self._on_game_start_fn(event[1])
            elif kind == "update" and self._on_opponent_move_fn:
                self._on_opponent_move_fn(event[1])
            elif kind == "left":
                self._fire_opponent_left()

        # Fallback: if the network thread died without sending "left"
        # (dropped connection, TCP RST, crash...), detect it here.
        if self._game_started and not self._network_ended and not self._client.is_running():
            self._fire_opponent_left()

    def _fire_opponent_left(self) -> None:
        if self._network_ended:
            return
        self._network_ended = True
        if self._on_opponent_left_fn:
            self._on_opponent_left_fn()
        else:
            print("The opponent has left the game.")
