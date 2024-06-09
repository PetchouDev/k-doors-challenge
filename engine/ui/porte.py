import pygame

from engine.utils import Vector


class Porte:
    """Classe représentant une porte dans le jeu."""

    __slots__ = ["position", "x", "y", "sheet", "image", "rect"]

    def __init__(self, x, y) -> None:
        """
        Initialise une instance de la classe Porte.

        :param x: La position en x de la porte.
        :type x: int
        :param y: La position en y de la porte.
        :type y: int
        """
        
        self.position = Vector(x, y) * 32
        self.x = x
        self.y = y

        self.sheet = pygame.image.load("ressources/objects/porte.png")
        self.image = pygame.Surface((64, 64))
        self.image.blit(self.sheet, (0, 0), (0, 0, 64, 64))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

    def draw(self, screen: pygame.Surface, offset:Vector) -> None:
        """
        Dessine l'objet sur l'écran à la position spécifiée.

        Args:
            screen (pygame.Surface): La surface de l'écran sur laquelle dessiner l'objet.
            offset (Vector): Le décalage à appliquer à la position de l'objet.

        Returns:
            None
        """
        render_pos = self.position + offset
        self.rect.topleft = render_pos.coords
        screen.blit(self.image, self.rect.topleft)

    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Retourne:
            dict: Un dictionnaire contenant les coordonnées x et y de l'objet.
        """
        return {
            "x": self.x,
            "y": self.y
        }
    
    def from_json(data_json: dict):
        """
        Crée une instance de la classe Porte à partir d'un dictionnaire JSON.

        Args:
            data_json (dict): Le dictionnaire JSON contenant les données de la porte.

        Returns:
            Porte: Une instance de la classe Porte.
        """
        return Porte(
            x=data_json["x"],
            y=data_json["y"]
        )

