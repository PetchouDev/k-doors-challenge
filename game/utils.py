from typing import Optional

import pygame


def get_image(self, col:int, row:int, resize:Optional[int]=None) -> pygame.Surface:
    """
    Récupère une image à partir d'une feuille de sprites et la redimensionne si nécessaire.

    Args:
        col (int): La colonne de l'image dans la feuille de sprites.
        row (int): La ligne de l'image dans la feuille de sprites.
        resize (Optional[int]): La taille de redimensionnement de l'image (facultatif).

    Returns:
        pygame.Surface: L'image récupérée.

    """
    x,y = self.image_sheet_size
    image = pygame.Surface((x, y))
    image.blit(self.sheet, (0, 0), (col*x, row*y, x, y))

    if resize:
        # redimensionner l'image 
        coef = resize / x
        image = pygame.transform.rotozoom(image, 0, coef)

    image.set_colorkey((0, 0, 0))  

    return image