from __future__ import annotations
import uuid
from ..utils import get_image
import pygame
import time
from engine.utils import Vector
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entites import Joueur

class Objet:
    """Une classe représentant un objet du jeu"""

    __slots__ = ("id", "nom", "description", "image", "quantite", "quantite_max", "est_selectionne", "offsets")

    def __init__(self, nom:str="Lorem Ipsum", description:str="Lorem Ipsum", quantite:int=1, quantite_max:int=1, est_selectionne:bool=False) -> None:
        self.id = uuid.uuid4()
        self.nom = nom
        self.description = description
        self.quantite = quantite
        self.quantite_max = quantite_max
        self.est_selectionne = est_selectionne # Si l'objet est sélectionné dans l'inventaire

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
    
    def __str__(self) -> str:
        return self.nom


    def __eq__(self, o: object) -> bool:
        return o.id == self.id

    def utiliser(self, *args):
        ...
    
    def from_json(data_json: dict) -> Objet:
        return Objet(
            nom = data_json["nom"],
            description = data_json["description"],
            quantite = data_json["quantite"],
            quantite_max = data_json["quantite_max"],
            est_selectionne = data_json["est_selectionne"]
        )

    @property
    def label(self) -> str:
        return f"{self.nom} (x{self.quantite})"

    def to_json(self) -> dict:
        return {
            "nom": self.nom,
            "description": self.description,
            "quantite": self.quantite,
            "quantite_max": self.quantite_max,
            "est_selectionne": self.est_selectionne
        }
    
    def get_image(self, row:int, col:int) -> pygame.Surface:
        """Récupère une image de la feuille de sprite"""
        return get_image(self, row, col)

    def draw(self, screen: pygame.Surface, player:Joueur) -> None:
        """Dessine l'objet sur l'écran"""

        player_pos = Vector(*player.rect.topleft)
        self.rect.topleft = (player_pos + self.offsets[player.orientation] + player.frame*Vector(1, -1)).coords
            
            
        
        screen.blit(self.image, self.rect.topleft)
        
    
