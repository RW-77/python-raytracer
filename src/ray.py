from vec3 import vec3, point3

# essentially a parametrization of the form alpha(t) = a + tv
class ray:
    
    def __init__(self, origin: point3 = None, direction: vec3 = None):
        self.orig: point3 = origin
        self.dir: vec3 = direction

    def __repr__(self) -> str:
        return "{self.__class__.__name__}(origin={self.orig}, direction={self.dir})".format(self=self)

    def at(self, t) -> vec3:
        return self.orig + t*self.dir