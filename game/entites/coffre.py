from __future__ import annotations
from .entite import Entite
from .contenant import Contenant
from engine.utils import Vector

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..objets import Objet



class Coffre(Entite, Contenant):
    """Un coffre, une entité du jeu qui contient des objets"""

    __slots__ = ("inventaire","est_ouvert")

    def __init__(self, position: Vector) -> None:
        Entite.__init__(
            self,
            nom="Coffre",
            vie=-1, # Un coffre ne peut pas être détruit,
            vie_max=-1,
            position=position,
            vitesse=0
        )
        Contenant.__init__(self)
        self.est_ouvert = False
    
    def ouvrir(self) -> List[Objet]:
        """Ouvre le coffre et fait tomber son contenu autour
        
        Retourne:
            List[Objet]: La liste des objets contenus dans le coffre
            """
        self.est_ouvert = True
        #TODO faire tomber le contenu du coffre
        return self.inventaire

    def from_json(data_json: dict) -> Entite:
        coffre = Coffre(Vector.from_json(data_json["position"]))
        coffre.est_ouvert = data_json["est_ouvert"]
        contenant = Contenant.from_json(data_json)
        coffre.inventaire = contenant.inventaire
        return coffre

    def to_json(self) -> dict:
        entite_json = Entite.to_json(self)
        contenant_json = Contenant.to_json(self)
        return {**entite_json, **contenant_json, "est_ouvert": self.est_ouvert}