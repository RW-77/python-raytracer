import sys

from utils import Ray, Interval
from hittable import Hittable, HitRecord, AABB


class HittableList(Hittable):
    """
    Represents the scene itself as a list of all `Hittable` objects within it.
    """

    def __init__(self, object: Hittable = None) -> None:
        self.bbox: AABB = AABB()
        self.objects: list[Hittable] = []
        if isinstance(object, Hittable):
            self.add(object)

    @property
    def bounding_box(self) -> AABB:
        """Returns the bounding box of the entire scene."""

        return self.bbox

    def add(self, object: Hittable) -> None:
        """Adds an object to the scene."""

        self.objects.append(object)
        self.bbox = AABB.merge(self.bbox, object.bounding_box)

    def clear(self) -> None:
        """
        Removes all objects from the scene.
        """

        self.objects.clear()

    def hit(self, _r: Ray, ray_t: Interval) -> HitRecord | None:
        """
        Returns true if the ray hits any object in the scene.

        TODO: Update to store hit record information from calling individual hittable `hit` function
        and then return it as part of a tuple
        """

        hit_anything: bool = False
        t_closest: float = ray_t.upper_b
        hit_anything = True
        rec = self.objects[0].hit(_r, Interval(ray_t.lower_b, t_closest)) or None
        # for object in self.objects:
        #     # pass in t_closest for processing only objects that are closer than previously found objects
        #     temp_rec = object.hit(_r, Interval(ray_t.lower_b, t_closest)) or None
        #     if temp_rec is not None:
        #         hit_anything = True
        #         t_closest = temp_rec.t
        #         rec = temp_rec
        #
        return rec
