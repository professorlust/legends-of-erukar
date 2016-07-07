from erukar.engine.factories.ProbablisticGenerator import ProbablisticGenerator
import sys, inspect

class ModuleDecorator(ProbablisticGenerator):
    def __init__(self, module, generation_parameters):
        super().__init__()

        self.decoration_module = sys.modules[module]
        poss = [x[1] for x in inspect.getmembers(self.decoration_module, inspect.isclass)]

        weights, values = zip(*[(p.Probability, p) for p in poss])
        self.create_distribution(values, weights)


    def apply_one_to(self, room):
        '''shortcut to make one and apply it'''
        self.create_one().apply_to(room)
