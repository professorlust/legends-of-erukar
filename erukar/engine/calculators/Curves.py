import math

class Curves:
    AbsoluteScalingFactor = 0.01

    def dropoff(x_min, x_max, y_min, y_max, at_value):
        return -1*(y_max-y_min)*math.pow((at_value-x_max+x_min)/(x_min-x_max), 2) + y_max

    def item_stat_efficacy(value, requirement, cutoff, scaling_factor):
        actual_value = max(0, value - requirement)
        scalar = 1.0 if requirement is 0 else min(1.0, value / requirement)
        offset = min(actual_value, cutoff) * scaling_factor
        return scalar, offset
