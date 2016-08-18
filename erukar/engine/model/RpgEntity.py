from erukar.engine.model.Interactible import Interactible
import math, random, re

class RpgEntity(Interactible):
    nDxy_expression = '(\d+)d(\d+)([+-]\d+)?'
    base_armor_class = 10

    def regex(self, to_evaluate):
        '''Regex on the damage string'''
        captured = re.search(RpgEntity.nDxy_expression, to_evaluate)
        return [int(x) if x is not None else 0 for x in captured.groups()]

    def roll(self, roll_range, distribution=None):
        '''Roll on a string such as '1d20' or '6d6+6' '''
        if distribution is None:
            distribution = random.uniform
        return round(distribution(*roll_range))

    def calculate_armor_class(self):
        return RpgEntity.base_armor_class

    def necessary_acuity(self):
        return 0
