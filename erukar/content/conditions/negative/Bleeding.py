from erukar.system.engine import Condition, Damage, DamageScalar
import erukar


class Bleeding(Condition):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Bleeding'
    Participle  = 'Bleeding'
    Description = 'Lose 5% max health every 5 seconds'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        self.damage = []
        self.damage_efficacy = 1.0
        self.affects_dying = False

    def do_tick_effect(self):
        if self.target.has_condition(erukar.engine.conditions.Dead):
            return
        if self.target.has_condition(erukar.engine.conditions.Dying)\
           and not self.affects_dying:
            return

        self.target.take_damage(10, self.instigator)
