import pygame
from engine.utils import Vector

class Porte:
    def __init__(self, x, y) -> None:
        self.position = Vector(x, y) * 32
        self.x = x
        self.y = y

        self.sheet = pygame.image.load("ressources/objects/porte.png")
        self.image = pygame.Surface((64, 64))
        self.image.blit(self.sheet, (0, 0), (0, 0, 64, 64))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        print(x, y)

    def draw(self, screen: pygame.Surface, offset:Vector):
        render_pos = self.position + offset
        self.rect.topleft = render_pos.coords
        screen.blit(self.image, self.rect.topleft)


    def to_json(self) -> dict:
        return {
            "x": self.x,
            "y": self.y
        }
    
    def from_json(data_json: dict):
        return Porte(
            x=data_json["x"],
            y=data_json["y"]
        )

