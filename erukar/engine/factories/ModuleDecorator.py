from erukar.engine.factories.ProbablisticGenerator import ProbablisticGenerator
from erukar.engine import InitializationException
import sys, inspect, functools, math

class ModuleDecorator(ProbablisticGenerator):
    ConditionalProb = 'ProbabilityFrom{}'

    def __init__(self, module, generation_parameters):
        super().__init__()
        self.generation_parameters = generation_parameters
        self.decoration_module = sys.modules[module]

    def initialize(self):
        poss = [x[1] for x in inspect.getmembers(self.decoration_module, inspect.isclass)]

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
