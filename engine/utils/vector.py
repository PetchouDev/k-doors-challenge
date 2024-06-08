from __future__ import annotations
from typing import Any
import math


alpha_ref = "xyzt"

class Vector():
    def __init__(self, *coords):
        self.coords = list(coords)

    def __str__(self):
        return f"Vector{tuple(self.coords)}"

    def __add__(self, other):
        return Vector(*[a + b for a, b in zip(self.coords, other.coords)])
    
    def __sub__(self, other):  
        return Vector(*[a - b for a, b in zip(self.coords, other.coords)])
    
    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.scalar_product(other)
        else:
            return Vector(*[a * other for a in self.coords])
        
    # multiply by int 
    def __rmul__(self, other):
        return Vector(*[a * other for a in self.coords])
    
    def __truediv__(self, other):
        return Vector(*[a / other for a in self.coords])
    
    def __floordiv__(self, other):
        return Vector(*[a // other for a in self.coords])
    
    # unpack
    def __iter__(self):
        return iter(self.coords)
    
    # get the opposite vector
    def __neg__(self):
        return Vector(*[-a for a in self.coords])
    
    # add an axis to the vector
    def new_axis(self, coord:float):
        self.coords.append(coord)

    # get a specific axis
    def get_axis(self, axis:int) -> float:
        if axis < len(self.coords):
            return self.coords[axis]    
        return 0
    
    # get the angle in degree
    def angle(self) -> float:
            """
            Calculates the angle (in degrees) of the vector with respect to the positive x-axis.
            The angle is always between 0 and 360 degrees.
            
            Returns:
                float: The angle of the vector in degrees.
            """
            return (180 * math.atan2(self.y, self.x) / math.pi) % 360
    
    # get an axis by its from x, y, z, t
    def __getattribute__(self, name: str) -> Any:
        if name in alpha_ref:
            return self.get_axis(alpha_ref.index(name))
        return super().__getattribute__(name)
    
    # get the number of axis
    def __len__(self):
        return len(self.coords)
    
    # get the distance of the vector
    def distance(self) -> float:
        """
        Calculates the Euclidean distance of the vector from the origin.
        
        Returns:
            float: The Euclidean distance of the vector.
        """
        return sum([c ** 2 for c in self.coords]) ** 0.5
    
    def distance_between(self, other) -> float:
        return (self - other).distance()
    
    # get the dot product of two vectors
    def scalar_product(self, other) -> float:
        return sum([a * b for a, b in zip(self.coords, other.coords)])
    
    # get the cross product of two vectors
    def vector_product(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    # get the unit vector of the vector
    def unit_vector(self):
        dist = self.distance()
        if dist == 0:
            return Vector(*[0 for _ in self.coords])
        return self / dist
    
    def normalize(self):
        self.coords = self.unit_vector().coords
        return self
    
    def __setattribute__(self, name: str, value: Any):
        if isinstance(name, int):
            self.coords[name] = value

    @property
    def x(self):
        return self.get_axis(0)
    
    @x.setter
    def x(self, value):
        self.coords[0] = value

    @property
    def y(self):
        return self.get_axis(1)
    
    @y.setter
    def y(self, value):
        self.coords[1] = value

    @property
    def z(self):
        return self.get_axis(2)
    
    @z.setter
    def z(self, value):
        self.coords[2] = value
    
    def from_json(data_json: dict) -> Vector:
        return Vector(*[data_json["x"], data_json["y"]])
    
    def to_json(self) -> dict:
        return {
            "x": self.x,
            "y": self.y
        }
    
    def copy(self):
        return Vector(*self.coords)

    


if __name__ == "__main__":
    test = Vector(3, 4)
    print(test.normalize())