from abc import ABC, abstractmethod
from typing import Tuple

from utils import Ray, Vector, Point, dot
from utils import Interval

class HitRecord:
    """
    Bundles all relevant information about a ray-object intersection into a class:
    - point of contact (`Point`)
    - surface normal vector (`Vector`)
    - material type of surface (`Material`)
    - time at which ray intersects object (`float`)
    - whether surface is hit from outside (`bool`)
    """

    def __init__(self, p: Point = None, normal: Vector = None, mat = None, t: float = None, front_face: bool = None) -> None:
        self.p = p
        self.normal = normal
        self.mat = mat
        self.t = t
        self.front_face = front_face
    
    def set_face_normal(self, _r: Ray, _outward_normal: Vector) -> None:
        """
        Sets the hit record normal vector, outward_normal is assumed to be of unit length.
        """
        
        self.front_face = dot(_r.dir, _outward_normal) < 0
        self.normal = _outward_normal if self.front_face else -_outward_normal
    
    def copy(self, other) -> None:
        """
        NOTE: Temporary copy function for hit record.
        TODO: If code is refactored to return hit_record instead of directly updating it, remove
        this function.
        """

        self.p = other.p
        self.normal = other.normal
        self.mat = other.mat
        self.t = other.t
        self.front_face = other.front_face

class Hittable(ABC):
    """Abstract base class representing any object in the scene which is \"hittable\" by the ray."""
    
    @abstractmethod
    def hit(_r: Ray, ray_t: Interval) -> (HitRecord | None):
        """
        TODO: Change after refactoring `hit` to return `HitRecord` object.
        """
        pass