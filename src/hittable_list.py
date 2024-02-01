from utils import Ray, Interval
from hittable import Hittable, HitRecord

class HittableList(Hittable):
    """
    Represents the scene itself as a list of all `Hittable` objects within it.
    """
    
    def __init__(self, object: Hittable = None) -> None:
        self.objects = [] # make list or numpy array later if possible
        if isinstance(object, Hittable):
            self.add(object)

    def clear(self) -> None:
        """
        Removes all objects from the scene.
        """

        self.objects.clear()

    def add(self, object: Hittable) -> None:
        """
        Adds an object to the scene.
        """

        self.objects.append(object)

    def hit(self, _r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        """
        Returns true if the ray hits any object in the scene.

        TODO: Update to store hit record information from calling individual hittable `hit` function
        and then return it as part of a tuple
        """
        temp_rec = HitRecord()
        hit_anything: bool = False
        # TODO: rename to t_closest
        closest_so_far: float = ray_t.upper_b

        # find the closest object that is hit
        for object in self.objects:
            # pass in closest_so_far for processing only objects that are closer than previously found objects
            if object.hit(_r, Interval(ray_t.lower_b, closest_so_far), temp_rec): 
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.copy(temp_rec)
        
        return hit_anything