import sys, time, math

from utils import interval
from utils import vec3, rgb, point3, dot, cross, normalize, write_color, random
from utils import ray, rand_float
from hittable_list import hittable_list
from camera import camera
from sphere import sphere
from material import lambertian, metal, dielectric


def main():
    
    # Create World
    world: hittable_list = hittable_list()

    ground_material: lambertian = lambertian(rgb(0.5, 0.5, 0.5))
    world.add(sphere(point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat: float = rand_float()
            center: point3 = point3(a + 0.9*rand_float(), 0.2, b + 0.9*rand_float())

            if (center - point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo: rgb = rgb.random() * rgb.random()
                    sphere_material: lambertian = lambertian(albedo)
                    world.add(sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo: rgb = rgb.random(0.5, 1)
                    fuzz: float = rand_float(0, 0.5)
                    sphere_material: metal = metal(albedo, fuzz)
                    world.add(sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material: dielectric = dielectric(1.5)
                    world.add(sphere(center, 0.2, sphere_material))

    material1: dielectric = dielectric(1.5)
    world.add(sphere(point3(0, 1, 0), 1.0, material1))

    material2: lambertian = lambertian(rgb(0.4, 0.2, 0.1))
    world.add(sphere(point3(-4, 1, 0), 1.0, material2))

    material3: metal = metal(rgb(0.7, 0.6, 0.5), 0.0)
    world.add(sphere(point3(4, 1, 0), 1.0, material3))

    aspect_ratio: float = 16.0/9.0
    image_width: int = 1200
    samples_per_pixel: int = 500
    max_depth: int = 50

    vfov: float = 20
    lookfrom: point3 = point3(13, 2, 3)
    lookat: point3 = point3(0, 0, 0)
    vup: vec3 = vec3(0, 1, 0)

    defocus_angle: float = 0.6
    focus_dist: float = 10.0

    cam: camera = camera(aspect_ratio=aspect_ratio, image_width=image_width, samples_per_pixel=samples_per_pixel, max_depth=max_depth, vfov=vfov, lookfrom=lookfrom, lookat=lookat, vup=vup, defocus_angle=defocus_angle, focus_dist=focus_dist)

    cam.render(world)
    
if __name__ == '__main__':
    main()