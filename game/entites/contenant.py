from __future__ import annotations

from typing import List, TYPE_CHECKING
import importlib

if TYPE_CHECKING:
    from ..objets import Objet

class Contenant:
    """Une classe représentant une entité avec un inventaire. Doit être héritée par une classe Entite."""

    #__slots__ = ("inventaire")
    # Nous sommes obligés de ne pas utiliser __slots__ car sinon cela crée un conflit de type
    # 'multiple bases have instance lay-out conflict' avec la classe Entite dans la classe Coffre et Joueur

    def __init__(self, inventaire: List[Objet] = []) -> None:
            """
            Initialise un objet Contenant avec un inventaire donné.

            Args:
                inventaire (List[Objet], optional): La liste des objets contenus dans le contenant. Par défaut, l'inventaire est vide.
            """
            
            self.inventaire = inventaire
    
    def from_json(data_json: dict) -> Contenant:
        """
        Crée un objet Contenant à partir des données JSON.

        Args:
            data_json (dict): Les données JSON contenant les informations de l'objet Contenant.

        Returns:
            Contenant: L'objet Contenant créé à partir des données JSON.
        """
        module_objets = importlib.import_module("game.objets") # Importe le module objets
        # Pour chaque entité, on importe la classe correspondante et on crée l'objet
        objets=[getattr(module_objets, classe).from_json(objet) for classe, objet in data_json["inventaire"]]

        return Contenant(inventaire=objets)

    def to_json(self) -> dict:
            """
            Convertit l'objet en un dictionnaire JSON.

            Returns:
                dict: Le dictionnaire JSON représentant l'objet.
            """
            return {
                "inventaire": [(objet.__class__.__name__, objet.to_json()) for objet in self.inventaire]
            }
    
