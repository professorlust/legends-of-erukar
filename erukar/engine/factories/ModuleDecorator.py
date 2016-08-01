from erukar.engine.factories.ProbablisticGenerator import ProbablisticGenerator
import sys, inspect

class ModuleDecorator(ProbablisticGenerator):
    ConditionalProb = 'ProbabilityFrom{}'

    def __init__(self, module, generation_parameters):
        super().__init__()
        self.generation_parameters = generation_parameters
        self.decoration_module = sys.modules[module]
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
        prob_weight = 0.0
        if hasattr(modifier, 'Probability'):
            prob_weight = getattr(modifier, 'Probability')

        if self.generation_parameters is None:
            return prob_weight

        for parameter in vars(self.generation_parameters):
            var_format = self.ConditionalProb.format(parameter.capitalize()) 
            if hasattr(modifier, var_format):
                cond_weight = getattr(modifier, var_format) 
                generation_actual = getattr(self.generation_parameters, parameter)
                prob_weight += cond_weight * generation_actual 

        return prob_weight

    def apply_one_to(self, room):
        '''shortcut to make one and apply it'''
        self.create_one().apply_to(room)
