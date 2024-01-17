import sys, time, math

from utils import Interval
from utils import Vector, RGB, Point, dot, cross, normalize, write_color, random
from utils import Ray, rand_float
from hittable_list import HittableList
from camera import Camera
from sphere import Sphere
from material import Lambertian, Metal, Dielectric


def main():
    
    # Create World
    world: HittableList = HittableList()

    ground_material: Lambertian = Lambertian(RGB(0.5, 0.5, 0.5))
    world.add(Sphere(Point(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat: float = rand_float()
            center: Point = Point(a + 0.9*rand_float(), 0.2, b + 0.9*rand_float())

            if (center - Point(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo: RGB = RGB.random() * RGB.random()
                    sphere_material: Lambertian = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo: RGB = RGB.random(0.5, 1)
                    fuzz: float = rand_float(0, 0.5)
                    sphere_material: Metal = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material: Dielectric = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1: Dielectric = Dielectric(1.5)
    world.add(Sphere(Point(0, 1, 0), 1.0, material1))

    material2: Lambertian = Lambertian(RGB(0.4, 0.2, 0.1))
    world.add(Sphere(Point(-4, 1, 0), 1.0, material2))

    material3: Metal = Metal(RGB(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point(4, 1, 0), 1.0, material3))

    aspect_ratio: float = 16.0/9.0
    image_width: int = 1200
    samples_per_pixel: int = 500
    max_depth: int = 50

    vfov: float = 20
    lookfrom: Point = Point(13, 2, 3)
    lookat: Point = Point(0, 0, 0)
    vup: Vector = Vector(0, 1, 0)

    defocus_angle: float = 0.6
    focus_dist: float = 10.0

    cam: Camera = Camera(aspect_ratio=aspect_ratio, image_width=image_width, samples_per_pixel=samples_per_pixel, max_depth=max_depth, vfov=vfov, lookfrom=lookfrom, lookat=lookat, vup=vup, defocus_angle=defocus_angle, focus_dist=focus_dist)

    cam.render(world)
    
if __name__ == '__main__':
    main()