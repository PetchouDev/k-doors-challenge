from typing import Any, TYPE_CHECKING

import pygame

from engine.ui.tileset import Tileset
from engine.ui.porte import Porte
from engine.utils.vector import Vector

from game.constantes import TILEMAP_PATH, DEBUG, SOUNDS

if TYPE_CHECKING:
    from game.entites.entite import Entite

# initialiser pygame
pygame.init()
pygame.mixer.init()

class Tilemap:
    """Classe représentant la carte de l'étage du jeu."""

    __slots__ = ["matrice", "size", "tile_size", "walls", "doors", "tilesets", "entree", "sortie", "offset"]

    def __init__(self, matrice:list[list[int]], entree:Vector, sortie:Vector, tile_size:tuple[int, int]=(32, 32)) -> None:
        """
        Initialise un objet Tilemap avec une matrice, une entrée, une sortie et une taille de tuile donnée.

        Paramètres :
            - matrice (list[list[int]]): La matrice de la carte.
            - entree (Vector): La position de l'entrée de la carte.
            - sortie (Vector): La position de la sortie de la carte.
            - tile_size (tuple[int, int]): La taille des tuiles de la carte.

        Renvoie :
            None

        """
        self.matrice = matrice
        self.size = (len(matrice[0]), len(matrice))
        self.tile_size = tile_size
        self.walls:dict[tuple[int, int]: [pygame.Surface]] = {}
        self.doors:dict[tuple[int, int]: [pygame.Surface]] = {}
        self.tilesets = {
            "terrain": Tileset(TILEMAP_PATH, (8, 8), mode="terrain"),
        }

        self.entree = entree
        self.sortie = sortie
        
        self.offset = Vector(0, 0)
        self.setup_walls()
        self.setup_doors()

    def is_wall(self, x, y) -> bool:
        """
        Vérifie si la case aux coordonnées (x, y) est un mur.

        Args:
            x (int): La coordonnée x de la case.
            y (int): La coordonnée y de la case.

        Renvoie:
            bool: True si la case est un mur, False sinon.
        """
        try:
            return self.matrice[y][x] in [0, 2]
        except IndexError:
            return True

    def setup_walls(self) -> None:
        """
        Configure les murs du tilemap en fonction de la matrice de tuiles.

        Cette méthode parcourt la matrice de tuiles et détermine le type de mur à afficher en fonction des tuiles environnantes.
        Les différents types de murs sont définis par des textures spécifiques.

        Renvoie:
            None
        """
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.matrice[y][x] in [0, 2]:
                    walls = self.walls_around(x, y)
                    if ["left", "right", "up", "down", "up_left", "up_right", "down_left", "down_right"] == walls:
                        texture = "stone"
                    elif "right" in walls and "down" in walls and not "left" in walls and not "up" in walls:
                        texture = "down_right_ext_wall"
                    elif "left" in walls and "down" in walls and not "right" in walls and not "up" in walls:
                        texture = "down_left_ext_wall"
                    elif "right" in walls and "up" in walls and not "left" in walls and not "down" in walls:
                        texture = "up_right_ext_wall"
                    elif "left" in walls and "up" in walls and not "right" in walls and not "down" in walls:
                        texture = "up_left_ext_wall"
                    elif not "up" in walls and "left" in walls and "right" in walls and "down" in walls:
                        texture = "down_wall"
                    elif not "down" in walls and "left" in walls and "right" in walls and "up" in walls:
                        texture = "up_wall"
                    elif not "right" in walls and "left" in walls and "up" in walls and "down" in walls:
                        texture = "left_wall"
                    elif not "left" in walls and "right" in walls and "up" in walls and "down" in walls:
                        texture = "right_wall"
                    elif all([i in walls for i in ["right", "left", "down", "up", "up_right", "down_right", "down_left"]]) and not "up_left" in walls:
                        texture = "down_right_int_wall"
                    elif all([i in walls for i in ["right", "left", "down", "up", "up_left", "down_right", "down_left"]]) and not "up_right" in walls:
                        texture = "down_left_int_wall"
                    elif all([i in walls for i in ["right", "left", "down", "up", "up_right", "up_left", "down_right"]]) and not "down_left" in walls:
                        texture = "up_right_int_wall"
                    elif all([i in walls for i in ["right", "left", "down", "up", "up_right", "up_left", "down_left"]]) and not "down_right" in walls:
                        texture = "up_left_int_wall"
                    
                    wall_image = pygame.Surface(self.tile_size)
                    wall_image.blit(self.tilesets["terrain"].tiles[texture], (0, 0))
                    wall_image.set_colorkey((0, 0, 0)) 
                    self.walls[(x, y)] = wall_image
    
    def setup_doors(self) -> None:
            """
            Configure les portes de la carte.
            
            Parcourt la matrice de la carte et identifie les cases contenant une valeur de 2,
            qui représentent les portes. Cette fonction ne fait rien pour le moment.
            """
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    if self.matrice[y][x] == 2:
                        pass

    def walls_around(self, x:int, y:int) -> list[str]:
        """
        Renvoie une liste des murs autour de la position (x, y).

        Args:
            x (int): La coordonnée x de la position.
            y (int): La coordonnée y de la position.

        Envoie:
            list[str]: Une liste contenant les directions des murs autour de la position (x, y).
                      Les directions possibles sont "left", "right", "up", "down", "up_left",
                      "up_right", "down_left" et "down_right".
        """
        walls = []
        if self.is_wall(x-1, y):
            walls.append("left")
        if self.is_wall(x+1, y):
            walls.append("right")
        if self.is_wall(x, y-1):
            walls.append("up")
        if self.is_wall(x, y+1):
            walls.append("down")
        if self.is_wall(x-1, y-1):
            walls.append("up_left")
        if self.is_wall(x+1, y-1):
            walls.append("up_right")
        if self.is_wall(x-1, y+1):
            walls.append("down_left")
        if self.is_wall(x+1, y+1):
            walls.append("down_right")
        return walls

    def draw(self, screen: pygame.Surface, offset=Vector(0, 0), portes: list[Porte] = []) -> None:
            """
            Dessine la carte sur l'écran avec un décalage optionnel et une liste de portes.

            Args:
                screen (pygame.Surface): La surface sur laquelle dessiner la carte.
                offset (Vector, optional): Le décalage de la carte. Par défaut, (0, 0).
                portes (list[Porte], optional): La liste des portes à dessiner. Par défaut, [].

            Returns:
                None
            """
            
            # Nouvel offset
            self.offset += offset

            # Taille de l'écran en tiles
            screen_width, screen_height = screen.get_size()
            tile_width, tile_height = self.tile_size

            # Calculer les limites visibles
            start_x = max(0, -self.offset.x // tile_width)
            start_y = max(0, -self.offset.y // tile_height)

            end_x = min(self.size[0], int(screen_width - self.offset.x) // tile_width + 1)
            end_y = min(self.size[1], int(screen_height - self.offset.y) // tile_height + 1)

            # Convertir en entiers
            start_x, start_y, end_x, end_y = map(int, (start_x, start_y, end_x, end_y))

            # Dessiner le sol en premier
            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    pos = (x * tile_width + self.offset.x, y * tile_height + self.offset.y)
                    screen.blit(self.tilesets["terrain"].tiles["ground"], pos)

                    if DEBUG:
                        # cadriage vert pour les rect des sols
                        pygame.draw.rect(screen, (0, 255, 0), (pos, (tile_width, tile_height)), 1)

                        # dessiner des carrés mauves sur le sol pour l'arrivée et le départ
                        carre = pygame.Surface(self.tile_size)
                        carre.fill((255, 0, 255))
                        screen.blit(carre.copy(), (self.entree.x * tile_width + self.offset.x, self.entree.y * tile_height + self.offset.y))
                        screen.blit(carre.copy(), (self.sortie.x * tile_width + self.offset.x, self.sortie.y * tile_height + self.offset.y))

            # Dessiner les murs depuis le dictionnaire
            for (x, y), texture in self.walls.items():
                if start_x <= x < end_x and start_y <= y < end_y:
                    pos = (x * tile_width + self.offset.x, y * tile_height + self.offset.y)
                    screen.blit(texture, pos)
                    

                    if DEBUG:
                        # cadriage rouge pour les rect des murs
                        pygame.draw.rect(screen, (255, 0, 0), (pos, (tile_width, tile_height)), 1)

            drawn = []
            # Dessiner les portes
            for porte in portes:
                if (porte.x, porte.y) not in drawn:
                    porte.draw(screen, self.offset)
                    drawn+= [(porte.x, porte.y), (porte.x + 1, porte.y), (porte.x, porte.y + 1), (porte.x + 1, porte.y + 1)]

                if DEBUG:
                    # relier porte / joueur en bleu
                    pygame.draw.line(screen, (0, 255, 255), porte.rect.topleft, (screen.get_width()//2, screen.get_height()//2))

    def detect_collision(self, wall_rect: pygame.Rect, other_rect: pygame.Rect) -> bool:
        """
        Vérifie s'il y a une collision entre deux rectangles.

        Args:
            wall_rect (pygame.Rect): Le rectangle représentant le mur.
            other_rect (pygame.Rect): L'autre rectangle à vérifier.

        Returns:
            bool: True s'il y a une collision, False sinon.
        """
        return wall_rect.colliderect(other_rect)

    def resolve_collision(self, player_rect, wall_rect, velocity) -> Vector:
        """
        Résout une collision entre le joueur et un mur en ajustant la position et la vitesse du joueur.

        Args:
            player_rect (pygame.Rect): Le rectangle représentant la position et la taille du joueur.
            wall_rect (pygame.Rect): Le rectangle représentant la position et la taille du mur.
            velocity (pygame.Vector2): Le vecteur de vitesse actuel du joueur.

        Returns:
            Vector: Le vecteur de vitesse ajusté du joueur.
        """
        if self.detect_collision(player_rect, wall_rect):
            # Collision sur l'axe x
            if abs(wall_rect.centerx - player_rect.centerx) < 24 and abs(wall_rect.centery - player_rect.centery) < 24:
                # Si le joueur va à gauche
                if velocity.x < 0:
                    player_rect.left = wall_rect.right
                    velocity.x = 0

                # Si le joueur va à droite
                elif velocity.x > 0:
                    player_rect.right = wall_rect.left
                    velocity.x = 0

            # Collision sur l'axe y
            if abs(wall_rect.centery - player_rect.centery) < 32 and abs(wall_rect.centerx - player_rect.centerx) < 32:
                # Si le joueur va en haut
                if velocity.y < 0:
                    player_rect.top = wall_rect.bottom
                    velocity.y = 0

                # Si le joueur va en bas
                elif velocity.y > 0:
                    player_rect.bottom = wall_rect.top
                    velocity.y = 0

        return velocity

    def correct_movement(self, other, velocity: Vector) -> Vector:
            """
            Corrige le mouvement de l'objet 'other' en fonction de la collision avec les murs du tilemap.
            
            Args:
                other (object): L'objet avec lequel la collision doit être vérifiée.
                velocity (Vector): Le vecteur de vitesse de l'objet 'other'.
            
            Returns:
                Vector: Le vecteur de vitesse corrigé après la résolution de la collision avec les murs.
            """
            
            future_rect = other.hitbox.copy()
            future_rect.center = (Vector(*other.rect.center) + velocity).coords 

            for (x, y), wall in self.walls.items():
            
                wall_rect = wall.get_rect()
                wall_rect.topleft = (x * self.tile_size[0] + self.offset.x, y * self.tile_size[1] + self.offset.y)
                velocity = self.resolve_collision(future_rect, wall_rect, velocity)

            return velocity
    
    def verifier_portes(self, joueur, portes: list[Porte]) -> None:
        """
        Vérifie les portes et effectue les actions appropriées en fonction de la distance entre le joueur et les portes.

        Args:
            joueur (Joueur): L'objet représentant le joueur.
            portes (list[Porte]): La liste des portes à vérifier.

        Returns:
            None
        """
        # Vérifier les portes
        for i, porte in enumerate(portes):
            distance = (Vector(*porte.rect.center) - Vector(*joueur.rect.center)).distance()
            if distance < 100:
                # savoir si le joueur a une clé
                for j, objet in enumerate(joueur.inventaire):
                    if objet.nom == "Clé" and objet.quantite > 0:
                        # suppression de la clé
                        objet.quantite -= 1
                        if objet.quantite == 0:
                            joueur.inventaire.pop(j)

                        # son d'ouverte de porte
                        pygame.mixer.Sound("ressources/audio/" + SOUNDS["porte"]).play()

                        # suppression de la porte et des portes adjacentes
                        portes_a_supprimer = [i]
                        for k, porte_adjacente in enumerate(portes):
                            if porte_adjacente.x == porte.x and porte_adjacente.y == porte.y + 1:
                                portes_a_supprimer.append(k)
                            elif porte_adjacente.x == porte.x +1 and porte_adjacente.y == porte.y + 1:
                                portes_a_supprimer.append(k)
                            elif porte_adjacente.x == porte.x + 1 and porte_adjacente.y == porte.y:
                                portes_a_supprimer.append(k)
                            

                        while len(portes_a_supprimer) > 0:
                            portes.pop(portes_a_supprimer.pop(0))

                            portes_a_supprimer = [i - 1 for i in portes_a_supprimer]


                        # suppression des murs
                        self.walls.pop((porte.x, porte.y))
                        self.walls.pop((porte.x + 1, porte.y))
                        self.walls.pop((porte.x, porte.y + 1))
                        self.walls.pop((porte.x + 1, porte.y + 1))

                        # mise à jour de la matrice
                        self.matrice[porte.y][porte.x] = 1
                        self.matrice[porte.y][porte.x + 1] = 1
                        self.matrice[porte.y + 1][porte.x] = 1
                        self.matrice[porte.y + 1][porte.x + 1] = 1
                        break

