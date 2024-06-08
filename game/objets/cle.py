from __future__ import annotations

from typing import List, Tuple, Callable, Any, Optional, TYPE_CHECKING
import datetime
import pygame

from .objet import Objet

if TYPE_CHECKING:
    from ..entites.joueur import Joueur



class Cle(Objet):
    """Une classe représentant une clé, un objet consommable du jeu qui ouvre des portes"""

    def __init__(self, quantite:int=1) -> None:
        super().__init__(
            nom="Clé",
            description = "Ouvre des portes",
            quantite = quantite,
            quantite_max = 1000,
            )
        
        self.sheet = pygame.image.load("ressources/objects/key.png")
        self.image = pygame.Surface((32, 32))
        self.image.blit(self.sheet, (0, 0), (0, 0, 32, 32))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        
    def from_json(data_json: dict) -> Cle:
        return Cle(quantite=data_json["quantite"])
