from .FactoryBase import FactoryBase
from erukar.ext.math import Random
import numpy

class ProbablisticGenerator(FactoryBase):
    def __init__(self):
        self.is_initialized = False
        self.bins = []
        self.values = []

    def create_distribution(self, possibilities, weights):
        '''
        The possibilities and weights must be lists in the same order
        '''
        self.bins, self.values = Random.create_random_distribution(possibilities, weights)
        self.is_initialized = True

    def create_one(self):
        if not self.is_initialized:
            raise InitializationException(self.decoration_module)
        return Random.get_from_custom_distribution(numpy.random.uniform(0, 1), self.bins, self.values)()
