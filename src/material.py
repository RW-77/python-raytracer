import math
from abc import ABC, abstractmethod

from utils import Vector, Ray, RGB, dot, rand_unit_vec, normalize, reflect, refract, rand_float
from hittable import HitRecord

class Material(ABC):

    @abstractmethod
    def scatter(_ray_in: Ray, _rec: HitRecord, attenuation: RGB, scattered: Ray):
        pass

class Lambertian(Material):

    def __init__(self, albedo: RGB) -> None:
        self.albedo = albedo
    
    def scatter(self, _ray_in: Ray, _rec: HitRecord, attenuation: RGB, scattered: Ray) -> bool:
        '''calculates and sets attenuation color values and scatter ray'''
        scatter_dir: Vector = _rec.normal + rand_unit_vec()

        # catch degenerate scatter direction
        if scatter_dir.near_zero():
            scatter_dir = _rec.normal

        scattered.orig = _rec.p
        scattered.dir = scatter_dir

        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z

        return True
    
class Metal(Material):
    def __init__(self, albedo: RGB, fuzz: float) -> None:
        self.albedo: RGB = albedo
        self.fuzz: float = min(fuzz, 1.0)

    def scatter(self, _ray_in: Ray, _rec: HitRecord, attenuation: RGB, scattered: Ray) -> bool:
        reflected: Vector = reflect(normalize(_ray_in.dir), _rec.normal)
        
        scattered.orig = _rec.p
        scattered.dir = reflected + self.fuzz*rand_unit_vec()

        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z

        return dot(scattered.dir, _rec.normal) > 0.0
    
class Dielectric(Material):
    def __init__(self, refractive_index) -> None:
        self.ir = refractive_index

    def reflectance(self, cosine: float, ref_idx: float) -> float:
        '''uses Schlick's approximation to determine reflectance'''
        r0: float = (1-ref_idx) / (1+ref_idx)
        r0 = r0*r0
        return r0 + (1-r0)*math.pow((1-cosine), 5)
    
    def scatter(self, _ray_in: Ray, _rec: HitRecord, attenuation: RGB, scattered: Ray) -> bool:
        attenuation.x = 1.0
        attenuation.y = 1.0
        attenuation.z = 1.0
        refraction_ratio: float = (1.0/self.ir) if _rec.front_face else self.ir

        unit_dir: Vector = normalize(_ray_in.dir)
        cos_theta: float = min(dot(-unit_dir, _rec.normal), 1.0)
        sin_theta: float = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract: bool = refraction_ratio * sin_theta > 1.0

        if cannot_refract or self.reflectance(cos_theta, refraction_ratio) > rand_float():
            direction: Vector = reflect(unit_dir, _rec.normal)
        else:
            direction: Vector = refract(unit_dir, _rec.normal, refraction_ratio)

        scattered.orig = _rec.p
        scattered.dir = direction

        return True