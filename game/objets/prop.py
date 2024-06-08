import pygame

from engine.utils import Vector

from game.objets.objet import Objet


class Prop(Objet):
    """Une classe représentant un objet au sol non ramassable dans le jeu"""

    def __init__(self, nom:str, nom_image: str) -> None:
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
        return self.nom

    def to_json(self) -> dict:
        return {
            "image": self.nom_image,
            "nom": self.nom
        }
    
    def from_json(data_json: dict):
        return Prop(
            nom=data_json["nom"],
            nom_image=data_json["image"]
        )
        
    

