# Libraries de la bibliothèque standard
from __future__ import annotations
from typing import List, Tuple, Callable, Any, Optional, TYPE_CHECKING
import datetime

# Bibliothèques tierces
import pygame

# Bibliothèques de l'application
from .objet import Objet


if TYPE_CHECKING:
    from ..entites.joueur import Joueur


class Consommable(Objet):
    """
    Une classe représentant un objet consommable du jeu
    Un consommable peut être consommé, il est alors retiré de l'inventaire du joueur et des effets
    sont appliqués au joueur
    """

    __slots__ = ("effets", "en_attente", "temps_attente")

    def __init__(
            self, nom:str, description:str, quantite:int, quantite_max:int,
            effets: List[Tuple[Callable, List[Any]]] = [], temps_attente:int = 0) -> None:
        """
        Initialise un objet Consommable avec les paramètres spécifiés.

        Args:
            nom (str): Le nom du consommable.
            description (str): La description du consommable.
            quantite (int): La quantité actuelle du consommable.
            quantite_max (int): La quantité maximale du consommable.
            effets (List[Tuple[Callable, List[Any]]], optional): Les effets du consommable. Chaque effet est une fonction liée à des paramètres. Les paramètres peuvent être de tous types. La fonction est appelée avec les paramètres donnés dans la fonction `Consommable.utiliser`. Defaults to [].
            temps_attente (int, optional): Le temps d'attente avant de pouvoir réutiliser l'objet, définit pour chaque consommable, en millisecondes. Defaults to 0.
        
        
        Returns:
            None
        """
        
        super().__init__(nom, description, quantite, quantite_max)
        
        self.effets = effets

        self.en_attente: Optional[datetime.datetime] = None
        self.temps_attente = temps_attente
       
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
        """
        Crée une instance de la classe Consommable à partir d'un dictionnaire JSON.

        Args:
            data_json (dict): Le dictionnaire JSON contenant les données du consommable.

        Returns:
            Consommable: L'instance de la classe Consommable créée à partir des données JSON.
        """
        return Consommable(
            nom = data_json["nom"],
            description = data_json["description"],
            quantite = data_json["quantite"],
            quantite_max = data_json["quantite_max"],
            effets = data_json["effets"],
            temps_attente = data_json["temps_attente"]
        )
    
    def to_json(self) -> dict:
        """
        Convertit l'objet Consommable en un dictionnaire JSON.

        Returns:
            dict: Le dictionnaire JSON représentant l'objet Consommable.
        """
        return {
            **super().to_json(),
            "effets": self.effets,
            "temps_attente": self.temps_attente
        }
        
class Pomme(Consommable):
    """Une classe représentant une pomme, un objet consommable du jeu qui redonne de la vie au joueur"""

    def __init__(self, quantite:int=1) -> None:
        """
        Initialise un objet consommable avec les paramètres spécifiés.

        Args:
            quantite (int, optional): La quantité d'objets consommables. Par défaut, 1.

        Returns:
            None
        """
        super().__init__(
            nom="Pomme",
            description = "Redonne 5 points de vie quand consommé. Le joueur ne peut en manger que toutes les 10 secondes. Limitée à 15 par inventaire.",
            quantite = quantite,
            quantite_max = 15,
            effets = [("ajouter_vie", [5])],
            temps_attente = 10000
        )
        
    def from_json(data_json: dict) -> Pomme:
        """
        Crée une instance de la classe Pomme à partir des données JSON.

        Args:
            data_json (dict): Les données JSON contenant les informations de la Pomme.

        Returns:
            Pomme: Une instance de la classe Pomme avec les informations extraites des données JSON.
        """
        return Pomme(quantite=data_json["quantite"])

