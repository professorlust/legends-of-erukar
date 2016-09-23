import math

class Curves:
    def dropoff(x_min, x_max, y_min, y_max, at_value):
        return -1*(y_max-y_min)*math.pow((at_value-x_max+x_min)/(x_min-x_max), 2) + y_max
