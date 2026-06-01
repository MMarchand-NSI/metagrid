# Changelog

## [0.6.0] - 2026-06-01

### ♻️ Refactoring

- Renomme CrafterFactory.py en crafter_factory.py (snake_case) ([`1669c81`](https://github.com/MMarchand-NSI/metagrid/commit/1669c817fdaa55dffa3278a80eaeeb851b2ba92f))

- Refactorise NetworkedEngine : i_go_first explicite, méthodes réseau privées

- _i_created remplace c.game_id is not None pour le flag i_go_first (plus fiable)
- create(), join(), create_or_join() deviennent _create(), _join(), _create_or_join()
- l'API publique n'expose plus que send_move() et disconnect()
- docstring mise à jour ([`fceaa91`](https://github.com/MMarchand-NSI/metagrid/commit/fceaa91d14104ab1518c1c577a6e9079b921bcd4))


### ✨ Nouveautés

- Ajoute le chargement automatique du .env et simplifie l'API réseau

- python-dotenv ajouté en dépendance principale
- GameClient charge le .env automatiquement via load_dotenv()
- url et token deviennent optionnels, lus depuis METAGRID_URL / METAGRID_TOKEN
- create_or_join() absorbé dans NetworkedEngine.start()
- morpion_reseau.py ne contient plus aucune credential ([`50935ed`](https://github.com/MMarchand-NSI/metagrid/commit/50935ed47e26b247ba57770226fd632a4c921411))

- Ajoute .env.example avec des valeurs placeholder

Remplace les valeurs réelles du serveur par des placeholders pour éviter
toute fuite de credentials lors d'un partage du projet. ([`0d4cc7e`](https://github.com/MMarchand-NSI/metagrid/commit/0d4cc7ecc2185e42cbadcdd226fe355e27f43928))


### 🐛 Corrections

- Corrige game_client : timeout sur create(), init de _pending_create, load_dotenv différé

- create() lève TimeoutError si le serveur ne répond pas en 10 s (au lieu de retourner "")
- _pending_create initialisé à None dans __init__ (plus de hasattr)
- load_dotenv() déplacé dans __init__ pour éviter l'effet de bord à l'import
- messages d'erreur mentionnent aussi les variables d'environnement ([`1fe5379`](https://github.com/MMarchand-NSI/metagrid/commit/1fe5379c7867dcc946823d8940bdc09e6a82132c))

- Corrige __init__ : supprime create/join obsolètes de la docstring de create_networked ([`ec23d77`](https://github.com/MMarchand-NSI/metagrid/commit/ec23d7793866f9bee5389c018b2896ea35d1ebf2))

- Corrige networked : UnboundLocalError si stdin fermé dans _create_or_join

Initialise choice avant la boucle et attrape EOFError pour donner un
message d'erreur explicite au lieu d'un UnboundLocalError trompeur. ([`96a6811`](https://github.com/MMarchand-NSI/metagrid/commit/96a68118b5ea3ba7102a54582cbcda405443b1c3))

- Corrige game_client : 4 bugs de robustesse

- load_dotenv() remis au niveau module (appelé une seule fois à l'import)
- _start_loop() détecte un thread mort après stop() et réinitialise l'état
- except Exception aveugle remplacé : ConnectionClosed ignoré, autres erreurs affichées
- _pending_create remis à None après usage (empêche un double-fire) ([`3ad24b9`](https://github.com/MMarchand-NSI/metagrid/commit/3ad24b903265db3d0082bfec6c775f86c18d9d56))

- Corrige networked : thread orphelin et polling inutile post-partie

- atexit.register déplacé avant _create_or_join() pour garantir _shutdown()
  même si la connexion échoue (TimeoutError, ConnectionError)
- _drain_queue() retourne immédiatement si _network_ended (évite
  thread.is_alive() à 60 fps après la fin de la partie) ([`0c58b8d`](https://github.com/MMarchand-NSI/metagrid/commit/0c58b8d248d95a85c82592b4879816efe21d0403))

- Corrige game_client : _ws, CancelledError, load_dotenv, assert

- _start_loop() réinitialise _ws = None pour éviter _send_sync sur
  un WebSocket fermé lors d'une reconnexion
- CancelledError (BaseException) reraisé pour ne pas écraser _connect_error
  lors d'une fermeture propre de la boucle asyncio
- find_dotenv(usecwd=True) pour chercher .env depuis le CWD explicitement
- assert remplacé par RuntimeError avec message explicite dans _send_sync ([`5ec9e92`](https://github.com/MMarchand-NSI/metagrid/commit/5ec9e92d9741386eec7e2cf11ec2460f6e553efd))

- Corrige game_client : fuite event loop, CancelledError, to_thread superflu

- _start_loop ferme l'ancien event loop avant d'en créer un nouveau
- CancelledError appelle _ready.set() avant de reraiser pour éviter
  un blocage silencieux de 5 s dans _start_loop
- _dispatch appelé directement dans la coroutine (non-bloquant) au lieu
  de passer par asyncio.to_thread — supprime overhead inutile ([`3b710a1`](https://github.com/MMarchand-NSI/metagrid/commit/3b710a13cbeee1a3bef1401de43e396e740a41b1))

- Corrige networked : validation du game_id dans _create_or_join

Un identifiant vide envoyé au serveur provoquait une session muette
(on_game_start jamais appelé, fenêtre arcade figée sans message).
La saisie est maintenant redemandée tant que l'ID est vide. ([`0b5db9a`](https://github.com/MMarchand-NSI/metagrid/commit/0b5db9a8bf2f4de781ab18e8bbf06e9ab467250e))

- Corrige game_client : deadlock ping/pong quand _dispatch dans le thread asyncio

_send_sync bloque sur .result() en attendant que la boucle asyncio exécute
ws.send() — impossible car la boucle est elle-même bloquée sur .result().
Le ping est maintenant intercepté dans _connect_and_listen avec await ws.send()
avant d'appeler _dispatch, supprimant la branche ping de _dispatch. ([`254ad8b`](https://github.com/MMarchand-NSI/metagrid/commit/254ad8b478c55d7e134b97e898f5f3d10fed29ff))

- Corrige networked : espaces internes filtres dans le game_id saisi ([`65fc2d7`](https://github.com/MMarchand-NSI/metagrid/commit/65fc2d7e7228f2a9a1f224aaa0ea73e547802e94))

- Corrige networked : erreurs serveur routees dans la queue

Les erreurs serveur (game_id invalide, token expire...) etaient printees
depuis le thread asyncio mais invisibles pour l'UI arcade. Elles sont
maintenant injectees dans la queue et traitees comme une fin de partie :
message affiche + _fire_opponent_left() pour terminer proprement le jeu. ([`29366fe`](https://github.com/MMarchand-NSI/metagrid/commit/29366fe84925f0e898057bbf7d4003e3366dac8d))

- Fix: skip_existing sur PyPI pour eviter echec sur re-run ([`dc086c4`](https://github.com/MMarchand-NSI/metagrid/commit/dc086c4eced7a52daa061c0503f47a0efdf5664d))


### 📚 Documentation

- Docs: mise à jour du CHANGELOG pour v0.5.0 ([`9329fff`](https://github.com/MMarchand-NSI/metagrid/commit/9329fffe0ad0ad100f3c1b72aa645fc5a488f04d))

- Docs: section jeux réseau tour par tour dans README.md et README.fr.md ([`5a076ec`](https://github.com/MMarchand-NSI/metagrid/commit/5a076ec9d332048c4dc63341be2be8b9c22ea81e))

## [0.5.0] - 2026-05-30

### ✨ Nouveautés

- Feat: add networked tic-tac-toe game with WebSocket support

- Implemented morpion_reseau.py for a two-player tic-tac-toe game over WebSocket.
- Created game_client.py to handle WebSocket connections and game state updates.
- Added networked.py to wrap an AbstractEngine with network capabilities, enabling game creation, joining, and move sending.
- Included necessary decorators for handling game events such as game start, opponent moves, and opponent disconnection. ([`436171c`](https://github.com/MMarchand-NSI/metagrid/commit/436171cea3e4f8e20a4df1d763a24a98ee60377f))

- Feat: enhance game client and network engine with type hints and improved documentation ([`42a473d`](https://github.com/MMarchand-NSI/metagrid/commit/42a473d98f8b5e2474642a4a61d11380ec39a607))


### 📚 Documentation

- Docs: mise à jour du CHANGELOG pour v0.4.0 ([`ba461bd`](https://github.com/MMarchand-NSI/metagrid/commit/ba461bd9c0a542c66b603d5aeb35e5b731912c20))


### 🔧 Changements

- Merge branch 'main' of https://github.com/MMarchand-NSI/metagrid ([`16aafbc`](https://github.com/MMarchand-NSI/metagrid/commit/16aafbc11b04acb3a7e49168e05568f81a330afb))

## [0.4.0] - 2026-05-30

### ✨ Nouveautés

- Feat: add GitHub Actions for automated release and changelog generation
chore: update Python interpreter path in VSCode settings
docs: create CHANGELOG.md and cliff.toml for automated changelog generation
refactor: rename callback functions to on_* in examples for consistency
feat: implement Minesweeper example with game logic and UI ([`a62f836`](https://github.com/MMarchand-NSI/metagrid/commit/a62f836bdfb1a82263ffd8122dd59af840d19434))


### 📚 Documentation

- Docs: mise à jour du CHANGELOG pour v0.3.0 ([`bb0c62d`](https://github.com/MMarchand-NSI/metagrid/commit/bb0c62d2f3bdf0f37d39143543008766f85e703f))

- Docs: add bilingual README with full tutorial (EN/FR) ([`246d727`](https://github.com/MMarchand-NSI/metagrid/commit/246d72723afd25f8425748a0222dcbc9c8bfc7c0))


### 🔧 Changements

- Affiche les chiffres dans le 2048, lève la restriction single-char de set_cell_char ([`68e0ed7`](https://github.com/MMarchand-NSI/metagrid/commit/68e0ed7f1fccd7c9fcd208cf1901341e213842a4))

- Revert "Affiche les chiffres dans le 2048, lève la restriction single-char de set_cell_char"

This reverts commit 68e0ed7f1fccd7c9fcd208cf1901341e213842a4. ([`b4c3829`](https://github.com/MMarchand-NSI/metagrid/commit/b4c38299abf4c86a5ae5d8ecd6010fa8cd82e557))

## [0.3.0] - 2026-05-14

### ♻️ Refactoring

- Renomme les décorateurs de callbacks en on_* (closes #6) ([`adb80c4`](https://github.com/MMarchand-NSI/metagrid/commit/adb80c4488510d782f0f2411caa7f9ee7f279628))

- Refactorise le parcours des voisins avec di/dj ([`27cf8d9`](https://github.com/MMarchand-NSI/metagrid/commit/27cf8d960ccb9492f3d0f466cba30889ab0dbc70))


### ✨ Nouveautés

- Ajoute des docstrings pédagogiques au démineur ([`9557359`](https://github.com/MMarchand-NSI/metagrid/commit/955735993cc8b474706b8546050288545988ec70))

- Ajoute la génération automatique du changelog via git-cliff ([`193c847`](https://github.com/MMarchand-NSI/metagrid/commit/193c847e249c1617a526ff8f23105f8cd240aa48))


### 🐛 Corrections

- Fix issues critiques #7 #8 #9

- #7 : on_mouse_press ignore les clics hors grille
- #8 : set_cell_char met à jour la couleur si le texte existe déjà
- #9 : touches spéciales mappées via _KEY_MAP (flèches, Echap, F1-F12…) ([`4524048`](https://github.com/MMarchand-NSI/metagrid/commit/4524048c4553ad27c8bd5b8beedc7234cd3d8e7c))

- Fix issues importantes #10 #11 #12 #13

- #10 : _check_bounds unifie la validation (indices négatifs inclus) pour set_cell_color et set_cell_image
- #11 : texture blanche créée une seule fois dans __init__ et réutilisée
- #12 : cache des sons dans _sound_cache pour éviter les rechargements
- #13 : load_image redimensionne via PIL.resize() au lieu d'assigner width/height sur la texture ([`2f8f6dd`](https://github.com/MMarchand-NSI/metagrid/commit/2f8f6dd9c4455bb0072ac5af64d203b01dd012d7))

- Fix issues mineures #14 #15 #16 #17 #18 #19 #20

- #14 : couleur→color, nb_lignes→nrows, nb_colonnes→ncols dans toute l'API
- #15 : _init_fn renommé en on_init_fn pour uniformiser les callbacks
- #16 : docstrings mis à jour avec les nouveaux noms on_*
- #17 : suppression du double init de frame_no dans ArcadeEngine
- #18 : _BUTTON_MAP déplacé au niveau module
- #19 : code mort immediate_update supprimé
- #20 : assert remplacé par ValueError dans set_cell_char
- Imports inutiles supprimés (View, Callable) dans arcade_impl ([`43a86ba`](https://github.com/MMarchand-NSI/metagrid/commit/43a86bafc6da411b6c964e2e39ffb3a4f4617041))

- Corrige les bugs du démineur

- Flood-fill ne révèle plus les mines voisines
- Game over bloque les interactions et révèle toutes les mines
- Mines affichées en rouge après game over
- create(HAUTEUR, LARGEUR) — ordre des paramètres corrigé
- decouvre() simplifiée (deux branches identiques fusionnées)
- draw() restructuré : un seul set_cell_char par case par frame
- Détection de victoire ajoutée
- Drapeau impossible à poser sur une case déjà révélée ([`b80554c`](https://github.com/MMarchand-NSI/metagrid/commit/b80554c562e0426772d194684d002b2e684e5f1d))


### 🔧 Changements

- Jeu memory+gestion transparence ([`ccad5b3`](https://github.com/MMarchand-NSI/metagrid/commit/ccad5b33232fdb28405c7990b7e11ba6c926f2b6))

- Expose mouse button in callback_click (closes #5)

fn_click now receives a third argument "left", "right", or "middle".
Updated all examples to match the new signature. ([`ac28564`](https://github.com/MMarchand-NSI/metagrid/commit/ac2856408228b0faa5d846c8f38c8cfb5dddff77))

- Demineur ([`64691f5`](https://github.com/MMarchand-NSI/metagrid/commit/64691f51ebe6b73dcb56d374534f7175e803987c))

## [0.2.1] - 2026-04-27

### ✨ Nouveautés

- Ajoute .claude/ au gitignore ([`a44e616`](https://github.com/MMarchand-NSI/metagrid/commit/a44e616478116b05586d42a4d992db9bfb3af935))


### 🔧 Changements

- Ajout de nouveaux exemples de jeux : 2048, Memory, Puissance 4, et Lights Out. Mise à jour des exemples existants pour utiliser AbstractEngine et améliorer la structure du code.

Co-authored-by: Copilot <copilot@github.com> ([`a567221`](https://github.com/MMarchand-NSI/metagrid/commit/a567221a65584af7306fcd069f0461d9d30fdf17))

- Rend update optionnel dans AbstractEngine, nettoie les exemples

Supprime l'assertion sur fn_update dans start() : la méthode update
n'est plus obligatoire, comme callback_click. L'implémentation arcade
gérait déjà le cas None. Les exemples sans logique temporelle
(taquin, sokoban, wordle, puissance4, jeu2048, lights_out) sont
nettoyés en conséquence. ([`c5a5ffb`](https://github.com/MMarchand-NSI/metagrid/commit/c5a5ffb8d0a344bf70ba355576b1e106778d34c6))

- Merge pull request #4 from MMarchand-NSI/MMarchand-NSI/issue3

Rend update optionnel dans AbstractEngine ([`5efc8bb`](https://github.com/MMarchand-NSI/metagrid/commit/5efc8bbe0060d80e2c940193da791929773bfc65))

## [0.2.0] - 2026-04-13

### 🔧 Changements

- Relocalisation de la méthode init dans les classes, renommage de classes, gestion de la taille des lettres, doc ([`4a4cd66`](https://github.com/MMarchand-NSI/metagrid/commit/4a4cd669576802ac5ff8f5a0619bd5dfcfd5dbec))

- Refonte de l'API : décorateurs pour les callbacks, nettoyage

- Remplacement de start(init, fn_click, ...) par des décorateurs @game.init, @game.draw, @game.update, @game.callback_click, @game.callback_key
- start() ne prend plus aucun paramètre
- Suppression de show_init_dialog et InformationView
- exit() implémenté avec window.close()
- Gestion d'erreur explicite sur set_cell_image si image non chargée
- Documentation des calques couleur/image/char
- Mise à jour de tous les exemples en conséquence
- Correction d'un bug dans sokoban (dimensions de la grille avant init) ([`21cd74f`](https://github.com/MMarchand-NSI/metagrid/commit/21cd74fedbc1bd760820dd16429424739d6c3d7d))

- Ajout de la GitHub Action de publication PyPI via OIDC ([`1600c5f`](https://github.com/MMarchand-NSI/metagrid/commit/1600c5f6a70a61017b6abefbb5d7b4272ca9a443))

- Ajout du script de release ([`21551f4`](https://github.com/MMarchand-NSI/metagrid/commit/21551f4af60f748b8f09e3bb0256e50a03ca7b6a))

## [0.1.3] - 2025-10-31

### 🔧 Changements

- First commit ([`004f876`](https://github.com/MMarchand-NSI/metagrid/commit/004f87680bf56dec148361f89b17b8c0dbd538fa))

- Lockfile ([`490c1a8`](https://github.com/MMarchand-NSI/metagrid/commit/490c1a8e5d8c40f98d328110083dd6a1268d617d))

- Nettoyage ([`c848d99`](https://github.com/MMarchand-NSI/metagrid/commit/c848d997097e82d0beea4b17932fdf8e46d70ed6))

- Modification pyproject ([`e19f45d`](https://github.com/MMarchand-NSI/metagrid/commit/e19f45db76077dee25d195e1250d550309c93697))

- Rename to metagrid cause already taken ([`8a8c93d`](https://github.com/MMarchand-NSI/metagrid/commit/8a8c93d9ff667cc017a80a9def1ba146f9d694d9))

- Update doc ([`20677d0`](https://github.com/MMarchand-NSI/metagrid/commit/20677d0e9328166c659fb7ef1ecb1a0708149e19))

- Modif hatch ([`a97c15a`](https://github.com/MMarchand-NSI/metagrid/commit/a97c15aa9ae00cae837d11e1369e1d0e5ca52f52))

- Ajout de py.typed ([`7f7f2a7`](https://github.com/MMarchand-NSI/metagrid/commit/7f7f2a77e459ad48abf2392da0e9d43bb4dfeaee))


