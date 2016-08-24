from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import random

class MultipleModuleDecorator(ModuleDecorator):
    '''
    Like the ModuleDecorator, except that it creates multiple items
    and treats each item independently, instead of choosing from a list
    '''
    def initialize(self):
        poss = list(self.get_possibilities())
        self.items = [(x, self.calculate_probability(x)) for x in poss]

    def apply_one_to(self, room):
        '''shortcut to make one and apply it'''
        for item in self.items:
            if random.random() < item[1]:
                new_one = self.create_type(item[0])
                new_one.apply_to(room)

