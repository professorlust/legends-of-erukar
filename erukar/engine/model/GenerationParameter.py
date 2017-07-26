import scipy.stats
import math, functools, operator

class GenerationParameter():
    def __init__(self, correlation=0.0, strength=1.0):
        self.correlation = correlation
        self.strength = strength

    def variable_correlation(self, value):
        return -1 * (value-self.correlation - 1/self.strength) * (value-self.correlation + 1/self.strength)
