import metagrid
from random import choice


# liste de mots pourris
mots_5_lettres = [
    "abime", "abord", "about", "acier", "actif", "adieu", "aider", "aigre", "aimer", "alarm",
    "album", "allee", "alpha", "amour", "angle", "anime", "appel", "arbre", "argent", "aride",
    "armee", "arret", "asile", "astre", "attic", "aube", "audit", "avion", "avoir", "avril",
    "bagne", "balai", "banal", "barbe", "baron", "bases", "basse", "beaux", "belge", "belle",
    "berce", "berge", "berne", "besoin", "bible", "bijou", "blanc", "bleus", "blond", "blues",
    "boire", "boite", "bonne", "borde", "borne", "bosse", "botte", "bouge", "bouse", "brave",
    "brise", "bruit", "brume", "buche", "bureau", "cache", "cadre", "cagee", "cairn", "calme",
    "canon", "carte", "cause", "ceint", "celle", "cerne", "cesse", "chaine", "champ", "chant",
    "chaos", "chaud", "chefs", "chien", "choix", "chope", "chose", "clair", "classe", "clore",
    "clown", "coeur", "colis", "colle", "combe", "compte", "conte", "copie", "corne", "corps",
    "coton", "coupe", "court", "crane", "crier", "croix", "culte", "cycle", "danse", "datte",
    "debut", "degre", "delai", "demie", "dense", "depot", "derme", "devin", "dicte", "digne",
    "diner", "disco", "donne", "douce", "douze", "drame", "droit", "durci", "duree", "echec",
    "eclat", "ecole", "effet", "elles", "email", "encre", "ennui", "entra", "envie", "erige",
    "escal", "esprit", "etage", "etang", "etats", "etend", "etude", "evite", "exact", "exige",
    "extra", "fable", "facon", "facon", "faire", "faims", "farde", "farce", "faste", "fatig",
    "faute", "femur", "ferme", "fibre", "fiche", "filer", "fille", "final", "finir", "fixer",
    "flanc", "fleur", "folie", "force", "forme", "fosse", "fouet", "foule", "franc", "froid",
    "fruit", "fusion", "gagee", "gains", "garde", "gazer", "genre", "germe", "gifle", "glace",
    "gouté", "goutte", "grace", "grand", "grive", "grole", "grues", "guide", "habit", "haine",
    "halte", "hante", "hasard", "havre", "herbe", "heure", "hiver", "honor", "hotel", "houle",
    "humain", "hurle", "image", "imite", "index", "infir", "intro", "issue", "jambe", "jaune",
    "jeter", "jeudi", "jouer", "jouet", "joyau", "judge", "juste", "laver", "lente", "libre",
    "ligne", "liste", "livre", "local", "lourd", "lueur", "lundi", "lutte", "maire", "major",
    "malin", "manie", "manif", "marge", "masse", "matin", "mauve", "merci", "merle", "metre",
    "miens", "miner", "mince", "moins", "monde", "monte", "moral", "motif", "moule", "moyen"
]

NB_LIGNES = 6
NB_COLONNES = 5
CELL_SIZE = 100

grille: list[list[str]] # Grille de lettres
icurseur: int           # ligne du curseur
jcurseur: int           # colonne du curseur
mot_secret: str         # mot à deviner
flag_game_over: bool    # True si le jeu est terminé

jeu = metagrid.create(NB_LIGNES, NB_COLONNES, CELL_SIZE, 4)

images = ["curseur", "faux", "malplace", "trouve", "vide"]
for nom in images:
    jeu.load_image(nom, f"assets/wordle/{nom}.png")


def gagne() -> bool:
    """
    Gagné?
    """
    return all(mot_secret[j]==grille[icurseur][j] for j in range(5))


@jeu.init
def init():
    """
    Initialisation des variables du jeu
    """
    global grille, icurseur, jcurseur, mot_secret, flag_game_over
    grille = [ ['']*5 for _ in range(6)]
    icurseur, jcurseur = 0, 0
    mot_secret = choice(mots_5_lettres).upper()
    flag_game_over = False


@jeu.callback_key
def touche(s: str):
    global icurseur, jcurseur, grille, flag_game_over
    if ord(s) == 65307:   # ESC
        init()
        return
    if flag_game_over:
        return
    if jcurseur == 5 and ord(s) == 65293: # ENTER
        if gagne():
            jeu.play_sound(r"assets/sounds/victory.mp3")
            flag_game_over = True
        elif icurseur==5:
            jeu.play_sound(r"assets/sounds/gameover.mp3")
            flag_game_over = True
        icurseur += 1
        jcurseur = 0
    elif jcurseur > 0 and ord(s) == 65288:  # BACKSPACE
        jcurseur -= 1
        grille[icurseur][jcurseur] = ''
    elif jcurseur < 5 and s>='a' and s<='z':
        grille[icurseur][jcurseur] = s.upper()
        jcurseur += 1


@jeu.draw
def dessiner():
    """
    Dessiner toutes les lettres.
    Pour les lignes au dessus du curseur, il faut choisir le sprite en fonction de la place des lettres.
    Sinon il faut afficher vide sauf le curseur
    """
    global icurseur, jcurseur, grille
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            jeu.set_cell_char(i, j, grille[i][j], "#FFFFFF")
            if i<icurseur:
                if grille[i][j] == mot_secret[j]:
                    jeu.set_cell_image(i,j, "trouve")
                elif grille[i][j] in mot_secret:
                    jeu.set_cell_image(i,j, "malplace")
                else:
                    jeu.set_cell_image(i,j, "faux")
            elif (i,j)==(icurseur, jcurseur):
                jeu.set_cell_image(i, j, "curseur")
            else:
                jeu.set_cell_image(i, j, "vide")


@jeu.update
def update():
    pass


jeu.start()
