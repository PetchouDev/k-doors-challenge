from __future__ import annotations

import pygame

from .objet import Objet

class Cle(Objet):
    """Une classe représentant une clé, un objet consommable du jeu qui ouvre des portes"""

    __slots__ = ["sheet", "rect"]

    def __init__(self, quantite:int=1) -> None:
        """
        Initialise un objet de type Clé.

        Args:
            quantite (int, optional): La quantité de clés. Par défaut, 1.
        """
        
        super().__init__(
            nom="Clé",
            description="Ouvre des portes",
            quantite=quantite,
            quantite_max=1000,
        )
        
        self.sheet = pygame.image.load("ressources/objects/key.png")
        self.image = pygame.Surface((32, 32))
        self.image.blit(self.sheet, (0, 0), (0, 0, 32, 32))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        
    def from_json(data_json: dict) -> Cle:
        """
        Crée une instance de la classe Cle à partir d'un dictionnaire JSON.

        Args:
            data_json (dict): Le dictionnaire JSON contenant les données de la clé.

        Returns:
            Cle: Une instance de la classe Cle avec les données du dictionnaire JSON.
        """
        return Cle(quantite=data_json["quantite"])
