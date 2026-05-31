"""
game_client.py
==============
Generic WebSocket client for the game server.

Students do not write this file: they import it via metagrid.
Dependency: websockets  (pip install metagrid[network])
"""

import json
import os
import threading
import asyncio
from collections.abc import Callable
from typing import Any
import websockets
from urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))  # search upward from CWD, once at import


class GameClient:
    """
    Synchronous client for the WebSocket game server.

    Parameters
    ----------
    url : str | None
        Base WebSocket URL of the server. Falls back to METAGRID_URL env var.
    token : str | None
        Access token provided by the teacher. Falls back to METAGRID_TOKEN env var.
    on_start : callable(client)
        Called when the game starts (both players are connected).
    on_update : callable(client, state)
        Called when the opponent sends a game state.
        `state` is the decoded JSON value (dict, list, int, etc.).
    on_opponent_left : callable(client), optional
    on_error : callable(client, reason), optional
    """

    def __init__(
        self,
        on_start: Callable[["GameClient"], None],
        on_update: Callable[["GameClient", Any], None],
        on_opponent_left: Callable[["GameClient"], None] | None = None,
        on_error: Callable[["GameClient", str], None] | None = None,
        url: str | None = None,
        token: str | None = None,
    ) -> None:
        url = url or os.environ.get("METAGRID_URL")
        token = token or os.environ.get("METAGRID_TOKEN")
        if not url:
            raise ValueError(
                "METAGRID_URL manquant : définis-le dans ton fichier .env "
                "ou via la variable d'environnement METAGRID_URL"
            )
        if not token:
            raise ValueError(
                "METAGRID_TOKEN manquant : définis-le dans ton fichier .env "
                "ou via la variable d'environnement METAGRID_TOKEN"
            )
        separator = "&" if "?" in url else "?"
        self._url = url + separator + urlencode({"token": token})

        self._on_start = on_start
        self._on_update = on_update
        self._on_opponent_left: Callable[["GameClient"], None] = (
            on_opponent_left or (lambda c: None)
        )
        self._on_error: Callable[["GameClient", str], None] = (
            on_error or (lambda c, r: print(f"[Server error] {r}"))
        )

        self._ws: Any = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._game_id: str | None = None
        self._pending_create: Callable[[str], None] | None = None
        self._ready = threading.Event()
        self._thread: threading.Thread | None = None
        self._connect_error: str | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create(self) -> str:
        """
        Create a new game.
        Blocks until the game ID is received.
        Raises ConnectionError if the token is rejected.
        Raises TimeoutError if the server does not respond within 10 s.
        """
        id_event = threading.Event()
        result: dict[str, str] = {}

        def on_created(game_id: str) -> None:
            result["game_id"] = game_id
            id_event.set()

        self._pending_create = on_created
        self._start_loop()
        self._check_connect_error()
        self._send_sync({"type": "create"})
        if not id_event.wait(timeout=10):
            raise TimeoutError(
                "Le serveur n'a pas répondu à la création de la partie (timeout 10 s)"
            )
        return result["game_id"]

    def join(self, game_id: str) -> None:
        """Join an existing game by its ID."""
        self._start_loop()
        self._check_connect_error()
        self._send_sync({"type": "join", "game_id": game_id})

    def move(self, state: Any) -> None:
        """
        Send a game state to the opponent.
        `state` can be any JSON-serialisable value.
        """
        self._send_sync({"type": "move", "state": state})

    def stop(self) -> None:
        """Close the WebSocket connection and stop the client."""
        ws, loop = self._ws, self._loop
        if ws and loop and not loop.is_closed():
            try:
                future = asyncio.run_coroutine_threadsafe(ws.close(), loop)
                future.result(timeout=3.0)  # wait for the close frame to be sent
            except Exception:
                pass

    def run(self) -> None:
        """Block until the game ends. Responds to Ctrl+C."""
        if self._thread:
            try:
                while self._thread.is_alive():
                    self._thread.join(timeout=0.5)
            except KeyboardInterrupt:
                self.stop()

    def is_running(self) -> bool:
        """Return True if the network thread is still active."""
        return self._thread is not None and self._thread.is_alive()

    def wait(self, timeout: float) -> None:
        """Wait for the network thread to finish (at most `timeout` seconds)."""
        if self._thread is not None:
            self._thread.join(timeout=timeout)

    # ------------------------------------------------------------------
    # Internal asyncio loop
    # ------------------------------------------------------------------

    def _start_loop(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            self._ready.wait(timeout=5)
            return
        # First start, or thread died after stop() — reset state fully
        self._ws = None
        self._connect_error = None
        self._ready = threading.Event()
        old_loop = self._loop
        if old_loop is not None:
            old_loop.close()
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self._ready.wait(timeout=5)

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        assert self._loop is not None
        self._loop.run_until_complete(self._connect_and_listen())

    async def _connect_and_listen(self) -> None:
        try:
            async with websockets.connect(
                self._url,
                ping_interval=5,   # detect dead connections in ~10 s
                ping_timeout=5,
                close_timeout=2,   # clean close within 2 s
            ) as ws:
                self._ws = ws
                self._ready.set()
                try:
                    async for raw in ws:
                        try:
                            self._dispatch(raw)
                        except Exception as e:
                            print(f"[metagrid] erreur dans le traitement d'un message : {e}")
                except websockets.exceptions.ConnectionClosed:
                    pass  # connection lost mid-game → fallback handles it
        except websockets.exceptions.InvalidStatus as e:
            if e.response.status_code == 401:
                self._connect_error = (
                    "Token rejected (HTTP 401). "
                    "Check that the token is correct."
                )
            else:
                self._connect_error = f"Connection refused: HTTP {e.response.status_code}"
            self._ready.set()
        except asyncio.CancelledError:
            self._ready.set()
            raise  # normal task cancellation — do not set _connect_error
        except Exception as e:
            self._connect_error = f"Connection error: {e}"
            self._ready.set()

    def _check_connect_error(self) -> None:
        if self._connect_error:
            raise ConnectionError(self._connect_error)

    def _dispatch(self, raw: str | bytes) -> None:
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            return

        msg_type = msg.get("type")

        if msg_type == "created":
            self._game_id = msg.get("game_id")
            if self._pending_create is not None and self._game_id is not None:
                self._pending_create(self._game_id)
                self._pending_create = None  # consumed; prevent double-fire

        elif msg_type == "start":
            self._on_start(self)

        elif msg_type == "update":
            self._on_update(self, msg.get("state"))

        elif msg_type == "opponent_left":
            self._on_opponent_left(self)

        elif msg_type == "ping":
            self._send_sync({"type": "pong"})

        elif msg_type == "error":
            self._on_error(self, msg.get("reason", "unknown"))

    def _send_sync(self, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload)
        ws, loop = self._ws, self._loop
        if ws is None or loop is None:
            raise RuntimeError("_send_sync appelé avant l'établissement de la connexion WebSocket")
        future = asyncio.run_coroutine_threadsafe(ws.send(raw), loop)
        future.result(timeout=5)

    @property
    def game_id(self) -> str | None:
        return self._game_id
