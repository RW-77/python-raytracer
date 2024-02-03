import sys
import random
import math
from typing import Any

from utils import rand_float

class Vector:
    """
    A 3-dimensional vector.
    """

    te = "Unsupported operand type for {op}."

    def __init__(self, x: float = 0, y : float = 0, z : float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """String expression for `Vector`"""

        return "{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})".format(self=self)

    def __str__(self):
        """String representation of 'Vector'"""

        return "({self.x}, {self.y}, {self.z})".format(self=self)

    def __neg__(self):
        """Performs element-wise negation."""

        return Vector(-self.x, -self.y, -self.z)
    
    def __add__(self, v):
        """Performs element-wise vector addition."""

        if isinstance(v, Vector):
            return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
        else:
            raise TypeError(Vector.te.format(op="vector addition") + f": {type(v)}")

    # def __radd__(self, v):
    #     """Performs element-wise vector addition."""

    #     if isinstance(v, Vector):
    #         return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
    #     else:
    #         raise TypeError(Vector.te.format(op="vector addition") + f": {type(v)}")

    def __iadd__(self, v):
        """Performs in-place element-wise vector addition."""

        if isinstance(v, Vector):
            self.x += v.x
            self.y += v.y
            self.z += v.z
        else:
            raise TypeError(Vector.te.format(op="in-place vector addition"))

    def __sub__(self, v):
        """Performs element-wise vector subtraction."""

        if isinstance(v, Vector):
            return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
        else:
            raise TypeError(Vector.te.format(op="vector subtraction"))

    def __rsub__(self, v):
        """Performs element-wise vector subtraction."""

        return self.__sub__(v)

    def __isub__(self, v):
        """Performs in-place element-wise vector subtraction."""

        if isinstance(v, Vector):
            self.x -= v.x
            self.y -= v.y
            self.z -= v.z
        else:
            raise TypeError(Vector.te.format(op="in-place vector subtraction"))

    def __mul__(self, v):
        """Performs element-wise vector multiplication."""

        if isinstance(v, (int, float)):
            return Vector(self.x * v, self.y * v, self.z * v)
        if isinstance(v, Vector):
            return Vector(self.x * v.x, self.y * v.y, self.z * v.z)
        else:
            raise TypeError(Vector.te.format(op="scalar/vector multiplication"))

    def __rmul__(self, v):
        """Performs element-wise vector multiplication."""

        return self.__mul__(v)

    def __imul__(self, s):
        """Performs in-place scalar multiplication."""

        if isinstance(s, (int, float)):
            self.x *= s
            self.y *= s
            self.z *= s
            return self
        else:
            raise TypeError(Vector.te.format(op="in-place scalar multiplication"))

    def __truediv__(self, v):
        """Performs element-wise vector division."""

        if isinstance(v, (int, float)):
            if v != 0:
                return self * (1 / v)
            else:
                raise ValueError("Unsupported: division by 0.")
        else:
            raise TypeError(Vector.te.format(op="scalar division"))
        
    # in-place scalar division
    def __itruediv__(self, s):
        """Performs in-place element-wise vector division."""

        if isinstance(s, (int, float)):
            if s != 0:
                return self.__imul__(1 / s)
            else:
                raise ValueError("Unsupported: diviwsion by 0.")
        else:
            raise TypeError(Vector.te.format(op="in-place scalar division"))

    # NOTE: consider precomputing as member attribute
    def length(self):
        """Returns the magnitude of this vector."""

        return math.sqrt(dot(self, self))
    
    # magnitude squared
    def length_squared(self):
        """Returns the square of the magnitude of this vector."""

        return dot(self, self)
    
    def near_zero(self) -> bool:
        """Returns true if all components of this vector are sufficiently close to 0."""

        s: float = 1e-8
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s
    
    @classmethod
    def random(cls, lower_b: float = 0, upper_b: float = 1):
        """Returns a vector with each component a random `float` within [`lower_b`, `upper_b`] or [0, 1] if no arguments are passed in."""
        return cls(rand_float(lower_b, upper_b), rand_float(lower_b, upper_b), rand_float(lower_b, upper_b))

from utils import Interval

# RGB and Point are aliases for Vector
global RGB, Point
RGB = Point = Vector

def dot(v1, v2):
    """Returns the dot product of `v1` and `v2`."""

    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def cross(v1, v2):
    """Returns the cross product of `v1` and `v2`."""

    return Vector(v1.y*v2.z - v1.z*v2.y, -v1.x*v2.z + v1.z*v2.x,  v1.x*v2.y - v1.y*v2.x)

def normalize(v):
    """Returns the norm of a vector."""
    return v / v.length()

def rand_in_unit_disk():
    """Returns a random vector within (but not necessarily on) the unit disk using a rejection method."""

    while True:
        p: Vector = Vector(rand_float(-1,1), rand_float(-1,1), 0)
        if p.length_squared() < 1: # within unit sphere
            return p
        
def rand_unit_vec() -> Vector:
    """Returns random unit vector which is ON the unit sphere."""

    while True:
        p: Vector = Vector.random(-1, 1)
        if p.length_squared() < 1: # within unit sphere
            break
    return normalize(p)

def rand_on_hemisphere(normal: Vector) -> Vector:
    """Returns a random unit vector on the same hemisphere as the surface normal."""

    on_unit_sphere: Vector = rand_unit_vec()
    if dot(on_unit_sphere, normal) > 0.0: # same hemisphere as normal
        return on_unit_sphere
    else:
        return -on_unit_sphere
    
def reflect(_v: Vector, _n: Vector) -> Vector:
    """Returns the reflected vector based on the incident vector and the surface normal."""

    return _v - 2*dot(_v, _n)*_n

def refract(_uv: Vector, _n: Vector, ref_idx_ratio) -> Vector:
    """Returns the refracted vector based on the incident vector, the surface normal, and the refractive index ratio of the medium transition."""

    cos_theta: float = min(dot(-_uv, _n), 1.0)
    sin_theta: float = math.sqrt(1.0 - cos_theta*cos_theta)

    r_out_perp: Vector = ref_idx_ratio * (_uv + cos_theta*_n)
    r_out_parallel: Vector = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * _n

    return r_out_perp + r_out_parallel
    
# # gamma 2 transform
# def linear_to_gamma(linear_component: float) -> float:
#     return math.sqrt(linear_component)

def write_color(out, pixel_color: RGB, samples_per_pixel: int):
    """Writes gamme-transformed RGB values of vector to stream `out`."""
    
    if not hasattr(write_color, '_intensity'):
        write_color._intensity = Interval(0.000, 0.999)

    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    # divide color by number of samples
    scale: float = 1.0 / samples_per_pixel
    r *= scale
    g *= scale
    b *= scale

    # apply linear to gamma transform
    r = math.sqrt(r)
    g = math.sqrt(g)
    b = math.sqrt(b)

    # write translated [0, 255] value of each color component
    r_out = int(256 * write_color._intensity.clamp(r))
    g_out = int(256 * write_color._intensity.clamp(g))
    b_out = int(256 * write_color._intensity.clamp(b))

    out.write(f"{r_out} {g_out} {b_out}\n")