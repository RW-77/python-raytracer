from math import inf

class Interval:
    """Represents an interval with bounds `lower_b` and `upper_b`."""

    EMTPY = None
    UNIVERSE = None

    def __init__(self, lower_b: float = inf, upper_b: float = -inf) -> None:
        self.upper_b: float = upper_b
        self.lower_b: float = lower_b

    def contains(self, x: float) -> bool:
        """Returns true if `x` is within [`self.lower`, `self.upper`]."""

        return self.lower_b <= x <= self.upper_b
    
    def surrounds(self, x: float) -> bool:
        """Returns true if `x` is within (`self.lower`, `self.upper`)."""

        return self.lower_b < x < self.upper_b
    
    def clamp(self, x: float) -> float:
        """Restrict x to be within [`self.lower`, `self.upper`]."""

        if x < self.lower_b:
            return self.lower_b
        if x > self.upper_b:
            return self.upper_b
        return x
    
Interval.EMPTY = Interval(inf, -inf)
Interval.UNIVERSE = Interval(-inf, inf)