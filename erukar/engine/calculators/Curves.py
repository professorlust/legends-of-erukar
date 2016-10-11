import math

class Curves:
    AbsoluteScalingFactor = 0.01

    def dropoff(x_min, x_max, y_min, y_max, at_value):
        return -1*(y_max-y_min)*math.pow((at_value-x_max+x_min)/(x_min-x_max), 2) + y_max

    def item_stat_efficacy(value, requirement, scaling_factor, max_scale):
        if value < requirement:
            return 0.5*math.pow((value/requirement), 2)
        value -= requirement
        actual_scaling_factor = scaling_factor * Curves.AbsoluteScalingFactor
        return 1+(max_scale-1)*(1 - 1/((value + 1/actual_scaling_factor)*actual_scaling_factor))
