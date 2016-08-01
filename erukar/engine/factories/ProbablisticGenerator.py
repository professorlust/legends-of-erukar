from erukar.engine.factories.FactoryBase import FactoryBase
from erukar.engine.environment import *
import numpy as np
import math, random

class ProbablisticGenerator(FactoryBase):
    def __init__(self):
        self.bins = []
        self.values = []

    def create_distribution(self, possibilities, weights):
        '''
        The possibilities and weights must be lists in the same order
        '''
        bins = self.calculate_bin_widths(weights) 
        values = np.array(possibilities)
        self.order_bins_and_values(bins, values)

    def calculate_bin_widths(self, weights):
        min_value = min(weights)
        if all(w for w in weights if w == min_value):
            min_value = 0
        total_weight = sum(weights)
        return np.array([(x-min_value)/total_weight for x in np.add.accumulate(weights)])

    def order_bins_and_values(self, bins, values):
        '''Orders the bins in an increasing order and adjusts the values accordingly'''
        self.bins, self.values = zip(*sorted(zip(bins, values)))

    def create_one(self):
        return self.values[np.digitize(np.random.uniform(0, 1), self.bins)]()
