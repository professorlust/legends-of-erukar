from erukar.ext.math import Modules
from .ProbablisticGenerator import ProbablisticGenerator
import functools
import math
import numpy


class ModuleDecorator(ProbablisticGenerator):
    ConditionalProb = 'ProbabilityFrom{}'

    def __init__(self, module, generation_parameters):
        super().__init__()
        self.generation_parameters = generation_parameters
        if isinstance(module, str):
            self.initialize(module)

    def initialize(self, module):
        poss = list(Modules.get_members_of(module))

        weights, values = zip(*[(self.calculate_probability(p), p) for p in poss])
        self.create_distribution(values, weights)

    def calculate_probability(self, modifier):
        '''
        Grants the system the capacity for clustered stochastic generation.
        Takes weights from a GenerationProfile object and then uses conditional
        probability weighting in modifiers to determine what is more likely to
        occur given environmental factors.
        '''
        prob_weights = []
        overall_probability = 1.0
        if hasattr(modifier, 'Probability'):
            overall_probability = getattr(modifier, 'Probability')

        if self.generation_parameters is None:
            return overall_probability

        for parameter in vars(self.generation_parameters):
            var_format = self.ConditionalProb.format(parameter.capitalize())
            if hasattr(modifier, var_format):
                cond_weight = getattr(modifier, var_format)
                actual = getattr(self.generation_parameters, parameter)
                prob_weights.append(self.semi_conditional_probabiity(actual, cond_weight))

        if len(prob_weights) > 0:
            return overall_probability*(1+functools.reduce(lambda x_i, X: X*x_i, prob_weights))

        return overall_probability

    def semi_conditional_probabiity(self, x, c):
        return math.pow(math.exp(2*(x-c)), c-x)

    def apply_one_to(self, room):
        '''shortcut to make one and apply it'''
        mod = self.create_one()
        mod.apply_to(room)

    def get_one_type(self):
        type_to_create = self.values[numpy.digitize(numpy.random.uniform(0, 1), self.bins)]
        return type_to_create[1]

    def create_one(self):
        type_to_create = self.values[numpy.digitize(numpy.random.uniform(0, 1), self.bins)]
        return self.create_type(type_to_create)

    def create_type(self, type_to_create):
        new_one = type_to_create[1]()
        setattr(new_one, 'generation_parameters', self.generation_parameters)
        return new_one
