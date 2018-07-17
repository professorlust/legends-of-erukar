from erukar.system.engine import Condition, Dead, Dying


class HealthDrain(Condition):
    IsTemporary = True
    Duration = 4  # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Health Drain'
    Participle  = 'Draining Health'
    Description = 'Lose a percentage of health every tick'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        self.damage = []
        self.damage_type = 'arcane'
        self.damage_amount = 10

    def do_tick_effect(self, cmd):
        if self.should_clear():
            self.target.conditions.remove(self)
            return

        damage = (self.damage_amount, self.damage_type)
        result = self.target.apply_damage(damage, self.target)
        if result['total'] > 0:
            max_health = self.instigator.maximum_health()
            self.instigator.health = min(max_health, result['total'])

    def should_clear(self):
        return self.instigator is None\
            or self.instigator.is_incapacitated()\
            or self.target.has_condition(Dead)\
            or self.target.has_condition(Dying)

    def mutate_damage_type(self, new_type):
        self.damage_type = new_type

    def mutate_power(self, new_amount):
        self.damage_amount = new_amount
