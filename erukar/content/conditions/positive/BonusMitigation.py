from erukar.system.engine import Condition


class BonusMitigation(Condition):
    IsTemporary = True
    Duration = 30  # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun = 'Bonus {} Mitigation'
    Participle = 'Bonus {} Mitigation'
    Description = 'Increases {} Mitigation by {}'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        self.damage_type = 'fire'
        self.mitigation_amount = 0

    def damage_mitigation(self, damage_type):
        if damage_type == self.damage_type:
            yield (self.mitigation_amount, 0)

    def mutate_damage_type(self, new_type):
        self.damage_type = new_type

    def name(self):
        return self.Noun.format(self.damage_type.capitalize())
