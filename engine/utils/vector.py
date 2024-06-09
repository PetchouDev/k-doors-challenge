from __future__ import annotations
from typing import Any
import math

# coordonnées de référence
alpha_ref = "xyzt"

class Vector():
    """Classe représentant un vecteur de dimension n."""

    def __init__(self, *coords) -> None:
            """
            Initialise un nouvel objet Vector avec les coordonnées spécifiées.

            Args:
                *coords: Les coordonnées du vecteur.

            Returns:
                None
            """
            self.coords = list(coords)

    def __str__(self) -> str:
            """
            Renvoie une représentation sous forme de chaîne de caractères du vecteur.
            
            Retourne une chaîne de caractères contenant le mot "Vector" suivi des coordonnées du vecteur.
            
            Returns:
                str: La représentation sous forme de chaîne de caractères du vecteur.
            """
            return f"Vector{tuple(self.coords)}"

    def __add__(self, other) -> Vector:
            """
            Retourne la somme de deux vecteurs.

            Args:
                other (Vector): Le vecteur à ajouter.

            Returns:
                Vector: Le vecteur résultant de l'addition.
            """
            return Vector(*[a + b for a, b in zip(self.coords, other.coords)])
    
    def __sub__(self, other) -> Vector:
            """
            Soustrait deux vecteurs et retourne le résultat sous forme d'un nouveau vecteur.

            Args:
                other (Vector): Le vecteur à soustraire.

            Returns:
                Vector: Le résultat de la soustraction des deux vecteurs.
            """
            return Vector(*[a - b for a, b in zip(self.coords, other.coords)])
    
    def __mul__(self, other) -> Vector:
            """
            Multiplie le vecteur actuel par un autre vecteur ou un scalaire.

            Si le paramètre `other` est un vecteur, la méthode retourne le produit vectoriel des deux vecteurs.
            Sinon, la méthode retourne un nouveau vecteur obtenu en multipliant chaque coordonnée du vecteur actuel par `other`.

            Args:
                other (Vector or float): Le vecteur ou le scalaire avec lequel multiplier le vecteur actuel.

            Returns:
                Vector: Le résultat de la multiplication.

            Raises:
                None

            Examples:
                >>> v1 = Vector(1, 2, 3)
                >>> v2 = Vector(4, 5, 6)
                >>> v3 = v1 * v2
                >>> print(v3)
                Vector(4, 10, 18)

                >>> v4 = v1 * 2
                >>> print(v4)
                Vector(2, 4, 6)
            """
            if isinstance(other, Vector):
                return self.vector_product(other)
            else:
                return Vector(*[a * other for a in self.coords])
        
    def __rmul__(self, other) -> Vector:
            """
            Multiplie le vecteur par un scalaire.

            Args:
                other: Le scalaire avec lequel multiplier le vecteur.

            Returns:
                Un nouveau vecteur résultant de la multiplication par le scalaire.
            """
            return Vector(*[a * other for a in self.coords])
    
    def __truediv__(self, other) -> Vector:
            """
            Effectue la division de chaque coordonnée du vecteur par un autre nombre.
            
            Args:
                other (float): Le nombre par lequel diviser chaque coordonnée du vecteur.
            
            Returns:
                Vector: Un nouveau vecteur résultant de la division de chaque coordonnée par le nombre spécifié.
            """
            return Vector(*[a / other for a in self.coords])
    
    def __floordiv__(self, other) -> Vector:
        """
        Effectue la division entière de chaque coordonnée du vecteur par un autre nombre.
        
        Args:
            other (float): Le nombre par lequel diviser chaque coordonnée du vecteur.
        
        Returns:
            Vector: Un nouveau vecteur résultant de la division entière de chaque coordonnée par le nombre spécifié.
        """
        return Vector(*[a // other for a in self.coords])
    
    def __iter__(self) -> list:
        """
        Retourne un itérateur sur les coordonnées du vecteur.
        
        :return: Un itérateur sur les coordonnées du vecteur.
        :rtype: list
        """
        return iter(self.coords)
    
    def __neg__(self) -> Vector:
        """
        Retourne le vecteur opposé à celui-ci.
        
        :return: Le vecteur opposé.
        :rtype: Vector
        """
        return Vector(*[-a for a in self.coords])
    
    def new_axis(self, coord:float) -> None:
            """
            Ajoute une nouvelle coordonnée à l'axe du vecteur.

            Args:
                coord (float): La coordonnée à ajouter.

            Returns:
                None
            """
            self.coords.append(coord)

    def get_axis(self, axis:int) -> float:
            """
            Renvoie la valeur de la coordonnée sur l'axe spécifié.

            Args:
                axis (int): L'indice de l'axe.

            Returns:
                float: La valeur de la coordonnée sur l'axe spécifié.
            """
            if axis < len(self.coords):
                return self.coords[axis]    
            return 0
    
    def angle(self) -> float:
            """
            Calcule l'angle (en degrés) du vecteur par rapport à l'axe x positif.
            L'angle est toujours compris entre 0 et 360 degrés.
            
            Returns:
                float: L'angle du vecteur en degrés.
            """
            return (180 * math.atan2(self.y, self.x) / math.pi) % 360
    
    def __getattribute__(self, name: str) -> Any:
            """
            Renvoie la valeur de l'attribut spécifié par `name` s'il existe dans `alpha_ref`.
            Sinon, renvoie la valeur de l'attribut en utilisant la méthode de la classe parente.
            
            Args:
                name (str): Le nom de l'attribut à récupérer.
            
            Returns:
                Any: La valeur de l'attribut spécifié par `name` s'il existe dans `alpha_ref`.
                     Sinon, la valeur de l'attribut en utilisant la méthode de la classe parente.
            """
            if name in alpha_ref:
                return self.get_axis(alpha_ref.index(name))
            return super().__getattribute__(name)
    
    def __len__(self) -> int:
        """
        Renvoie la longueur du vecteur.

        :return: La longueur du vecteur.
        :rtype: int
        """
        return len(self.coords)
    
    def distance(self) -> float:
        """
        Calculates the Euclidean distance of the vector from the origin.
        
        Returns:
            float: The Euclidean distance of the vector.
        """
        return sum([c ** 2 for c in self.coords]) ** 0.5
    
    def distance_between(self, other) -> float:
            """
            Calcule la distance entre ce vecteur et un autre vecteur donné.

            Args:
                other: L'autre vecteur avec lequel calculer la distance.

            Returns:
                La distance entre les deux vecteurs.

            """
            return (self - other).distance()
    
    def scalar_product(self, other) -> float:
        """
        Calcule le produit scalaire entre ce vecteur et un autre vecteur.

        Args:
            other (Vector): L'autre vecteur avec lequel calculer le produit scalaire.

        Returns:
            float: Le résultat du produit scalaire.
        """
        return sum([a * b for a, b in zip(self.coords, other.coords)])
    
    def vector_product(self, other):
        """
        Calcule le produit vectoriel entre ce vecteur et un autre vecteur.

        Args:
            other (Vector): L'autre vecteur avec lequel effectuer le produit vectoriel.

        Returns:
            Vector: Le résultat du produit vectoriel sous forme d'un nouveau vecteur.
        """
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def unit_vector(self) -> Vector:
            """
            Calcule et renvoie le vecteur unitaire de ce vecteur.
            
            Returns:
                Vector: Le vecteur unitaire.
            """
            dist = self.distance()
            if dist == 0:
                return Vector(*[0 for _ in self.coords])
            return self / dist
    
    def normalize(self) -> Vector:
        """
        Normalise le vecteur en le divisant par sa norme.
        
        Retourne le vecteur normalisé.
        """
        self.coords = self.unit_vector().coords
        return self
    
    def __setattribute__(self, name: str, value: Any) -> None:
            """
            Modifie la valeur d'une coordonnée du vecteur.

            Args:
                name (str): Le nom de la coordonnée à modifier.
                value (Any): La nouvelle valeur de la coordonnée.

            Returns:
                None
            """
            if isinstance(name, int):
                self.coords[name] = value

    @property
    def x(self) -> float:
            """
            Renvoie la valeur de la coordonnée x du vecteur.
            
            Returns:
                float: La valeur de la coordonnée x du vecteur.
            """
            return self.get_axis(0)
    
    @x.setter
    def x(self, value) -> None:
        """
        Modifie la coordonnée x du vecteur.

        Args:
            value (float): La nouvelle valeur de la coordonnée x.

        Returns:
            None
        """
        self.coords[0] = value

    @property
    def y(self) -> float:
        """
        Renvoie la valeur de la coordonnée y du vecteur.
        
        Returns:
            float: La valeur de la coordonnée y du vecteur.
        """
        return self.get_axis(1)
    
    @y.setter
    def y(self, value) -> None:
        """
        Modifie la coordonnée y du vecteur.

        Args:
            value (float): La nouvelle valeur de la coordonnée y.
        
        Returns:
            None
        """
        self.coords[1] = value

    @property
    def z(self) -> float:
        """
        Renvoie la valeur de la coordonnée z du vecteur.
        
        Returns:
            float: La valeur de la coordonnée z du vecteur.
        """
        return self.get_axis(2)
    
    @z.setter
    def z(self, value) -> None:
        """
        Modifie la coordonnée z du vecteur.

        Args:
            value (float): La nouvelle valeur de la coordonnée z.

        Returns:
            None
        """
        self.coords[2] = value
    
    def from_json(data_json: dict) -> Vector:
        """
        Crée un objet Vector à partir d'un dictionnaire JSON.

        Args:
            data_json (dict): Le dictionnaire JSON contenant les données du vecteur.

        Returns:
            Vector: L'objet Vector créé à partir des données JSON.
        """
        return Vector(*[data_json["x"], data_json["y"]])
    
    def to_json(self) -> dict:
            """
            Convertit le vecteur en un dictionnaire JSON.

            Retourne:
                dict: Un dictionnaire contenant les coordonnées x et y du vecteur.
            """
            return {
                "x": self.x,
                "y": self.y
            }
    
    def copy(self) -> Vector:
        """
        Renvoie une copie du vecteur actuel.

        Returns:
            Vector: Une copie du vecteur actuel.
        """
        return Vector(*self.coords)
