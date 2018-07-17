from erukar.system.engine import Condition
import random


class Dying(Condition):
    Incapacitates = True
    Revive = '{} has regained the strength to fight!'
    IsDying = '{} is dying!'

    def do_end_of_turn_effect(self, cmd):
        dc = 45
        skill_range = self.target.stat_random_range('resolve')
        mod = 10*(1-(pow((self.target.resolve-1000)/1000, 2)))

        if random.uniform(*skill_range)+mod >= dc:
            self.target.conditions.remove(self)
            self.target.health = 1
            cmd.append_result(
                self.target.uid,
                self.Revive.format(self.target.alias()))
            return
        cmd.append_result(
            self.target.uid,
            self.IsDying.format(self.target.alias()))