class Coeur(Consommable):
    """Un coeur qui permet d'augmenter la vie maximale du joueur"""

    __slots__ = ("sheet", "image", "rect")

    def __init__(self, quantite:int=1, *args, **kwargs) -> None:
        """
        Initialise un objet consommable.

        Args:
            quantite (int, optional): La quantité d'objets consommables. Par défaut, 1.

        Returns:
            None
        """
        super().__init__(
            nom="Coeur",
            description="Rajouter 20 PV à la vie max du joueur, et régénère 20 PV. Limité à 15 par inventaire.",
            quantite=quantite,
            quantite_max=15,
            effets=[("augmenter_vie_max", [20]), ("ajouter_vie", [20])],
            temps_attente=5000
        )
        self.sheet = pygame.image.load("ressources/objects/heart.png")
        self.image = pygame.transform.scale(self.sheet, (32, 32))
        self.rect = self.image.get_rect()
    
    def from_json(data_json: dict) -> Coeur:
        """
        Crée une instance de la classe Coeur à partir des données JSON fournies.

        Args:
            data_json (dict): Les données JSON contenant les informations nécessaires pour créer l'objet Coeur.

        Returns:
            Coeur: L'instance de la classe Coeur créée à partir des données JSON.
        """
        return Coeur(quantite=data_json["quantite"])
    
    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Returns:
            dict: Le dictionnaire JSON représentant l'objet.
        """
        return super().to_json()
    
class Potion(Consommable):
    """Une potion qui permet de soigner le joueur"""

    __slots__ = ("sheet", "image", "rect")

    def __init__(self, quantite:int=1, *args, **kwargs) -> None:
        """
        Initialise un objet consommable.

        Args:
            quantite (int, optional): La quantité d'objets consommables. Par défaut, 1.

        Attributes:
            nom (str): Le nom de l'objet consommable.
            description (str): La description de l'objet consommable.
            quantite (int): La quantité d'objets consommables.
            quantite_max (int): La quantité maximale d'objets consommables pouvant être stockés.
            effets (list): La liste des effets de l'objet consommable.
            temps_attente (int): Le temps d'attente en millisecondes avant de pouvoir utiliser à nouveau l'objet consommable.
            sheet (pygame.Surface): La surface de l'image de l'objet consommable.
            image (pygame.Surface): L'image redimensionnée de l'objet consommable.
            rect (pygame.Rect): Le rectangle englobant l'image de l'objet consommable.

        Returns:
            None
        """
        
        super().__init__(
            nom="Potion",
            description="Redonne 50 points de vie quand consommé. Le joueur ne peut en utiliser que toutes les 3 secondes. Limitée à 15 par inventaire.",
            quantite=quantite,
            quantite_max=15,
            effets=[("ajouter_vie", [50])],
            temps_attente=5000
        )

        self.sheet = pygame.image.load("ressources/objects/potion.png")
        self.image = pygame.transform.scale(self.sheet, (32, 32))

        self.rect = self.image.get_rect()
    
    def from_json(data_json: dict) -> Potion:
        """
        Crée une instance de la classe Potion à partir des données JSON fournies.

        Args:
            data_json (dict): Un dictionnaire contenant les données JSON de la potion.

        Returns:
            Potion: Une instance de la classe Potion avec les attributs initialisés à partir des données JSON.
        """
        return Potion(quantite=data_json["quantite"])

    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Returns:
            dict: Le dictionnaire JSON représentant l'objet.
        """
        return super().to_json()

class Botte(Consommable):
    """Une potion qui permet de soigner le joueur"""

    __slots__ = ("sheet", "image", "rect")

    def __init__(self, quantite:int=1, *args, **kwargs) -> None:
        """
        Initialise un objet consommable.

        Args:
            quantite (int, optional): La quantité d'objets consommables. Par défaut 1.
        """
        
        super().__init__(
            nom="Botte",
            description="Ajoute 25 points de vitesse au joueur. Limitée à 15 par inventaire.",
            quantite=quantite,
            quantite_max=15,
            effets=[("ajouter_vitesse", [25])],
            temps_attente=5000  # 5 secondes
        )

        self.sheet = pygame.image.load("ressources/objects/botte.png")
        self.image = pygame.transform.scale(self.sheet, (32, 32))
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
    
    def from_json(data_json: dict) -> Potion:
        """
        Crée une instance de la classe Potion à partir des données JSON fournies.

        Args:
            data_json (dict): Les données JSON contenant les informations de la potion.

        Returns:
            Potion: Une instance de la classe Potion avec les informations fournies.

        """
        return Botte(quantite=data_json["quantite"])

    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Returns:
            dict: Le dictionnaire JSON représentant l'objet.
        """
        return super().to_json()
