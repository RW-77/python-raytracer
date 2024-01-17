from abc import ABC, abstractmethod

from utils import Ray, Vector, Point, dot
from utils import Interval

class HitRecord:

    def __init__(self, p: Point = None, normal: Vector = None, mat = None, t: float = None, front_face: bool = None) -> None:
        self.p = p
        self.normal = normal
        self.mat = mat
        self.t = t
        self.front_face = front_face
    
    def set_face_normal(self, _r: Ray, _outward_normal: Vector) -> None:
        '''sets the hit record normal vector (determines orietation)'''
        '''_outward_normal is assumed to be of unit length'''
        
        self.front_face = dot(_r.dir, _outward_normal) < 0
        self.normal = _outward_normal if self.front_face else -_outward_normal
    
    def copy(self, other) -> None:
        self.p = other.p
        self.normal = other.normal
        self.mat = other.mat
        self.t = other.t
        self.front_face = other.front_face

class Hittable(ABC):

    @abstractmethod
    def hit(_r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        pass