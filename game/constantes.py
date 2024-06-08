DEBUG = False
GHOST = False

# constantes du jeu
FRAME_RATE = 30 # En Hz (ou s-1)
PLAYER_SPEED = 400 if GHOST else 200 if DEBUG else 140 # En pixels par secondes
NB_EMPLACEMENTS_INVENTAIRE = 5
NB_COEUR_MAX = 5
VIE_JOUEUR_DEFAUT = 100
VITESSE_MAX_JOUEUR = 240

DISTANCE_POUR_RAMASSER_OBJET = 30 # En pixels
DISTANCE_AGRO_MONSTRES = 200 # En pixels
DISTANCE_AGRO_STOP_MONSTRES = 30 # En pixels
DISTANCE_ATTAQUE_MONSTRE = 35 # En pixels
DISTANCE_ATTAQUE_JOUEUR = 60 # En pixels
DISTANCE_AFFICHAGE_NOM_OBJET = 100 # En pixels

TAILLE_BORDURE_INVENTAIRE = 3 # En pixels

RECUL_DEGATS_ATTAQUEE = 30 # En pixels, pour l'entité attaquée
RECUl_DEGATS_ATTAQUANT = 10 # En pixels, pour l'attaquant

DUREE_ROUGE_ENTITE_APRES_ATTAQUE = 500 # En ms


TILEMAP_PATH = "ressources/environment/tileset.png"

DEAD_ZONE = (150, 125) # En pixels (x, y)

PLAYER_SPRITE = "ressources/players/player.png" # Dossier contenant les sprites du joueur (celui de Charlie par défaut)

SWORD_SPRITE = "ressources/objects/sword.png" # Dossier contenant les sprites de l'épée

TAILLE_DONGEON = (50, 50) # Taille du dongeon en tiles


SOUNDS = { 
    "OST": [
            "Egress Cave OST Version.mp3",
            "Forgotten Wasteland OST Version.mp3",
            "Ruins Zone OST Version.mp3"
        ],
    "cle": "cle.mp3",
    "coup": "coup.mp3",
    "cri": "cri_gobelin.mp3",
    "epee": "epee.mp3",
    "game_over": "game_over.mp3",
    "pas": "pas.mp3",
    "porte": "porte.mp3",
    "soin": "soin.mp3",
    "victoire": "victoire.mp3",
}

DELAIS_MORT = 1000 # En ms