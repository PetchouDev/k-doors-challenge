from __future__ import annotations

import pygame

from engine.utils import Vector

from game.objets.objet import Objet


class Prop(Objet):
    """Une classe représentant un objet au sol non ramassable dans le jeu"""

    __slots__ = ["nom_image", "sheet", "rect"]

    def __init__(self, nom:str, nom_image: str) -> None:
        """
        Initialise un objet Prop avec un nom et une image.

        Args:
            nom (str): Le nom de l'objet.
            nom_image (str): Le chemin vers l'image de l'objet.
        """
        # Appeler le constructeur de la classe mère
        super().__init__(
            nom=nom,
            description="Un objet au sol",
            quantite=1,
            quantite_max=1
        )
        self.nom_image = nom_image
        self.sheet = pygame.image.load(nom_image)
        self.image = pygame.Surface((48, 48))
        self.image.blit(self.sheet, (0, 0), (0, 0, 48, 48))
        self.image.set_colorkey((0, 0, 0))
        #pygame.transform.rotozoom(self.image, 0, 0.1)
        self.rect = self.image.get_rect()
    
    @property
    def label(self) -> str:
        """
        Renvoie le nom de l'objet.
        
        Returns:
            str: Le nom de l'objet.
        """
        return self.nom

    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Retourne:
            dict: Un dictionnaire contenant les attributs de l'objet.
        """
        return {
            "image": self.nom_image,
            "nom": self.nom
        }
    
    def from_json(data_json: dict) -> Prop:
        """
        Crée une instance de la classe Prop à partir d'un dictionnaire JSON.

        Args:
            data_json (dict): Le dictionnaire JSON contenant les données de la Prop.

        Returns:
            Prop: L'instance de la classe Prop créée à partir des données JSON.
        """
        return Prop(
            nom=data_json["nom"],
            nom_image=data_json["image"]
        )
