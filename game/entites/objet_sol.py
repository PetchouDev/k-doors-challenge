# Libraires de la bibliothèque standard
from __future__ import annotations
from typing import TYPE_CHECKING, Any
import importlib
import datetime

# Bibliothèques tierces
import pygame
from pygame import font as pyfont

# Bibliothèques de l'application
from engine.utils import Vector
from .entite import Entite
from ..constantes import DISTANCE_POUR_RAMASSER_OBJET, DISTANCE_AFFICHAGE_NOM_OBJET


if TYPE_CHECKING:
    from engine.ui.tilemap import Tilemap
    from ..objets import Objet
    from .joueur import Joueur
    from typing import Optional


class ObjetAuSol(Entite):
    """Une classe représentant un objet au sol dans le jeu"""

    __slots__ = ("objet", "recuperable_a")

    def __init__(self, objet:Objet, position:Vector, collectible=True) -> None:
        """
        Initialise un objet sol.

        Paramètres:
            - objet (Objet): L'objet à placer au sol
            - position (Vector): La position de l'objet
            - collectible (bool): Indique si l'objet est collectible ou non

        Retourne:
            None
        """
        # Appeler le constructeur de la classe mère
        super().__init__(
            nom=objet.nom,
            vie=-1,
            vie_max=-1,
            position=position,
            vitesse=0
        )
        self.collectible = collectible
        if not collectible:
            self.vitesse = -10
        self.objet = objet
        self.recuperable_a: Optional[datetime.datetime] = None

        self.rect = self.image.get_rect()
        self._font = None
    
    @property
    def image(self) -> Any | pygame.Surface:
            """
            Renvoie l'image de l'objet.
            
            Returns:
                pygame.Surface: L'image de l'objet
            """
            return self.objet.image
    
    def get_image(self, row, col) -> pygame.Surface:
        """
        Renvoie l'image correspondante à la position spécifiée.

        Args:
            row (int): Le numéro de ligne de l'image.
            col (int): Le numéro de colonne de l'image.

        Returns:
            pygame.Surface: L'image correspondante à la position spécifiée.
        """
        return self.objet.get_image(row, col)
    
    def load_font(self) -> None:
        """
        Charge la police de caractères utilisée pour afficher du texte.
        """
        self._font = pyfont.SysFont("monospace", 20, bold=True)
    
    @property
    def font(self) -> pyfont.Font:
        """
        Renvoie la police de caractères utilisée par l'objet.

        Si la police n'a pas encore été chargée, elle est chargée avant d'être renvoyée.

        Returns:
            La police de caractères utilisée par l'objet.
        """
        if not self._font:
            self.load_font()
        return self._font
    
    def draw(self, screen, player_pos: Vector, map: Tilemap) -> None:
        """
        Dessine l'objet sol sur l'écran.

        Args:
            screen (pygame.Surface): La surface de l'écran sur laquelle dessiner.
            player_pos (Vector): La position du joueur.
            map (Tilemap): La carte du jeu.

        Returns:
            None
        """
        topleft = super().draw(screen, player_pos, map)
        if self.real_pos.distance_between(player_pos) <= DISTANCE_AFFICHAGE_NOM_OBJET:
            label = self.objet.label

            text = self.font.render(label, True, (0, 0, 0))
            screen.blit(text, (topleft[0] + self.width//2 - text.get_width()//2, topleft[1] - 20))

    def ramasser(self, joueur:Joueur) -> bool:
        """Permet au joueur de ramasser l'objet

        Args:
            joueur (Joueur): Le joueur qui ramasse l'objet

        Retourne:
            bool: True si l'objet a été ramassé, False sinon
        """
        # Si le joueur est trop loin, on ne peut pas ramasser l'objet
        if (not self.recuperable_a or self.recuperable_a < datetime.datetime.now()) and self.real_pos.distance_between(joueur.real_pos) <= DISTANCE_POUR_RAMASSER_OBJET:
            est_ajoute = joueur.ajouter_inventaire(self.objet)
            return est_ajoute == True # Renvoie False même si l'objet a été rajouté, tant qu'il y en reste au sol
            # Cela permet de ne pas supprimer l'objet du sol si l'inventaire est plein
        
        return False
    
    def from_json(data_json: dict) -> ObjetAuSol:
        """
        Crée un objet ObjetAuSol à partir des données JSON.

        Args:
            data_json (dict): Les données JSON contenant les informations de l'objet au sol.

        Returns:
            ObjetAuSol: L'objet au sol créé à partir des données JSON.
        """
        module_objets = importlib.import_module("game.objets") # Importe le module objets
        # On importe la classe correspondante et on crée l'objet
        objet = getattr(module_objets, data_json["objet"][0]).from_json(data_json["objet"][1])
        return ObjetAuSol(objet, Vector.from_json(data_json["position"]), data_json["collectible"])

    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Retourne:
            dict: Le dictionnaire JSON représentant l'objet.
        """
        return {
            "objet": [self.objet.__class__.__name__, self.objet.to_json()],
            "position": self.position.to_json(),
            "collectible": self.collectible
        }
