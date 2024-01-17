from utils import Ray, Interval
from hittable import Hittable, HitRecord

class HittableList(Hittable):
    
    def __init__(self, object: Hittable = None) -> None:
        self.objects = [] # make list or numpy array later if possible
        if isinstance(object, Hittable):
            self.add(object)

    def clear(self) -> None:
        self.objects.clear()

    def add(self, object: Hittable) -> None:
        self.objects.append(object)

    def hit(self, _r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        temp_rec = HitRecord()
        hit_anything: bool = False
        closest_so_far = ray_t.upper_b

        # we only need the closest object that is hit, meaning 
        for object in self.objects:
            if object.hit(_r, Interval(ray_t.lower_b, closest_so_far), temp_rec): # pass in closest_so_far for processing closer objects
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.copy(temp_rec)
        
        return hit_anything