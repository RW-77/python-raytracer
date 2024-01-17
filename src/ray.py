from vec3 import Vector, Point

# essentially a parametrization of the form alpha(t) = a + tv
class Ray:
    
    def __init__(self, origin: Point = None, direction: Vector = None):
        self.orig: Point = origin
        self.dir: Vector = direction

    def __repr__(self) -> str:
        return "{self.__class__.__name__}(origin={self.orig}, direction={self.dir})".format(self=self)

    def at(self, t) -> Vector:
        return self.orig + t*self.dir