import pygame

def resize(image: pygame.Surface, coeff: float) -> pygame.Surface:
    image = pygame.transform.scale(image, (image.get_width() * coeff, image.get_height() * coeff))
    image.set_colorkey((0, 0, 0))  
    return image