import sys

from utils import Interval, Ray, Point, min_max

class AABB:
    """
    Docstring for AABB class.
    """

    def __init__(self, ix: Interval = Interval(), iy: Interval = Interval(), iz: Interval = Interval()):
        self.slab_x = ix
        self.slab_y = iy
        self.slab_z = iz
    
    @classmethod
    def from_corners(cls, _a: Point, _b: Point):
        """Alternate constructor for AABB which constructs the bounding box using two corners"""

        ix = Interval(min(_a.x, _b.x), max(_a.x, _b.x))
        iy = Interval(min(_a.y, _b.y), max(_a.y, _b.y))
        iz = Interval(min(_a.z, _b.z), max(_a.z, _b.z))
        return cls(ix, iy, iz)
    
    @classmethod
    def merge(cls, _box0: 'AABB', _box1: 'AABB') -> 'AABB':
        """
        Constructors a bounding box from two bounding boxes.
        """

        ix = Interval.merge(_box0.slab_x, _box1.slab_x)
        iy = Interval.merge(_box0.slab_y, _box1.slab_y)
        iz = Interval.merge(_box0.slab_z, _box1.slab_z)
        return cls(ix, iy, iz)
    
    def axis(self, n: int) -> Interval:
        """TODO: remove late if restricting vector to 3 dimensions."""
        
        if n == 1:
            return self.slab_y
        if n == 2:
            return self.slab_z
        return self.slab_x
    
    def hit(self, _r: Ray, ray_t: Interval) -> bool:
        """Returns true if a ray intersects this `AABB` within `ray_t`."""

        # sys.stderr.write(f"Determining if there is collision with AABB:\n\t{self.slab_x}\n\t{self.slab_y}\n\t{self.slab_z}\n")
        # lower_b = ray_t.lower_b
        # upper_b = ray_t.upper_b
        # sys.stderr.write(f"Ray:\n\torigin = {_r.origin}\n\tdirection = {_r.dir}\n")

        lower_b = ray_t.lower_b
        upper_b = ray_t.upper_b

        inv_ray_dir: float = 1.0 / _r.dir.x
        t0: float = (self.slab_x.lower_b - _r.origin.x) * inv_ray_dir
        t1: float = (self.slab_x.upper_b - _r.origin.x) * inv_ray_dir

        if inv_ray_dir < 0.0:
            t0, t1 = t1, t0

        if t0 > lower_b:
            lower_b = t0
        if t1 < upper_b:
            upper_b = t1

        if upper_b <= lower_b:
            return False
        
        
        inv_ray_dir: float = 1 / _r.dir.y
        t0 = (self.slab_y.lower_b - _r.origin.y) * inv_ray_dir
        t1 = (self.slab_y.upper_b - _r.origin.y) * inv_ray_dir

        if inv_ray_dir < 0:
            t0, t1 = t1, t0

        if t0 > lower_b:
            lower_b = t0
        if t1 < upper_b:
            upper_b = t1

        if upper_b <= lower_b:
            return False
        
        
        inv_ray_dir: float = 1 / _r.dir.z
        t0 = (self.slab_z.lower_b - _r.origin.z) * inv_ray_dir
        t1 = (self.slab_z.upper_b - _r.origin.z) * inv_ray_dir

        if inv_ray_dir < 0:
            t0, t1 = t1, t0

        if t0 > lower_b:
            lower_b = t0
        if t1 < upper_b:
            upper_b = t1

        if upper_b <= lower_b:
            return False
        
        return True
    
    def __str__(self) -> str:
        return f"slab_x = {self.slab_x}\nslab_y = {self.slab_y}\nslab_z = {self.slab_z}"