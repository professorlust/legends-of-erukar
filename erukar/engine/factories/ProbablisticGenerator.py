from erukar.engine.factories.FactoryBase import FactoryBase
from erukar.engine.exceptions.InitializationException import InitializationException
from erukar.engine.environment import *
from erukar.engine.calculators.Random import Random
import numpy as np

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
        return Random.get_from_custom_distribution(np.random.uniform(0, 1), self.bins, self.values)()
