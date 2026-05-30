# Changelog

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


