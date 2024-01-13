import sys
import random
import math
from typing import Any

from utils import rand_float

class vec3:
    te = "Unsupported operand type for {op}."

    # constructor
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # dev representation
    def __repr__(self):
        return "{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})".format(self=self)

    # string representation (user)
    def __str__(self):
        return "({self.x}, {self.y}, {self.z})".format(self=self)

    # vector negation
    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)
    
    # vector addition
    def __add__(self, v):
        if isinstance(v, vec3):
            return vec3(self.x + v.x, self.y + v.y, self.z + v.z)
        else:
            raise TypeError(vec3.te.format(op="vector addition") + f": {type(v)}")

    def __radd__(self, v):
        sys.stderr.write(f"\n\n{type(self)} {type(v)}\n")
        return self + v

    # in-place vector addition
    def __iadd__(self, v):
        if isinstance(v, vec3):
            self.x += v.x
            self.y += v.y
            self.z += v.z
        else:
            raise TypeError(vec3.te.format(op="in-place vector addition"))

    # vector subtraction
    def __sub__(self, v):
        if isinstance(v, vec3):
            return vec3(self.x - v.x, self.y - v.y, self.z - v.z)
        else:
            raise TypeError(vec3.te.format(op="vector subtraction"))

    def __rsub__(self, v):
        return self.__sub__(v)

    # in-place vector subtraction
    def __isub__(self, v):
        if isinstance(v, vec3):
            self.x -= v.x
            self.y -= v.y
            self.z -= v.z
        else:
            raise TypeError(vec3.te.format(op="in-place vector subtraction"))

    # scalar/vector multiplication
    def __mul__(self, v):
        if isinstance(v, (int, float)):
            return vec3(self.x * v, self.y * v, self.z * v)
        if isinstance(v, vec3):
            return vec3(self.x * v.x, self.y * v.y, self.z * v.z)
        else:
            raise TypeError(vec3.te.format(op="scalar/vector multiplication"))

    def __rmul__(self, v):
        return self.__mul__(v)

    # scalar multiplication
    def __imul__(self, s):
        if isinstance(s, (int, float)):
            self.x *= s
            self.y *= s
            self.z *= s
            return self
        else:
            raise TypeError(vec3.te.format(op="in-place scalar multiplication"))

    # scalar division
    def __truediv__(self, v):
        if isinstance(v, (int, float)):
            if v != 0:
                return self * (1 / v)
            else:
                raise ValueError("Unsupported: division by 0.")
        else:
            raise TypeError(vec3.te.format(op="scalar division"))
        
    # in-place scalar division
    def __itruediv__(self, s):
        if isinstance(s, (int, float)):
            if s != 0:
                return self.__imul__(1 / s)
            else:
                raise ValueError("Unsupported: diviwsion by 0.")
        else:
            raise TypeError(vec3.te.format(op="in-place scalar division"))

    # vector magnitude
    def length(self):
        return math.sqrt(dot(self, self))
    
    # magnitude squared
    def length_squared(self):
        return dot(self, self)
    
    def near_zero(self) -> bool:
        s: float = 1e-8
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s
    
    @classmethod
    def random(cls, lower_b: float = None, upper_b: float = None):
        if lower_b is not None and upper_b is not None:
            return cls(rand_float(lower_b, upper_b), rand_float(lower_b, upper_b), rand_float(lower_b, upper_b))
        else:
            return cls(rand_float(), rand_float(), rand_float())
            

from utils import interval

global rgb, point3
rgb = point3 = vec3

# dot product
def dot(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

# cross product
def cross(v1, v2):
    return vec3(v1.y*v2.z - v1.z*v2.y, -v1.x*v2.z + v1.z*v2.x,  v1.x*v2.y - v1.y*v2.x)

# normalizer
def normalize(v):
    '''returns norm of vector'''

    return v / v.length()

def rand_in_unit_disk():
    while True:
        p: vec3 = vec3(rand_float(-1,1), rand_float(-1,1), 0)
        if p.length_squared() < 1: # within unit sphere
            return p
        
def rand_unit_vec() -> vec3:
    '''returns random vector ON unit sphere'''

    while True:
        p: vec3 = vec3.random(-1, 1)
        if p.length_squared() < 1: # within unit sphere
            break
    return normalize(p)

def rand_on_hemisphere(normal: vec3) -> vec3:
    on_unit_sphere: vec3 = rand_unit_vec()
    if dot(on_unit_sphere, normal) > 0.0: # same hemisphere as normal
        return on_unit_sphere
    else:
        return -on_unit_sphere
    
def reflect(_v: vec3, _n: vec3) -> vec3:
    return _v - 2*dot(_v, _n)*_n

def refract(_uv: vec3, _n: vec3, etai_over_etat) -> vec3:
    '''refrective function which accepts a surface normal vector and unrefracted vector'''
    '''returns refracted vector'''

    cos_theta: float = min(dot(-_uv, _n), 1.0)
    sin_theta: float = math.sqrt(1.0 - cos_theta*cos_theta)

    r_out_perp: vec3 = etai_over_etat * (_uv + cos_theta*_n)
    r_out_parallel: vec3 = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * _n

    return r_out_perp + r_out_parallel
    
# # gamma 2 transform
# def linear_to_gamma(linear_component: float) -> float:
#     return math.sqrt(linear_component)

# write to ppm file
def write_color(out, pixel_color: rgb, samples_per_pixel: int):
    if not hasattr(write_color, '_intensity'):
        write_color._intensity = interval(0.000, 0.999)

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