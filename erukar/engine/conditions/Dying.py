from erukar.engine.model.Condition import Condition
import random

class Dying(Condition):
    Incapacitates = True

    def do_end_of_turn_effect(self):
        dc = 45
        skill_range = self.target.stat_random_range('resolve')
        mod = 10*(1-(pow((self.target.resolve-1000)/1000, 2)))

        if random.uniform(*skill_range)+mod >= dc:
            self.target.conditions.remove(self)
            self.target.health = 1
            return '{} has regained the strength to fight!'.format(self.target.alias())

        return '{} is dying!'.format(self.target.alias())
