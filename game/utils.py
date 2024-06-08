import pygame
from typing import Optional

def get_image(self, col:int, row:int, resize:Optional[int]=None) -> pygame.Surface:
    """Récupère une image de la feuille de sprite"""
    x,y = self.image_sheet_size
    image = pygame.Surface((x, y))
    image.blit(self.sheet, (0, 0), (col*x, row*y, x, y))

    if resize:
        # redimensionner l'image 
        coef = resize / x
        image = pygame.transform.rotozoom(image, 0, coef)

    image.set_colorkey((0, 0, 0))  

    return image