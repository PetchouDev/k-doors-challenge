import pygame


class Tileset:
    """Classe représentant la feuille de textures de la carte."""

    __slots__ = ["tile_size", "tiles"]

    def __init__(self, path: str, tile_size: tuple[int, int] = (8, 8), mode: str = "") -> None:
        """
        Initialise un objet Tileset.

        Paramètres:
            path (str): Le chemin vers l'image de la feuille de textures.
            tile_size (tuple[int, int]): La taille des tuiles de la feuille de textures.
            mode (str): Le mode de la feuille de textures.

        Returns:
            None
        """
        self.tile_size = tile_size
        self.tiles = []
        self.load(path, mode)

    def load(self, path: str, name: str = "") -> None:
            """
            Charge les tuiles à partir d'un fichier image spécifié par le chemin `path`.
            Les tuiles sont stockées dans la liste `self.tiles`.
            
            Args:
                path (str): Le chemin du fichier image contenant les tuiles.
                name (str, optional): Le nom du tileset. Par défaut, il est vide.
            
            Returns:
                None
            """
            
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
            """
            Renvoie la surface correspondante à l'index spécifié.

            Args:
                index (int): L'index de la surface à récupérer.

            Returns:
                pygame.Surface: La surface correspondante à l'index spécifié.
            """
            return self.tiles[index]
    
    def __len__(self) -> int:
            """
            Renvoie la longueur du tileset.
            
            Retourne le nombre de tuiles dans le tileset.
            
            Returns:
                int: La longueur du tileset.
            """
            return len(self.tiles)
    
    def draw(self, screen: pygame.Surface) -> None:
            """
            Dessine les tuiles du tileset sur l'écran.

            Args:
                screen (pygame.Surface): La surface sur laquelle dessiner les tuiles.
            
            Returns:
                None
            """
            for i, tile in enumerate(self.tiles):
                screen.blit(tile, (i * self.tile_size[0], 0))
