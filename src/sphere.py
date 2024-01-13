import math

from hittable import hittable, hit_record
from material import material
from utils import point3, dot
from utils import ray, interval

class sphere(hittable):
    def __init__(self, center: point3, radius: float, mat: material) -> None:
        self.center = center
        self.radius = radius
        self.mat = mat
    
    def hit(self, _r: ray, ray_t: interval, rec: hit_record):
        oc = _r.orig - self.center
        a = _r.dir.length_squared()
        half_b = dot(oc, _r.dir)
        c = oc.length_squared() - self.radius*self.radius
        
        disc = half_b*half_b - a*c
        if disc < 0:
            return False
        sqrtd = math.sqrt(disc)

        # find nearest root within [ray_tmin, ray_tmax]
        root = (-half_b - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (-half_b + sqrtd) / a
            if not ray_t.surrounds(root):
                return False
        
        # update later using hit_record.copy()
        rec.t = root
        rec.p = _r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(_r, outward_normal)
        rec.mat = self.mat

        return True