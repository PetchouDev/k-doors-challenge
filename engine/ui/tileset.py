import pygame

#from game.constantes import *

class Tileset:
    def __init__(self, path: str, tile_size: tuple[int, int] = (8, 8), mode: str = ""):
        self.tile_size = tile_size
        self.tiles = []
        self.load(path, mode)

    def load(self, path: str, name: str = ""):
        image = pygame.image.load(path)
        #image = image.convert_alpha()
        for y in range(0, image.get_height(), self.tile_size[1]):
            for x in range(0, image.get_width(), self.tile_size[0]):
                tile = pygame.transform.scale(image.subsurface(pygame.Rect(x, y, self.tile_size[0], self.tile_size[1])), (32, 32))
                self.tiles.append(tile)

        # process the name of the tileset
        if name == "terrain":
            self.tiles = {
                "ground": self.tiles[580],
                "down_left_int_wall": self.tiles[568],
                "down_right_int_wall": self.tiles[571],
                "up_left_int_wall": self.tiles[472],
                "up_right_int_wall": self.tiles[475],
                "up_wall": self.tiles[473],
                "down_wall": self.tiles[570],
                "left_wall": self.tiles[504],
                "right_wall": self.tiles[539],
                "stone": self.tiles[454],
                "up_left_ext_wall": self.tiles[410],
                "up_right_ext_wall": self.tiles[411],
                "down_left_ext_wall": self.tiles[442],
                "down_right_ext_wall": self.tiles[443],
            }
            
    def get(self, index: int) -> pygame.Surface:
        return self.tiles[index]
    
    def __len__(self):
        return len(self.tiles)
    
    def draw(self, screen: pygame.Surface):
        for i, tile in enumerate(self.tiles):
            screen.blit(tile, (i * self.tile_size[0], 0))

        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tileset")
    tileset = Tileset("ressources/tileset.png", (8, 8))
    tileset.draw(screen)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()