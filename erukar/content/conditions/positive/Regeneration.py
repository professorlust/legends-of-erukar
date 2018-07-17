from erukar.system.engine import Condition, Dead, Dying


class Regeneration(Condition):
    IsTemporary = True
    Duration = 5
    Incapacitates = False

    Noun        = 'Regeneration'
    Participle  = 'Regnerating'
    Description = 'Gain a percentage of maximum health every tick'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        self.heal_percentage = 0.05

    def do_tick_effect(self, cmd):
        if self.should_clear():
            self.exit()
            return

        max_health = self.target.maximum_health()
        new_health = self.target.health + self.heal_percentage * max_health
        self.target.health = min(max_health, new_health)

    def should_clear(self):
        return self.target.has_condition(Dead)\
            or self.target.has_condition(Dying)\
            or self.target.health >= self.target.maximum_health()

    def mutate_percent(self, pct):
        self.heal_percentage = pct
