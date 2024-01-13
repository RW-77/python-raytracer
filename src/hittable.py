from abc import ABC, abstractmethod

from utils import ray, vec3, point3, dot
from utils import interval

class hit_record:

    def __init__(self, p: point3 = None, normal: vec3 = None, mat = None, t: float = None, front_face: bool = None) -> None:
        self.p = p
        self.normal = normal
        self.mat = mat
        self.t = t
        self.front_face = front_face
    
    def set_face_normal(self, _r: ray, _outward_normal: vec3) -> None:
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

class hittable(ABC):

    @abstractmethod
    def hit(_r: ray, ray_t: interval, rec: hit_record) -> bool:
        pass