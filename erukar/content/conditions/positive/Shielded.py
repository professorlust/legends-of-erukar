from erukar.system.engine import Condition

class Shielded(Condition):
    IsTemporary = True
    Duration = 300
    Incapacitates = False

    Noun = '{damage} Shield'
    Participle = '{damage} Shielding'
    Description = 'Allows the deflection of a total of {value} {damage} damage ({remaining} remaining in shield)'

    BaseShield = 10

    def __init__(self,target, instigator=None):
        super().__init__(target, instigator)
        if instigator is None:
            instigator = target
        self.damage_type = 'force'

    def set_efficacy(self, efficacy):
        self.shield_value = Shielded.BaseShield * efficacy
        self.remaining = self.shield_value
        self.Description = self.Description.format(
            value=self.shield_value,
            remaining=self.remaining,
            damage=self.damage_type)
        self.Noun = self.Noun.format(damage=self.damage_type.capitalize())
        self.Participle = self.Participle.format(damage=self.damage_type.capitalize())
