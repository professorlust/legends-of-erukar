from erukar.engine.model.Affliction import Affliction
import random

class Dying(Affliction):
    Incapacitates = True

    def do_end_of_turn_effect(self):
        dc = 35
        skill_range = self.afflicted.stat_random_range('resolve')
        mod = 10*(1-(pow((self.afflicted.resolve-1000)/1000, 2)))

        if random.uniform(*skill_range)+mod >= dc:
            self.afflicted.afflictions.remove(self)
            return '{} has regained the strength to fight!'.format(self.afflicted.alias())

        return '{} is dying!'.format(self.afflicted.alias())
