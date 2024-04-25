from math import inf

class Interval:
    """Represents an interval with bounds `lower_b` and `upper_b`."""

    EMTPY = None
    UNIVERSE = None

    def __init__(self, lower_b: float = inf, upper_b: float = -inf) -> None:
        """
        Constructs an interval from `lower_b` to `upper_b`. If no arguments are provided, the interval is empty
        by default.
        """
        self.upper_b: float = upper_b
        self.lower_b: float = lower_b

    def __str__(self) -> str:
        return f"[{self.lower_b}, {self.upper_b}]"

    @classmethod
    def merge(cls, _a : 'Interval', _b : 'Interval') -> 'Interval':
        """
        Constructs an interval from two intervals.
        """
        lower_b = min(_a.lower_b, _b.lower_b)
        upper_b = max(_a.upper_b, _b.upper_b)
        return cls(lower_b, upper_b)

    def size(self) -> float:
        """Returns the size of the interval which is simply the upper bound minus the lower bound."""
        
        return self.upper_b - self.lower_b
    
    def expanded(self, delta: float) -> 'Interval':
        """Returns a new interval with `delta` padding added to each end."""

        padding: float = delta/2
        return Interval(self.lower_b - padding, self.upper_b + padding)

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