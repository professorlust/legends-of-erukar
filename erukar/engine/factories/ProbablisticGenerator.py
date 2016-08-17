from erukar.engine.factories.FactoryBase import FactoryBase
from erukar.engine import InitializationException
from erukar.engine.environment import *
import numpy as np
import math, random

class ProbablisticGenerator(FactoryBase):
    MinimumAcceptableWeight = -0.3
    def __init__(self):
        self.is_initialized = False
        self.bins = []
        self.values = []

    def create_distribution(self, possibilities, weights):
        '''
        The possibilities and weights must be lists in the same order
        '''
        bins = self.calculate_bin_widths(weights) 
        values = np.array(possibilities)
        self.order_bins_and_values(bins, values)
        self.is_initialized = True

    def calculate_bin_widths(self, W):
        '''Determines the probablistic proportions for binning'''
        if all(w_i <= self.MinimumAcceptableWeight for w_i in W) or len(set(W)) == 1:
            return [1/len(W)] * len(W)

        W_prime = [w_i for w_i in W if w_i > self.MinimumAcceptableWeight]
        weights = [self.cluster(w_i, W_prime) for w_i in W_prime]
        return [w_i / sum(weights) for w_i in weights]

    def cluster(self, w_i, W):
        '''
        Uses cluster algorithm developed for this project as follows:
        where N is the length, w_i is the current weight, and W is the set of weights
        1 / (N * (1 + (-w_i + sum(W))/(N-1) - w_i))
        '''
        min_W = max(min(0, min(W)), 0)
        return (w_i - min_W)/(max(W)-min_W)

    def order_bins_and_values(self, bins, values):
        '''Orders the bins in an increasing order and adjusts the values accordingly'''
        sortedzip = sorted(zip(bins, values), key=lambda x: x[0])
        self.bins, self.values = zip(*sortedzip)
        self.bins = np.add.accumulate(self.bins)

    def create_one(self):
        if not self.is_initialized:
            raise InitializationException(self.decoration_module)
        return self.values[np.digitize(np.random.uniform(0, 1), self.bins)]()
