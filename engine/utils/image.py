import pygame

def resize(image: pygame.Surface, coeff: float) -> pygame.Surface:
    """
    Redimensionne une image selon un coefficient donné.

    Args:
        image (pygame.Surface): L'image à redimensionner.
        coeff (float): Le coefficient de redimensionnement.

    Returns:
        pygame.Surface: L'image redimensionnée.
    """
    image = pygame.transform.scale(image, (image.get_width() * coeff, image.get_height() * coeff))
    image.set_colorkey((0, 0, 0))  
    return image