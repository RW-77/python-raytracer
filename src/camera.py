import sys
import math
import time
from typing import Union

from utils import Vector, Point, RGB, normalize, cross, write_color, rand_on_hemisphere, rand_unit_vec, rand_in_unit_disk
from utils import Ray, Interval, rand_float, deg_to_rad
from hittable_list import HittableList
from hittable import Hittable, HitRecord
from material import Lambertian, Metal

class Camera:
    """
    Represents the camera which constructs the 2D image using the 3D scene. The camera is 
    responsible for shooting rays into the scene, detecting ray-object intersections and then 
    coloring pixels appropriately.
    """

    def __init__(self, aspect_ratio: float = 1.0, image_width: int = 100, samples_per_pixel: int = 10, max_depth: int = 10, 
                 vfov: float = 90, lookfrom: Point = Point(0,0,-1), lookat: Point = Point(0,0,0), vup: Vector = Vector(0,1,0), defocus_angle: float = 0.0, focus_dist: float = 10.0) -> None:

        self.aspect_ratio: float = aspect_ratio # ratio of image width / height
        self.image_width: int = image_width # rendered image width (pixel count)
        self.samples_per_pixel: int = samples_per_pixel # count of random samples for each pixel
        self.max_depth: int = max_depth

        self.vfov: float = vfov
        self.lookfrom: Point = lookfrom
        self.lookat: Point = lookat
        self.vup: Vector = vup

        self.defocus_angle: float = defocus_angle # variation angle of rays through each pixel
        self.focus_dist: float = focus_dist # distance from camera `lookfrom` point to plane of perfect focus

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
        """
        Dispatches rays into world and uses ray-intersection information to construct rendered image
        """

        start_time = time.time()

        print(f"P3\n{self.image_width} {self.image_height}\n255")

        for j in range(self.image_height):

            sys.stderr.write(f"\rScanlines remaining: {self.image_height-j} ")
            for i in range(self.image_width):

                # if not (j == int(self.image_height*0.5) and i == self.image_width * (2/3)):
                #     continue

                # initial pixel_color is black
                pixel_color = RGB(0, 0, 0)
                # Collect random sample around original pixel for antialiasing
                for sample in range(0, self.samples_per_pixel):
                    # DEBUG
                    # sys.stderr.write(f"Pixel ({i}, {j}): Sample {sample}\n")

                    sample_ray: Ray = self.rand_pixel_ray(i, j)
                    sample_ray_color: RGB = self.ray_color(sample_ray, self.max_depth, _world)
                    # summing colors to be blended (averaged) in write_color

                    pixel_color = pixel_color + sample_ray_color
                # write_color divides total color sum by sample size for averaging
                write_color(sys.stdout, pixel_color, self.samples_per_pixel)

        sys.stderr.write(f"\rDone. Render took {time.time() - start_time} seconds.\n")

    def rand_pixel_ray(self, i: int, j: int) -> Ray:
        """
        Get a randomly-sampled camera ray for the pixel at location (i, j), originating from the camera defocus.
        """
        # Computes the coordinates of the point at (i, j)
        pixel_center: Point = self.pixel00_loc + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
        # Computes the coordinates of the sampled pixel around (i, j)
        pixel_sample: Point = pixel_center + self.pixel_sample_square()
        
        ray_origin: Point = self.center if (self.defocus_angle <= 0) else self.defocus_disk_sample()
        # Compute vector to sample pixel
        ray_dir: Vector = pixel_sample - ray_origin

        return Ray(ray_origin, ray_dir)
    
    def pixel_sample_square(self) -> Point:
        """
        Returns random point in square surrounding a pixel at origin.
        NOTE: This is called by `defocus_disk_sample` which converts the point returned by this function to a ray.
        Can we combine the functions?
        """

        px: float = -0.5 + rand_float()
        py: float = -0.5 + rand_float()

        return (px * self.pixel_delta_u) + (py * self.pixel_delta_v)
    
    def defocus_disk_sample(self) -> Point:
        """
        Returns random point in the camera defocus disk.
        """
        # get a random vector in the unit disk
        p: Point = rand_in_unit_disk()
        # modify vector to fit within camera's frame of reference
        return self.center + (p.x * self.defocus_disk_u) + (p.y * self.defocus_disk_v)

    def ray_color(self, _r: Ray, depth: int, _world: Hittable) -> RGB:
        """
        Returns the RGB color value for a ray `_r` that has been shot into `_world`. Since this function is recursive
        we restrict the maximum recursion depth after which the ray will return `RGB(0, 0, 0)`.
        """

        # if ray bounce limit exceeded, no more light is gathered
        if depth <= 0:
            return RGB(0, 0, 0)

        # check if object is hit AND update rec to hold the information of the nearest object (if hit)
        rec = _world.hit(_r, Interval(0.001, math.inf)) or None
        if rec is not None:

            # DEBUG
            # sys.stderr.write("`rec` info:\n")
            # sys.stderr.write(str(rec) + "\n")

            attenuation, scattered = rec.mat.scatter(_r, rec) or (None, None)
            
            # rays are not scattered in all scenarios (can be absorbed for instance)
            if attenuation is not None and scattered is not None:
                return attenuation * self.ray_color(scattered, depth-1, _world)
            else:
                return RGB(0, 0, 0)
        else:
            # sys.stderr.write("`rec` is `None`:\n")

            # if the ray does not hit any objects in the scene, then the background (sky) is colored using a gradient
            unit_dir = normalize(_r.dir)
            a = 0.5 * (unit_dir.y + 1.0)
            return (1.0-a)*RGB(1.0, 1.0, 1.0) + a*RGB(0.5, 0.7, 1.0)