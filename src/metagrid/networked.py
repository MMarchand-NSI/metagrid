import atexit
import queue
from .backends import AbstractEngine


class NetworkedEngine:
    """
    Enveloppe un AbstractEngine avec une couche réseau (WebSocket).

    Les événements réseau arrivent depuis un thread background et sont
    injectés dans la boucle arcade via une queue thread-safe, drainée
    à chaque frame dans on_update.

    Callbacks supplémentaires :
        @game.on_game_start   → fn(je_commence: bool)
        @game.on_opponent_move → fn(state)
        @game.on_opponent_left → fn()   (optionnel)

    Méthodes supplémentaires :
        game.create() → str    # crée une partie, renvoie l'ID à partager
        game.join(game_id)     # rejoint une partie existante
        game.send_move(state)  # envoie l'état au serveur
    """

    def __init__(self, engine: AbstractEngine, url: str, token: str):
        from .game_client import GameClient

        self._engine = engine
        self._queue: queue.Queue = queue.Queue()
        self._user_update_fn = None
        self._on_game_start_fn = None
        self._on_opponent_move_fn = None
        self._on_opponent_left_fn = None
        self._game_started = False   # True dès que les deux joueurs sont connectés
        self._network_ended = False  # True quand on a déjà traité la fin de connexion

        self._client = GameClient(
            url=url,
            token=token,
            on_start=lambda c: self._queue.put(("start", c.game_id is not None)),
            on_update=lambda c, state: self._queue.put(("update", state)),
            on_opponent_left=lambda c: self._queue.put(("left",)),
        )

    # ------------------------------------------------------------------
    # Callbacks réseau
    # ------------------------------------------------------------------

    def on_game_start(self, fn):
        """Decorator. Appelé quand les deux joueurs sont connectés.
        Reçoit je_commence (bool) : True si tu as créé la partie.
        """
        self._on_game_start_fn = fn
        return fn

    def on_opponent_move(self, fn):
        """Decorator. Appelé quand l'adversaire envoie un état de jeu.
        Reçoit state : la valeur JSON envoyée par l'adversaire.
        """
        self._on_opponent_move_fn = fn
        return fn

    def on_opponent_left(self, fn):
        """Decorator. Appelé quand l'adversaire quitte la partie."""
        self._on_opponent_left_fn = fn
        return fn

    # ------------------------------------------------------------------
    # Actions réseau
    # ------------------------------------------------------------------

    def create(self) -> str:
        """Crée une nouvelle partie. Bloque jusqu'à réception de l'ID."""
        return self._client.create()

    def join(self, game_id: str) -> None:
        """Rejoint une partie existante."""
        self._client.join(game_id)

    def send_move(self, state) -> None:
        """Envoie l'état du jeu à l'adversaire."""
        self._client.move(state)

    def disconnect(self) -> None:
        """Ferme la connexion réseau (à appeler quand la partie est terminée)."""
        self._client.stop()

    # ------------------------------------------------------------------
    # on_update : intercepté pour drainer la queue réseau chaque frame
    # ------------------------------------------------------------------

    def on_update(self, fn):
        """Decorator. Enregistre la fonction appelée à chaque frame (avant draw)."""
        self._user_update_fn = fn
        return fn

    def start(self) -> None:
        user_update = self._user_update_fn

        def combined_update():
            if user_update:
                user_update()
            self._drain_queue()

        # Enregistré avant arcade.run() : s'exécute même si pyglet appelle
        # sys.exit() au lieu de retourner proprement, avant que les threads
        # daemon soient tués.
        atexit.register(self._shutdown)

        self._engine.on_update_fn = combined_update
        try:
            self._engine.start()
        finally:
            self._shutdown()

    def _shutdown(self) -> None:
        """Ferme proprement la connexion WebSocket. Idempotent."""
        atexit.unregister(self._shutdown)
        self._client.stop()  # bloque jusqu'à ce que le close frame soit envoyé (max 3 s)
        thread = self._client._thread
        if thread is not None:
            thread.join(timeout=1.0)

    # ------------------------------------------------------------------
    # Délégation vers le moteur sous-jacent
    # ------------------------------------------------------------------

    def __getattr__(self, name):
        return getattr(self._engine, name)

    # ------------------------------------------------------------------
    # Interne
    # ------------------------------------------------------------------

    def _drain_queue(self):
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

        # Filet de sécurité : si le thread réseau est mort sans envoyer "left"
        # (connexion coupée, RST TCP, crash...), on le détecte ici.
        if (self._game_started
                and not self._network_ended
                and self._client._thread is not None
                and not self._client._thread.is_alive()):
            self._fire_opponent_left()

    def _fire_opponent_left(self):
        if self._network_ended:
            return
        self._network_ended = True
        if self._on_opponent_left_fn:
            self._on_opponent_left_fn()
        else:
            print("L'adversaire a quitté la partie.")
