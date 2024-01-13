import random
import math

# utility functions

def deg_to_rad(degrees: float) -> float:
    return degrees * math.pi / 180.0

def rand_float(lower_b: float = None, upper_b: float = None) -> float:
    '''returns a random real number in [lower_b, upper_b) if lower_b and upper_b specified'''
    '''otherwise returns random real number in [0, 1)'''

    random_float = random.random()
    if lower_b is not None and upper_b is not None:
        return lower_b + (upper_b - lower_b) * random_float
    else:
        return random_float