from vec3 import Vector, Point

class Ray:
    """
    Represents a light ray which is traced by the program, which is essentially a parametrization of a
    line in 3D space. Composed of a starting `Point` and a direction `Vector` (of the form alpha(t) = a + tv).
    """

    def __init__(self, origin: Point = None, direction: Vector = None):
        self.orig: Point = origin
        self.dir: Vector = direction

    def __repr__(self) -> str:
        """String expression for `Ray`."""

        return "{self.__class__.__name__}(origin={self.orig}, direction={self.dir})".format(self=self)

    def at(self, t) -> Vector:
        """Returns the point at `t` along the `ray`."""

        return self.orig + t*self.dir