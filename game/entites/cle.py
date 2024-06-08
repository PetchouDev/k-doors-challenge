from __future__ import annotations

from typing import TYPE_CHECKING

from engine.utils import Vector
from .entite import Entite

import pygame

from ..constantes import DISTANCE_POUR_RECUPERER_COFFRE_CLE

if TYPE_CHECKING:
    from engine.utils import Vector
    from .joueur import Joueur

class eCle(Entite):
    """Une classe représentant une entité de type clé dans le jeu"""

    def __init__(self, position: Vector) -> None:
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
    
    def get_frame(self, velocity: Vector):
        return self.image

    def from_json(data_json: dict) -> Cle:
        return Cle(
            position=Vector(data_json["position"]["x"], data_json["position"]["y"])
        )

    def to_json(self) -> dict:
        super_json = super().to_json()
        return {**super_json, "est_recuperee": self.est_recuperee}

