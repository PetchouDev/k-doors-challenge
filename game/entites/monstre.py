from __future__ import annotations

from .entite import Entite

from typing import TYPE_CHECKING
from engine.utils import Vector
import pygame
import random

import time

if TYPE_CHECKING:
    ...


class Gobelin(Entite):
    """Un gobelin, une entité hostile du jeu"""

    def __init__(self, position: Vector) -> None:
        super().__init__(
            nom="Gobelin",
            vie=20,
            vie_max=20,
            position=position,
            vitesse=0.6, # lent
            degats=10,
            width=16,
            height=24,
            temps_attente=1000 # 1 seconde
        )

        # Déclarer la feuille de texture du monstre
        self.sheet = pygame.image.load(f"ressources/entities/gobelin_{random.choice([1, 2])}.png")
        self.image_sheet_size = (32, 32)

        # Charger l'image du monstre
        self.image = self.get_image(1, 4)

        # Créer un rect pour l'image du monstre
        self.rect = self.image.get_rect()
        
        # definir une oriantation pour le monstre (par défault au sud)
        self.orientation = "S"

        # compter l'image d'animation
        self.frame = 0

        # compter le temps de chaque frame
        self.clock = 0

        # répertorier les images {orientation: {frame: image}}
        self.images = {
            "S": {
                1: self.get_image(0, 4),
                2: self.get_image(1, 4),
                3: self.get_image(2, 4),
                0: self.get_image(3, 4),
            },
            "N": {
                1: self.get_image(0, 7),
                2: self.get_image(1, 7),
                3: self.get_image(2, 7),
                0: self.get_image(3, 7),
            },
            "O": {
                1: self.get_image(0, 5),
                2: self.get_image(1, 5),
                3: self.get_image(2, 5),
                0: self.get_image(3, 5),
            },
            "E": {
                1: self.get_image(0, 6),
                2: self.get_image(1, 6),
                3: self.get_image(2, 6),
                0: self.get_image(3, 6),
            }
        }

        # image de départ
        self.image = self.images["S"][1]

        # rect
        self.rect = self.image.get_rect()


    def from_json(data_json: dict) -> Gobelin:
        """
        Creates a Gobelin object from a JSON dictionary.

        Args:
            data_json (dict): The JSON dictionary containing the Gobelin data.

        Returns:
            Gobelin: The Gobelin object created from the JSON data.
        """
        return Gobelin(
            position=Vector.from_json(data_json["position"])
        )
    
    def get_frame(self, velocity: Vector) -> pygame.Surface:
        # obtenir la frame
        elapsed_time = time.time() - self.last_frame
        if elapsed_time > 0.2:
            self.frame = (self.frame + 1) % 4
            self.last_frame = time.time()

        return self.images[self.orientation][self.frame]


