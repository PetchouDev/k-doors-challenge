from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from engine.utils import Vector

from .entite import Entite

from ..constantes import DISTANCE_POUR_RAMASSER_OBJET

if TYPE_CHECKING:
    from engine.utils import Vector
    from .joueur import Joueur

class Cle(Entite):
    """Une classe représentant une entité de type clé dans le jeu"""

    __slots__ = ["est_recuperee", "sheet", "image", "rect"]

    def __init__(self, position: Vector) -> None:
        """
        Initialise un objet Clé avec les paramètres spécifiés.

        Args:
            position (Vector): La position initiale de la clé.

        Attributes:
            nom (str): Le nom de la clé.
            vie (int): Les points de vie de la clé.
            vie_max (int): Le nombre maximum de points de vie de la clé.
            position (Vector): La position actuelle de la clé.
            vitesse (int): La vitesse de déplacement de la clé.
            degats (int): Les dégâts infligés par la clé.
            est_recuperee (bool): Indique si la clé a été récupérée ou non.
            sheet (pygame.Surface): La feuille d'image contenant l'apparence de la clé.
            image (pygame.Surface): L'image de la clé.
            rect (pygame.Rect): Le rectangle englobant l'image de la clé.
        """
        # Appeler le constructeur de la classe mère
        super().__init__(
            nom="Clé", 
            vie=-1, 
            vie_max=-1, 
            position=position, 
            vitesse=0,
            degats=0,
        )
        self.est_recuperee = False

        self.sheet = pygame.image.load("ressources/objects/key.png")
        self.image = pygame.Surface((32, 32))
        self.image.blit(self.sheet, (0, 0), (0, 0, 32, 32))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

    def recuperer(self, joueur: Joueur) -> bool:
        """Permet au joueur de récupérer la clé

        Args:
            joueur (Joueur): Le joueur qui récupère la clé

        Retourne:
            bool: True si la clé a été récupérée, False sinon
        """
        if self.est_recuperee:
            return False
        
        # Si le joueur est trop loin, on ne peut pas récupérer la clé
        if self.real_pos.distance(joueur.real_pos) <= DISTANCE_POUR_RECUPERER_COFFRE_CLE:
            self.est_recuperee = True
            return True
        
        return False
    
    def get_frame(self, velocity: Vector) -> pygame.Surface:
        """
        Renvoie l'image de la clé.

        Args:
            velocity (Vector): La vélocité de la clé.

        Returns:
            pygame.Surface: L'image de la clé.
        """
        return self.image

    def from_json(data_json: dict) -> Cle:
        """
        Crée une instance de la classe Cle à partir d'un dictionnaire JSON.

        Args:
            data_json (dict): Le dictionnaire JSON contenant les données de la clé.

        Returns:
            Cle: Une instance de la classe Cle avec les données du dictionnaire JSON.
        """
        return Cle(
            position=Vector(data_json["position"]["x"], data_json["position"]["y"])
        )

    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Returns:
            dict: Le dictionnaire JSON représentant l'objet.
        """
        super_json = super().to_json()
        return {**super_json, "est_recuperee": self.est_recuperee}
