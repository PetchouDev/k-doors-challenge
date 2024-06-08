from __future__ import annotations

from time import time
import tkinter as tk

from PIL import ImageTk
import PIL.Image
import pygame

from typing import Union, TYPE_CHECKING
from .entite import Entite
from .objet_sol import ObjetAuSol
from .contenant import Contenant
from engine.utils import Vector
from datetime import datetime

from game.objets import Prop

from ..constantes import NB_EMPLACEMENTS_INVENTAIRE, SOUNDS, PLAYER_SPEED, VITESSE_MAX_JOUEUR

if TYPE_CHECKING:
    from ..objets import Objet


class Joueur(Entite, Contenant):
    """Une classe représentant le joueur du jeu"""


    def __init__(self, nom:str, vie:int, position:Vector, rendered_position:Vector=Vector(0,0), vie_max:int = 100, buff_vitesse:int = None) -> None:
        Entite.__init__(
            self,
            nom=nom,
            vie=vie,
            vie_max=vie_max,
            position=position,
            vitesse=1,
            width=16,
            height=24
        )
        Contenant.__init__(self)

        self.attaque = False

        self.buff_vitesse = buff_vitesse if buff_vitesse else 0


        # Déclarer la feuille de texture du joueur
        self.sheet = pygame.image.load("ressources/players/player.png")
        self.image_sheet_size = (32, 48)

        # Charger l'image du joueur
        self.image = self.get_image(4, 9)

        # Créer un rect pour l'image du joueur
        self.rect = self.image.get_rect()

        # Position du joueur à l'écran
        self.rendered_position = rendered_position

        # Créer un rect pour l'image du joueur
        self.rect = self.image.get_rect()

        # Hitbox du joueur (32x32)
        self.hitbox = pygame.Rect(self.rect.topleft, (24, 32))
        self.hitbox.midbottom = (Vector(*self.rect.midbottom) + Vector(0, -8)).coords

        # definir une oriantation pour le joueur (par défault au sud)
        self.orientation = "S"

        # compter l'image d'animation
        self.frame = 0

        # compter le temps de chaque frame
        self.clock = 0

        # intervalle de temps avec la frame précédente
        self.last_frame = time()

        # répertorier les images {orientation: {frame: image}}
        self.images = { # TODO: Modifier pour l'épée
            "N": {
                0: self.get_image(0, 9),
                1: self.get_image(0, 11),
                2: self.get_image(0, 10),
            },
            "NE": {
                0: self.get_image(1, 9),
                1: self.get_image(1, 11),
                2: self.get_image(1, 10),
            },
            "E": {
                0: self.get_image(2, 9),
                1: self.get_image(2, 11),
                2: self.get_image(2, 10),
            },
            "SE": {
                0: self.get_image(3, 9),
                1: self.get_image(3, 11),
                2: self.get_image(3, 10),
            },
            "S": {
                0: self.get_image(4, 9),
                1: self.get_image(4, 11),
                2: self.get_image(4, 10),
            },
            "SO": {
                0: self.get_image(5, 9),
                1: self.get_image(5, 11),
                2: self.get_image(5, 10),
            },
            "O": {
                0: self.get_image(6, 9),
                1: self.get_image(6, 11),
                2: self.get_image(6, 10),
            },
            "NO": {
                0: self.get_image(7, 9),
                1: self.get_image(7, 11),
                2: self.get_image(7, 10),
            },
        }

        # récupérer l'objet sélectionné
        self.selected_item = self.get_selected_item()

        # créer une ombre elliptique pour le joueur
        
        self.ombre = pygame.Surface((32, 12))
        pygame.draw.ellipse(self.ombre, (64, 64, 64, 64), (0, 0, 32, 12))
        self.ombre.set_colorkey((0, 0, 0))
        self.ombre_rect = self.ombre.get_rect()


    

    

    def ajouter_vie(self, vie:int) -> int:
        """Ajoute de la vie au joueur
        
        Args:
            vie (int): La quantité de vie à ajouter
        
        Retourne:
            int: La vie actuelle du joueur
        
        """
        self.vie = min(self.vie + vie, self.vie_max)
        
        return self.vie
    
    def augmenter_vie_max(self, vie:int):
        self.vie_max += vie
    
    def retirer_vie(self, vie:int) -> int:
        """Retire de la vie au joueur
        
        Args:
            vie (int): La quantité de vie à retirer
        
        Retourne:
            int: La vie actuelle du joueur
        
        """
        self.vie -= vie

        if self.vie <= 0:
            # son de mort
            pygame.mixer.Sound("ressources/audio/" + SOUNDS["game_over"]).play()

            # mettre la vie à 0
            self.vie = 0

    def ajouter_vitesse(self, vitesse:int) -> int:
        """Ajoute de la vitesse au joueur
        
        Args:
            vitesse (int): La quantité de vitesse à ajouter
        
        Retourne:
            int: La vitesse actuelle du joueur
        
        """
        self.buff_vitesse = min(self.buff_vitesse + vitesse, VITESSE_MAX_JOUEUR - PLAYER_SPEED)
        
        return self.buff_vitesse
            

    def ajouter_inventaire(self, o_ajout:Objet) -> Union[Objet, bool]:
        """Ajoute un objet à l'inventaire du joueur.
        
        Args:
            o_ajout (Objet): L'objet à ajouter
        
        Retourne:
            Union[Objet, bool]: S'il y a assez de place dans l'inventaire, retourne True, sinon retourne l'objet restant
                                Exemple : Si j'ai 12 pommes (quantité max 15) et que j'en ajouté 6, il me restera 3 pommes
                                          Ces 3 pommes seront retournées
        
        """
        
        for objet_inv in self.inventaire:
            if o_ajout.nom == objet_inv.nom: # Si l'objet est déjà dans l'inventaire
                if o_ajout.nom == "Epee":
                    if o_ajout.degats > objet_inv.degats:
                        objet_inv.degats = o_ajout.degats
                        return True
                    else:
                        False

                elif (o_ajout.quantite + objet_inv.quantite) <= objet_inv.quantite_max: # Si on peut ajouter la quantité demandée
                    objet_inv.quantite += o_ajout.quantite
                    return True
                else:
                    # Calcul de la quantité restante dans l'objet qu'on ajoute, après ajout à l'inventaire
                    quantite_restante = o_ajout.quantite - (objet_inv.quantite_max - objet_inv.quantite)

                    # On ajoute la quantité possible à l'objet déjà présent
                    objet_inv.quantite = objet_inv.quantite_max

                    # On définit la quantité de l'objet ajouté, à celle restante. Il devient ainsi l'objet restant
                    o_ajout.quantite = quantite_restante

                    # On retourne l'objet restant
                    return False
        
        # Si l'objet n'est pas dans l'inventaire
                
        if len(self.inventaire) < NB_EMPLACEMENTS_INVENTAIRE: # Si l'inventaire n'est pas plein
            self.inventaire.append(o_ajout)
            return True
        
        return False # Si l'inventaire est plein, on retourne l'objet restant (qui est le même que l'objet ajouté)

    def from_json(data_json: dict) -> Joueur:
        joueur = Joueur(
            nom=data_json["nom"],
            vie=data_json["vie"],
            vie_max=data_json["vie_max"],
            position=Vector.from_json(data_json["position"]),
            buff_vitesse=data_json["buff_vitesse"]
        )
        contenant = Contenant.from_json(data_json)
        joueur.inventaire = contenant.inventaire
        return joueur
    
    def to_json(self) -> dict:
        entite_json = Entite.to_json(self)
        contenant_json = Contenant.to_json(self)
        return {**entite_json, **contenant_json, "buff_vitesse": self.buff_vitesse}

    def draw(self, rendered_movement: Vector, absolute_movement: Vector, screen: pygame.display) -> None:
        self.rendered_position += rendered_movement
        self.rect.topleft = self.rendered_position.coords
        self.hitbox.midbottom = (Vector(*self.rect.midbottom) + Vector(0, -8)).coords

        self.position += absolute_movement

        # dessiner l'ombre du joueur en premier
        self.ombre_rect.midbottom = self.rect.midbottom
        screen.blit(self.ombre, self.ombre_rect.topleft)

        # dessiner le joueur
        self.image = self.get_frame(absolute_movement)
        selected_item = self.get_selected_item()
        # si le joueur regarde vers le nord ou l'ouest, on dessine l'ojet sélectionné avant le joueur
        if selected_item and self.orientation in ["N", "O", "NO", "SO"]:
            selected_item.draw(screen, self)
        
        if self.rouge_jusqua is not None and datetime.now() < self.rouge_jusqua:
            #dessin de l'entité en rouge
            image = self.image.copy()
            image.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(image, self.rect.topleft)
        
        else:

            # dessin du joueur
            screen.blit(self.image, self.rect.topleft)
        
        # dessiner l'objet sélectionné après le joueur si le joueur regarde vers le sud ou l'est
        if selected_item and self.orientation in ["S", "E", "SE", "NE"]:
            selected_item.draw(screen, self)

    @property
    def rect_pos(self):
        return Vector(*self.rect.topleft)

    def get_selected_item(self) -> Objet:
        selected =  next((objet for objet in self.inventaire if objet.est_selectionne), None)
        if selected is None and len(self.inventaire) > 0:
            self.inventaire[0].est_selectionne = True
            selected = self.inventaire[0]
        return selected

    def select_item(self, index: int) -> None:
        self.selected_item = None
        for i, objet in enumerate(self.inventaire):
            objet.est_selectionne = False
            if i == index:
                objet.est_selectionne = True
                self.selected_item = objet

    def get_item_index(self, object: str|Objet) -> int:
        for i, obj in enumerate(self.inventaire):
            if isinstance(object, str):
                if obj.nom == object:
                    return i 
            else:
                if obj == object:
                    return i


