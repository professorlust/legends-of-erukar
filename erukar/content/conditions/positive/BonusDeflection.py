from erukar.system.engine import Condition


class BonusDeflection(Condition):
    IsTemporary = True
    Duration = 30  # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun = 'Bonus {} Deflection'
    Participle = 'Bonus {} Deflection'
    Description = 'Increases {} Deflection by {}'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        self.damage_type = 'fire'
        self.deflection_amount = 0

    def damage_mitigation(self, damage_type):
        if damage_type == self.damage_type:
            yield (0.00, self.deflection_amount)

    def mutate_damage_type(self, new_type):
        self.damage_type = new_type

    def name(self):
        return self.Noun.format(self.damage_type.capitalize())
