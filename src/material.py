import math
from abc import ABC, abstractmethod

from utils import Vector, Ray, RGB, dot, rand_unit_vec, normalize, reflect, refract, rand_float
from hittable import HitRecord

class Material(ABC):
    """
    Abstract base class representing different material types which are assigned to objects.

    Calculates the resulting ray (if any) that is scattered when hit by an incident ray (containing hit information)

    Methods:
    scatter(_ray_in: Ray, _rec: HitRecord, attenuation: RGB, scattered: Ray) -> bool
        calculates the scattered ray and determines how much it should be attenuated
    """

    @abstractmethod
    def scatter(_ray_in: Ray, _rec: HitRecord, attenuation: RGB, scattered: Ray): 
        '''
        Based on an incident ray and `HitRecord` (holding information about the ray-object intersection),
        calculates for respective material the outgoing ray and attenuation (intensity) of that ray

        Args:
        `_ray_in : Ray`
            The incident ray which hits the object whose information we will use to calculate the scattered ray
        `_rec : HitRecord`
            A structure which groups together information about a ray-object intersection 
            which will also be use to calculate the scatttered ray

        Returns:
        `tuple` (scattered, attenuation)
        '''
        pass

class Lambertian(Material):
    """
    Material type which models diffuse (matte) surfaces. Diffuse surfaces can be thought of as random-like, with photons 
    being scattered in random directions.
    This is more accurately achieved using the Lambertian distribution. Rays are scattered proportional to cos(theta); that is, 
    the probability a ray is scattered in a certain direction is proportional to its angle from the surface normal.
    """

    def __init__(self, albedo: RGB) -> None:
        self.albedo = albedo
    
    def scatter(self, _ray_in: Ray, _rec: HitRecord, attenuation: RGB, scattered: Ray) -> bool:
        """
        Creates scatter ray using Lambertian reflectance in which a ray has a cos(phi) probability of
        being scattered at angle that is phi from the surface normal.

        Generating this probability distribution is mathematically equivalent to setting the direction vector
        of the resulting ray from the hit point towards a random point on a unit sphere centered on the end 
        of the unit surface normal.

        Args:
        `_ray_in : Ray`
            The incident ray which hits the object whose information we will use to calculate the scattered ray
        `_rec : HitRecord`
            A structure which groups together information about a ray-object intersection 
            which will also be use to calculate the scatttered ray

        Returns:
        `tuple` (scattered: Ray, attenuation: RGB)
        """
        
        scatter_dir: Vector = _rec.normal + rand_unit_vec()

        # catch degenerate scatter direction in the case where the random point on the sphere points directly back to the hit point
        if scatter_dir.near_zero():
            scatter_dir = _rec.normal

        scattered.orig = _rec.p
        scattered.dir = scatter_dir

        # NOTE: scatter should handle the scattering of the ray, but it makes more sense for ray_color to handle the mixing of color values
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
         
        return True
    
class Metal(Material):
    """
    Material type which models metal surfaces. Rays are reflected about the surface normal with a specified specularity
    which can be thought of as the precision of reflectance.
    """
    def __init__(self, albedo: RGB, fuzz: float) -> None:
        self.albedo: RGB = albedo
        self.fuzz: float = min(fuzz, 1.0)

    def scatter(self, _ray_in: Ray, _rec: HitRecord, attenuation: RGB, scattered: Ray) -> bool:
        """
        Reflects incident ray about surface normal vector. A fuzz factor is used to add slight randomness to the 
        reflected rays. The incident ray is reflected and then normalized. A sphere with radius `fuzz` is centered
        on the normalized reflected ray similar to the Lambertian distribution which allows for a certain randomness
        in reflectance, specified by `fuzz`.

        Args:
        `_ray_in : Ray`
            The incident ray which hits the object whose information we will use to calculate the scattered ray
        `_rec : HitRecord`
            A structure which groups together information about a ray-object intersection which will also be use to 
            calculate the scatttered ray

        Returns:
        `tuple` (scattered: Ray, attenuation: RGB)
        """
        reflected: Vector = reflect(normalize(_ray_in.dir), _rec.normal)
        
        scattered.orig = _rec.p
        scattered.dir = reflected + self.fuzz*rand_unit_vec()

        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z

        # surface absorbs rays that scatter below it
        return dot(scattered.dir, _rec.normal) > 0.0
    
class Dielectric(Material):
    """
    Material type which models dielectric surfaces. Light is absored or transmitted 
    rather than automatically reflected by the surface. Absorbance and reemiittance is dictated by Snell's Law and Fresnel equations

    Note: this class is limited in encapsulating all dielectric materials. It assumes colorlessness (no albedo) and transparency (attenuation set to (1, 1, 1)). So basically just clear glass for now.
    """

    def __init__(self, refractive_index) -> None:
        self.ir: float = refractive_index

    def reflectance(self, cosine: float, ref_idx: float) -> float:
        """uses Schlick's approximation to determine reflectance"""

        r0: float = (1-ref_idx) / (1+ref_idx)
        r0 = r0*r0
        return r0 + (1-r0)*math.pow((1-cosine), 5)
    
    def scatter(self, _ray_in: Ray, _rec: HitRecord, attenuation: RGB, scattered: Ray) -> bool:
        """
        Calculates outgoing ray based on the refractive index of the dielectric material, the ray, and hit information, assuming incident ray is transitioning from air (refractive index of 1).
        The ray is reflected and possibly refracted depending on the refraction ratio and incident angle.
        """

        attenuation.x = 1.0
        attenuation.y = 1.0
        attenuation.z = 1.0
        # assumes ray is transitioning to or from air medium (refractive index of 1.0)
        refraction_ratio: float = (1.0/self.ir) if _rec.front_face else self.ir

        unit_dir: Vector = normalize(_ray_in.dir)
        cos_theta: float = min(dot(-unit_dir, _rec.normal), 1.0)
        sin_theta: float = math.sqrt(1.0 - cos_theta*cos_theta)

        # true if there is no solution to Snell's law
        cannot_refract: bool = refraction_ratio * sin_theta > 1.0

        if cannot_refract or self.reflectance(cos_theta, refraction_ratio) > rand_float():
            # cannot refract, must reflect
            direction: Vector = reflect(unit_dir, _rec.normal)
        else:
            # can refract
            direction: Vector = refract(unit_dir, _rec.normal, refraction_ratio)

        scattered.orig = _rec.p
        scattered.dir = direction

        return True