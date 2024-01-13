from utils import ray, interval
from hittable import hittable, hit_record

class hittable_list(hittable):
    
    def __init__(self, object: hittable = None) -> None:
        self.objects = [] # make list or numpy array later if possible
        if isinstance(object, hittable):
            self.add(object)

    def clear(self) -> None:
        self.objects.clear()

    def add(self, object: hittable) -> None:
        self.objects.append(object)

    def hit(self, _r: ray, ray_t: interval, rec: hit_record) -> bool:
        temp_rec = hit_record()
        hit_anything: bool = False
        closest_so_far = ray_t.upper_b

        # we only need the closest object that is hit, meaning 
        for object in self.objects:
            if object.hit(_r, interval(ray_t.lower_b, closest_so_far), temp_rec): # pass in closest_so_far for processing closer objects
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.copy(temp_rec)
        
        return hit_anything