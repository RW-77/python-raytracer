import math
from typing import Union

from hittable import Hittable, HitRecord
from material import Material
from utils import Vector, Point, dot
from utils import Ray, Interval

class Sphere(Hittable):
    """Represents a sphere with center `self.center` and radius `self.radius` of material `mat`."""
    
    def __init__(self, center: Point, radius: float, mat: Material) -> None:
        self.center = center
        self.radius = radius
        self.mat = mat
    
    def hit(self, _r: Ray, ray_t: Interval) -> (HitRecord | None):
        """
        Returns true if hit by the ray any t within an interval, and updates the hit record information
        accordingly in O(1) time.
        Calculates the surface normal, whether the sphere was hit from the outside, the point and time (t) 
        of contact.
        """

        oc = _r.orig - self.center
        a = _r.dir.length_squared()
        half_b = dot(oc, _r.dir)
        c = oc.length_squared() - self.radius*self.radius
        
        disc = half_b*half_b - a*c
        if disc < 0:
            return None
        sqrtd = math.sqrt(disc)

        # find nearest root within [ray_tmin, ray_tmax]
        root = (-half_b - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (-half_b + sqrtd) / a
            if not ray_t.surrounds(root):
                return None
        
        rec = HitRecord(p=_r.at(root),t=root, mat=self.mat)
        outward_normal: Vector = (rec.p - self.center) / self.radius
        rec.set_face_normal(_r, outward_normal)

        return rec