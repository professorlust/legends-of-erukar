from erukar.engine.model.Affliction import Affliction
import random

class Dying(Affliction):
    Incapacitates = True

    def do_begin_of_turn_effect(self):
        dc = self.afflicted.resolve + 20
        skill_range = self.afflicted.skill_range('resolve')

        if random.uniform(*skill_range) >= dc:
            self.afflicted.afflictions.remove(self)
            return '{} has regained the strength to fight!'.format(self.afflicted.alias())

        return '{} is dying!'.format(self.afflicted.alias())
