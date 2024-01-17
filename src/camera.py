import sys
import math
import time

from utils import Vector, Point, RGB, normalize, cross, write_color, rand_on_hemisphere, rand_unit_vec, rand_in_unit_disk
from utils import Ray, Interval, rand_float, deg_to_rad
from hittable_list import HittableList
from hittable import Hittable, HitRecord
from material import Lambertian, Metal

class Camera:

    def __init__(self, aspect_ratio: float = 1.0, image_width: int = 100, samples_per_pixel: int = 10, max_depth: int = 10, vfov: float = 90, lookfrom: Point = (0,0,-1), lookat: Point = (0,0,0), vup: Vector = Vector(0,1,0), defocus_angle: float = 0, focus_dist: float = 10) -> None:
        '''initializes camera public variables'''

        self.aspect_ratio: float = aspect_ratio # ratio of image width / height
        self.image_width: int = image_width # rendered image width (pixel count)
        self.samples_per_pixel: int = samples_per_pixel # count of random samples for each pixel
        self.max_depth: int = max_depth

        self.vfov: float = vfov
        self.lookfrom = lookfrom
        self.lookat = lookat
        self.vup = vup

        self.defocus_angle: float = defocus_angle # variation angle of rays through each pixel
        self.focus_dist: float = focus_dist # distasnce from camera lookfrom point to plane of perfect focus

        # calculate image height (>= 1) (non-imaginary)
        self.image_height: int = max(int(self.image_width / self.aspect_ratio), 1)

        self.center: Point = lookfrom

        # determine viewport dimensions
        # focal_length: float = (self.lookfrom - self.lookat).length()
        theta: float = deg_to_rad(vfov)
        h = math.tan(theta/2)
        viewport_height = 2 * h * self.focus_dist
        viewport_width = viewport_height * (self.image_width/self.image_height)

        # calculate u, v, w unit basis vector for camera coordinate frame
        self.w: Vector = normalize(self.lookfrom - self.lookat)
        self.u: Vector = normalize(cross(self.vup, self.w))
        self.v = cross(self.w, self.u)

        # horizontal and vertical viewport edge guidance vectors
        viewport_u: Vector = viewport_width * self.u # vector across viewport horizontal edge
        viewport_v: Vector = viewport_height * -self.v # vector down viewport vertical edge

        # horizontal and vertical delta vectors (from pixel to pixel)
        # delta depends on number of pixels in image (1 per shift)
        self.pixel_delta_u: Vector = viewport_u / self.image_width
        self.pixel_delta_v: Vector = viewport_v / self.image_height

        # calculate location of upper left pixel
        viewport_upper_left: Point = self.center - (self.focus_dist * self.w) - viewport_u/2 - viewport_v/2
        # not entirely sure why this next step is necessary, maybe to make sure the 00 pixel is within the vp?
        self.pixel00_loc: Point  = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

        # calculate camera defocus disk basis vectors
        defocus_radius: float = self.focus_dist * math.tan(deg_to_rad(self.defocus_angle / 2))
        self.defocus_disk_u: Vector = self.u * defocus_radius # defocus disk horizontal radius
        self.defocus_disk_v: Vector = self.v * defocus_radius # defocus disk vertical radius

    def render(self, _world: HittableList) -> None:
        '''dispatches rays into world uses results to construct rendered image'''
        start_time = time.time()

        # dimensions to PPM
        print(f"P3\n{self.image_width} {self.image_height}\n255")

        for j in range(self.image_height):
            # progress meter
            sys.stderr.write(f"\rScanlines remaining: {self.image_height-j} ")

            for i in range(self.image_width):
                
                pixel_color: RGB = RGB(0, 0, 0)
                for sample in range(0, self.samples_per_pixel):
                    r: Ray = self._get_ray(i, j)
                    rc: RGB = self._ray_color(r, self.max_depth, _world)
                    pixel_color = pixel_color + rc

                write_color(sys.stdout, pixel_color, self.samples_per_pixel)

        sys.stderr.write(f"\rDone.\nRender took {time.time() - start_time} seconds")


    def _get_ray(self, i: int, j: int) -> Ray:
        '''get a randomly-sampled camera ray for the pixel atl location (i, j), originating'''
        '''from the camera defocus'''

        pixel_center: Point = self.pixel00_loc + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
        pixel_sample: Point = pixel_center + self._pixel_sample_square()

        ray_origin: Point = self.center if (self.defocus_angle <= 0) else self.defocus_disk_sample()
        ray_dir: Vector = pixel_sample - ray_origin

        return Ray(ray_origin, ray_dir)
    
    def _pixel_sample_square(self) -> Point:
        '''returns random point in square surrounding a pixel at origin'''

        px: float = -0.5 + rand_float()
        py: float = -0.5 + rand_float()

        return (px * self.pixel_delta_u) + (py * self.pixel_delta_v)
    
    def defocus_disk_sample(self) -> Point:
        '''returns random point in the camera defocus disk'''
        p: Point = rand_in_unit_disk()
        return self.center + (p.x * self.defocus_disk_u) + (p.y * self.defocus_disk_v)

    def _ray_color(self, _r: Ray, depth: int, _world: Hittable) -> RGB:
        rec = HitRecord()

        # if ray bounce limit exceeded, no more light gathered
        if depth <= 0:
            return RGB(0, 0, 0)

        # this will check if object is hit AND update rec to nearest object (if hit)
        if _world.hit(_r, Interval(0.001, math.inf), rec):
            scattered = Ray()
            attenuation = RGB(0, 0, 0)
            if rec.mat.scatter(_r, rec, attenuation, scattered):
                return attenuation * self._ray_color(scattered, depth-1, _world)
            return RGB(0, 0, 0)

        unit_dir = normalize(_r.dir)
        a = 0.5 * (unit_dir.y + 1.0)
        return (1.0-a)*RGB(1.0, 1.0, 1.0) + a*RGB(0.5, 0.7, 1.0)