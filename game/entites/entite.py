# Librairies de la bibliothèque standard
from __future__ import annotations # Permet d'utiliser le nom de la classe dans la définition de la classe
from typing import Optional, TYPE_CHECKING
from time import time

# Librairies de la bibliothèque tierce
import pygame
pygame.mixer.init() 

# Librairies locales
from engine.utils import Vector
import datetime
from ..utils import get_image
from ..constantes import FRAME_RATE, PLAYER_SPEED, DISTANCE_AGRO_MONSTRES, DUREE_ROUGE_ENTITE_APRES_ATTAQUE, SOUNDS


if TYPE_CHECKING:
    from .joueur import Joueur
    from engine.ui.tilemap import Tilemap
else:
    Joueur = None


class Entite(pygame.sprite.Sprite):
    """Représente une entité du jeu (joueur, monstre, coffre, etc.)"""

    #__slots__ = ("nom", "vie", "vie_max", "position", "image", "vitesse", "degats", "temps_attente")
    # Nous sommes obligés de ne pas utiliser __slots__ car sinon cela crée un conflit de type
    # 'multiple bases have instance lay-out conflict' avec la classe Contenant dans la classe Coffre et Joueur


    def __init__(self, nom:str, vie:int, vie_max:int, position:Vector, vitesse:float=1, degats:int=0, temps_attente:int=0, width:int=32, height:int=32) -> None:
        """
        Initialise une instance de la classe Entite.

        Args:
            nom (str): Le nom de l'entité.
            vie (int): Le nombre de points de vie de l'entité.
            vie_max (int): Le nombre maximum de points de vie de l'entité.
            position (Vector): La position de l'entité dans l'espace.
            vitesse (float, optional): La vitesse de déplacement de l'entité. Par défaut 1.
            degats (int, optional): Les dégâts infligés par l'entité. Par défaut 0.
            temps_attente (int, optional): Le temps d'attente avant de pouvoir attaquer, en millisecondes. Par défaut 0.
            width (int, optional): La largeur de l'entité. Par défaut 32.
            height (int, optional): La hauteur de l'entité. Par défaut 32.
        """
        
        self.nom = nom
        self.vie = vie
        self.vie_max = vie_max
        self.position = position
        self.vitesse = vitesse
        self.degats = degats
        self.temps_attente = temps_attente
        self.en_attente: Optional[datetime.datetime] = None
        self.rouge_jusqua = None

        super().__init__()

        self.orientation = "S"
        self.width = 32
        self.height = 32

        self.orientation = "S"
        self.frame = 0
        self.clock = 0
        self.last_frame = time()
        self.flottement = Vector(0, 0)
        self.ombre = pygame.Surface((32, 12))
        pygame.draw.ellipse(self.ombre, (64, 64, 64, 64), (0, 0, 32, 12))
        self.ombre.set_colorkey((0, 0, 0))
        self.ombre_rect = self.ombre.get_rect()

    def est_attaquable(self, attaquant: Entite) -> bool:
        """Indique si l'entité est attaquable

        Une entité est attaquable si elle a une vie maximale définie et si elle n'est pas l'attaquant lui-même.
        Ou si elle est en attente d'attaque.
        
        Retourne:
            bool: True si l'entité est attaquable, False sinon
        """
        if self.vie_max == -1 or self==attaquant:
            return False
        elif attaquant.en_attente is not None and datetime.datetime.now() < attaquant.en_attente:
            return False
        return True
    
    def attaquer(self, entite_attaquee: Entite, degats:int) -> bool:
        """Attaque l'entité et lui inflige des dégâts.
        
        Args:
            degats (int): Les dégâts à infliger
        
        Retourne:
            bool: True si l'attaque a lieu, sinon False
        """
        if not entite_attaquee.est_attaquable(self):
            return False # L'entité ne peut pas être détruite, donc il n'y a pas d'attaque
    
        # Gérer le cas plus complexe où le joueur reçoit des dégats
        from .joueur import Joueur

        pygame.mixer.Sound("ressources/audio/" + SOUNDS["coup"]).play()

        if isinstance(entite_attaquee, Joueur):
            entite_attaquee.retirer_vie(degats)

            if self.temps_attente is not None:
                self.en_attente = datetime.datetime.now() + datetime.timedelta(milliseconds=self.temps_attente)
        
        else:
            entite_attaquee.vie -= degats # On inflige les dégâts

            # L'entité meurt
            if entite_attaquee.vie < 0:
                entite_attaquee.vie = 0
            
            # On définit le moment où le joueur pourra attaquer à nouveau
            arme = self.get_selected_item()
            if arme.temps_attente:
                self.en_attente = datetime.datetime.now() + datetime.timedelta(milliseconds=arme.temps_attente)
        
        entite_attaquee.rouge_jusqua = datetime.datetime.now() + datetime.timedelta(milliseconds=DUREE_ROUGE_ENTITE_APRES_ATTAQUE) # On rend l'entité rouge pendant 500ms

        # L'attaque a eu lieu
        return True 
    
    @property
    def occupe(self) -> bool:
            """
            Vérifie si l'entité est occupée.

            Returns:
                bool: True si l'entité est occupée, False sinon.
            """
            return True if self.en_attente is not None and datetime.datetime.now() < self.en_attente else False

    @property
    def real_pos(self) -> Vector:
        """
        Renvoie la position réelle de l'entité.

        :return: Un objet Vector représentant la position réelle de l'entité.
        """
        return Vector(*self.rect.center)
    
    def from_json(data_json: dict) -> Entite:
        """
        Crée une instance de la classe Entite à partir d'un dictionnaire JSON.

        Args:
            data_json (dict): Le dictionnaire JSON contenant les données de l'entité.

        Returns:
            Entite: Une instance de la classe Entite créée à partir des données JSON.
        """
        return Entite(
            nom=data_json["nom"],
            vie=data_json["vie"],
            vie_max=data_json["vie_max"],
            position=Vector.from_json(data_json["position"]),
            vitesse=data_json["vitesse"],
            degats=data_json["degats"],
            temps_attente=data_json["temps_attente"],
            width=data_json["width"],
            height=data_json["height"]
        )

    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Returns:
            dict: Le dictionnaire JSON représentant l'objet.
        """
        return {
            "nom": self.nom,
            "vie": self.vie,
            "vie_max": self.vie_max,
            "position": self.position.to_json(),
            "vitesse": self.vitesse,
            "degats": self.degats,
            "temps_attente": self.temps_attente,
            "width": self.width,
            "height": self.height
        }
    
    def get_image(self, row, col) -> pygame.Surface:
        """
        Renvoie l'image correspondante à la position spécifiée.

        Args:
            row (int): Le numéro de ligne de l'image.
            col (int): Le numéro de colonne de l'image.

        Returns:
            pygame.Surface: L'image correspondante à la position spécifiée.
        """
        return get_image(self, row, col)
    
    def get_frame(self, velocity: Vector) -> pygame.Surface:
        """
        Renvoie la surface d'image correspondante à l'entité en fonction de sa vitesse et de sa direction.

        Args:
            velocity (Vector): Le vecteur de vitesse de l'entité.

        Returns:
            pygame.Surface: La surface d'image correspondante à l'entité.

        """
        # mise à jour de l'horloge
        self.clock += PLAYER_SPEED * self.vitesse / (FRAME_RATE * 50)
        if self.vitesse <= 0:
            return self.image
        elif velocity.x == 0 and velocity.y == 0:
            return self.images[self.orientation][2] # ne pas changer de direction, mais attendre
        else:
            # vérifier la direction
            self.orientation = self.get_orientation(velocity)

            # changer de frame si l'interval de temps est écoulé
            if self.clock > 0.4:
                self.frame = (self.frame + 1) % 2
                self.clock = 0

            # retourner l'image correspondante
            return self.images[self.orientation][self.frame]

    def get_orientation(self, velocity: Vector) -> str:
        """
        Renvoie l'orientation de l'entité en fonction de sa vélocité.

        Args:
            velocity (Vector): La vélocité de l'entité.

        Returns:
            str: L'orientation de l'entité. Les valeurs possibles sont :
                - "N" pour le nord
                - "S" pour le sud
                - "E" pour l'est
                - "O" pour l'ouest
                - Une combinaison de ces valeurs pour les orientations diagonales.
        """
        if velocity.x == 0 and velocity.y == 0:
            return self.orientation
        else:
            orientation = ""
            if velocity.y < 0:
                orientation += "N"
            elif velocity.y > 0:
                orientation += "S"
            
            if velocity.x > 0:
                orientation += "E"
            elif velocity.x < 0:
                orientation += "O"

            return orientation

    def draw(self, screen: pygame.display, player_pos: Vector, map: Tilemap) -> None:
            """
            Dessine l'entité à l'écran.

            Args:
                screen (pygame.display): L'écran sur lequel l'entité doit être dessinée.
                player_pos (Vector): La position du joueur.
                map (Tilemap): La carte sur laquelle l'entité se trouve.

            Returns:
                None
            """
            
            # position par rapport au joueur
            distance = self.real_pos - player_pos

        
            if self.vitesse > 0:
                if distance.distance() <= DISTANCE_AGRO_MONSTRES:
                    angle = distance.angle()

                    # en déduire l'orientation de l'entité en fonction de l'angle
                    if 45 <= angle < 135:
                        self.orientation = "N"
                    elif 135 <= angle < 225:
                        self.orientation = "E"
                    elif 225 <= angle < 315:
                        self.orientation = "S"
                    else:
                        self.orientation = "O"

            

            image = self.get_frame(distance)        

            # calculer la position de l'entité à l'écran
            render_pos = self.position + map.offset

            # placer l'entité à l'écran
            self.rect.topleft = (render_pos + self.flottement).coords

            # dessiner une ellipse pour l'ombre (x=32, y=16) centrée sur le milieu du bas de l'entité
            self.ombre_rect.midbottom = (Vector(*self.rect.midbottom) - self.flottement).coords


            if self.vitesse > 0 and self.rouge_jusqua is not None and datetime.datetime.now() < self.rouge_jusqua:
                #dessin de l'entité en rouge
                image.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(image, self.rect.topleft)
            else:
                # dessin du l'entité
                screen.blit(image, self.rect.topleft)
        
            return self.rect.topleft

