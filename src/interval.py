from math import inf

class interval:

    EMTPY = None
    UNIVERSE = None

    def __init__(self, lower_b: float = inf, upper_b: float = -inf) -> None:
        self.upper_b = upper_b
        self.lower_b = lower_b

    def contains(self, x: float) -> bool:
        return self.lower_b <= x <= self.upper_b
    
    def surrounds(self, x: float) -> bool:
        return self.lower_b < x < self.upper_b
    
    def clamp(self, x: float) -> float:
        '''restrict x within [self.lower_b, self.upper_b]'''

        if x < self.lower_b:
            return self.lower_b
        if x > self.upper_b:
            return self.upper_b
        return x
    
interval.EMPTY = interval(inf, -inf)
interval.UNIVERSE = interval(-inf, inf)