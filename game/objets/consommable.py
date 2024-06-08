from __future__ import annotations

from typing import List, Tuple, Callable, Any, Optional, TYPE_CHECKING
import datetime
import pygame

from .objet import Objet

if TYPE_CHECKING:
    from ..entites.joueur import Joueur

class Consommable(Objet):
    """Une classe représentant un objet consommable du jeu
    Un consommable peut être consommé, il est alors retiré de l'inventaire du joueur et des effets
    sont appliqués au joueur
    """

    __slots__ = ("effets", "en_attente", "temps_attente")

    def __init__(
            self, nom:str, description:str, quantite:int, quantite_max:int,
            effets: List[Tuple[Callable, List[Any]]] = [], temps_attente:int = 0) -> None:
        super().__init__(nom, description, quantite, quantite_max)
        
        # Un effet est une fonction, lié à des paramètres
        # Les paramètres peuvent être de tous types
        # La fonction est appelée avec les paramètres donnés dans la fonction <Consommable.utiliser>
        self.effets = effets

        self.en_attente: Optional[datetime.datetime] = None # Si un objet a été utilisé, temps avant de pouvoir l'utiliser à nouveau, en ms
        self.temps_attente = temps_attente # Temps d'attente avant de pouvoir réutiliser l'objet, définit pour chaque consommable, en ms
       

    def utiliser(self, joueur:Joueur) -> bool:
        """Utilise l'objet consommable sur le joueur

        Args:
            joueur (Joueur): Le joueur sur lequel utiliser l'objet
        
        Retourne:
            bool: True si l'objet a été utilisé avec succès, False sinon (si en attente par exemple)
        """
        #Si l'objet est en attente, on ne peut pas l'utiliser
        if self.en_attente is not None and datetime.datetime.now() < self.en_attente:
            return False

        #Appliquer tous les effets de l'objet
        for effet, args in self.effets:
            getattr(joueur, effet)(*args) # On appelle la méthode de joueur correspondant à l'effet

        #Retirer l'objet de l'inventaire si c'est le dernier
        self.quantite -= 1
        if self.quantite == 0:
            joueur.inventaire.remove(self)
        
        #Appliquer le temps d'attente
        if self.temps_attente is not None:
            # On définit le moment où on pourra ré-utiliser l'objet
            self.en_attente = datetime.datetime.now() + datetime.timedelta(milliseconds=self.temps_attente)
        
        return True

    def from_json(data_json: dict) -> Consommable:
        return Consommable(
            nom = data_json["nom"],
            description = data_json["description"],
            quantite = data_json["quantite"],
            quantite_max = data_json["quantite_max"],
            effets = data_json["effets"],
            temps_attente = data_json["temps_attente"]
        )
    
    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "effets": self.effets,
            "temps_attente": self.temps_attente
        }
        
class Pomme(Consommable):
    """Une classe représentant une pomme, un objet consommable du jeu qui redonne de la vie au joueur"""

    def __init__(self, quantite:int=1) -> None:
        super().__init__(
            nom="Pomme",
            description = "Redonne 5 points de vie quand consommé. Le joueur ne peut en manger que toutes les 10 secondes. Limitée à 15 par inventaire.",
            quantite = quantite,
            quantite_max = 15,
            effets = [("ajouter_vie", [5])],
            temps_attente = 10000
            )
        
    def from_json(data_json: dict) -> Pomme:
        return Pomme(quantite=data_json["quantite"])


class Coeur(Consommable):
    """Un coeur qui permet d'augmenter la vie maximale du joueur"""
    def __init__(self, quantite:int=1, *args, **kwargs) -> None:
        super().__init__(
            nom="Coeur",
            description = "Rajouter 20 PV à la vie max du joueur, et régénère 20 PV. Limité à 15 par inventaire.",
            quantite = quantite,
            quantite_max = 15,
            effets = [("augmenter_vie_max", [20]), ("ajouter_vie", [20])],
            temps_attente = 5000
            )
        self.sheet = pygame.image.load("ressources/objects/heart.png")
        self.image = pygame.transform.scale(self.sheet, (32, 32))
        self.rect = self.image.get_rect()
    
    def from_json(data_json: dict) -> Coeur:
        return Coeur(quantite=data_json["quantite"])
    
    def to_json(self) -> dict:
        return super().to_json()
    
    

class Potion(Consommable):
    """Une potion qui permet de soigner le joueur"""
    def __init__(self, quantite:int=1, *args, **kwargs) -> None:
        super().__init__(
            nom="Potion",
            description = "Redonne 50 points de vie quand consommé. Le joueur ne peut en utiliser que toutes les 3 secondes. Limitée à 15 par inventaire.",
            quantite = quantite,
            quantite_max = 15,
            effets = [("ajouter_vie", [50])],
            temps_attente = 5000
            )

        self.sheet = pygame.image.load("ressources/objects/potion.png")
        self.image = pygame.transform.scale(self.sheet, (32, 32))

        self.rect = self.image.get_rect()
    
    def from_json(data_json: dict) -> Potion:
        return Potion(quantite=data_json["quantite"])

    def to_json(self) -> dict:
        return super().to_json()


class Botte(Consommable):
    """Une potion qui permet de soigner le joueur"""
    def __init__(self, quantite:int=1, *args, **kwargs) -> None:
        super().__init__(
            nom="Botte",
            description = "Ajoute 25 points de vitesse au joueur. Limitée à 15 par inventaire.",
            quantite = quantite,
            quantite_max = 15,
            effets = [("ajouter_vitesse", [25])],
            temps_attente = 5000 # 5 secondes
            )

        self.sheet = pygame.image.load("ressources/objects/botte.png")
        self.image = pygame.transform.scale(self.sheet, (32, 32))
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
    
    def from_json(data_json: dict) -> Potion:
        return Botte(quantite=data_json["quantite"])

    def to_json(self) -> dict:
        return super().to_json()
