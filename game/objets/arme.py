# Libraries de la bibliothèque standard
from __future__ import annotations
from typing import List, Tuple, Callable, Any, Optional, TYPE_CHECKING
import datetime
import time

# Bibliothèques tierces
import pygame
pygame.init()

# Bibliothèques de l'application
from engine.utils import Vector
from game.constantes import SWORD_SPRITE
from .objet import Objet
from ..utils import get_image


if TYPE_CHECKING:
    from ..entites import Joueur, Entite


class Arme(Objet):
    """
    Une classe représentant une arme du jeu
    Une arme peut être utilisée et avoir des effets lorsqu'elle est utilisée (avec succès)
    """

    __slots__ = ("degats", "effets", "en_attente", "temps_attente")

    def __init__(
            self, 
            nom:str, description:str, quantite:int=1, quantite_max:int=1, degats:int=0, 
            effets: List[Tuple[Callable, List[Any]]] = [], temps_attente:int = 0) -> None:
        """
        Initialise un objet de type Arme avec les paramètres spécifiés.

        Args:
            nom (str): Le nom de l'arme.
            description (str): La description de l'arme.
            quantite (int, optional): La quantité d'armes. Par défaut 1.
            quantite_max (int, optional): La quantité maximale d'armes. Par défaut 1.
            degats (int, optional): Les dégâts infligés par l'arme. Par défaut 0.
            effets (List[Tuple[Callable, List[Any]]], optional): Les effets spéciaux de l'arme. Par défaut [].
            temps_attente (int, optional): Le temps d'attente avant de pouvoir réutiliser l'arme. Par défaut 0.
        """
        # Appeler le constructeur de la classe mère
        super().__init__(nom, description, quantite, quantite_max)
        self.degats = degats

        # Voir la documentation dans __init__ de la classe Consommable
        self.effets = effets

        self.en_attente: Optional[datetime.datetime] = None
        self.temps_attente = temps_attente
    
    def utiliser(self, joueur: Joueur, entite:Entite) -> bool:
        """Utilise l'objet arme sur une entité (attaque)
        
        Args:
            entite (Any): L'entité sur laquelle attaquer
        
        Retourne:
            bool: True si l'objet a été utilisé avec succès, False sinon (si en attente par exemple)
        """
        # Si l'objet est en attente, on ne peut pas l'utiliser
        if self.en_attente is not None and datetime.datetime.now() < self.en_attente:
            return False

        #Appliquer tous les effets de l'objet
        for effet, args in self.effets:
            getattr(joueur, effet)(*args) # On appelle la méthode de joueur correspondant à l'effet
        
        # Attaquer l'entité
        entite.attaquer(self.degats)
        
        # Appliquer le temps d'attente
        if self.temps_attente is not None:
            # On définit le moment où on pourra ré-utiliser l'objet
            self.en_attente = datetime.datetime.now() + datetime.timedelta(milliseconds=self.temps_attente)
        
    @property
    def label(self) -> str:
        """
        Renvoie une chaîne de caractères représentant l'arme.

        Returns:
            str: La chaîne de caractères représentant l'arme, au format "{nom} ({degats} dégâts)".
        """
        return f"{self.nom} ({self.degats} dégâts)"

    def from_json(data_json: dict) -> Arme:
        """
        Crée une instance de la classe Arme à partir d'un dictionnaire JSON.

        Args:
            data_json (dict): Le dictionnaire JSON contenant les données de l'arme.

        Returns:
            Arme: L'instance de la classe Arme créée à partir des données JSON.
        """
        arme = Arme(
            nom = data_json["nom"],
            description = data_json["description"],
            quantite = data_json["quantite"],
            quantite_max = data_json["quantite_max"],
            degats = data_json["degats"],
            effets=data_json["effets"],
            temps_attente = data_json["temps_attente"]
        )
        return arme

    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Retourne:
            dict: Le dictionnaire JSON représentant l'objet.
        """
        return {
            **super().to_json(),
            "degats": self.degats,
            "effets": self.effets,
            "temps_attente": self.temps_attente
        }

class Epee(Arme):
    """Une classe représentant une épée, une arme du jeu qui inflige des dégâts à une entité"""

    __slots__ = ("frame", "clock", "last_frame", "sheet", "image_sheet_size", "images", "offsets", "image", "rect", 
                    "temps_attente", "icone")

    def __init__(self, degats:int=5) -> None:
        """
        Initialise un objet Arme avec les paramètres spécifiés.

        Args:
            degats (int, optional): Les points de dégâts infligés par l'arme. Par défaut 5.
        """
        
        super().__init__(
            nom = "Épée",
            description = "Une épée basique. Inflige x points de dégâts à une entité. Aucun effet spécial. 0.2s d'attente entre 2 attaques.",
            degats = degats,
            temps_attente = 200 # en millisecondes
        )
        
        # variables d'animation
        self.frame = 0
        self.clock = 0
        self.last_frame = time.time()

        # feuillets de sprite
        self.sheet = pygame.image.load(SWORD_SPRITE)
        self.image_sheet_size = (96, 96)

        icone= pygame.Surface((64, 64))
        icone_src = pygame.image.load("ressources/objects/epee_icon.png")
        icone.blit(icone_src, (0, 0))
        icone.set_colorkey((0, 0, 0))

        del icone_src

        self.images = {
            "common": icone,
            "static": self.get_image(7, 0),
            "N": {
                0: [self.get_image(5, 1), Vector(-10, -10)],
                1: [self.get_image(5, 2), Vector(-28, -10)],
                2: [self.get_image(5, 2), Vector(-28, -10)], # on double la dernère frame car l'anima n'est pas une boucle, sinon on ne la verait pas (ou 30ms...)
            },
            "NE": {
                0: [self.get_image(4, 3), Vector(-10, 10)],
                1: [self.get_image(6, 2), Vector(-15, -20)],
                2: [self.get_image(6, 2), Vector(-15, -20)],
            },
            "E": {
                0: [self.get_image(4, 2), Vector(-10, -10)],
                1: [self.get_image(5, 1), Vector(0, -20)],
                2: [self.get_image(5, 1), Vector(0, -20)],
            },
            "SE": {
                0: [self.get_image(7, 3), Vector(-15, 10)],
                1: [self.get_image(6, 1), Vector(-15, 5)],
                2: [self.get_image(6, 1), Vector(-15, 5)],
            },
            "S": {
                0: [self.get_image(4, 1), Vector(-40, 10)],
                1: [self.get_image(4, 2), Vector(-10, 10)],
                2: [self.get_image(4, 2), Vector(-10, 10)],
            },
            "SO": {
                0: [self.get_image(5, 3),Vector(-30, -20)],
                1: [self.get_image(4, 1), Vector(-36, 15)],
                2: [self.get_image(4, 1), Vector(-36, 15)],
            },
            "O": {
                0: [self.get_image(7, 1), Vector(-30, -10)],
                1: [self.get_image(7, 2), Vector(-30, 10)],
                2: [self.get_image(7, 2), Vector(-30, 10)],
            },
            "NO": {
                0: [self.get_image(6, 3), Vector(-15, -30)],
                1: [self.get_image(7, 1), Vector(-30, -10)],
                2: [self.get_image(7, 1), Vector(-30, -10)],
            },
        }

        """self.images["common"] = self.images["NO"][1]

        self.offsets = {
            "N": Vector(-24, -10),
            "NE": Vector(-10, -10),
            "E": Vector(-10, 10),
            "SE": Vector(-15, 10),                      # Utilisation pour régler les offsets, les textures de l'épée étant toutes décalées...
            "S": Vector(-10, 10),
            "SO": Vector(-30, -20),
            "O": Vector(-10, 20),
            "NO": Vector(-30, -10),
        } """

        self.offsets = {
            "N": Vector(-20, 0),
            "NE": Vector(-20, 0),
            "E": Vector(-24, 0),
            "SE": Vector(-32, 0),
            "S": Vector(-36, 0),
            "SO": Vector(-36, 0),
            "O": Vector(-36, 0),
            "NO": Vector(-32, 0),
        }

        # image 
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect()
    
    def from_json(data_json: dict) -> Epee:
        """
        Crée une instance de la classe Epee à partir des données JSON fournies.

        Args:
            data_json (dict): Les données JSON contenant les informations de l'épée.

        Returns:
            Epee: Une instance de la classe Epee avec les informations extraites des données JSON.
        """
        epee = Epee()
        epee.est_selectionne = data_json["est_selectionne"]
        return epee

    def get_image(self, row:int, col:int) -> pygame.Surface:
        """
        Renvoie l'image correspondante à la position donnée.

        Args:
            row (int): La ligne de l'image dans la grille.
            col (int): La colonne de l'image dans la grille.

        Returns:
            pygame.Surface: L'image correspondante à la position donnée.
        """
        return get_image(self, col, row, resize=64)
    
    def draw(self, screen: pygame.Surface, player:Joueur) -> None:
        """
        Dessine l'arme à l'écran en fonction de l'état du joueur.

        Args:
            screen (pygame.Surface): La surface sur laquelle l'arme doit être dessinée.
            player (Joueur): Le joueur dont l'état détermine l'apparence de l'arme.

        Returns:
            None
        """
        
        self.clock = time.time()

        # si le joueur n'est pas en train d'attaquer, on affiche l'épée normalement
        if not player.attaque:
            # réinitialiser l'animation
            self.frame = 0
            self.last_frame = 0
            self.image = self.images["static"]
            player_pos = Vector(*player.rect.topleft)
            self.rect.topleft = (player_pos + self.offsets[player.orientation] + player.frame*Vector(1, -1)).coords
            
            
        # sinon, on affiche l'épée en fonction de l'orientation du joueur
        elif self.clock - self.last_frame > 0.2:
            self.last_frame = self.clock # on met à jour le dernier moment où on a changé de frame
            self.image, topleft = self.images[player.orientation][self.frame] # on récupère l'image et le décalage
            self.frame = (self.frame + 1) % 3 # on prepare la prochaine frame
            self.rect.topleft = (Vector(*player.rect.topleft) + topleft).coords # on place la nouvelle image à la bonne position
            

        # si l'animation est terminée (2 frames), on débloque le joueur
        if self.frame == 0 :
            player.en_attente = None
            player.attaque = False
            
        
        screen.blit(self.image, self.rect.topleft)

